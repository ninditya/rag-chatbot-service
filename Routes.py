import logging
import time
from typing import Literal, Optional
from fastapi import APIRouter, HTTPException, Header
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
    def __init__(self, rag_workflow: RagWorkflow, document_store: DocumentStore, add_api_key: str = ""):
        self.rag_workflow = rag_workflow
        self.document_store = document_store
        self.add_api_key = add_api_key
        self.router = APIRouter()
        self._register_routes()

    def _register_routes(self):
        self.router.post("/ask")(self.ask)
        self.router.post("/fact-check")(self.fact_check)
        self.router.post("/add")(self.add)
        self.router.api_route("/status", methods=["GET", "HEAD"])(self.status)
        self.router.get("/metrics")(self.metrics)

    def _raise_for_runtime(self, e: Exception) -> None:
        if isinstance(e, RuntimeError) and "QUOTA_EXHAUSTED" in str(e):
            raise HTTPException(
                status_code=429,
                detail="Kuota API harian habis. Coba lagi besok atau aktifkan billing di Google AI Studio.",
            )
        raise HTTPException(status_code=500, detail="Terjadi kesalahan internal. Coba lagi nanti.")

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
                "llm_fallback": result.get("llm_fallback", False),
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error on /ask: %s", e, exc_info=True)
            self._raise_for_runtime(e)

    def fact_check(self, req: FactCheckRequest):
        start = time.time()
        try:
            result = self.rag_workflow.fact_check(req.claim)
            return {
                "claim": req.claim,
                "result": result["answer"],
                "context_used": result.get("context", []),
                "latency_sec": round(time.time() - start, 3),
                "llm_fallback": result.get("llm_fallback", False),
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error on /fact-check: %s", e, exc_info=True)
            self._raise_for_runtime(e)

    def add(self, req: DocumentRequest, x_api_key: Optional[str] = Header(None)):
        if self.add_api_key and x_api_key != self.add_api_key:
            raise HTTPException(status_code=401, detail="X-Api-Key tidak valid atau tidak ada.")
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

    def metrics(self):
        return ""
