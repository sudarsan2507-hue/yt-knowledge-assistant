import os
from yt_dlp import YoutubeDL


def extract_audio(youtube_url: str):
    # Ensure output directory exists
    output_dir = "audio"
    os.makedirs(output_dir, exist_ok=True)

    # Use video ID to avoid invalid characters in filenames on Windows
    outtmpl = os.path.join(output_dir, "%(id)s.%(ext)s")

    # Check for cookies to bypass bot detection
    cookie_file = "cookies.txt"
    if os.environ.get("YOUTUBE_COOKIES"):
        with open("cookies.txt", "w") as f:
            f.write(os.environ.get("YOUTUBE_COOKIES"))
    
    # If using Render Secret Files, it might be at /etc/secrets/cookies.txt
    # Locate FFmpeg using imageio-ffmpeg (Reliable cross-platform)
    import imageio_ffmpeg
    try:
        ffmpeg_binary = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"DEBUG: Imageio-FFmpeg found binary at: {ffmpeg_binary}")
    except Exception as e:
        print(f"WARNING: Could not find ffmpeg via imageio: {e}")
        ffmpeg_binary = None

    ydl_opts = {
        # Best available audio
        "format": "bestaudio/best",
        
        # Output file template
        "outtmpl": outtmpl,

        # Convert audio to mp3
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],

        # Options
        "quiet": True,
        "no_warnings": True,
        "nocheckcertificate": True,
        "noplaylist": True,
    }

    if ffmpeg_binary:
        ydl_opts["ffmpeg_location"] = ffmpeg_binary

    if os.path.exists(cookie_file):
        ydl_opts["cookiefile"] = cookie_file

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        filename = ydl.prepare_filename(info)
        final_filename = os.path.splitext(filename)[0] + ".mp3"
        
        # Verify file exists and is not empty
        if not os.path.exists(final_filename) or os.path.getsize(final_filename) == 0:
            raise Exception("The downloaded file is empty or missing.")
            
        return final_filename


if __name__ == "__main__":
    url = input("Enter YouTube URL: ").strip()
    extract_audio(url)
