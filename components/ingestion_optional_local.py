import re
from youtube_transcript_api import YouTubeTranscriptApi


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
    Fetch the best available YouTube transcript and return the
    language code supplied by YouTube itself.

    We intentionally do NOT use langdetect here. Transcript
    language metadata is more reliable than guessing the language
    from transcript text.
    """
    video_id = extract_video_id(url)

    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)

    # Prefer manually created transcripts.
    transcript = None

    for item in transcript_list:
        if not item.is_generated:
            transcript = item
            break

    # Fall back to an auto-generated transcript.
    if transcript is None:
        for item in transcript_list:
            if item.is_generated:
                transcript = item
                break

    if transcript is None:
        raise ValueError("No transcript available for this video.")

    fetched_transcript = transcript.fetch()

    text = "\n".join(
        snippet.text
        for snippet in fetched_transcript
    )

    # IMPORTANT:
    # Use YouTube's actual transcript language metadata.
    language_code = transcript.language_code

    return {
        "video_id": video_id,
        "transcript": text,
        "language_code": language_code,
    }
