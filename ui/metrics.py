import html
import streamlit as st


def display_metrics(
    total_chunks: int,
    total_characters: int,
    language: str
):

    col1, col2, col3, col4 = st.columns(
        4,
        gap="medium"
    )

    # ========================================================
    # TOTAL CHUNKS
    # ========================================================

    with col1:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Total Chunks
                </div>

                <div class="metric-value">
                    {total_chunks}
                </div>

                <div class="metric-description">
                    Indexed transcript sections
                </div>

            </div>
            """
        )

    # ========================================================
    # CHARACTERS
    # ========================================================

    with col2:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Characters
                </div>

                <div class="metric-value">
                    {total_characters:,}
                </div>

                <div class="metric-description">
                    English transcript
                </div>

            </div>
            """
        )

    # ========================================================
    # LANGUAGE
    # ========================================================

    with col3:

        safe_language = html.escape(
            str(language or "Unknown")
        )

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Language
                </div>

                <div class="metric-value">
                    {safe_language}
                </div>

                <div class="metric-description">
                    Source language
                </div>

            </div>
            """
        )

    # ========================================================
    # RETRIEVAL
    # ========================================================

    with col4:

        st.html(
            """
            <div class="metric-card">

                <div class="metric-label">
                    Retrieval
                </div>

                <div class="metric-value">
                    Hybrid
                </div>

                <div class="metric-description">
                    FAISS + BM25 + Reranker
                </div>

            </div>
            """
        )