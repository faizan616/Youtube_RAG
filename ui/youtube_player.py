import streamlit as st


def display_youtube_video(video_url: str):

    if not video_url:
        st.info("No video loaded.")
        return

    st.video(video_url)