from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Wraps EmbeddingGemma for query and document embedding."""

    def __init__(self, model_name: str = "google/embeddinggemma-300m", device: str = "cuda"):
        self.device = device
        self.model = SentenceTransformer(model_name, device=device)
        # Warm up with a dummy encode
        self.model.encode(["warmup"], device=device)

    def embed_query(self, query: str) -> list[float]:
        """Embed a single search query using the query prompt."""
        embedding = self.model.encode(
            query,
            prompt_name="query",
            normalize_embeddings=True,
            device=self.device,
        )
        return embedding.tolist()

    def embed_documents(self, texts: list[str], batch_size: int = 32) -> list[list[float]]:
        """Embed a batch of document chunks using the document prompt."""
        embeddings = self.model.encode(
            texts,
            prompt_name="document",
            normalize_embeddings=True,
            batch_size=batch_size,
            show_progress_bar=True,
            device=self.device,
        )
        return embeddings.tolist()
