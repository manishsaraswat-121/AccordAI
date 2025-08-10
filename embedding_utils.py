from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

def build_embeddings_model(model_name: str) -> SentenceTransformer:
    return SentenceTransformer(model_name)

def embed_texts(model: SentenceTransformer, texts: list) -> np.ndarray:
    return model.encode(texts, convert_to_numpy=True, show_progress_bar=False)

def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatIP:
    d = embeddings.shape[1]
    index = faiss.IndexFlatIP(d)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    return index

def retrieve_top_k(index: faiss.IndexFlatIP, query_emb: np.ndarray, k: int = 5):
    faiss.normalize_L2(query_emb)
    D, I = index.search(query_emb, k)
    return D[0], I[0]
