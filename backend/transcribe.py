import os
from openai import OpenAI

# Global client
client = OpenAI()

OUTPUT_DIR = "transcripts"

def transcribe_audio(audio_path):
    """
    Transcribes audio using OpenAI's Whisper API.
    Returns structured data with timestamps.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Transcribing via OpenAI API: {audio_path}")
    
    try:
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file, 
                response_format="verbose_json"
            )
        
        # Parse segments for UI
        # OpenAI verbose_json return object has .segments list
        transcript_data = []
        full_text = transcript.text
        
        # Check if segments exist (sometimes short audio might not return segments in same way, but usually does for verbose_json)
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
        print(f"OpenAI Transcription failed: {e}")
        raise e

if __name__ == "__main__":
    # Test block
    pass
