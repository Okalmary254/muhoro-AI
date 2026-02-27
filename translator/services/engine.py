from langdetect import detect
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

MODEL_NAME = "facebook/nllb-200-distilled-600M"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

LANG_MAP = {
    "en": "eng_Latn",
    "fr": "fra_Latn",
    "de": "deu_Latn",
    "sw": "swh_Latn",
    "es": "spa_Latn", 
    "it": "itl_Latn" 
}

def translate_text(text, target_lang="eng_Latn"):
    detected = detect(text)

    if isinstance(detected, dict):
        detected = detected.get("language")

    if detected not in LANG_MAP:
        raise ValueError(f"Unsupported language: {detected}")

    src_lang = LANG_MAP[detected]

    inputs = tokenizer(
        text,
        return_tensors="pt",
        src_lang=src_lang
    )
    generated_tokens = model.generate(
    **inputs,
    forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_lang),
    max_new_tokens=50,
    num_beams=5,
    do_sample=False,
    temperature=0.0
    )

    translation = tokenizer.batch_decode(
        generated_tokens,
        skip_special_tokens=True
    )[0]

    return {
        "detected_language": detected,
        "translation": translation
    }