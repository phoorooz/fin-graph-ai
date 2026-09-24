import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent),
)

from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService


INPUT_FILE = Path(
    "data/processed/microsoft_2025_chunks.txt"
)


def load_chunks():
    text = INPUT_FILE.read_text(
        encoding="utf-8"
    )

    raw_chunks = text.split("--- CHUNK ")

    chunks = []

    for raw_chunk in raw_chunks:
        raw_chunk = raw_chunk.strip()

        if not raw_chunk:
            continue

        lines = raw_chunk.split("\n", 1)

        if len(lines) == 2:
            chunk_text = lines[1].strip()

            if chunk_text:
                chunks.append(chunk_text)

    return chunks


def main():
    chunks = load_chunks()

    print(f"Loaded {len(chunks)} chunks.")

    embedding_service = EmbeddingService()

    print("Creating embeddings...")

    embeddings = embedding_service.embed_texts(chunks)

    print(
        f"Created {len(embeddings)} embeddings."
    )

    vector_store = VectorStoreService()

    vector_store.create_collection()

    count = vector_store.upsert_chunks(
        embeddings=embeddings,
        chunks=chunks,
    )

    print(
        f"Inserted {count} chunks into Qdrant."
    )


if __name__ == "__main__":
    main()