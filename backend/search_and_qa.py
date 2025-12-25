import sqlite3
import numpy as np
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "embeddings", "video_embeddings.sqlite")
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 3

# Global variable for lazy loading
model = None

def get_search_model():
    global model
    if model is None:
        print("Loading Search model... (Lazy)")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(MODEL_NAME)
    return model


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search(query):
    model_instance = get_search_model()
    query_vec = model_instance.encode(query)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

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
