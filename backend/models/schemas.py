from pydantic import BaseModel, Field


# --- Ingest ---
class IngestResponse(BaseModel):
    document_id: str
    filename: str
    num_chunks: int
    message: str


class DocumentInfo(BaseModel):
    id: str
    filename: str
    content_type: str | None
    num_chunks: int
    created_at: str


# --- Search ---
class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    top_k: int = Field(default=10, ge=1, le=100)


class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    filename: str
    text: str
    similarity: float
    chunk_index: int


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
    total: int
