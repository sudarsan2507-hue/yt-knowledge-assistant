# YT Knowledge Assistant

A powerful AI assistant that watches YouTube videos for you and answers questions based on their content using embeddings and LLMs. Now featuring a vibrant "AI Buddy" interface!

## Features
- **Video Processing**: Downloads audio, transcribes it (Whisper), and generates structured summaries.
- **RAG Q&A**: Asks questions about the video content and gets accurate answers sourced from the transcript.
- **Smart Translation**: Choose between processing in the **Original Language** or translating the summary/insights to **English**.
- **Modern UI**: A clean, "Anime Mode" inspired frontend with your personal "AI Buddy".

## Tech Stack
- **Backend**: Python, FastAPI
- **Vector DB**: SQLite (lightweight, local storage) with `FastEmbed` for on-the-fly embedding generation.
- **Frontend**: HTML5, Vanilla CSS, JavaScript (No heavy frameworks).
- **AI Models**: OpenAI (GPT) for reasoning, Whisper for transcription.

## Setup

### 1. Backend
```bash
pip install -r requirements.txt
python -m uvicorn backend.app:app --reload --port 8000
```

### 2. Frontend
- Open `frontend/index.html` in your browser.
- Or serve with Live Server (VS Code) for the best experience.

## Deployment (Render)

### 1. Build Command
```bash
pip install -r requirements.txt
```

### 2. Start Command
**CRITICAL**: Render defaults to `gunicorn app:app` which fails. You MUST use:
```bash
uvicorn backend.app:app --host 0.0.0.0 --port 10000
```
*(Update this in Settings > Start Command)*

### 3. Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API Key.
- `PYTHON_VERSION`: `3.10.0` (Recommended).

### 4. YouTube Bot Detection Fix (Cookies)
To avoid "Sign in to confirm you're not a bot" errors:
1. Install "Get cookies.txt LOCALLY" extension in your browser.
2. Go to YouTube and export cookies to a file.
3. In Render Dashboard > **Environment** > **Secret Files**.
4. Add a file named `cookies.txt` and paste the content.
