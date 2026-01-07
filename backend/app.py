from dotenv import load_dotenv
load_dotenv()

import sys
import io

# Force UTF-8 for stdout/stderr to handle emojis on Windows console
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# import your existing logic
from backend.search_and_qa import search
from backend.llm_answer import generate_answer
from backend.video_processing import process_youtube_video


from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global Exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "type": type(exc).__name__}
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend is running"}


class AskRequest(BaseModel):
    question: str


class ProcessRequest(BaseModel):
    url: str


@app.post("/process_video")
def process_video_endpoint(data: ProcessRequest):
    logger.info(f"Processing URL: {data.url}")
    try:
        result = process_youtube_video(data.url)
        if "error" in result:
             logger.error(f"Processing failed logic: {result['error']}")
        return result
    except Exception as e:
        logger.error(f"Processing Error: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/ask")
def ask(data: AskRequest):
    logger.info(f"Asking: {data.question}")
    try:
        # Step 5: retrieve relevant chunks
        results = search(data.question)
    
        # extract only text from results
        context = [text for _, text in results]
    
        # Step 6: generate final answer
        answer = generate_answer(data.question, context)
    
        return {
            "question": data.question,
            "answer": answer
        }
    except Exception as e:
        logger.error(f"QA Error: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": str(e)})

# Mount Frontend Static Files (Last to avoid blocking API)
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
else:
    print(f"WARNING: Static dir not found at {static_dir}")

if __name__ == "__main__":
    import uvicorn
    # Use 0.0.0.0 for public access
    uvicorn.run(app, host="0.0.0.0", port=8000)
