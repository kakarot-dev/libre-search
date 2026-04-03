from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Embedding
    EMBEDDING_MODEL: str = "google/embeddinggemma-300m"
    EMBEDDING_DIM: int = 768
    DEVICE: str = "cuda"

    # SurrealDB
    SURREALDB_URL: str = "ws://localhost:8000"
    SURREALDB_NS: str = "semantic_search"
    SURREALDB_DB: str = "main"
    SURREALDB_USER: str = "root"
    SURREALDB_PASS: str = "root"

    # Chunking
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 64

    class Config:
        env_file = "../.env"


settings = Settings()
