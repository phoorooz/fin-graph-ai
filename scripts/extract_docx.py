from pathlib import Path

from docx import Document


INPUT_FILE = Path("data/documents/microsoft_2025_annual_report.docx")
OUTPUT_FILE = Path("data/processed/microsoft_2025_annual_report.txt")


def extract_text():
    document = Document(INPUT_FILE)

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        "\n\n".join(paragraphs),
        encoding="utf-8",
    )

    print(f"Extracted {len(paragraphs)} paragraphs.")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    extract_text()