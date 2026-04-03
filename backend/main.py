from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from services.embedding import EmbeddingService
from services.database import DatabaseService
from routers import ingest, search


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load model + connect DB
    app.state.embedder = EmbeddingService(
        model_name=settings.EMBEDDING_MODEL,
        device=settings.DEVICE,
    )
    app.state.db = DatabaseService(
        url=settings.SURREALDB_URL,
        namespace=settings.SURREALDB_NS,
        database=settings.SURREALDB_DB,
        username=settings.SURREALDB_USER,
        password=settings.SURREALDB_PASS,
    )
    await app.state.db.connect()
    await app.state.db.init_schema()
    yield
    # Shutdown
    await app.state.db.close()


app = FastAPI(title="Semantic Search Engine", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router, prefix="/api")
app.include_router(search.router, prefix="/api")
