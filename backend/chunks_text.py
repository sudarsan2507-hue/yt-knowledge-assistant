import os
import json

TRANSCRIPTS_DIR = "transcripts"
CHUNKS_DIR = "chunks"

CHUNK_SIZE = 500      # words per chunk
OVERLAP = 100         # words overlap between chunks


def chunk_text(text, chunk_size, overlap):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))
        start += chunk_size - overlap

    return chunks


def process_transcripts():
    os.makedirs(CHUNKS_DIR, exist_ok=True)

    for file in os.listdir(TRANSCRIPTS_DIR):
        if not file.endswith(".txt"):
            continue

        transcript_path = os.path.join(TRANSCRIPTS_DIR, file)
        output_path = os.path.join(
            CHUNKS_DIR, file.replace(".txt", "_chunks.json")
        )

        with open(transcript_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        chunks = chunk_text(text, CHUNK_SIZE, OVERLAP)

        data = [
            {"chunk_id": i, "text": chunk}
            for i, chunk in enumerate(chunks)
        ]

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Created {len(chunks)} chunks → {output_path}")


if __name__ == "__main__":
    process_transcripts()
