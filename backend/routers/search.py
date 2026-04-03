from fastapi import APIRouter, Request

from models.schemas import SearchRequest, SearchResponse, SearchResult
from services.embedding import EmbeddingService
from services.database import DatabaseService

router = APIRouter(tags=["search"])


@router.post("/search", response_model=SearchResponse)
async def semantic_search(request: Request, body: SearchRequest):
    """Embed query, perform vector similarity search, return ranked results."""
    db: DatabaseService = request.app.state.db
    embedder: EmbeddingService = request.app.state.embedder

    # Embed the query
    query_embedding = embedder.embed_query(body.query)

    # Vector search in SurrealDB
    raw_results = await db.vector_search(
        query_embedding=query_embedding,
        top_k=body.top_k,
    )

    # Build response — convert RecordID objects to strings
    results = [
        SearchResult(
            chunk_id=str(r["id"]),
            document_id=str(r["document_id"]),
            filename=str(r.get("filename", "")),
            text=r["text"],
            similarity=float(r["similarity"]),
            chunk_index=r["chunk_index"],
        )
        for r in raw_results
    ]

    return SearchResponse(query=body.query, results=results, total=len(results))
