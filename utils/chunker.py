import os
from pydub import AudioSegment

def split_audio_to_chunks(wav_path, output_folder, chunk_ms=10000):
    """
    Splits the WAV file into 10-second chunks.
    """
    os.makedirs(output_folder, exist_ok=True)

    audio = AudioSegment.from_wav(wav_path)
    total_ms = len(audio)

    chunk_paths = []
    idx = 0

    for start in range(0, total_ms, chunk_ms):
        chunk = audio[start:start + chunk_ms]
        chunk_path = os.path.join(output_folder, f"chunk_{idx}.wav")
        chunk.export(chunk_path, format="wav")
        chunk_paths.append(chunk_path)
        idx += 1

    return chunk_paths
