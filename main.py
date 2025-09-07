from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
from extract import from_pdf, from_pptx, from_docx
from normalize_ar import normalize_ar
from chunking import split_into_chunks
from qgen import generate_mcq_from_chunk, generate_tf_short

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
def upload(lecture_title: str = Form(...), f: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, f.filename)
    with open(path, "wb") as w:
        w.write(f.file.read())
    ext = f.filename.lower().split(".")[-1]
    if ext == "pdf":
        text = from_pdf(path)
    elif ext == "pptx":
        text = from_pptx(path)
    elif ext == "docx":
        text = from_docx(path)
    else:
        return {"ok": False, "error": "صيغة غير مدعومة"}

    text = normalize_ar(text)
    chunks = split_into_chunks(text)

    questions = []
    for ch in chunks:
        questions += generate_mcq_from_chunk(ch, n=2)
        questions += generate_tf_short(ch)

    return {
        "ok": True,
        "lecture": lecture_title,
        "count": len(questions),
        "questions": questions[:50],  # حد أقصى مبدئي
    }
