import json
from src.chunking import load_and_chunk_guidance

INPUT_FOLDER = "data/raw/guidance"
OUTPUT_FILE = "data/processed/chunks.jsonl"

def main():
    records = load_and_chunk_guidance(INPUT_FOLDER)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    print(f"Wrote {len(records)} chunks to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
