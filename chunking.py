from typing import List

def split_into_chunks(text: str, max_chars: int = 900) -> List[str]:
    parts = []
    buf = []
    size = 0
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if size + len(line) + 1 > max_chars:
            parts.append("\n".join(buf))
            buf, size = [line], len(line)
        else:
            buf.append(line)
            size += len(line) + 1
    if buf:
        parts.append("\n".join(buf))
    return parts
