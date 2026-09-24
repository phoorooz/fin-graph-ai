from pathlib import Path

INPUT_FILE = Path("data/processed/microsoft_2025_clean.txt")
OUTPUT_FILE = Path("data/processed/microsoft_2025_chunks.txt")
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200


def create_chunks(text: str):
    chunks = []

    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def main():
    text = INPUT_FILE.read_text(encoding="utf-8")

    chunks = create_chunks(text)

    output = []

    for index, chunk in enumerate(chunks):
        output.append(
            f"--- CHUNK {index} ---\n\n{chunk}"
        )

    OUTPUT_FILE.write_text(
        "\n\n".join(output),
        encoding="utf-8",
    )

    print(f"Created {len(chunks)} chunks.")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()