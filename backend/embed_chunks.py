import os
import json
import sqlite3
CHUNKS_DIR = "chunks"
EMBED_DIR = "embeddings"
DB_PATH = os.path.join(EMBED_DIR, "video_embeddings.sqlite")

MODEL_NAME = "all-MiniLM-L6-v2"

# Global variable for lazy loading
model = None

def get_embedding_model():
    global model
    if model is None:
        print("Loading Embedding model... (Lazy)")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(MODEL_NAME)
    return model


def init_db():
    os.makedirs(EMBED_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY,
            source TEXT,
            chunk_id INTEGER,
            text TEXT,
            vector BLOB
        )
    """)

    conn.commit()
    return conn


def embed_chunks(chunks_data=None, source_name="unknown"):
    conn = init_db()
    cur = conn.cursor()

    if chunks_data:
        # Process in-memory chunks
        for item in chunks_data:
            text = item["text"]
            model_instance = get_embedding_model()
            vector = model_instance.encode(text).tobytes()

            cur.execute(
                "INSERT INTO embeddings (source, chunk_id, text, vector) VALUES (?, ?, ?, ?)",
                (source_name, item["chunk_id"], text, vector)
            )
        
        print(f"Embedded {len(chunks_data)} chunks for {source_name}")
        conn.commit()
        conn.close()
        return

    # Legacy file mode
    for file in os.listdir(CHUNKS_DIR):
        if not file.endswith("_chunks.json"):
            continue

        source = file.replace("_chunks.json", "")

        with open(os.path.join(CHUNKS_DIR, file), "r", encoding="utf-8") as f:
            chunks = json.load(f)

        for item in chunks:
            text = item["text"]
            model_instance = get_embedding_model()
            vector = model_instance.encode(text).tobytes()

            cur.execute(
                "INSERT INTO embeddings (source, chunk_id, text, vector) VALUES (?, ?, ?, ?)",
                (source, item["chunk_id"], text, vector)
            )

        print(f"Embedded {len(chunks)} chunks from {file}")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    embed_chunks()
