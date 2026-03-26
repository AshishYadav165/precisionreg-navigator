import json
import pickle
import faiss
import numpy as np
from src.embeddings import Embedder

class LocalVectorStore:
    def __init__(self, index, metadata):
        self.index = index
        self.metadata = metadata

    @classmethod
    def build(cls, jsonl_path: str, model_name: str = "all-MiniLM-L6-v2"):
        embedder = Embedder(model_name)
        records = []
        texts = []

        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                rec = json.loads(line)
                records.append(rec)
                texts.append(rec["text"])

        vectors = embedder.embed_texts(texts)
        vectors = np.array(vectors).astype("float32")

        index = faiss.IndexFlatL2(vectors.shape[1])
        index.add(vectors)
        return cls(index, records)

    def save(self, index_path: str, metadata_path: str):
        faiss.write_index(self.index, index_path)
        with open(metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)

    @classmethod
    def load(cls, index_path: str, metadata_path: str):
        index = faiss.read_index(index_path)
        with open(metadata_path, "rb") as f:
            metadata = pickle.load(f)
        return cls(index, metadata)

    def search(self, query_vector, k: int = 5):
        q = np.array([query_vector]).astype("float32")
        distances, indices = self.index.search(q, k)
        return [self.metadata[i] for i in indices[0] if i != -1]
