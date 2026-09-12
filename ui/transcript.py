import streamlit as st


def format_transcript(text: str) -> str:
    """
    Convert caption-style line breaks into normal readable text.

    YouTube transcripts often contain a newline after every
    caption segment. We replace those with spaces so the
    transcript reads like normal paragraphs.
    """

    if not text:
        return ""

    # Remove unnecessary whitespace
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # Join caption lines into normal continuous text
    return " ".join(lines)


def display_transcript(
    original_transcript: str,
    english_transcript: str,
    language: str
):

    st.markdown(
        "### 📄 Transcript"
    )

    st.caption(
        f"Source language: {language}"
    )

    original_tab, english_tab = st.tabs(
        [
            "Original",
            "English"
        ]
    )

    # ========================================================
    # ORIGINAL
    # ========================================================

    with original_tab:

        formatted_original = format_transcript(
            original_transcript
        )

        st.text_area(
            "Original transcript",
            value=formatted_original,
            height=650,
            disabled=True,
            label_visibility="collapsed",
        )

    # ========================================================
    # ENGLISH
    # ========================================================

    with english_tab:

        formatted_english = format_transcript(
            english_transcript
        )

        st.text_area(
            "English transcript",
            value=formatted_english,
            height=650,
            disabled=True,
            label_visibility="collapsed",
        )