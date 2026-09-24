from pathlib import Path

from ftfy import fix_text


INPUT_FILE = Path("data/processed/microsoft_2025_annual_report.txt")
OUTPUT_FILE = Path("data/processed/microsoft_2025_clean.txt")


def main():
    text = INPUT_FILE.read_text(encoding="utf-8")

    cleaned = fix_text(text)

    # Convert non-breaking spaces to normal spaces.
    cleaned = cleaned.replace("\u00a0", " ")

    OUTPUT_FILE.write_text(
        cleaned,
        encoding="utf-8",
    )

    print("Text encoding fixed.")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()