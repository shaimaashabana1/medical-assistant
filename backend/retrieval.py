import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

CHUNKS_PATH = "data/chunks.json"
INDEX_PATH = "vector_store/medquad.index"
METADATA_PATH = "vector_store/chunks_metadata.json"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
MIN_CHUNK_LENGTH = 20  # filters out near-empty chunks like "Answer:"

print("Loading embedding model...")
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
print("Embedding model loaded.")


def load_chunks(path=CHUNKS_PATH):
    with open(path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    # Filter out low-value chunks (e.g. "Answer:", "Question:" headers)
    before = len(chunks)
    chunks = [c for c in chunks if len(c["text"].strip()) >= MIN_CHUNK_LENGTH]
    after = len(chunks)
    print(f"Loaded {before} chunks, kept {after} after filtering short/empty ones.")

    return chunks


def build_index(chunks):
    texts = [c["text"] for c in chunks]

    print("Encoding chunks...")
    embeddings = embedding_model.encode(
        texts,
        show_progress_bar=True,
        batch_size=64,
        convert_to_numpy=True
    )

    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    print(f"FAISS index built with {index.ntotal} vectors.")
    return index


def save_index(index, chunks):
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)

    faiss.write_index(index, INDEX_PATH)

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"Index saved to {INDEX_PATH}")
    print(f"Metadata saved to {METADATA_PATH}")


def load_index():
    index = faiss.read_index(INDEX_PATH)
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    return index, chunks


# ==========================================================
# Build the index once when this module is imported
# (In production, you'd normally build it once offline and
# just load it here instead of rebuilding every run)
# ==========================================================

if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
    print("Existing FAISS index found. Loading it...")
    index, chunks = load_index()
else:
    print("No existing index found. Building a new one...")
    chunks = load_chunks()
    index = build_index(chunks)
    save_index(index, chunks)


def retrieve(query: str, top_k: int = 5) -> list:
    """
    Given a query string, returns the top_k most similar chunks.
    Each result includes the chunk text plus its metadata
    (question, focus_area, source, similarity_score).
    """
    query_embedding = embedding_model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(query_embedding, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        chunk = chunks[idx]
        results.append({
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "question": chunk["question"],
            "focus_area": chunk["focus_area"],
            "source": chunk["source"],
            "similarity_score": float(score)
        })

    return results