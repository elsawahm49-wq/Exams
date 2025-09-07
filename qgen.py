import random
from typing import List, Dict, Any
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# نموذج خفيف لبداية العمل
_tok = AutoTokenizer.from_pretrained("valhalla/t5-small-qg-hl")
_mod = AutoModelForSeq2SeqLM.from_pretrained("valhalla/t5-small-qg-hl")

def _qg_highlight(text: str, answer: str) -> str:
    # الصيغة المطلوبة للنموذج: تمييز الإجابة داخل النص
    return f"generate question: {text} <hl> {answer} <hl>"

def _sentences(chunk: str) -> List[str]:
    # تقسيم بسيط للجمل (يمكن تحسينه لاحقًا)
    raw = chunk.replace("؟", ".").replace("!", ".")
    sents = [s.strip() for s in raw.split(".") if len(s.strip()) > 12]
    return sents

def generate_mcq_from_chunk(chunk: str, n: int = 3) -> List[Dict[str, Any]]:
    sents = _sentences(chunk)
    out = []
    if not sents:
        return out
    k = min(n, len(sents))
    for _ in range(k):
        ans = random.choice(sents)
        inp = _qg_highlight(chunk, ans)
        ids = _tok.encode(inp, return_tensors="pt", truncation=True, max_length=512)
        gen = _mod.generate(ids, max_length=64, num_beams=4)
        q = _tok.decode(gen[0], skip_special_tokens=True)
        wrong_pool = [s for s in sents if s != ans][:10]
        if len(wrong_pool) >= 3:
            wrongs = random.sample(wrong_pool, 3)
        else:
            wrongs = wrong_pool
            while len(wrongs) < 3:
                wrongs.append(ans[::-1][: max(10, len(ans)//2)])  # تعبئة بدائل عشوائية بسيطة
        choices = wrongs + [ans]
        random.shuffle(choices)
        out.append({
            "type": "mcq",
            "stem": q,
            "choices": choices,
            "answer": ans,
            "explanation": "الإجابة مأخوذة من نفس المقطع؛ حسّن المشتتات لاحقًا.",
        })
    return out

def generate_tf_short(chunk: str):
    sents = _sentences(chunk)
    out = []
    if not sents:
        return out
    base = random.choice(sents)
    fake = base.replace(" هو ", " ليس ") if " هو " in base else base + " ليس دائماً"
    out.append({
        "type": "tf",
        "stem": fake + " (صح/خطأ)",
        "answer": False,
        "explanation": f"النص الأصلي: {base}",
    })
    out.append({
        "type": "short",
        "stem": "لخّص الفكرة الرئيسية للمقطع في سطرين.",
        "answer": None,
        "explanation": "سؤال مفتوح للتقويم البنائي.",
    })
    return out
