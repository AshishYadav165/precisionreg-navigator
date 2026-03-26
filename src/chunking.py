from pathlib import Path
from pypdf import PdfReader

def read_pdf_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = []
    for page_num, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        if page_text.strip():
            text.append(page_text)
    return "\n".join(text)

def simple_chunk(text: str, chunk_size: int = 1200, overlap: int = 200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def load_and_chunk_guidance(folder: str):
    records = []
    for file in Path(folder).glob("*.pdf"):
        full_text = read_pdf_text(str(file))
        chunks = simple_chunk(full_text)
        for i, chunk in enumerate(chunks):
            records.append({
                "source_id": f"{file.stem}_{i}",
                "title": file.stem,
                "section": f"chunk_{i}",
                "text": chunk,
                "citation": file.stem,
            })
    return records
