import os
import time

import streamlit as st
from dotenv import load_dotenv
from langchain_core.documents import Document

from components.ingestion import ingest_youtube_video
from components.translation import translate_to_english, split_transcript
from components.chunking import chunk_text
from components.embedding import get_embedding_model
from components.vector_store import create_vector_store
from components.retreiver import HybridRetriever
from components.re_ranker import DocumentReranker
from components.llm_client import get_groq_llm

from components.prompt_templates import (
    SUMMARY_PROMPT,
    SUMMARY_MAP_PROMPT,
    SUMMARY_REDUCE_PROMPT,
    FINAL_SUMMARY_PROMPT,
    QA_PROMPT,
)

from ui.styles import load_custom_css
from ui.header import display_header

from ui.loader import (
    create_processing_status,
    show_ingestion,
    show_translation,
    show_chunking,
    show_embeddings,
    show_vector_store,
    show_summary,
    show_reranker,
    finish_processing,
    fail_processing,
)

from ui.youtube_player import display_youtube_video
from ui.summary import display_summary
from ui.metrics import display_metrics
from ui.chat import display_chat
from ui.transcript import display_transcript

from ui.components import (
    display_section_divider,
    display_empty_state,
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="YouTube RAG",
    page_icon="▶️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# SESSION STATE
# ============================================================

def initialize_session_state():

    defaults = {

        "video_loaded": False,

        "video_url": "",

        "video_id": "",

        "original_transcript": "",

        "english_transcript": "",

        "language_code": "",

        "documents": [],

        "vector_store": None,

        "hybrid_retriever": None,

        "reranker": None,

        "llm": None,

        "summary": "",

        "chat_history": [],

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# ============================================================
# SUMMARY HELPERS
# ============================================================

def _llm_text(response):
    """
    Extract visible assistant text from a LangChain AIMessage.

    Handles:
    - normal string content
    - list/block content
    - None content
    """
    content = getattr(response, "content", None)

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):

        parts = []

        for block in content:

            if isinstance(block, dict):

                text = block.get("text") or block.get("content")

                if text:
                    parts.append(str(text))

            elif block:

                parts.append(str(block))

        return "\n".join(parts).strip()

    if content is not None:

        return str(content).strip()

    return str(response).strip()


def _invoke_summary(
    llm,
    messages,
    label,
    max_attempts=2,
):
    """
    Invoke the summary model.

    If the model returns empty visible content,
    retry after the configured delay.
    """

    delay = float(
        os.getenv(
            "SUMMARY_REQUEST_DELAY_SECONDS",
            "13",
        )
    )

    last_error = None

    for attempt in range(1, max_attempts + 1):

        if attempt > 1:

            time.sleep(delay)

        try:

            response = llm.invoke(messages)

            text = _llm_text(response)

            if text:

                return text

            last_error = "empty response"

        except Exception as exc:

            last_error = exc

    raise RuntimeError(
        f"{label} returned empty text after "
        f"{max_attempts} attempts. "
        f"Last error: {last_error}"
    )


def _split_summary_transcript(
    transcript: str,
    max_chars: int = 7000,
) -> list[str]:
    """
    Split a long transcript into sections used ONLY
    for hierarchical summarization.

    These are NOT the RAG chunks.
    """

    if not transcript:

        return []

    paragraphs = [
        paragraph.strip()
        for paragraph in transcript.split("\n")
        if paragraph.strip()
    ]

    chunks = []

    current = []

    current_len = 0

    for paragraph in paragraphs:

        paragraph_len = len(paragraph)

        if (
            current
            and current_len + paragraph_len + 1 > max_chars
        ):

            chunks.append(
                "\n".join(current)
            )

            current = []

            current_len = 0

        current.append(paragraph)

        current_len += paragraph_len + 1

    if current:

        chunks.append(
            "\n".join(current)
        )

    return chunks


# ============================================================
# SUMMARY
# ============================================================

def generate_summary(
    transcript: str,
    llm,
    status=None,
):
    """
    Generate a summary.

    <= 50,000 characters:
        One direct final-summary request.

    > 50,000 characters:
        MAP -> REDUCE -> FINAL SUMMARY.
    """

    if not transcript or not transcript.strip():

        return "No summary available."

    # --------------------------------------------------------
    # CONFIGURATION
    # --------------------------------------------------------

    summary_threshold = int(
        os.getenv(
            "SUMMARY_MAP_THRESHOLD_CHARS",
            "50000",
        )
    )

    section_chars = int(
        os.getenv(
            "SUMMARY_SECTION_CHARS",
            "7000",
        )
    )

    request_delay = float(
        os.getenv(
            "SUMMARY_REQUEST_DELAY_SECONDS",
            "13",
        )
    )

    # --------------------------------------------------------
    # SHORT TRANSCRIPT
    # --------------------------------------------------------

    if len(transcript) <= summary_threshold:

        if status is not None:

            status.steps["summary"].write(
                "⏳ **Summary** • Generating final summary"
            )

        return _invoke_summary(
            llm,
            FINAL_SUMMARY_PROMPT.format_messages(
                content=transcript
            ),
            "Final summary",
        )

    # --------------------------------------------------------
    # LONG TRANSCRIPT
    # --------------------------------------------------------

    sections = _split_summary_transcript(
        transcript,
        max_chars=section_chars,
    )

    if not sections:

        return "No summary available."

    intermediate = []

    total_sections = len(sections)

    # --------------------------------------------------------
    # MAP
    # --------------------------------------------------------

    for index, section in enumerate(
        sections,
        start=1,
    ):

        if status is not None:

            status.steps["summary"].write(
                f"⏳ **Summary** • "
                f"Summarizing section "
                f"{index}/{total_sections}"
            )

        text = _invoke_summary(
            llm,
            SUMMARY_MAP_PROMPT.format_messages(
                transcript=section
            ),
            f"Summary section {index}/{total_sections}",
        )

        intermediate.append(text)

        # Avoid sending many requests inside
        # the same TPM window.
        if index < total_sections:

            time.sleep(request_delay)

    # --------------------------------------------------------
    # REDUCE
    # --------------------------------------------------------

    level = 1

    while len(intermediate) > 1:

        reduced = []

        batches = list(
            range(
                0,
                len(intermediate),
                4,
            )
        )

        total_batches = len(batches)

        for batch_number, start in enumerate(
            batches,
            start=1,
        ):

            batch = intermediate[
                start:start + 4
            ]

            combined = "\n\n---\n\n".join(batch)

            if status is not None:

                status.steps["summary"].write(
                    f"⏳ **Summary** • "
                    f"Combining summaries "
                    f"{batch_number}/{total_batches} "
                    f"(level {level})"
                )

            # ------------------------------------------------
            # If the combined batch is still large,
            # reduce individual summaries separately.
            # ------------------------------------------------

            if (
                len(combined) > 6500
                and len(batch) > 1
            ):

                for item_index, item in enumerate(
                    batch,
                    start=1,
                ):

                    reduced_text = _invoke_summary(
                        llm,
                        SUMMARY_REDUCE_PROMPT.format_messages(
                            summaries=item
                        ),
                        f"Summary reduce step "
                        f"(level {level})",
                    )

                    reduced.append(
                        reduced_text
                    )

                    time.sleep(
                        request_delay
                    )

            else:

                reduced_text = _invoke_summary(
                    llm,
                    SUMMARY_REDUCE_PROMPT.format_messages(
                        summaries=combined
                    ),
                    f"Summary reduce step "
                    f"(level {level})",
                )

                reduced.append(
                    reduced_text
                )

                if batch_number < total_batches:

                    time.sleep(
                        request_delay
                    )

        intermediate = reduced

        level += 1

    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------

    if status is not None:

        status.steps["summary"].write(
            "⏳ **Summary** • Creating final summary"
        )

    final_summary = _invoke_summary(
        llm,
        FINAL_SUMMARY_PROMPT.format_messages(
            content=intermediate[0]
        ),
        "Final summary",
    )

    return final_summary


# ============================================================
# QA
# ============================================================

def answer_question(
    question: str,
):

    retriever = st.session_state[
        "hybrid_retriever"
    ]

    reranker = st.session_state[
        "reranker"
    ]

    llm = st.session_state[
        "llm"
    ]

    # --------------------------------------------------------
    # HYBRID RETRIEVAL
    # --------------------------------------------------------

    candidates = retriever.search(
        question
    )

    # --------------------------------------------------------
    # RERANKING
    # --------------------------------------------------------

    documents = reranker.rerank(
        query=question,
        documents=candidates,
        top_k=4,
    )

    # --------------------------------------------------------
    # CONTEXT
    # --------------------------------------------------------

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    # --------------------------------------------------------
    # PROMPT
    # --------------------------------------------------------

    messages = QA_PROMPT.format_messages(
        context=context,
        question=question,
    )

    # --------------------------------------------------------
    # GROQ
    # --------------------------------------------------------

    response = llm.invoke(
        messages
    )

    answer = _llm_text(
        response
    )

    return {
        "answer": answer,
        "source_documents": documents,
    }


# ============================================================
# PROCESS VIDEO
# ============================================================

def process_video(url: str):

    # A new URL starts a completely new
    # one-video knowledge base.

    st.session_state[
        "video_loaded"
    ] = False

    st.session_state[
        "chat_history"
    ] = []

    st.session_state[
        "video_url"
    ] = url

    status = create_processing_status()

    try:

        # ====================================================
        # 1. INGESTION
        # ====================================================

        data = ingest_youtube_video(
            url
        )

        language_code = data.get(
            "language_code",
            "unknown",
        )

        original_transcript = data[
            "transcript"
        ]

        show_ingestion(
            status,
            language_code,
        )

        # ====================================================
        # 2. TRANSLATION
        # ====================================================

        # ----------------------------------------------------
        # English video
        # ----------------------------------------------------

        if language_code.lower().startswith("en"):

            # Already English.
            # Do NOT call Groq translation.

            english_transcript = (
                original_transcript
            )

            show_translation(
                status,
                skipped=True,
            )

        # ----------------------------------------------------
        # Non-English video
        # ----------------------------------------------------

        else:

            english_transcript = (
                translate_to_english(
                    original_transcript,
                    language_code,
                )
            )

            translation_requests = len(
                split_transcript(
                    original_transcript,
                    max_chars=3000,
                )
            )

            show_translation(
                status,
                translation_requests,
            )

        # ====================================================
        # 3. CHUNKING
        # ====================================================

        chunks = chunk_text(
            english_transcript
        )

        documents = []

        for index, chunk in enumerate(
            chunks,
            start=1,
        ):

            if isinstance(
                chunk,
                Document,
            ):

                chunk.metadata[
                    "chunk_id"
                ] = index

                documents.append(
                    chunk
                )

            else:

                documents.append(
                    Document(
                        page_content=str(
                            chunk
                        ),
                        metadata={
                            "chunk_id": index,
                            "source": (
                                "YouTube transcript"
                            ),
                        },
                    )
                )

        total_chunks = len(
            documents
        )

        total_characters = len(
            english_transcript
        )

        show_chunking(
            status,
            total_chunks,
            total_characters,
        )

        # ====================================================
        # 4. EMBEDDINGS
        # ====================================================

        embeddings = (
            get_embedding_model()
        )

        vector_store = (
            create_vector_store(
                documents,
                embeddings,
            )
        )

        show_embeddings(
            status
        )

        # ====================================================
        # 5. VECTOR STORE
        # ====================================================

        hybrid_retriever = (
            HybridRetriever(
                vector_store=vector_store,
                documents=documents,
            )
        )

        show_vector_store(
            status
        )

        # ====================================================
        # 6. RERANKER
        # ====================================================

        reranker = (
            DocumentReranker()
        )

        show_reranker(
            status
        )

        # ====================================================
        # 7. GROQ
        # ====================================================

        llm = get_groq_llm()

        # Summary uses a separate LLM instance so that
        # summary-specific configuration does not affect
        # Q&A or translation.

        summary_llm = get_groq_llm(
            model_name=os.getenv(
                "GROQ_SUMMARY_MODEL",
                os.getenv(
                    "GROQ_MODEL",
                    "openai/gpt-oss-20b",
                ),
            ),
            temperature=0.2,
            max_tokens=int(
                os.getenv(
                    "SUMMARY_MAP_MAX_TOKENS",
                    "900",
                )
            ),
            include_reasoning=False,
            reasoning_effort="low",
        )

        # ====================================================
        # 8. SUMMARY
        # ====================================================

        summary = generate_summary(
            english_transcript,
            summary_llm,
            status=status,
        )

        summary_threshold = int(
            os.getenv(
                "SUMMARY_MAP_THRESHOLD_CHARS",
                "50000",
            )
        )

        if len(english_transcript) > summary_threshold:

            summary_status = (
                "AI summary generated "
                "(hierarchical for long transcripts)"
            )

        else:

            summary_status = (
                "AI summary generated"
            )

        show_summary(
            status,
            summary_status,
        )

        # ====================================================
        # SAVE STATE
        # ====================================================

        st.session_state[
            "video_loaded"
        ] = True

        st.session_state[
            "video_url"
        ] = url

        st.session_state[
            "video_id"
        ] = data[
            "video_id"
        ]

        st.session_state[
            "original_transcript"
        ] = original_transcript

        st.session_state[
            "english_transcript"
        ] = english_transcript

        st.session_state[
            "language_code"
        ] = language_code

        st.session_state[
            "documents"
        ] = documents

        st.session_state[
            "vector_store"
        ] = vector_store

        st.session_state[
            "hybrid_retriever"
        ] = hybrid_retriever

        st.session_state[
            "reranker"
        ] = reranker

        st.session_state[
            "llm"
        ] = llm

        st.session_state[
            "summary"
        ] = summary

        # ====================================================
        # FINISHED
        # ====================================================

        finish_processing(
            status
        )

    except Exception as e:

        fail_processing(
            status,
            str(e),
        )

        st.error(
            f"Unable to process video: {e}"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    initialize_session_state()

    # --------------------------------------------------------
    # CSS
    # --------------------------------------------------------

    load_custom_css()

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    display_header()

    # --------------------------------------------------------
    # URL INPUT
    # --------------------------------------------------------

    st.markdown(
        "### 🔗 YouTube Video URL"
    )

    url_col, button_col = st.columns(
        [8, 1],
        gap="medium",
    )

    with url_col:

        url = st.text_input(
            "YouTube URL",

            value=st.session_state[
                "video_url"
            ],

            placeholder=(
                "Paste a YouTube video URL here..."
            ),

            label_visibility="collapsed",
        )

    with button_col:

        load_button = st.button(
            "Load",
            type="primary",
            use_container_width=True,
        )

    # --------------------------------------------------------
    # LOAD
    # --------------------------------------------------------

    if load_button:

        if not url.strip():

            st.warning(
                "Please enter a YouTube URL."
            )

        else:

            process_video(
                url.strip()
            )

    # --------------------------------------------------------
    # EMPTY STATE
    # --------------------------------------------------------

    if not st.session_state[
        "video_loaded"
    ]:

        display_section_divider()

        display_empty_state()

        return

    # ========================================================
    # VIDEO + SUMMARY
    # ========================================================

    display_section_divider()

    video_col, summary_col = st.columns(
        [7, 3],
        gap="large",
    )

    # --------------------------------------------------------
    # VIDEO 70%
    # --------------------------------------------------------

    with video_col:

        display_youtube_video(
            st.session_state[
                "video_url"
            ]
        )

    # --------------------------------------------------------
    # SUMMARY 30%
    # --------------------------------------------------------

    with summary_col:

        display_summary(
            st.session_state[
                "summary"
            ]
        )

    # ========================================================
    # METRICS
    # ========================================================

    display_section_divider()

    display_metrics(

        total_chunks=len(
            st.session_state[
                "documents"
            ]
        ),

        total_characters=len(
            st.session_state[
                "english_transcript"
            ]
        ),

        language=st.session_state[
            "language_code"
        ],
    )

    # ========================================================
    # ASK / TRANSCRIPT
    # ========================================================

    display_section_divider()

    ask_tab, transcript_tab = st.tabs(
        [
            "💬 Ask",
            "📄 Transcript",
        ]
    )

    # --------------------------------------------------------
    # ASK
    # --------------------------------------------------------

    with ask_tab:

        display_chat(
            answer_question
        )

    # --------------------------------------------------------
    # TRANSCRIPT
    # --------------------------------------------------------

    with transcript_tab:

        display_transcript(

            original_transcript=(
                st.session_state[
                    "original_transcript"
                ]
            ),

            english_transcript=(
                st.session_state[
                    "english_transcript"
                ]
            ),

            language=(
                st.session_state[
                    "language_code"
                ]
            ),
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()