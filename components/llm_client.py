import os
from typing import Optional

from langchain_groq import ChatGroq
from dotenv import load_dotenv


load_dotenv()


def get_groq_llm(
    model_name: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: int = 2000,
    **kwargs
) -> ChatGroq:
    """
    Create and return a LangChain-compatible Groq LLM.

    This component is responsible only for:
        - Loading Groq configuration
        - Creating the ChatGroq model

    It does NOT:
        - Fetch YouTube transcripts
        - Translate text
        - Chunk documents
        - Create embeddings
        - Create vector stores
        - Retrieve documents
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY must be set in environment variables."
        )

    if model_name is None:
        model_name = os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-20b"
        )

    return ChatGroq(
        groq_api_key=api_key,
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )