import os
from dotenv import load_dotenv

load_dotenv()

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "anthropic")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
VECTORSTORE_INDEX = os.getenv("VECTORSTORE_INDEX", "data/processed/faiss.index")
VECTORSTORE_METADATA = os.getenv("VECTORSTORE_METADATA", "data/processed/faiss_metadata.pkl")
SQLITE_PATH = os.getenv("SQLITE_PATH", "data/sqlite/fda_precedents.db")
