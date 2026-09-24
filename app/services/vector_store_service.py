import os

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


class VectorStoreService:
    COLLECTION_NAME = "financial_documents"
    VECTOR_SIZE = 384

    def __init__(self):
        qdrant_url = os.getenv(
            "QDRANT_URL",
            "http://localhost:6333",
        )

        self.client = QdrantClient(url=qdrant_url)

    def create_collection(self):
        collections = self.client.get_collections()

        existing_names = {
            collection.name
            for collection in collections.collections
        }

        if self.COLLECTION_NAME not in existing_names:
            self.client.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=self.VECTOR_SIZE,
                    distance=Distance.COSINE,
                ),
            )

            return {
                "status": "created",
                "collection": self.COLLECTION_NAME,
            }

        return {
            "status": "already_exists",
            "collection": self.COLLECTION_NAME,
        }

    def upsert_chunks(
        self,
        embeddings: list[list[float]],
        chunks: list[str],
    ):
        points = []

        for index, (embedding, chunk) in enumerate(
            zip(embeddings, chunks)
        ):
            points.append(
                PointStruct(
                    id=index,
                    vector=embedding,
                    payload={
                        "document": "microsoft_2025_annual_report",
                        "chunk_id": index,
                        "text": chunk,
                    },
                )
            )

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=points,
        )

        return len(points)

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ):
        results = self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=query_vector,
            limit=limit,
        )

        return results.points