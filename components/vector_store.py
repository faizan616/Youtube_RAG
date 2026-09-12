from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings


def create_vector_store(
    documents: List[Document],
    embeddings: Embeddings
) -> FAISS:
    """
    Create a FAISS vector store from documents.

    Args:
        documents: Documents that need to be stored.
        embeddings: Embedding model used to convert text into vectors.

    Returns:
        FAISS vector store.
    """

    return FAISS.from_documents(
        documents,
        embeddings
    )


def save_vector_store(
    vector_store: FAISS,
    path: str
) -> None:
    """
    Save the FAISS vector store to disk.
    """

    vector_store.save_local(path)


def load_vector_store(
    path: str,
    embeddings: Embeddings
) -> FAISS:
    """
    Load an existing FAISS vector store from disk.
    """

    return FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )


def add_documents_to_vector_store(
    vector_store: FAISS,
    documents: List[Document]
) -> FAISS:
    """
    Add additional documents to an existing vector store.
    """

    vector_store.add_documents(documents)

    return vector_store


def similarity_search(
    vector_store: FAISS,
    query: str,
    k: int = 4
) -> List[Document]:
    """
    Find the most relevant documents for a user query.

    Args:
        vector_store: FAISS vector store.
        query: User's question.
        k: Number of relevant documents to return.

    Returns:
        List of relevant Document objects.
    """

    return vector_store.similarity_search(
        query,
        k=k
    )