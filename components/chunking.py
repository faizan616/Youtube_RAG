from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(
    documents: List[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List[Document]:
    """
    Split LangChain Documents into smaller chunks.

    Responsibility:
        Document → smaller Documents

    Args:
        documents: List of LangChain Document objects.
        chunk_size: Maximum size of each chunk.
        chunk_overlap: Number of overlapping characters.

    Returns:
        List of chunked Document objects.
    """

    if not documents:
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size."
        )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            " ",
            "",
        ],
    )

    chunked_documents = text_splitter.split_documents(
        documents
    )

    # Add metadata to each chunk
    for index, document in enumerate(chunked_documents):
        document.metadata["chunk_index"] = index

    return chunked_documents


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List[str]:
    """
    Split plain text into smaller text chunks.

    Responsibility:
        Plain text → text chunks

    Args:
        text: Text to split.
        chunk_size: Maximum size of each chunk.
        chunk_overlap: Number of overlapping characters.

    Returns:
        List of text chunks.
    """

    if not text or not text.strip():
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size."
        )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            " ",
            "",
        ],
    )

    return text_splitter.split_text(text)