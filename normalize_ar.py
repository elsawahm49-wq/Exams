import re

DIAC = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]")

MAP = {
    "أ": "ا", "إ": "ا", "آ": "ا",
    "ى": "ي", "ة": "ه", "ؤ": "و", "ئ": "ي",
}

def normalize_ar(text: str) -> str:
    t = DIAC.sub("", text)
    for k, v in MAP.items():
        t = t.replace(k, v)
    t = re.sub(r"\s+", " ", t).strip()
    return t
