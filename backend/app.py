from dotenv import load_dotenv
load_dotenv()

import sys
import io

# Force UTF-8 for stdout/stderr to handle emojis on Windows console
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from fastapi import FastAPI
from pydantic import BaseModel

# import your existing logic
from backend.search_and_qa import search
from backend.llm_answer import generate_answer
from backend.video_processing import process_youtube_video


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str


class ProcessRequest(BaseModel):
    url: str


@app.post("/process_video")
def process_video_endpoint(data: ProcessRequest):
    result = process_youtube_video(data.url)
    return result


@app.post("/ask")
def ask(data: AskRequest):
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
