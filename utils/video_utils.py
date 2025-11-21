import subprocess
import shlex
import os

def burn_subtitles_ffmpeg(input_video: str, srt_file: str, output_video: str, fontfile: str = None):
    srt_path = os.path.abspath(srt_file)
    input_path = os.path.abspath(input_video)
    output_path = os.path.abspath(output_video)
    # simple subtitles filter
    cmd = f'ffmpeg -y -i "{input_path}" -vf subtitles={shlex.quote(srt_path)} -c:a copy "{output_path}"'
    print("Running ffmpeg (burning subtitles)...")
    subprocess.run(cmd, shell=True)
    print("Saved:", output_path)
    return output_path

def softmux_subtitles(input_video: str, srt_file: str, output_video: str):
    cmd = f'ffmpeg -y -i "{input_video}" -i "{srt_file}" -c copy -c:s mov_text "{output_video}"'
    subprocess.run(cmd, shell=True)
    return output_video
