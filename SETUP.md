# Installation & Running

## Prerequisites

Before installing and running the YouTube RAG Chat Bot, ensure you have the following prerequisites:

- **Python 3.8+** (tested with Python 3.9-3.11)
- **Git** (for cloning the repository)
- **An API key from Groq** (for LLM functionality)
- **Internet connection** (to fetch YouTube transcripts and access external APIs)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd youtube-rag-chat-bot
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Using venv
python -m venv .venv-RAG
.\.venv-RAG\Scripts\activate  # Windows
source .venv-RAG/bin/activate  # Linux/Mac

# Or using conda
conda create -n youtube-rag python=3.9
conda activate youtube-rag
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root based on the provided example:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edit the `.env` file to add your actual Groq API key:

```env
GROQ_API_KEY=your_actual_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b

# Optional: dedicated model for transcript translation
GROQ_TRANSLATION_MODEL=openai/gpt-oss-20b

# Summary settings
GROQ_SUMMARY_MODEL=openai/gpt-oss-20b
SUMMARY_MAP_THRESHOLD_CHARS=50000
SUMMARY_SECTION_CHARS=7000
SUMMARY_MAP_MAX_TOKENS=900
SUMMARY_REQUEST_DELAY_SECONDS=13
```

> **Note**: Never commit your `.env` file to version control as it contains sensitive API keys.

### 5. Verify Installation

```bash
python -c "import streamlit; print('Streamlit version:', streamlit.__version__)"
python -c "import langchain; print('LangChain installed')"
```

## Running the Application

### Development Mode

```bash
streamlit run app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`.

### Production Deployment

For production deployment, consider using:

```bash
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq API key for LLM access | (Required) |
| `GROQ_MODEL` | Model name for QA and translation | `openai/gpt-oss-20b` |
| `GROQ_TRANSLATION_MODEL` | Model name specifically for translation | Value of `GROQ_MODEL` |
| `GROQ_SUMMARY_MODEL` | Model name for summarization | Value of `GROQ_MODEL` |
| `SUMMARY_MAP_THRESHOLD_CHARS` | Character threshold for hierarchical summarization | `50000` |
| `SUMMARY_SECTION_CHARS` | Chunk size for map-reduce summarization | `7000` |
| `SUMMARY_MAP_MAX_TOKENS` | Maximum tokens for summary generation | `900` |
| `SUMMARY_REQUEST_DELAY_SECONDS` | Delay between LLM requests to avoid rate limits | `13` |

### Model Selection

The application uses Groq models by default. To use different models:

1. Obtain API access to desired models from Groq
2. Update the corresponding environment variables in `.env`
3. Available models can be found at [Groq Model Documentation](https://console.groq.com/docs/models)

## Troubleshooting

### Common Issues

#### 1. "GROQ_API_KEY not set" Error
- **Cause**: Missing or incorrect API key in `.env` file
- **Solution**: Verify `.env` file contains `GROQ_API_KEY=your_key_here` and restart the application

#### 2. YouTube Transcript Errors
- **Cause**: Video unavailable, region-restricted, or no transcript available
- **Solution**: Try a different YouTube URL or check video accessibility

#### 3. Slow Processing Times
- **Cause**: Network latency, model loading, or long videos
- **Solution**: 
  - First run loads models into memory (subsequent runs faster)
  - Long videos use hierarchical summarization which takes more time
  - Consider shorter videos for testing

#### 4. Streamlit Port Already in Use
- **Cause**: Another application using port 8501
- **Solution**: 
  ```bash
  streamlit run app.py --server.port=8502  # Use different port
  ```

### Dependency Issues

#### Missing Packages
If you encounter import errors:
```bash
pip install --upgrade -r requirements.txt
```

#### Version Conflicts
Try creating a fresh virtual environment:
```bash
# Remove existing
rm -rf .venv-RAG  # Windows: rmdir /s .venv-RAG
# Recreate
python -m venv .venv-RAG
.\.venv-RAG\Scripts\activate
pip install -r requirements.txt
```

## Development Setup

### Code Style
The project follows standard Python conventions:
- PEP 8 for styling
- Descriptive variable and function names
- Comprehensive docstrings for public functions

### Adding Dependencies
To add new packages:
```bash
pip install new-package-name
pip freeze > requirements.txt  # Update requirements file
```

### Making Changes
1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## Deployment Guides

### Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

ENTRYPOINT ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t youtube-rag .
docker run -p 8501:8501 youtube-rag
```

### Cloud Platforms

The application can be deployed to:
- **Streamlit Community Cloud** (push to GitHub, connect to streamlit.io/cloud)
- **Heroku** (with appropriate buildpack)
- **AWS Elastic Beanstalk**
- **Google Cloud Run**
- **Azure App Services**

## Verification

After installation, verify the setup by:
1. Loading a short YouTube video (under 5 minutes)
2. Confirming transcript loads correctly
3. Checking that summary is generated
4. Testing the Q&A functionality with a simple question
5. Verifying source citations appear in answers

## Support

For issues or questions:
1. Check the README.md for general information
2. Review error messages in the Streamlit interface
3. Consult the troubleshooting section above
4. Ensure all dependencies are correctly installed
5. Verify API keys and internet connectivity

Happy building! 🚀