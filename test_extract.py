
import sys
import os
# Mocking the stdout hack to see if it causes issues
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from backend.audio_extract import extract_audio

url = "https://youtu.be/fLeJJPxua3E"
print(f"Testing extraction for {url}")

try:
    path = extract_audio(url)
    print(f"Success! Saved to {path}")
except Exception as e:
    print(f"Failed: {e}")
