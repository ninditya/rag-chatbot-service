import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from RagWorkflow import RagWorkflow
from DocumentStore import DocumentStore

class QuestionRequest(BaseModel):
    question: str

class DocumentRequest(BaseModel):
    text: str

def create_router(rag_workflow: RagWorkflow, document_store: DocumentStore) -> APIRouter:
    router = APIRouter()

    @router.post("/ask")
    def ask(req: QuestionRequest):
        start = time.time()
        try:
            result = rag_workflow.ask(req.question)
            return {
                "question": req.question,
                "answer": result["answer"],
                "context_used": result.get("context", []),
                "latency_sec": round(time.time() - start, 3),
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/add")
    def add(req: DocumentRequest):
        try:
            doc_id = document_store.add_document(req.text)
            return {"id": doc_id, "status": "added"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/status")
    def status():
        return {
            **document_store.get_status(),
            "graph_ready": rag_workflow.is_ready,
        }

    return router
