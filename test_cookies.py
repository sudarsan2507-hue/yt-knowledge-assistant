import sys
import os

# Add project root to sys.path
sys.path.append(os.getcwd())

from backend.audio_extract import extract_audio

# Age restricted video (The Weeknd - Earned It) - often requires sign in
# Or use one known to be restricted.
# Let's use a very common one for testing: https://www.youtube.com/watch?v=F7Jb8f_8g80 (Contoversial content, often restricted)
# Or just the user's url if they had one.
# Let's try to run with the one from verify_fix.py first to see the debug output, 
# then try a restricted one.

target_url = "https://www.youtube.com/watch?v=vnCS2JCwe0s" # "Age Restricted Video Test" - this might not exist or work.
# Better: https://www.youtube.com/watch?v=Ilo_KYXvXfw (A restricted video)

print("--- Testing Audio Extraction with Debug ---")
try:
    # Use a known safe video first to check paths, then restricted
    # extract_audio("https://youtu.be/fLeJJPxua3E")
    
    print("\nAttempting Age Restricted Video...")
    # This video is often used for age restriction testing
    file = extract_audio("https://www.youtube.com/watch?v=Ilo_KYXvXfw") 
    print(f"Success! Saved to {file}")
except Exception as e:
    print(f"FAILED: {e}")
