import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent),
)

from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService


def main():
    query = "Why did Microsoft's revenue increase in 2025?"

    embedding_service = EmbeddingService()
    vector_store = VectorStoreService()

    query_vector = embedding_service.embed_text(query)

    results = vector_store.search(
        query_vector=query_vector,
        limit=5,
    )

    print(f"\nQuery: {query}\n")
    print(f"Found {len(results)} results.\n")

    for index, result in enumerate(results, start=1):
        print("=" * 80)
        print(f"RESULT {index}")
        print(f"Score: {result.score}")
        print(f"Chunk ID: {result.payload['chunk_id']}")
        print()
        print(result.payload["text"][:1000])
        print()


if __name__ == "__main__":
    main()