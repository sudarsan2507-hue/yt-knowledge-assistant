import os
from yt_dlp import YoutubeDL


def extract_audio(youtube_url: str):
    # Ensure output directory exists
    output_dir = "audio"
    os.makedirs(output_dir, exist_ok=True)

    # Use video ID to avoid invalid characters in filenames on Windows
    outtmpl = os.path.join(output_dir, "%(id)s.%(ext)s")

    ydl_opts = {
        # Best available audio
        "format": "bestaudio/best",

        # Output file template
        "outtmpl": outtmpl,

        # Explicit ffmpeg location (DIRECTORY, not exe)
        "ffmpeg_location": r"D:\Download_chrome(P1)\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin",

        # Convert audio to mp3
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],

        # Reduce noise
        "quiet": True,
        "no_warnings": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        # Construct the expected filename (yt-dlp replaces extension)
        filename = ydl.prepare_filename(info)
        final_filename = os.path.splitext(filename)[0] + ".mp3"
        return final_filename


if __name__ == "__main__":
    url = input("Enter YouTube URL: ").strip()
    extract_audio(url)
