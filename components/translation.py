import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


LANGUAGE_NAMES = {
    "en": "English",
    "ta": "Tamil",
    "hi": "Hindi",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "ko": "Korean",
    "bn": "Bengali",
    "mr": "Marathi",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "ur": "Urdu",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ja": "Japanese",
    "zh": "Chinese",
}


def get_language_name(language_code: str) -> str:
    code = (language_code or "").lower().strip()
    base_code = code.split("-")[0]
    return LANGUAGE_NAMES.get(base_code, code or "the source language")


def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not set. Please add it to your .env file."
        )
    return Groq(api_key=api_key)


def split_transcript(text: str, max_chars: int = 3000) -> list[str]:
    """Split transcript only for translation API request sizing."""
    if not text:
        return []

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    chunks = []
    current = []
    current_length = 0

    for line in lines:
        line_length = len(line)
        if current and current_length + line_length + 1 > max_chars:
            chunks.append("\n".join(current))
            current = []
            current_length = 0

        current.append(line)
        current_length += line_length + 1

    if current:
        chunks.append("\n".join(current))

    return chunks


def _looks_suspicious(source: str, translation: str) -> bool:
    """Detect output that is obviously too short to be a full translation."""
    if len(source) < 500:
        return False
    return len(translation.strip()) < len(source) * 0.35


def _translate_request(client, model: str, language_name: str, source_language: str, chunk: str) -> str:
    prompt = f"""
Translate EVERY sentence in the following YouTube transcript from {language_name} ({source_language}) to English.

This is a COMPLETE TRANSLATION task, NOT a summarization task.

Rules:
- Translate every sentence and every caption.
- Do not summarize, compress, shorten, or paraphrase away information.
- Do not skip repeated information.
- Do not combine multiple sentences into one shorter sentence.
- Preserve the original order.
- Preserve names, numbers, examples, explanations, technical terms, and details.
- Do not add information that is not present in the source.
- Return only the English translation.
- Do not add headings, notes, explanations, or markdown.

SOURCE TRANSCRIPT:
{chunk}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_completion_tokens=3000,
        include_reasoning=False,
        reasoning_effort="low",
    )

    return (getattr(response.choices[0].message, "content", None) or "").strip()


def _translate_chunk_with_fallback(
    client,
    model: str,
    language_name: str,
    source_language: str,
    chunk: str,
    depth: int = 0,
) -> str:
    """Translate a chunk, retrying and recursively splitting suspicious output.

    A short model response is NOT accepted as a valid translation. Instead of
    failing the whole video immediately, the problematic source chunk is split
    into smaller requests and translated completely.
    """
    last_error = None

    # First try the complete chunk twice.
    for _ in range(2):
        try:
            result = _translate_request(
                client, model, language_name, source_language, chunk
            )
            if result and not _looks_suspicious(chunk, result):
                return result
            if not result:
                last_error = "empty translation"
            else:
                last_error = (
                    f"suspiciously short output ({len(result)} chars for "
                    f"{len(chunk)} source chars)"
                )
        except Exception as exc:
            last_error = exc

    # If the model still compresses a large chunk, split the SOURCE itself.
    # This preserves all source content instead of accepting a summary.
    if len(chunk) >= 800 and depth < 3:
        smaller_chunks = split_transcript(chunk, max_chars=max(900, len(chunk) // 2))
        if len(smaller_chunks) > 1:
            translated_parts = []
            for smaller in smaller_chunks:
                translated_parts.append(
                    _translate_chunk_with_fallback(
                        client,
                        model,
                        language_name,
                        source_language,
                        smaller,
                        depth + 1,
                    )
                )
            return "\n".join(translated_parts)

    raise RuntimeError(
        f"Translation failed after retries: {last_error}. "
        f"Source chunk length: {len(chunk)} chars. Model: {model}."
    )


def translate_to_english(text: str, source_language: str) -> str:
    """Translate the COMPLETE transcript to English without summarizing."""
    if not text or not text.strip():
        return text

    if (source_language or "").lower().startswith("en"):
        return text

    client = get_groq_client()
    model = os.getenv(
        "GROQ_TRANSLATION_MODEL",
        os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
    )
    language_name = get_language_name(source_language)

    # Keep normal translation requests around 3,000 chars as requested.
    text_chunks = split_transcript(text, max_chars=3000)
    translated_chunks = []

    for index, chunk in enumerate(text_chunks, start=1):
        translated = _translate_chunk_with_fallback(
            client,
            model,
            language_name,
            source_language,
            chunk,
        )
        translated_chunks.append(translated)

    result = "\n".join(translated_chunks).strip()
    if not result:
        raise RuntimeError("Translation produced no text.")

    return result
