import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from .language_aliases import LANGUAGE_ALIASES

MODEL_DIR = "models/nllb-200-distilled-600M"

_tokenizer = None
_model = None


# ------------------------------
# Load model (local only)
# ------------------------------
def load_nllb():
    global _tokenizer, _model

    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(
            MODEL_DIR,
            local_files_only=True
        )

    if _model is None:
        _model = AutoModelForSeq2SeqLM.from_pretrained(
            MODEL_DIR,
            local_files_only=True
        )

    return _tokenizer, _model


# ------------------------------
# Language resolver
# ------------------------------
def normalize_language_name(name):
    if not name:
        return None

    original = name.strip()
    lower = original.lower()

    # If user enters NLLB code directly
    if "_" in original:
        return original

    # Direct alias match
    if lower in LANGUAGE_ALIASES:
        return LANGUAGE_ALIASES[lower]

    # Partial match
    for lang_name, code in LANGUAGE_ALIASES.items():
        if lower in lang_name:
            return code

    return None


# ------------------------------
# Multi-line SRT loader (correct)
# ------------------------------
def load_srt(path):
    """
    Proper SRT parsing:
    - Handles multi-line blocks
    - Ignores index + time lines
    """
    segments = []
    block = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped == "":
                if len(block) >= 3:
                    # text lines start from index 2
                    text = " ".join(block[2:]).strip()
                    segments.append({
                        "text": text,
                        "start": 0,
                        "end": 0
                    })
                block = []
            else:
                block.append(stripped)

    # Handle last block
    if len(block) >= 3:
        text = " ".join(block[2:]).strip()
        segments.append({
            "text": text,
            "start": 0,
            "end": 0
        })

    return segments


# ------------------------------
# Translate one text line
# ------------------------------
def translate_text(text, tgt_lang):
    tokenizer, model = load_nllb()

    if not isinstance(text, str):
        raise ValueError("Invalid subtitle text")

    text = text.strip()
    if len(text) == 0:
        return ""

    inputs = tokenizer(text, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_lang),
        max_length=300
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# ------------------------------
# Translate full SRT
# ------------------------------
def translate_srt(srt_path, tgt_lang, gui_callback=None):
    segments = load_srt(srt_path)

    if tgt_lang is None:
        raise ValueError("Target language could not be resolved")

    total = len(segments)
    translated = []

    for i, seg in enumerate(segments):
        try:
            new_text = translate_text(seg["text"], tgt_lang)
        except Exception as e:
            raise RuntimeError(f"Translation failed on segment {i}: {e}")

        translated.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": new_text
        })

        # update progress in percent
        if gui_callback:
            percent = int(((i + 1) / total) * 100)
            gui_callback(percent, f"Translating {i+1}/{total}")

    return translated
