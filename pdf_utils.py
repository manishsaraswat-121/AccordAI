import fitz  # PyMuPDF
import re
from typing import List
from config import CHUNK_SIZE, CHUNK_OVERLAP

def extract_text_from_pdf(path) -> str:
    try:
        doc = fitz.open(str(path))
        text = [page.get_text("text") for page in doc]
        full_text = "\n".join(text)
        full_text = re.sub(r'\n{2,}', '\n\n', full_text)
        return full_text
    except Exception as e:
        print(f"PyMuPDF extraction failed for {path}: {e}")
        return ""

def normalize_text(text: str) -> str:
    t = text.replace('\r', '\n')
    t = re.sub(r"\n\s+\n", '\n\n', t)
    t = re.sub(r"[\t\x0b\x0c]+", ' ', t)
    t = re.sub(r' {2,}', ' ', t)
    t = re.sub(r'(^\s*Page\s*\d+\s*$)', '', t, flags=re.IGNORECASE | re.MULTILINE)
    return t.strip()

def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    chunks = []
    start = 0
    N = len(text)
    while start < N:
        end = min(start + size, N)
        chunks.append(text[start:end])
        if end == N:
            break
        start = end - overlap
    return chunks
