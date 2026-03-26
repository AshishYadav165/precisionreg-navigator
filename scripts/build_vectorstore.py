from src.vectorstore import LocalVectorStore

def main():
    store = LocalVectorStore.build("data/processed/chunks.jsonl")
    store.save(
        "data/processed/faiss.index",
        "data/processed/faiss_metadata.pkl"
    )
    print("Vectorstore built successfully.")

if __name__ == "__main__":
    main()
