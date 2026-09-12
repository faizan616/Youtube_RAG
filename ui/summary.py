import streamlit as st


def display_summary(summary: str):
    """
    Display the AI-generated summary inside a
    scrollable summary panel.
    """

    if not summary:
        summary = "No summary available."

    with st.container(
        height=520,
        border=True
    ):

        st.markdown(
            "### ✨ AI Summary"
        )

        st.markdown("---")

        # Render the summary as Markdown.
        # This makes **bold**, headings, bullets, etc.
        # display correctly.
        st.markdown(
            summary
        )