import streamlit as st


def display_section_divider():

    st.html(
        """
        <div class="section-divider"></div>
        """
    )


def display_empty_state():

    st.html(
        """
        <div class="empty-state">

            <div class="empty-title">
                🎬 Load a YouTube video
            </div>

            <div class="empty-text">
                Paste a YouTube URL above to extract,
                translate, index and chat with the video.
            </div>

        </div>
        """
    )