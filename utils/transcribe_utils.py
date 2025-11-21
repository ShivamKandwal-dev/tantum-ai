import concurrent.futures
from faster_whisper import WhisperModel
from tqdm import tqdm


def transcribe_single_chunk(model_path, chunk_path, language):
    """Worker process for CPU transcription."""
    model = WhisperModel(
        model_path,
        device="cpu",
        compute_type="int8"
    )

    segments, _ = model.transcribe(
        chunk_path,
        language=language,
        beam_size=1
    )

    output = []
    for seg in segments:
        output.append({
            "start": float(seg.start),
            "end": float(seg.end),
            "text": seg.text.strip()
        })

    return output


def parallel_transcribe_chunks(chunk_paths, model_path, language=None, gui_callback=None):
    total = len(chunk_paths)
    results = []

    pbar = tqdm(total=total, desc="Transcribing", ncols=70)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {
            executor.submit(transcribe_single_chunk, model_path, path, language): i
            for i, path in enumerate(chunk_paths)
        }

        for future in concurrent.futures.as_completed(futures):
            idx = futures[future]

            try:
                segs = future.result()
            except Exception as e:
                pbar.close()
                raise RuntimeError(f"Worker crashed: {e}")

            results.append((idx, segs))
            pbar.update(1)

            if gui_callback:
                gui_callback(idx + 1, total)

    pbar.close()

    results.sort(key=lambda x: x[0])
    final = []
    for _, segs in results:
        final.extend(segs)

    return final
