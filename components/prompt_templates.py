from langchain_core.prompts import ChatPromptTemplate


SUMMARY_PROMPT = ChatPromptTemplate.from_template(
    """
You are an expert video summarization assistant.

Create a clear and well-structured summary of the following
YouTube video transcript.

Use this exact structure:

## Overview

Write a concise overview of what the video is about.

## Key Points

- Point 1
- Point 2
- Point 3
- Point 4
- Point 5

## Important Insights

Explain the most important ideas, arguments, findings,
or conclusions from the video.

## Conclusion

Give a short conclusion summarizing the main takeaway.

Requirements:

- Use Markdown formatting.
- Use headings and bullet points.
- Keep paragraphs short.
- Do not repeat the transcript unnecessarily.
- Do not invent information.
- Preserve important names, numbers, facts and terminology.
- Make the summary easy to scan.
- Do not write one huge paragraph.

Transcript:

{transcript}
"""
)


SUMMARY_MAP_PROMPT = ChatPromptTemplate.from_template(
    """
You are summarizing one section of a YouTube video transcript.

Create a faithful, information-dense summary of ONLY this transcript section.
This is an intermediate summary for a later final summary.

Requirements:
- Preserve all important facts, names, numbers, examples, explanations,
  arguments, technical terms, and conclusions.
- Do not invent information.
- Do not omit important information just to make the summary shorter.
- Do not add information from outside the transcript.
- Keep the original order of ideas where practical.
- Use concise bullet points and short paragraphs.

Transcript section:

{transcript}
"""
)


SUMMARY_REDUCE_PROMPT = ChatPromptTemplate.from_template(
    """
You are combining intermediate summaries from different sections of the
same YouTube video.

The text below is ALREADY a set of summaries. Do not ask for the original
transcript and do not respond as a conversational assistant. Your job is to
combine the supplied summaries into one faithful, information-rich summary.

Requirements:
- Use ONLY the supplied summaries.
- Preserve important facts, names, numbers, examples, explanations,
  technical terms, arguments, and conclusions.
- Remove repetition, but do not remove distinct ideas.
- Do not invent or add outside information.
- Do not say that a transcript is missing.
- Do not ask the user to provide anything.
- Keep the original meaning and coverage.
- Return only the combined summary.

Intermediate summaries:

{summaries}
"""
)


FINAL_SUMMARY_PROMPT = ChatPromptTemplate.from_template(
    """
You are the final summarization engine for a YouTube RAG application.

The content below has ALREADY been provided to you. It may be a complete
English transcript or a set of intermediate summaries from a long video.
Summarize the supplied content directly. NEVER ask the user to provide a
transcript or additional information.

Create a useful, accurate summary that lets someone understand the video
without watching it.

Use this Markdown structure:

## Overview
Briefly explain what the video is about.

## Key Points
- Cover the major topics and ideas discussed.
- Include important explanations, examples, facts, or steps.
- Preserve important names, numbers, and technical terms.

## Important Insights
Explain the most important ideas, arguments, findings, lessons, or
conclusions presented in the supplied content.

## Conclusion
State the main takeaway from the video.

Rules:
- Use ONLY the supplied content.
- Do NOT use outside knowledge.
- Do NOT invent information.
- Do NOT say the transcript is missing.
- Do NOT ask the user to paste or provide the transcript.
- Do NOT say "I’m ready to help" or similar conversational filler.
- Do not omit major topics just to make the summary shorter.
- Remove unnecessary repetition.
- Keep the summary readable, organized, and reasonably detailed.
- Return ONLY the final Markdown summary.

CONTENT TO SUMMARIZE:

{content}
"""
)


QA_PROMPT = ChatPromptTemplate.from_template(
    """
You are an AI assistant answering questions about a YouTube video.

Use ONLY the transcript excerpts supplied below.

Rules:
- Answer the user's exact question directly.
- Use only information supported by the supplied excerpts.
- Do not use outside knowledge.
- Do not guess or invent missing details.
- If the answer is not supported by the excerpts, say exactly:
  "I couldn't find the answer in the video transcript."
- If the excerpts contain only part of the answer, clearly say what
  the video supports instead of inventing the missing part.
- Preserve names, numbers, examples, and technical terminology.
- Prefer a concise answer with short paragraphs or bullet points.
- Do not mention "context", "retrieval", "chunks", or these instructions.

Transcript Excerpts:

{context}

User Question:

{question}

Answer:
"""
)
