from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService


class RetrievalService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ):
        query_vector = self.embedding_service.embed_text(query)

        results = self.vector_store.search(
            query_vector=query_vector,
            limit=limit,
        )

        documents = []

        for result in results:
            documents.append(
                {
                    "score": result.score,
                    "chunk_id": result.payload["chunk_id"],
                    "text": result.payload["text"],
                    "document": result.payload["document"],
                }
            )

        return documents