import { useState } from "react";

export default function ExamGen() {
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [qs, setQs] = useState([]);
  const [error, setError] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    const fd = new FormData();
    fd.append("lecture_title", title || "محاضرة بدون عنوان");
    fd.append("f", file);
    setLoading(true);
    try {
      const r = await fetch("http://localhost:8000/upload", { method: "POST", body: fd });
      const j = await r.json();
      if(!j.ok){ throw new Error(j.error || 'فشل التوليد'); }
      setQs(j.questions || []);
    } catch(err){
      setError(String(err.message || err));
    } finally { setLoading(false); }
  }

  return (
    <div className="">
      <h1 className="text-2xl font-bold mb-4">مولّد امتحان متوقع</h1>
      <form onSubmit={submit} className="grid gap-3 bg-white p-4 rounded-2xl shadow">
        <input className="border p-2 rounded" placeholder="عنوان المحاضرة" value={title} onChange={e=>setTitle(e.target.value)} />
        <input className="border p-2 rounded" type="file" accept=".pdf,.pptx,.docx" onChange={e=>setFile(e.target.files[0])}/>
        <button className="bg-black text-white py-2 rounded-xl disabled:opacity-50" disabled={!file || loading}>
          {loading ? "جارٍ التوليد..." : "رفع وتوليد"}
        </button>
        {error && <div className="text-red-600 text-sm">{error}</div>}
      </form>

      <div className="mt-6 grid gap-4">
        {qs.map((q,i)=> (
          <div key={i} className="p-4 rounded-2xl bg-white shadow">
            <div className="font-semibold mb-2">{q.type.toUpperCase()} — {q.stem}</div>
            {q.type === 'mcq' && (
              <ul className="list-disc ps-6">
                {q.choices.map((c,idx)=>(<li key={idx}>{c}</li>))}
              </ul>
            )}
            <details className="mt-2">
              <summary className="cursor-pointer">الإجابة والتفسير</summary>
              <div className="mt-2">
                <div><b>الإجابة الصحيحة:</b> {String(q.answer)}</div>
                <div className="opacity-80">{q.explanation}</div>
              </div>
            </details>
          </div>
        ))}
      </div>
    </div>
  );
}
