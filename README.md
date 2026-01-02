# YT Knowledge Assistant

A powerful AI assistant that watches YouTube videos for you and answers questions based on their content using embeddings and LLMs.

## Features
- **Video Processing**: Downloads audio, transcribes it (Whisper), and generates structured summaries.
- **RAG Q&A**: Asks questions about the video content and gets accurate answers sourced from the transcript.
- **Modern UI**: A clean, "Anime Mode" inspired frontend.

## Setup

1. **Backend**:
   ```bash
   pip install -r requirements.txt
   python -m uvicorn backend.app:app --reload --port 8000
   ```

2. **Frontend**:
   - Open `frontend/index.html` in your browser.
   - Or serve with Live Server (VS Code).

## Deployment

### Dependencies
- Python 3.10+
- FFmpeg (must be installed in your environment PATH)

### Environment Variables
Create a `.env` file with:
```
OPENAI_API_KEY=your_key_here
```

### Hosting
- **Backend**: Can be deployed on Render, Railway, or any Python-supporting host.
- **Frontend**: Update `API_BASE` in `script.js` to point to your deployed backend URL.
