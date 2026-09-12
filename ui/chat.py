import html
import streamlit as st


def _source_to_dict(document, fallback_index: int):
    metadata = (
        getattr(document, "metadata", {})
        or {}
    )

    return {
        "chunk_id": metadata.get("chunk_id", fallback_index),
        "rerank_score": metadata.get("rerank_score"),
        "content": getattr(document, "page_content", ""),
    }


def display_source_chunks(documents):
    if not documents:
        return

    st.markdown("#### 📚 Sources used")

    for index, document in enumerate(documents, start=1):
        if isinstance(document, dict):
            chunk_id = document.get("chunk_id", index)
            score = document.get("rerank_score")
            content = str(document.get("content", "")).strip()
        else:
            source = _source_to_dict(document, index)
            chunk_id = source["chunk_id"]
            score = source["rerank_score"]
            content = str(source["content"]).strip()

        if len(content) > 600:
            content = content[:600] + "..."

        safe_content = html.escape(content)

        if score is not None:
            try:
                score_text = f"{float(score):.2f}"
            except Exception:
                score_text = str(score)
        else:
            score_text = "N/A"

        st.html(
            f"""
            <div class="source-card">
                <div class="source-header">
                    <span class="source-chunk">Chunk {html.escape(str(chunk_id))}</span>
                    <span class="source-score">Rerank: {html.escape(score_text)}</span>
                </div>
                <div class="source-content">{safe_content}</div>
            </div>
            """
        )


def _display_history():
    """Render saved questions and answers from the current video."""
    for item in st.session_state.get("chat_history", []):
        with st.chat_message("user"):
            st.markdown(item["question"])

        with st.chat_message("assistant"):
            st.markdown(item["answer"])
            display_source_chunks(item.get("sources", []))


def display_chat(answer_function):
    st.markdown("### 💬 Ask about this video")
    st.caption("Ask questions based on the video transcript.")

    _display_history()

    question = st.chat_input(
        "Ask anything about this video..."
    )

    if not question:
        return

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the video..."):
            try:
                result = answer_function(question)

                answer = result.get(
                    "answer",
                    "No answer generated."
                )

                documents = result.get(
                    "source_documents",
                    []
                )

            except Exception as e:
                st.error(
                    f"Unable to answer question: {e}"
                )
                return

        st.markdown(answer)
        display_source_chunks(documents)

    # Save a lightweight representation instead of keeping UI objects.
    st.session_state.setdefault("chat_history", []).append(
        {
            "question": question,
            "answer": answer,
            "sources": [
                _source_to_dict(document, index)
                for index, document in enumerate(documents, start=1)
            ],
        }
    )
