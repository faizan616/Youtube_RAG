import os
import re

import requests


def extract_video_id(url: str) -> str:
    patterns = [
        r"(?:v=|youtu\.be/|youtube\.com/embed/)([^&?/]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)

        if match:
            return match.group(1)

    raise ValueError("Invalid YouTube URL")


def ingest_youtube_video(url: str) -> dict:
    """
    Fetch a YouTube transcript through Supadata.

    Supadata handles transcript retrieval from YouTube and returns
    the transcript language metadata, so we do not need langdetect.
    """

    video_id = extract_video_id(url)

    api_key = os.getenv("SUPADATA_API_KEY")

    if not api_key:
        raise ValueError(
            "SUPADATA_API_KEY is not configured."
        )

    response = requests.get(
        "https://api.supadata.ai/v1/transcript",
        params={
            "url": url,
        },
        headers={
            "x-api-key": api_key,
        },
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    if "content" not in data:
        raise ValueError(
            "Supadata did not return a transcript."
        )

    content = data["content"]

    # Supadata returns transcript segments.
    # Convert them into the plain text expected by the RAG pipeline.
    if isinstance(content, list):
        text = "\n".join(
            segment["text"]
            for segment in content
            if segment.get("text")
        )
    else:
        # Handles plain-text response if returned.
        text = str(content)

    if not text.strip():
        raise ValueError(
            "The transcript returned by Supadata is empty."
        )

    # Supadata provides the detected transcript language.
    language_code = data.get("lang", "unknown")

    return {
        "video_id": video_id,
        "transcript": text,
        "language_code": language_code,
    }
