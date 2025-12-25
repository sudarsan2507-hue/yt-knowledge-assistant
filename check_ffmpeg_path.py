
import os

path = r"D:\Download_chrome(P1)\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin"
print(f"Checking path: {path}")

if os.path.exists(path):
    print("Path exists.")
    ffmpeg_exe = os.path.join(path, "ffmpeg.exe")
    if os.path.exists(ffmpeg_exe):
        print("ffmpeg.exe found.")
    else:
        print("ffmpeg.exe NOT found.")
else:
    print("Path does NOT exist.")
