import os

def sec_to_srt(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec - int(sec)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def save_srt(path, segments):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            start = sec_to_srt(seg.get("start", 0))
            end = sec_to_srt(seg.get("end", 0))
            text = seg["text"]

            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")


def save_txt(path, segments):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        for seg in segments:
            f.write(seg["text"] + "\n")
def load_srt(path):
    """
    Load SRT file and return list of {start, end, text}
    Safe for translation workflow.
    """
    segments = []
    if not os.path.exists(path):
        return segments

    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    blocks = raw.strip().split("\n\n")

    for block in blocks:
        lines = block.split("\n")
        if len(lines) < 3:
            continue

        # Time format: 00:00:01,500 --> 00:00:05,000
        time_line = lines[1]
        try:
            start_srt, end_srt = time_line.split(" --> ")
        except:
            continue

        text = " ".join(lines[2:]).strip()

        segments.append({
            "start": 0,
            "end": 0,
            "text": text
        })

    return segments
