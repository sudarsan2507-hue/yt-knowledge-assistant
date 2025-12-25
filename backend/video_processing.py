import os
import json
from openai import OpenAI
from backend.audio_extract import extract_audio
from backend.transcribe import transcribe_audio
from backend.chunks_text import chunk_text
from backend.embed_chunks import embed_chunks

openai_client = OpenAI()

def generate_structured_summary(text):
    """
    Generates a Topic/Subtopic structure from the transcript using LLM.
    """
    prompt = f"""
    Analyze the following video transcript and structure it into a clear, nested hierarchy of Topics and Subtopics.
    For each subtopic, provide a brief 1-sentence summary.
    
    Output JSON format:
    {{
        "title": "Video Title",
        "summary": "Main video summary",
        "topics": [
            {{
                "title": "Topic Name",
                "subtopics": [
                    {{ "name": "Subtopic Name", "summary": "Brief explanation" }}
                ]
            }}
        ]
    }}

    Transcript:
    {text[:15000]}  # Limit context window just in case
    """

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes video content into structured JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Summarization error: {e}")
        return {"title": "Error", "summary": "Could not generate summary.", "topics": []}


def process_youtube_video(url):
    print(f"--- Starting processing for {url} ---")

    # 1. Extract Audio
    print("1. Downloading audio...")
    try:
        audio_path = extract_audio(url)
        print(f"   Audio saved to: {audio_path}")
    except Exception as e:
        print(f"   Audio download failed: {e}")
        return {"error": str(e)}

    # 2. Transcribe
    print("2. Transcribing...")
    try:
        # Get absolute path for transcribe
        abs_audio_path = os.path.abspath(audio_path)
        transcript_data = transcribe_audio(abs_audio_path)
        
        # Unpack
        transcript_text = transcript_data["full_text"]
        transcript_segments = transcript_data["segments"]
        
        print(f"   Transcription complete. Length: {len(transcript_text)} chars")
    except Exception as e:
        print(f"   Transcription failed: {e}")
        return {"error": str(e)}

    # 3. Summarize (Topic/Subtopic)
    print("3. Generating structured summary (Calling OpenAI)...")
    structure = generate_structured_summary(transcript_text)
    print("   Summary generated.")

    # 4. Chunk & Embed for Q&A
    print("4. Chunking and Embedding...")
    chunks = chunk_text(transcript_text, chunk_size=500, overlap=100)
    
    # Prepare chunks with IDs
    chunks_data = [
        {"chunk_id": i, "text": chunk}
        for i, chunk in enumerate(chunks)
    ]
    
    # Use video title from summary as source name, or filename
    video_title = structure.get("title", os.path.basename(audio_path))
    embed_chunks(chunks_data, source_name=video_title)

    # Attach structured transcript to result
    structure["transcript"] = transcript_segments
    return structure
