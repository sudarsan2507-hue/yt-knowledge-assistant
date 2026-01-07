import sqlite3
import numpy as np
import os
from fastembed import TextEmbedding

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, "embeddings", "video_embeddings.sqlite")
TOP_K = 3

# Global variable for lazy loading
embedding_model = None

def get_model():
    global embedding_model
    if embedding_model is None:
        print("Loading FastEmbed model for search...")
        cache_dir = os.path.join(ROOT_DIR, "fastembed_cache")
        embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5", cache_dir=cache_dir)
    return embedding_model


def cosine_similarity(a, b):
    # Ensure standard numpy float 32
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search(query):
    model = get_model()
    
    # FastEmbed returns a generator of length 1 for single query
    print(f"Embedding query: {query}")
    query_generator = model.embed([query])
    query_vec = list(query_generator)[0].astype(np.float32)

    # Ensure DB directory exists
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Safety: Ensure table exists (if new DB created by connect)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY,
            source TEXT,
            chunk_id INTEGER,
            text TEXT,
            vector BLOB
        )
    """)

    cur.execute("SELECT text, vector FROM embeddings")
    rows = cur.fetchall()

    scored = []
    for text, blob in rows:
        vec = np.frombuffer(blob, dtype=np.float32)
        score = cosine_similarity(query_vec, vec)
        scored.append((score, text))

    conn.close()

    scored.sort(reverse=True, key=lambda x: x[0])
    return scored[:TOP_K]


def main():
    query = input("Ask a question: ").strip()
    results = search(query)

    print("\nMost relevant context:\n")
    for i, (score, text) in enumerate(results, 1):
        print(f"[{i}] {text}\n")


if __name__ == "__main__":
    main()
