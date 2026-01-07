import os
import json
import sqlite3
import numpy as np
from fastembed import TextEmbedding

CHUNKS_DIR = "chunks"
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMBED_DIR = os.path.join(ROOT_DIR, "embeddings")
DB_PATH = os.path.join(EMBED_DIR, "video_embeddings.sqlite")

# Global variable for lazy loading
# fastembed model is ~200MB, loads once
embedding_model = None

def get_model():
    global embedding_model
    if embedding_model is None:
        # "BAAI/bge-small-en-v1.5" is default and efficiently small
        print("Loading FastEmbed model...")
        cache_dir = os.path.join(ROOT_DIR, "fastembed_cache")
        embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5", cache_dir=cache_dir)
    return embedding_model

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

def reset_db():
    conn = init_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM embeddings")
    conn.commit()
    conn.close()
    print("Database reset: All embeddings cleared.")

def embed_chunks(chunks_data=None, source_name="unknown"):
    conn = init_db()
    cur = conn.cursor()
    
    model = get_model()
    
    # FastEmbed takes list of strings
    texts = []
    ids = []
    
    if chunks_data:
        # Extract texts
        texts = [item["text"] for item in chunks_data]
        ids = [item["chunk_id"] for item in chunks_data]
        
        # Batch embed
        print(f"Embedding {len(texts)} chunks via FastEmbed...")
        embeddings_generator = model.embed(texts) # Returns generator
        embeddings_list = list(embeddings_generator)
        
        for i, vector in enumerate(embeddings_list):
            # vector is numpy array
            vector_blob = vector.astype(np.float32).tobytes()
            cur.execute(
                "INSERT INTO embeddings (source, chunk_id, text, vector) VALUES (?, ?, ?, ?)",
                (source_name, ids[i], texts[i], vector_blob)
            )
        
        print(f"Embedded {len(texts)} chunks for {source_name}")
        conn.commit()
        conn.close()
        return

    # Legacy file mode (cleanup if needed, but keeping for compatibility)
    # ... (omitted for brevity as we mainly use the new flow)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    pass
