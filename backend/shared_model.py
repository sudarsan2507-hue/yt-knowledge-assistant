import os
import sys

# Limit threads to reduce memory usage on Render free tier
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

# Safe import to avoiding crashing if fastembed isn't installed (though it should be)
try:
    from fastembed import TextEmbedding
except ImportError:
    TextEmbedding = None

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Global variable for lazy loading
# fastembed model is ~200MB, loads once
embedding_model = None

def get_model():
    global embedding_model
    if embedding_model is None:
        if TextEmbedding is None:
             raise ImportError("FastEmbed not installed")
        
        # "BAAI/bge-small-en-v1.5" is default and efficiently small
        print("Loading FastEmbed model (Singleton)...")
        cache_dir = os.path.join(ROOT_DIR, "fastembed_cache")
        embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5", cache_dir=cache_dir)
        print("Model loaded.")
    return embedding_model
