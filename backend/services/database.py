from surrealdb import AsyncSurreal, RecordID


class DatabaseService:
    """Async SurrealDB client wrapper."""

    def __init__(self, url: str, namespace: str, database: str, username: str, password: str):
        self.url = url
        self.namespace = namespace
        self.database = database
        self.username = username
        self.password = password
        self._db: AsyncSurreal | None = None

    async def connect(self):
        self._db = AsyncSurreal(self.url)
        await self._db.connect()
        await self._db.signin({"username": self.username, "password": self.password})
        await self._db.use(self.namespace, self.database)

    async def close(self):
        if self._db:
            await self._db.close()

    async def init_schema(self):
        """Create tables and indexes if they don't exist."""
        # query() only returns first statement result, use query_raw for multi-statement
        await self._db.query_raw("""
            DEFINE TABLE document SCHEMAFULL;
            DEFINE FIELD filename     ON document TYPE string;
            DEFINE FIELD content_type ON document TYPE option<string>;
            DEFINE FIELD num_chunks   ON document TYPE int;
            DEFINE FIELD created_at   ON document TYPE datetime DEFAULT time::now();
        """)
        await self._db.query_raw("""
            DEFINE TABLE chunk SCHEMAFULL;
            DEFINE FIELD document_id ON chunk TYPE record<document>;
            DEFINE FIELD chunk_index ON chunk TYPE int;
            DEFINE FIELD text        ON chunk TYPE string;
            DEFINE FIELD embedding   ON chunk TYPE array<float> ASSERT array::len($value) = 768;
            DEFINE FIELD created_at  ON chunk TYPE datetime DEFAULT time::now();
        """)
        await self._db.query("""
            DEFINE INDEX idx_chunk_embedding
                ON chunk FIELDS embedding
                HNSW DIMENSION 768 DIST COSINE TYPE F32;
        """)
        await self._db.query("""
            DEFINE INDEX idx_chunk_document_id
                ON chunk FIELDS document_id;
        """)

    async def create_document(self, filename: str, content_type: str | None, num_chunks: int) -> RecordID:
        """Create a document record. Returns the RecordID."""
        result = await self._db.create("document", {
            "filename": filename,
            "content_type": content_type,
            "num_chunks": num_chunks,
        })
        return result["id"]

    async def store_chunks(self, doc_id: RecordID, chunks: list[str], embeddings: list[list[float]]):
        """Store all chunks with their embeddings for a document."""
        for i, (text, embedding) in enumerate(zip(chunks, embeddings)):
            await self._db.query(
                """CREATE chunk CONTENT {
                    document_id: $document_id,
                    chunk_index: $chunk_index,
                    text: $text,
                    embedding: $embedding
                };""",
                {
                    "document_id": doc_id,
                    "chunk_index": i,
                    "text": text,
                    "embedding": embedding,
                },
            )

    async def vector_search(self, query_embedding: list[float], top_k: int = 10) -> list[dict]:
        """Perform KNN vector search using the HNSW index."""
        result = await self._db.query(
            f"""
            SELECT
                id,
                document_id,
                document_id.filename AS filename,
                text,
                chunk_index,
                vector::similarity::cosine(embedding, $query_embedding) AS similarity
            FROM chunk
            ORDER BY similarity DESC
            LIMIT {top_k};
            """,
            {
                "query_embedding": query_embedding,
            },
        )
        return result

    async def list_documents(self) -> list[dict]:
        """List all documents."""
        result = await self._db.query("SELECT * FROM document ORDER BY created_at DESC;")
        return result

    async def get_document_chunks(self, doc_id: str) -> list[dict]:
        """Get all chunks for a document, ordered by chunk_index."""
        # Parse "document:xyz" into a RecordID
        table, rid = doc_id.split(":", 1)
        result = await self._db.query(
            "SELECT chunk_index, text FROM chunk WHERE document_id = $doc_id ORDER BY chunk_index ASC;",
            {"doc_id": RecordID(table, rid)},
        )
        return result

    async def delete_document(self, doc_id: str):
        """Delete a document and all its chunks."""
        table, rid = doc_id.split(":", 1)
        record = RecordID(table, rid)
        await self._db.query("DELETE chunk WHERE document_id = $doc_id;", {"doc_id": record})
        await self._db.query(f"DELETE {doc_id};")
