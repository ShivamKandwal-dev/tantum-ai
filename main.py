from fastapi import FastAPI, UploadFile, File
import os
import uuid

from utils.audio_utils import extract_wav_16k
from utils.chunker import split_audio_to_chunks
from utils.transcribe_utils import parallel_transcribe_chunks
from utils.srt_generator import save_srt, save_txt
from utils.translate_utils import translate_srt

app = FastAPI()

VIDEOAUDIO_DIR = "videoaudio"
VIDEOTEXT_DIR = "videotext"
MODEL_PATH = "models/medium"


@app.get("/")
def home():
    return {"message": "Tantum-AI backend is running on Render!"}


@app.post("/transcribe")
async def transcribe_api(file: UploadFile = File(...)):
    # Create folders
    os.makedirs(VIDEOAUDIO_DIR, exist_ok=True)
    os.makedirs(VIDEOTEXT_DIR, exist_ok=True)

    # Save uploaded file
    file_id = str(uuid.uuid4())
    filename = f"{file_id}.mp4"
    path = os.path.join(VIDEOAUDIO_DIR, filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    # Process audio
    audio_folder = os.path.join(VIDEOAUDIO_DIR, file_id)
    os.makedirs(audio_folder, exist_ok=True)

    wav_path = os.path.join(audio_folder, "audio.wav")
    extract_wav_16k(path, wav_path)

    chunk_paths = split_audio_to_chunks(wav_path, audio_folder)

    segments = parallel_transcribe_chunks(chunk_paths, MODEL_PATH)

    # Save outputs
    text_folder = os.path.join(VIDEOTEXT_DIR, file_id)
    os.makedirs(text_folder, exist_ok=True)

    srt_path = os.path.join(text_folder, "subtitles.srt")
    txt_path = os.path.join(text_folder, "transcript.txt")

    save_srt(srt_path, segments)
    save_txt(txt_path, segments)

    return {
        "status": "done",
        "file_id": file_id,
        "transcript": txt_path,
        "srt": srt_path
    }


@app.post("/translate")
async def translate_api(file_id: str, target_language: str):
    srt_path = os.path.join(VIDEOTEXT_DIR, file_id, "subtitles.srt")
    if not os.path.exists(srt_path):
        return {"error": "SRT file not found"}

    out_path = os.path.join(
        VIDEOTEXT_DIR, file_id, f"translated_{target_language}.srt"
    )

    translated = translate_srt(srt_path, target_language)
    save_srt(out_path, translated)

    return {
        "status": "done",
        "translated_srt": out_path
    }
