from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model(
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
):
    """
    Create and return the HuggingFace embedding model.

    This component is responsible only for:
        - Loading the embedding model
        - Converting text into embeddings

    It does NOT:
        - Fetch YouTube transcripts
        - Translate text
        - Split documents
        - Create the vector store
        - Retrieve documents
    """

    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={
            "device": "cpu"
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )