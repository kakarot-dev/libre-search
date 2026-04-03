from fastapi import APIRouter, UploadFile, File, Request, HTTPException

from models.schemas import IngestResponse, DocumentInfo
from services.embedding import EmbeddingService
from services.database import DatabaseService
from services.parser import parse_document
from services.chunker import chunk_text
from config import settings

router = APIRouter(tags=["ingest"])


@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(request: Request, file: UploadFile = File(...)):
    """Upload a document, parse, chunk, embed, and store."""
    db: DatabaseService = request.app.state.db
    embedder: EmbeddingService = request.app.state.embedder

    content_bytes = await file.read()
    filename = file.filename
    content_type = file.content_type

    # Parse to plain text
    text = parse_document(content_bytes, filename, content_type)
    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from document.")

    # Chunk
    chunks = chunk_text(text, chunk_size=settings.CHUNK_SIZE, overlap=settings.CHUNK_OVERLAP)

    # Embed all chunks
    embeddings = embedder.embed_documents(chunks)

    # Store in SurrealDB
    doc_id = await db.create_document(
        filename=filename, content_type=content_type, num_chunks=len(chunks)
    )
    await db.store_chunks(doc_id=doc_id, chunks=chunks, embeddings=embeddings)

    return IngestResponse(
        document_id=str(doc_id),
        filename=filename,
        num_chunks=len(chunks),
        message=f"Successfully ingested '{filename}' as {len(chunks)} chunks.",
    )


@router.get("/documents")
async def list_documents(request: Request):
    """List all ingested documents."""
    db: DatabaseService = request.app.state.db
    docs = await db.list_documents()
    return [
        DocumentInfo(
            id=str(d["id"]),
            filename=d["filename"],
            content_type=d.get("content_type"),
            num_chunks=d["num_chunks"],
            created_at=str(d["created_at"]),
        )
        for d in docs
    ]


@router.get("/documents/{doc_id:path}/chunks")
async def get_document_chunks(doc_id: str, request: Request):
    """Get all chunks for a document."""
    db: DatabaseService = request.app.state.db
    chunks = await db.get_document_chunks(doc_id)
    return [
        {"chunk_index": c["chunk_index"], "text": c["text"]}
        for c in chunks
    ]


@router.delete("/documents/{doc_id:path}")
async def delete_document(doc_id: str, request: Request):
    """Delete a document and all its chunks."""
    db: DatabaseService = request.app.state.db
    await db.delete_document(doc_id)
    return {"message": f"Document {doc_id} deleted."}
