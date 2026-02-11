import os
import sys
import shutil
import subprocess
import glob

def extract_audio(youtube_url: str):
    """
    Extracts audio from a YouTube video using the standalone yt-dlp.exe via subprocess.
    Ensures Node.js is used for signature decryption.
    """
    # Ensure output directory exists
    output_dir = "audio"
    os.makedirs(output_dir, exist_ok=True)

    # Determine project root and paths
    current_file = os.path.abspath(__file__)
    backend_dir = os.path.dirname(current_file)
    project_root = os.path.dirname(backend_dir)
    
    # Paths
    yt_dlp_exe = os.path.join(project_root, "yt-dlp.exe")
    cookie_file = os.path.join(project_root, "cookies.txt")
    
    # 1. Verify yt-dlp.exe exists
    if not os.path.exists(yt_dlp_exe):
        raise Exception(f"Critical Error: yt-dlp.exe not found at {yt_dlp_exe}. Please download the standalone executable.")

    print(f"DEBUG: Using standalone yt-dlp at: {yt_dlp_exe}")

    # 2. Cookie Handling (Write ENV to file if needed)
    if os.environ.get("YOUTUBE_COOKIES"):
        print("DEBUG: YOUTUBE_COOKIES env var found. Writing to file...")
        with open(cookie_file, "w") as f:
            f.write(os.environ.get("YOUTUBE_COOKIES"))
    
    # 3. Locate FFmpeg
    import imageio_ffmpeg
    try:
        ffmpeg_binary = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"DEBUG: Imageio-FFmpeg found binary at: {ffmpeg_binary}")
        ffmpeg_dir = os.path.dirname(ffmpeg_binary) # yt-dlp often wants the dir or full path
    except Exception as e:
        print(f"WARNING: Could not find ffmpeg via imageio: {e}")
        ffmpeg_binary = None

    # 4. Construct Command
    # output template: audio/VIDEO_ID.mp3 (yt-dlp handles the extension switch during conversion)
    # We use %(id)s to ensure clean filenames
    output_template = os.path.join(output_dir, "%(id)s.%(ext)s")
    
    cmd = [
        yt_dlp_exe,
        "--js-runtimes", "node",       # Force Node.js
        "-x",                          # Extract audio
        "--audio-format", "mp3",       # Convert to mp3
        "--audio-quality", "192K",     # Quality
        "--output", output_template,   # Output filename template
        "--no-playlist",               # Single video only
        "--force-overwrites",          # Overwrite if exists
        "--no-check-certificate",      # Skip SSL checks (optional, but requested in previous steps)
        "--verbose",                   # Debug output
    ]

    # Add Cookies if present
    if os.path.exists(cookie_file):
        print(f"DEBUG: Adding cookies from {cookie_file}")
        cmd.extend(["--cookies", cookie_file])
    
    # Add FFmpeg location
    if ffmpeg_binary:
        cmd.extend(["--ffmpeg-location", ffmpeg_binary])

    # Add URL
    cmd.append(youtube_url)

    print(f"DEBUG: Running Command: {' '.join(cmd)}")

    try:
        # Run the command
        # Capture stdout and stderr for logging
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False # We check return code manually to parse errors
        )

        # Log Output
        if result.stdout:
            print(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            # Parse error
            err_msg = result.stderr
            if "Sign in" in err_msg or "confirm you're not a bot" in err_msg:
                 raise Exception("YouTube requires sign-in. Please export fresh 'cookies.txt' to the project root.")
            elif "Video unavailable" in err_msg:
                 raise Exception("Video is unavailable (private, deleted, or region locked).")
            else:
                 raise Exception(f"yt-dlp failed (Code {result.returncode}): {err_msg[:200]}...")

        # Find the generated file
        # yt-dlp might have saved it as VIDEO_ID.mp3
        # Use simple ID extraction or glob to find the latest file if needed, 
        # but with --output %(id)s.%(ext)s, it should be predictable if we know the ID.
        # But we don't know the ID easily without parsing.
        # However, yt-dlp prints "[ffmpeg] Destination: audio\VIDEO_ID.mp3"
        
        # Simple hack: Look for the most recent mp3 in 'audio' folder? 
        # Or parse the STDOUT for "Destination: " or "Merging formats into"
        
        expected_filename = None
        for line in result.stdout.splitlines():
             if "Destination:" in line and ".mp3" in line:
                 expected_filename = line.split("Destination:")[1].strip()
             elif "Merging formats into" in line:
                 expected_filename = line.split("Merging formats into")[1].strip().strip('"')
             elif "has been downloaded" in line and ".mp3" in line:
                 # "audio\ID.mp3 has already been downloaded"
                 expected_filename = line.split(" ")[1].strip()

        # If we couldn't parse it, try to find by globbing the audio dir?
        # Actually, let's assume it succeeded if returncode 0.
        # But returning the filename is required for the pipeline.
        
        if not expected_filename:
             # Fallback: List files in audio dir and pick the newest one? 
             # Risky if multiple requests. 
             # Let's try to get ID from URL to predict filename?
             # Extract ID from URL is hard to do perfectly with just string manip.
             
             # Better: Use --print filename first? No that's another call.
             # Subprocess output usually contains the filename.
             pass

        if expected_filename:
            # Output from yt-dlp might be relative or absolute.
            # If it's relative to CWD, we are good.
            if not os.path.exists(expected_filename):
                # Try relative to audio dir?
                pass
            
            # Sanity check
            if os.path.exists(expected_filename):
                print(f"DEBUG: Successfully extracted audio to: {expected_filename}")
                return expected_filename
        
        # If we missed the filename parse, try to find it via Python glob?
        # Creating a wrapper that returns the path.
        # For now, searching standard pattern output.
        # If parsing fails, we raise.
        
        if not expected_filename or not os.path.exists(expected_filename):
             raise Exception("Download appeared successful but couldn't locate output file. Check logs.")

        return expected_filename

    except Exception as e:
        print(f"Process Error: {e}")
        raise e

if __name__ == "__main__":
    url = input("Enter YouTube URL: ").strip()
    try:
        extract_audio(url)
    except Exception as e:
        print(f"\nFINAL FAILURE: {e}")
