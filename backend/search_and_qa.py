import sqlite3
import numpy as np
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, "embeddings", "video_embeddings.sqlite")
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 3

import google.generativeai as genai

if "GEMINI_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Global variable for lazy loading
# model = None


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search(query):
    # model_instance = get_search_model()
    # query_vec = model_instance.encode(query)
    response = genai.embed_content(
        model="models/text-embedding-004",
        content=query
    )
    query_vec = np.array(response['embedding'], dtype=np.float32)

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
