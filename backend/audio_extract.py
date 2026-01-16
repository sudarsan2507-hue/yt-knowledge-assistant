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
    if not os.path.exists(cookie_file) and os.path.exists("/etc/secrets/cookies.txt"):
        cookie_file = "/etc/secrets/cookies.txt"

    ydl_opts = {
        # Best available audio (Simplified)
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
        "noplaylist": True, # Ensure we don't get a playlist
    }

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
