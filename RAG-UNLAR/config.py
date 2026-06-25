from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PDF_DIR = BASE_DIR / "data" / "pdfs"
DB_DIR = BASE_DIR / "db"

COLLECTION_NAME = "documentos"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 900
CHUNK_OVERLAP = 180
TOP_K = 4

LMSTUDIO_BASE_URL = "http://localhost:1234/v1"
LMSTUDIO_MODEL = "google/gemma-3-1b"

SYSTEM_PROMPT = (
    "Sos un asistente RAG genérico. Respondé únicamente con la información "
    "presente en los fragmentos recuperados. Si la respuesta no aparece en "
    "el contexto, indicá que no hay información suficiente."
)
