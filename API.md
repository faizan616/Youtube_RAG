# Backend/API Details

## Overview

This document details the backend components and API interfaces of the YouTube RAG Chat Bot. While the application is built as a monolithic Streamlit app, it follows a modular architecture where each component has well-defined responsibilities and interfaces.

## Component APIs

### 1. Ingestion Module (`components/ingestion.py`)

Fetches and processes YouTube video transcripts.

#### Functions

##### `extract_video_id(url: str) -> str`
Extracts YouTube video ID from various URL formats.

**Parameters:**
- `url`: YouTube URL (standard, youtu.be, or embed format)

**Returns:**
- Video ID string

**Raises:**
- `ValueError`: If URL format is invalid

##### `ingest_youtube_video(url: str) -> dict`
Main ingestion function that fetches transcript and metadata.

**Parameters:**
- `url`: YouTube video URL

**Returns:**
Dictionary containing:
- `video_id`: YouTube video ID
- `transcript`: Full transcript text
- `language_code`: Language code from YouTube metadata (e.g., 'en', 'es')

**Raises:**
- `ValueError`: For invalid URLs or unavailable transcripts
- `Exception`: For network or API errors

### 2. Translation Module (`components/translation.py`)

Handles translation of non-English transcripts to English.

#### Functions

##### `get_groq_client() -> Groq`
Initializes and returns Groq client instance.

**Returns:**
- Configured Groq client

**Raises:**
- `ValueError`: If GROQ_API_KEY is not set

##### `split_transcript(text: str, max_chars: int = 3000) -> list[str]`
Splits text into chunks for API request sizing.

**Parameters:**
- `text`: Input text to split
- `max_chars`: Maximum characters per chunk

**Returns:**
- List of text chunks

##### `translate_to_english(text: str, source_language: str) -> str`
Translates complete text to English without summarizing.

**Parameters:**
- `text`: Source text to translate
- `source_language`: Language code of source text

**Returns:**
- English translation of input text

**Raises:**
- `RuntimeError`: If translation fails or produces no text

### 3. Chunking Module (`components/chunking.py`)

Splits text into smaller chunks for processing.

#### Functions

##### `chunk_documents(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]`
Splits LangChain Documents into smaller chunks.

**Parameters:**
- `documents`: List of Document objects
- `chunk_size`: Maximum size of each chunk
- `chunk_overlap`: Number of overlapping characters

**Returns:**
- List of chunked Document objects

**Raises:**
- `ValueError`: If chunk_overlap >= chunk_size

##### `chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]`
Splits plain text into smaller text chunks.

**Parameters:**
- `text`: Text to split
- `chunk_size`: Maximum size of each chunk
- `chunk_overlap`: Number of overlapping characters

**Returns:**
- List of text chunks

**Raises:**
- `ValueError`: If chunk_overlap >= chunk_size

### 4. Embedding Module (`components/embedding.py`)

Initializes and returns embedding models.

#### Functions

##### `get_embedding_model(model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> HuggingFaceEmbeddings`
Creates and returns HuggingFace embedding model.

**Parameters:**
- `model_name`: Name of the sentence-transformers model

**Returns:**
- Configured HuggingFaceEmbeddings instance

### 5. Vector Store Module (`components/vector_store.py`)

Manages FAISS vector store operations.

#### Functions

##### `create_vector_store(documents: List[Document], embeddings: Embeddings) -> FAISS`
Creates FAISS vector store from documents.

**Parameters:**
- `documents`: Documents to store
- `embeddings`: Embedding model for vector conversion

**Returns:**
- FAISS vector store instance

##### `save_vector_store(vector_store: FAISS, path: str) -> None`
Saves FAISS vector store to disk.

**Parameters:**
- `vector_store`: FAISS instance to save
- `path`: Directory path for storage

##### `load_vector_store(path: str, embeddings: Embeddings) -> FAISS`
Loads existing FAISS vector store from disk.

**Parameters:**
- `path`: Directory path containing saved index
- `embeddings`: Embedding model used during creation

**Returns:**
- Loaded FAISS vector store instance

##### `add_documents_to_vector_store(vector_store: FAISS, documents: List[Document]) -> FAISS`
Adds additional documents to existing vector store.

**Parameters:**
- `vector_store`: Existing FAISS instance
- `documents`: Documents to add

**Returns:**
- Updated FAISS vector store instance

##### `similarity_search(vector_store: FAISS, query: str, k: int = 4) -> List[Document]`
Finds most relevant documents for a query.

**Parameters:**
- `vector_store`: FAISS vector store
- `query`: User's question
- `k`: Number of documents to return

**Returns:**
- List of relevant Document objects

### 6. Retriever Module (`components/retriever.py`)

Implements hybrid retrieval combining semantic and keyword search.

#### Class: `HybridRetriever`

Combines FAISS (dense) and BM25 (sparse) search methods.

##### `__init__(self, vector_store, documents, dense_k: int = 8, keyword_k: int = 8)`
Initializes the hybrid retriever.

**Parameters:**
- `vector_store`: FAISS vector store instance
- `documents`: List of Documents for BM25 indexing
- `dense_k`: Number of results from FAISS search
- `keyword_k`: Number of results from BM25 search

##### `search(self, query: str) -> List[Document]`
Performs hybrid search and returns merged, deduplicated results.

**Parameters:**
- `query`: Search query string

**Returns:**
- List of unique Document objects ranked by relevance

### 7. Reranker Module (`components/re_rank.py`)

Improves retrieval results using cross-encoder models.

#### Class: `DocumentReranker`

Uses cross-encoder models to re-score retrieval results.

##### `__init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2")`
Initializes the reranker with a cross-encoder model.

**Parameters:**
- `model_name`: Name of the cross-encoder model

##### `rerank(self, query: str, documents: list, top_k: int = 4) -> list`
Re-ranks documents based on query relevance.

**Parameters:**
- `query`: User's question
- `documents`: List of Document objects to re-rank
- `top_k`: Number of top documents to return

**Returns:**
- List of top-k re-ranked Document objects with relevance scores in metadata

### 8. LLM Client Module (`components/llm_client.py`)

Interfaces with Groq language models.

#### Functions

##### `get_groq_llm(model_name: Optional[str] = None, temperature: float = 0.2, max_tokens: int = 2000, **kwargs) -> ChatGroq`
Creates and returns LangChain-compatible Groq LLM.

**Parameters:**
- `model_name`: Specific model to use (optional)
- `temperature`: Sampling temperature (0.0 to 1.0)
- `max_tokens`: Maximum tokens in response
- `**kwargs`: Additional parameters passed to ChatGroq

**Returns:**
- Configured ChatGroq instance

**Raises:**
- `ValueError`: If GROQ_API_KEY is not set

### 9. Prompt Templates Module (`components/prompt_templates.py`)

Defines structured prompts for summarization and QA.

#### Templates

##### `SUMMARY_PROMPT`
Template for generating video summaries with specific structure.

**Variables:**
- `{transcript}`: Video transcript text

##### `SUMMARY_MAP_PROMPT`
Template for summarizing sections of long transcripts.

**Variables:**
- `{transcript}`: Transcript section text

##### `SUMMARY_REDUCE_PROMPT`
Template for combining intermediate summaries.

**Variables:**
- `{summaries}`: Set of intermediate summaries

##### `FINAL_SUMMARY_PROMPT`
Template for final summary generation.

**Variables:**
- `{content}`: Content to summarize (transcript or intermediate summaries)

##### `QA_PROMPT`
Template for question answering based on retrieved context.

**Variables:**
- `{context}`: Retrieved transcript excerpts
- `{question}`: User's question

## Data Models

### Document Format
The system uses LangChain `Document` objects with the following structure:
- `page_content`: Text content of the chunk
- `metadata`: Dictionary containing:
  - `chunk_id`: Sequential ID of the chunk
  - `chunk_index`: Index from chunking process (in chunking module)
  - `source`: Typically "YouTube transcript"
  - `rerank_score`: Relevance score from reranker (when applicable)

### Session State Keys
The application stores processed data in Streamlit session state:
- `video_loaded`: Boolean indicating if video is processed
- `video_url`: Original YouTube URL
- `video_id`: Extracted YouTube video ID
- `original_transcript`: Transcript in original language
- `english_transcript`: Translated transcript (or original if already English)
- `language_code`: Language code from YouTube
- `documents`: List of Document objects (chunks)
- `vector_store`: FAISS vector store instance
- `hybrid_retriever`: HybridRetriever instance
- `reranker`: DocumentReranker instance
- `llm`: Groq LLM for QA
- `summary`: AI-generated video summary
- `chat_history`: List of question-answer exchanges

## Integration Points

### Video Processing Flow
1. `ingestion.ingest_youtube_video()` → transcript data
2. `translation.translate_to_english()` (if needed) → English transcript
3. `chunking.chunk_text()` → text chunks
4. Convert chunks to Document objects with metadata
5. `embedding.get_embedding_model()` → embedding model
6. `vector_store.create_vector_store()` → FAISS index
7. `retriever.HybridRetriever()` → hybrid search capability
8. `re_ranker.DocumentReranker()` → reranking capability
9. `llm_client.get_groq_llm()` → LLM instances for QA and summarization
10. `prompt_templates.*` → structured prompts for LLM calls

### Query Processing Flow
1. User question received via UI
2. `hybrid_retriever.search(question)` → candidate documents
3. `reranker.rerank(question, documents)` → re-ranked documents
4. Build context from top document contents
5. Format `QA_PROMPT` with context and question
6. `llm.invoke(formatted_prompt)` → generated answer
7. Return answer with source documents

## External APIs

### Groq API
Used for:
- Text translation (non-English to English)
- Video summarization
- Question answering

**Endpoint**: `https://api.groq.com/openai/v1/chat/completions`
**Authentication**: Bearer token via `GROQ_API_KEY` environment variable

### YouTube Transcript API
Used for:
- Fetching video transcripts
- Obtaining language metadata

**No authentication required** for public videos
**Rate limits**: Apply based on IP address

### HuggingFace Models
Used for:
- Text embeddings (sentence-transformers)
- Cross-encoder reranking

**Models downloaded from**: HuggingFace model hub
**No API keys required** for public models
**Local caching**: Models cached after first download

## Error Handling

### Exception Types
Each module raises specific exceptions that are caught and handled in the main application:

- `ValueError`: Invalid input (URLs, parameters)
- `RuntimeError`: Processing failures (translation, model loading)
- `Exception`: Network or API failures

### Error Propagation
Errors are propagated up to the main `process_video()` function in `app.py`, where they are caught and displayed to the user via Streamlit's error handling mechanisms.

## Performance Considerations

### Model Loading
- Embedding and reranking models are loaded once per session
- LLM instances are created on-demand
- First video processing includes model loading overhead

### Memory Usage
- Vector stores are kept in session state for active video
- Large videos may consume significant memory for embeddings
- Consider implementing disk-based vector stores for large corpora

### API Rate Limits
- Groq API: Respect rate limits via request delays
- YouTube API: Implicit limits via video fetching frequency
- Mitigation: Caching and batching strategies

## Extensibility

### Adding New Components
1. Create new module in `components/` directory
2. Define clear input/output interfaces
3. Update `app.py` to instantiate and use new component
4. Add any required environment variables to `.env.example`

### Changing Models
1. Update relevant environment variables in `.env`
2. Modify default parameters in component initialization functions
3. Ensure compatibility with input/output formats

### Supporting Additional Languages
Current implementation translates all content to English. To support native language processing:
1. Modify translation module to bypass translation for supported languages
2. Update embedding models to multilingual variants
3. Adjust prompt templates for target language
4. Ensure LLM supports target language

## Security

### API Key Management
- API keys stored in `.env` file (never committed)
- Access restricted to backend components only
- Consider using secrets management for production deployments

### Data Privacy
- Transcripts processed in memory only
- No persistent storage of video content by default
- Vector stores can be configured for persistence if needed

### Input Sanitization
- YouTube URL validation via regex patterns
- Text processing handles Unicode properly
- HTML escaping in UI components prevents XSS