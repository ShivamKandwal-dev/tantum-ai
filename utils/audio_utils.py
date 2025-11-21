import subprocess
import os

def extract_wav_16k(video_path, output_path):
    """
    Extracts audio from video and converts to mono 16k WAV using FFmpeg.
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-ac", "1",
        "-ar", "16000",
        output_path
    ]

    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
