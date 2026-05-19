import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from EmbeddingService import EmbeddingService
from DocumentStore import DocumentStore
from RagWorkflow import RagWorkflow
from Routes import HealthRouter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY belum di-set. Salin .env.example ke .env dan isi API key.")

# Baca ALLOWED_ORIGINS dari .env, default hanya localhost untuk development
_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8501")
allowed_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app = FastAPI(title="HealthTruth RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")

embedding_service = EmbeddingService(api_key)
document_store = DocumentStore(embedding_service, qdrant_url=qdrant_url)
rag_workflow = RagWorkflow(document_store, api_key)

app.include_router(HealthRouter(rag_workflow, document_store).router)
