# System Architecture

## Overview

The YouTube RAG Chat Bot follows a modular architecture designed for clarity, maintainability, and scalability. The system is organized into distinct layers that handle specific responsibilities in the video processing and question-answering pipeline.

## High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌────────────────────┐
│   User Interface │    │  Processing Core  │    │   External Services │
│   (Streamlit UI) │◄──►│ (Components)     │◄──►│ (YouTube, Groq, etc)│
└─────────────────┘    └──────────────────┘    └────────────────────┘
```

## Component Layers

### 1. User Interface Layer (`ui/`)

Responsible for all user interactions and presentation logic:
- **Header**: Application branding and navigation
- **Chat Interface**: Question input and answer display with source citations
- **Summary Panel**: AI-generated video summaries
- **Transcript Viewer**: Original and translated transcript display
- **Metrics Panel**: Statistics about processed video
- **Loader Components**: Visual feedback during processing
- **Styles**: Custom CSS for consistent theming
- **Utility Functions**: Helpers for UI rendering

### 2. Processing Core Layer (`components/`)

Contains all business logic for video processing and RAG functionality:
- **Ingestion**: Extracts transcripts from YouTube videos
- **Translation**: Converts non-English content to English
- **Chunking**: Splits text into semantically meaningful chunks
- **Embedding**: Generates vector representations of text
- **Vector Store**: Manages FAISS index for semantic search
- **Retriever**: Combines dense (FAISS) and sparse (BM25) search
- **Reranker**: Improves result relevance using cross-encoder models
- **LLM Client**: Interface to Groq language models
- **Prompt Templates**: Structured prompts for summarization and QA

### 3. External Services Layer

Third-party services integrated into the system:
- **YouTube Transcript API**: Source of video transcripts
- **Groq**: Fast LLM inference for translation, summarization, and QA
- **HuggingFace**: Embedding models (sentence-transformers)
- **Sentence-Transformers**: Cross-encoder models for reranking
- **FAISS**: Efficient similarity search engine
- **Rank-BM25**: Keyword-based search implementation

## Data Flow

### Video Processing Pipeline

1. **Input**: User provides YouTube URL
2. **Ingestion**: 
   - Extract video ID from URL
   - Fetch transcript using YouTube Transcript API
   - Detect language from YouTube metadata
3. **Translation** (if non-English):
   - Split transcript into chunks for API limits
   - Translate each chunk to English using Groq
   - Reconstruct full English transcript
4. **Chunking**:
   - Split transcript into overlapping chunks (1000 chars, 200 overlap)
   - Preserve metadata (chunk ID, source info)
5. **Embedding**:
   - Initialize HuggingFace embedding model
   - Convert chunks to vector embeddings
6. **Storage**:
   - Create FAISS vector store from embedded chunks
   - Initialize HybridRetriever with both FAISS and BM25 indices
7. **Reranking Setup**:
   - Initialize DocumentReranker with cross-encoder model
8. **LLM Initialization**:
   - Create Groq LLM instances for QA and summarization
9. **State Storage**:
   - Save all components to Streamlit session state
10. **Summarization**:
    - Generate video summary using hierarchical approach for long videos
    - Store summary in session state

### Question Answering Pipeline

1. **Input**: User asks a question in chat interface
2. **Retrieval**:
   - HybridRetriever searches both FAISS (semantic) and BM25 (keyword) indices
   - Returns candidate documents from both methods
3. **Reranking**:
   - Documents re-scored using cross-encoder model
   - Top-k documents selected based on relevance scores
4. **Context Building**:
   - Combine content from top reranked documents
5. **Generation**:
   - Pass context and question to Groq LLM using QA prompt template
   - Generate answer based solely on provided context
6. **Output**:
   - Display answer with source citations showing relevant transcript excerpts

## Key Design Decisions

### Hybrid Retrieval
Combines semantic search (FAISS) with keyword search (BM25) to capture both meaning-based and exact-match relevance. This addresses limitations of pure semantic search where specific terminology might be missed.

### Document Reranking
Uses cross-encoder models to post-process retrieval results, significantly improving relevance by considering query-document pairs holistically rather than relying solely on embedding similarity.

### Modular Component Design
Each processing step is isolated in its own component with clear input/output contracts, making the system easy to test, modify, and extend.

### Language-Agnostic Processing
By translating all content to English early in the pipeline, downstream components (embedding, retrieval, LLM) can operate on a single language, simplifying implementation while maintaining multi-language support.

## Scalability Considerations

### Processing Efficiency
- Translation and embedding operations are batched where possible
- Caching strategies can be added for repeated queries on same video
- Vector store persistence allows reuse across sessions

### Memory Management
- Streamlit session state stores processed video data
- Components are reinitialized only when new video is loaded
- FAISS indexes can be saved/loaded to disk for large corpora

### Extensibility Points
- New embedding models can be swapped by modifying `embedding.py`
- Different LLMs can be integrated by updating `llm_client.py`
- Additional retrieval methods can be added to `HybridRetriever`
- Alternative summarization approaches can be implemented in prompt templates

## Security and Reliability

### Error Handling
- Graceful degradation when services are unavailable
- Informative error messages for users
- Fallback mechanisms (e.g., auto-generated transcripts when manual not available)

### Configuration
- Environment variables for API keys and model selection
- Configurable parameters for chunking, retrieval, and summarization
- Template-based prompts allow easy customization without code changes

## Technologies Used

### Core Framework
- **Streamlit**: Web application framework
- **LangChain**: LLM application development library

### AI/ML Components
- **Groq**: High-speed LLM inference
- **HuggingFace Transformers**: Embedding and reranking models
- **Sentence-Transformers**: Specialized sentence embedding models

### Data Processing
- **FAISS**: Facebook AI Similarity Search for efficient vector search
- **Rank-BM25**: Best Matching 25 for keyword-based retrieval
- **YouTube Transcript API**: Official YouTube transcript extraction

### Utilities
- **Python-Dotenv**: Environment variable management
- **Regex**: URL parsing and video ID extraction

## Future Enhancements

### Features
- Support for multiple videos in same knowledge base
- Video timestamp linking in answers
- Export capabilities (transcripts, summaries, QA history)
- Multi-language UI support
- Advanced analytics dashboard

### Performance
- GPU acceleration for embedding generation
- Persistent vector storage for large document collections
- Query caching for repeated questions
- Batch processing for translation operations

### Integration
- Additional LLM providers (OpenAI, Anthropic, etc.)
- Alternative vector databases (Pinecone, Weaviate, etc.)
- Custom UI themes and branding options