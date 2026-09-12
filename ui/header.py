import streamlit as st


def display_header():

    st.html(
        """
        <div class="app-header">

            <div class="youtube-logo">
                <div class="youtube-play"></div>
            </div>

            <div>
                <div class="app-title">
                    YouTube RAG
                </div>

                <div class="app-subtitle">
                    Understand any YouTube video with AI
                </div>
            </div>

        </div>
        """
    )