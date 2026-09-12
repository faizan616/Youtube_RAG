# YouTube RAG Chat Bot

A Retrieval-Augmented Generation (RAG) application that allows users to chat with YouTube videos. The system ingests YouTube video transcripts, processes them through a hybrid retrieval system (combining semantic search with keyword-based BM25), and enables users to ask questions about the video content.

## Features

- **YouTube Video Ingestion**: Fetch transcripts from YouTube videos using the YouTube Transcript API
- **Multi-language Support**: Automatic translation of non-English videos to English
- **Hybrid Retrieval**: Combines FAISS vector search with BM25 keyword search for optimal relevance
- **Document Reranking**: Uses cross-encoder models to improve result relevance
- **AI-Powered Summarization**: Generates comprehensive video summaries using LLMs
- **Interactive Chat Interface**: Ask questions and get answers with source citations
- **Streamlit Web UI**: Clean, responsive interface built with Streamlit

## Project Structure

```
youtube-rag-chat-bot/
├── app.py                    # Main Streamlit application
├── components/               # Core processing components
│   ├── ingestion.py          # YouTube transcript ingestion
│   ├── translation.py        # Text translation (non-English to English)
│   ├── chunking.py           # Text splitting into chunks
│   ├── embedding.py          # Embedding model initialization
│   ├── vector_store.py       # FAISS vector store operations
│   ├── retriever.py          # Hybrid retrieval (dense + sparse)
│   ├── re_ranker.py          # Document reranking with cross-encoder
│   ├── llm_client.py         # Groq LLM initialization
│   └── prompt_templates.py   # Prompt templates for summarization and QA
├── ui/                       # User interface components
│   ├── chat.py               # Chat interface
│   ├── summary.py            # Summary display
│   ├── transcript.py         # Transcript viewer
│   ├── metrics.py            # Statistics display
│   ├── header.py             # Application header
│   ├── loader.py             # Processing status indicators
│   ├── styles.py             # Custom CSS
│   ├── components.py         # Reusable UI components
│   └── utils.py              # UI utility functions
├── .env.example              # Environment variables template
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## How It Works

1. **Ingestion**: Extract transcript from YouTube video using video ID
2. **Translation**: Convert non-English transcripts to English (if needed)
3. **Chunking**: Split transcript into smaller, manageable chunks
4. **Embedding**: Convert text chunks into vector embeddings
5. **Storage**: Store embeddings in FAISS vector store
6. **Retrieval**: Use hybrid search (FAISS + BM25) to find relevant chunks
7. **Reranking**: Re-rank results using cross-encoder model for better relevance
8. **Generation**: Use LLM to generate answers or summaries based on retrieved context

## Getting Started

See [SETUP.md](SETUP.md) for installation and running instructions.

## Architecture Overview

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system architecture.

## API Details

See [API.md](API.md) for backend components and API details.

## RAG Pipeline

See [RAG_PIPELINE.md](RAG_PIPELINE.md) for detailed explanation of the RAG workflow.

## UI

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/cf0ef7be-3f5e-4fa8-af22-0cf6d2c80ef0" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3be9b901-2266-48ab-806e-d2b4093d429f" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a295c275-31d7-41ca-8bfe-6a4249b6d9d2" />




## License

MIT License - feel free to use and modify this project for your own purposes.
