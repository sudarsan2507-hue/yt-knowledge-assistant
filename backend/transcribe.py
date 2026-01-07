import os
from groq import Groq

# Configure Groq
# Ensure GROQ_API_KEY is in your environment variables
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

OUTPUT_DIR = "transcripts"

def transcribe_audio(audio_path):
    """
    Transcribes audio using Groq (Distil-Whisper).
    Returns structured data with timestamps.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Transcribing via Groq API: {audio_path}")
    
    try:
        with open(audio_path, "rb") as file:
            # Groq implementation usually matches OpenAI's
            transcript = client.audio.transcriptions.create(
                file=(os.path.basename(audio_path), file.read()),
                model="distil-whisper-large-v3-en",
                response_format="verbose_json",
            )
        
        # Parse segments for UI
        # Groq verbose_json return object has .segments list
        transcript_data = []
        full_text = transcript.text
        
        segments = getattr(transcript, "segments", [])
        
        for segment in segments:
            # Format: [00:12] Text...
            start_time = int(segment.get("start", 0))
            minutes = start_time // 60
            seconds = start_time % 60
            time_str = f"[{minutes:02d}:{seconds:02d}]"
            
            text = segment.get("text", "").strip()
            
            transcript_data.append({
                "time": time_str,
                "text": text
            })

        print(f"Transcription complete. Length: {len(full_text)} chars")
        
        return {
            "full_text": full_text,
            "segments": transcript_data
        }

    except Exception as e:
        print(f"Groq Transcription failed: {e}")
        raise e

if __name__ == "__main__":
    pass
