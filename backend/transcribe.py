import os
AUDIO_DIR = "audio"
OUTPUT_DIR = "transcripts"

# Global variable for lazy loading
model = None

def get_whisper_model():
    global model
    if model is None:
        print("Loading Whisper model... (Lazy)")
        from faster_whisper import WhisperModel
        model = WhisperModel(
            model_size_or_path="base",
            device="cpu",
            compute_type="int8"
        )
    return model

def transcribe_audio(audio_path=None):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if audio_path:
        # Process single file
        print(f"Transcribing: {audio_path}")
        model_instance = get_whisper_model()
        segments, _ = model_instance.transcribe(audio_path)
        
        transcript_data = []
        full_text = []
        
        for segment in segments:
            # Format: [00:12] Text...
            start_time = int(segment.start)
            minutes = start_time // 60
            seconds = start_time % 60
            time_str = f"[{minutes:02d}:{seconds:02d}]"
            
            text = segment.text.strip()
            
            transcript_data.append({
                "time": time_str,
                "text": text
            })
            full_text.append(text)
        
        # Return both full text (for summary) and segments (for UI)
        return {
            "full_text": " ".join(full_text),
            "segments": transcript_data
        }


if __name__ == "__main__":
    transcribe_audio()
