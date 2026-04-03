def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> list[str]:
    """Split text into overlapping chunks, preferring sentence boundaries."""
    if len(text) <= chunk_size:
        return [text.strip()] if text.strip() else []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # If not at the end, try to break at a sentence boundary
        if end < len(text):
            search_region = text[start:end]
            best_break = -1
            for marker in [". ", ".\n", "! ", "!\n", "? ", "?\n", "\n\n"]:
                pos = search_region.rfind(marker)
                if pos > best_break and pos > chunk_size // 4:
                    best_break = pos + len(marker)

            if best_break > 0:
                end = start + best_break

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        step = max((end - start) - overlap, 1)
        start = start + step

    return chunks
