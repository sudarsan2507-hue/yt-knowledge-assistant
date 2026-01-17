import os
import json
from groq import Groq
from backend.audio_extract import extract_audio
from backend.transcribe import transcribe_audio
from backend.chunks_text import chunk_text
from backend.embed_chunks import embed_chunks, reset_db

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def generate_structured_summary(text, language_mode="original"):
    """
    Generates a Topic/Subtopic structure from the transcript using Groq Llama 3.
    """
    
    lang_instruction = ""
    if language_mode == "english":
        lang_instruction = "IMPORTANT: The output MUST be in English, even if the transcript is in another language."

    prompt = f"""
    Analyze the following video transcript and structure it into a clear, nested hierarchy of Topics and Subtopics.
    For each subtopic, provide a brief 1-sentence summary.
    {lang_instruction}
    
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
    {text[:20000]}  # Groq has good context, but limit to be safe
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Powerful model for summarization
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes video content into structured JSON. You output ONLY JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Summarization error: {e}")
        return {"title": "Error", "summary": "Could not generate summary.", "topics": []}


def process_youtube_video(url, language_mode="original"):
    print(f"--- Starting processing for {url} [Mode: {language_mode}] ---")

    # 1. Extract Audio
    print("1. Downloading audio...")
    try:
        audio_path = extract_audio(url)
        print(f"   Audio saved to: {audio_path}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        error_msg = str(e)
        
        # Sanitize error message for UI
        if "Sign in" in error_msg:
            ui_msg = "This video is age-restricted or requires sign-in."
        elif "Video unavailable" in error_msg:
            ui_msg = "This video is unavailable (private or deleted)."
        elif "Requested format" in error_msg or "ffmpeg" in error_msg.lower():
             ui_msg = "Server Configuration Error: Audio processor (FFmpeg) not found. Please check deployment logs."
        elif "empty" in error_msg.lower():
             ui_msg = "Download failed (Empty file). Try a different video."
        else:
            ui_msg = f"Audio download failed. (Technicals: {error_msg[:50]}...)"

        print(f"   Audio download failed: {error_msg}")
        return {"error": ui_msg}

    # 2. Transcribe
    print("2. Transcribing...")
    try:
        # Get absolute path for transcribe
        abs_audio_path = os.path.abspath(audio_path)
        
        # Determine if we need to translate to English
        attempt_translation = (language_mode == "english")
        
        transcript_data = transcribe_audio(abs_audio_path, attempt_translation=attempt_translation)
        
        # Unpack
        transcript_text = transcript_data["full_text"]
        transcript_segments = transcript_data["segments"]
        
        print(f"   Transcription complete. Length: {len(transcript_text)} chars")
    except Exception as e:
        print(f"   Transcription failed: {e}")
        return {"error": str(e)}

    # 3. Summarize (Topic/Subtopic)
    print("3. Generating structured summary (Calling Groq Llama 3)...")
    structure = generate_structured_summary(transcript_text, language_mode=language_mode)
    print("   Summary generated.")

    # 4. Chunk & Embed for Q&A
    print("4. Chunking and Embedding...")
    reset_db()  # Clear previous video context
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

    # Cleanup: Delete audio file to save space
    if os.path.exists(audio_path):
        os.remove(audio_path)
        print(f"Deleted temporary audio file: {audio_path}")

    return structure
