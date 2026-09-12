import streamlit as st


class ProcessingStatus:
    """Small UI controller for the processing pipeline."""

    def __init__(self):
        self.status = st.status(
            "Processing video...",
            expanded=True
        )

        self.steps = {}

        labels = [
            ("ingestion", "Ingestion"),
            ("translation", "Translation"),
            ("chunking", "Chunking"),
            ("embeddings", "Embeddings"),
            ("vector_store", "Vector Store"),
            ("reranker", "Reranker"),
            ("summary", "Summary"),
        ]

        # Create all rows immediately so the user can see the
        # complete pipeline while processing is happening.
        for key, label in labels:
            self.steps[key] = self.status.empty()
            self.steps[key].write(f"○ **{label}** • Waiting...")

    def complete(self, key: str, message: str):
        self.steps[key].write(
            f"✓ **{message.split('•', 1)[0].strip()}**"
            + (f" • {message.split('•', 1)[1].strip()}" if "•" in message else "")
        )

    def write(self, message: str):
        """Compatibility helper for any caller that needs a status write."""
        self.status.write(message)

    def update(self, **kwargs):
        self.status.update(**kwargs)


def create_processing_status():
    return ProcessingStatus()


def show_ingestion(status, language: str):
    status.steps["ingestion"].write(
        f"✓ **Ingestion** • Transcript fetched • Language: `{language}`"
    )


def show_translation(
    status,
    translation_requests=None,
    skipped=False,
):
    if skipped:
        status.steps["translation"].write(
            "✓ **Translation** • Skipped • Transcript already in English"
        )
    else:
        status.steps["translation"].write(
            f"✓ **Translation** • Complete English transcript • "
            f"{translation_requests} translation requests"
        )


def show_chunking(status, total_chunks: int, total_characters: int):
    status.steps["chunking"].write(
        f"✓ **Chunking** • {total_chunks} chunks • "
        f"{total_characters:,} characters"
    )


def show_embeddings(status):
    status.steps["embeddings"].write(
        "✓ **Embeddings** • Embeddings generated"
    )


def show_vector_store(status):
    status.steps["vector_store"].write(
        "✓ **Vector Store** • FAISS + BM25 ready"
    )


def show_reranker(status):
    status.steps["reranker"].write(
        "✓ **Reranker** • CrossEncoder ready"
    )


def show_summary(status, message: str = "AI summary generated"):
    status.steps["summary"].write(
        f"✓ **Summary** • {message}"
    )


def finish_processing(status):
    status.update(
        label="Video ready • Processing complete",
        state="complete",
        expanded=True
    )


def fail_processing(status, error: str):
    status.update(
        label="Processing failed",
        state="error",
        expanded=True
    )

    status.write(f"✗ {error}")
