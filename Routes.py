import logging
import time
from typing import Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from RagWorkflow import RagWorkflow
from DocumentStore import DocumentStore

logger = logging.getLogger(__name__)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    mode: Literal["ringkas", "detail", "sumber"] = "ringkas"


class FactCheckRequest(BaseModel):
    claim: str = Field(..., min_length=1, max_length=2000)


class DocumentRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10_000)


class HealthRouter:
    def __init__(self, rag_workflow: RagWorkflow, document_store: DocumentStore):
        self.rag_workflow = rag_workflow
        self.document_store = document_store
        self.router = APIRouter()
        self._register_routes()

    def _register_routes(self):
        self.router.post("/ask")(self.ask)
        self.router.post("/fact-check")(self.fact_check)
        self.router.post("/add")(self.add)
        self.router.get("/status")(self.status)

    def ask(self, req: QuestionRequest):
        start = time.time()
        try:
            result = self.rag_workflow.ask(req.question, req.mode)
            return {
                "question": req.question,
                "mode": req.mode,
                "answer": result["answer"],
                "context_used": result.get("context", []),
                "latency_sec": round(time.time() - start, 3),
            }
        except Exception as e:
            logger.error("Error on /ask: %s", e, exc_info=True)
            raise HTTPException(status_code=500, detail="Terjadi kesalahan internal. Coba lagi nanti.")

    def fact_check(self, req: FactCheckRequest):
        start = time.time()
        try:
            result = self.rag_workflow.fact_check(req.claim)
            return {
                "claim": req.claim,
                "result": result["answer"],
                "context_used": result.get("context", []),
                "latency_sec": round(time.time() - start, 3),
            }
        except Exception as e:
            logger.error("Error on /fact-check: %s", e, exc_info=True)
            raise HTTPException(status_code=500, detail="Terjadi kesalahan internal. Coba lagi nanti.")

    def add(self, req: DocumentRequest):
        try:
            doc_id = self.document_store.add_document(req.text)
            return {"id": doc_id, "status": "added"}
        except Exception as e:
            logger.error("Error on /add: %s", e, exc_info=True)
            raise HTTPException(status_code=500, detail="Gagal menyimpan dokumen. Coba lagi nanti.")

    def status(self):
        return {
            **self.document_store.get_status(),
            "graph_ready": self.rag_workflow.is_ready,
        }
