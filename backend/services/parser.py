import io


def parse_document(content_bytes: bytes, filename: str, content_type: str | None) -> str:
    """Extract plain text from uploaded file based on type."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext == "pdf" or (content_type and "pdf" in content_type):
        return _parse_pdf(content_bytes)
    elif ext == "docx":
        return _parse_docx(content_bytes)
    elif ext in ("txt", "md", "csv", "log", "json", "xml", "html"):
        return content_bytes.decode("utf-8", errors="replace")
    else:
        # Fallback: try UTF-8 decode
        return content_bytes.decode("utf-8", errors="replace")


def _parse_pdf(content_bytes: bytes) -> str:
    """Extract text from PDF using pypdf."""
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(content_bytes))
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n\n".join(pages)


def _parse_docx(content_bytes: bytes) -> str:
    """Extract text from DOCX using python-docx."""
    from docx import Document

    doc = Document(io.BytesIO(content_bytes))
    return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
