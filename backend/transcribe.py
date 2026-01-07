import os
import json
import google.generativeai as genai
import time

# Configure Gemini
# Ensure GEMINI_API_KEY is in your environment variables
if "GEMINI_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = "transcripts"

def transcribe_audio(audio_path):
    """
    Transcribes audio using Google Gemini 1.5 Flash.
    Returns structured data with timestamps.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Transcribing via Gemini 1.5 Flash: {audio_path}")
    
    try:
        # 1. Upload File
        print("   Uploading file to Gemini...")
        audio_file = genai.upload_file(audio_path, mime_type="audio/mp3")
        
        # Optimize: Wait for processing (usually instant for small files)
        while audio_file.state.name == "PROCESSING":
            print('.', end='', flush=True)
            time.sleep(1)
            audio_file = genai.get_file(audio_file.name)
            
        if audio_file.state.name == "FAILED":
            raise ValueError("Audio processing failed on Gemini side")

        # 2. Prompt for Transcript with Timestamps
        print("   Generating transcript...")
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        prompt = """
        Analyze this audio and provide a verbatim transcript.
        Output MUST be a valid JSON object with the following structure:
        {
            "full_text": "The entire transcript as a single string",
            "segments": [
                {"time": "[MM:SS]", "text": "Text segment..."},
                ...
            ]
        }
        For segments, keep them roughly 10-30 seconds long.
        """
        
        response = model.generate_content(
            [audio_file, prompt],
            generation_config={"response_mime_type": "application/json"}
        )
        
        # 3. Parse and Return
        result = json.loads(response.text)
        
        # Cleanup remote file
        audio_file.delete()
        
        print(f"   Transcription complete. Length: {len(result.get('full_text', ''))} chars")
        return result

    except Exception as e:
        print(f"Gemini Transcription failed: {e}")
        import traceback
        traceback.print_exc()
        raise e

if __name__ == "__main__":
    pass
