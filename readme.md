# RAG Chatbot Service

A lightweight Retrieval-Augmented Generation (RAG) chatbot API built with FastAPI, LangGraph, and Qdrant. The service allows you to add documents to a knowledge base and query them through a natural-language question endpoint.

---

## Tech Stack

| Layer | Library |
|---|---|
| API Framework | FastAPI + Uvicorn |
| Workflow Orchestration | LangGraph |
| Vector Store | Qdrant (falls back to in-memory if unavailable) |
| Embedding | Deterministic hash-based embedding (128-dim) |

---

## Project Structure

```
.
├── main.py             # App entry point — wires dependencies together
├── EmbeddingService.py # Converts text to fixed-size vectors
├── DocumentStore.py    # Manages document storage in Qdrant or in-memory
├── RagWorkflow.py      # LangGraph pipeline: retrieve → answer
└── Routes.py           # FastAPI router with /add, /ask, /status endpoints
```

Each file maps to a single responsibility, making the codebase easy to extend or test in isolation.

---

## How It Works

1. **Add documents** — `POST /add` stores a piece of text as a vector in Qdrant (or in-memory fallback).
2. **Ask a question** — `POST /ask` embeds the question, retrieves the most relevant documents, and returns an answer synthesized from the top result.
3. **Check status** — `GET /status` reports the storage backend in use and the workflow readiness.

```
User question
     │
     ▼
EmbeddingService.embed()
     │
     ▼
DocumentStore.search()  ←── Qdrant / in-memory
     │
     ▼
RagWorkflow (LangGraph)
  retrieve → answer
     │
     ▼
API response
```

---

## Setup

### Prerequisites

- Python 3.11+
- (Optional) Qdrant running locally on port 6333

### Install dependencies

```bash
python -m venv env
source env/bin/activate
pip install fastapi uvicorn langgraph qdrant-client
```

### Run the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs are at `http://localhost:8000/docs`.

---

## API Endpoints

### `POST /add`
Add a document to the knowledge base.

**Request body:**
```json
{ "text": "LangGraph is a framework for building stateful LLM workflows." }
```

**Response:**
```json
{ "id": 0, "status": "added" }
```

---

### `POST /ask`
Ask a question against the stored documents.

**Request body:**
```json
{ "question": "What is LangGraph?" }
```

**Response:**
```json
{
  "question": "What is LangGraph?",
  "answer": "I found this: 'LangGraph is a framework for building stateful LLM workflows....'",
  "context_used": ["LangGraph is a framework for building stateful LLM workflows."],
  "latency_sec": 0.012
}
```

---

### `GET /status`
Check the current state of the service.

**Response:**
```json
{
  "qdrant_ready": true,
  "in_memory_docs_count": 0,
  "graph_ready": true
}
```

---

## Notes

- **Qdrant fallback** — if Qdrant is not reachable on startup, the service automatically falls back to an in-memory list with basic keyword search. Data in fallback mode does not persist across restarts.
- **Embedding** — the current `EmbeddingService` uses a deterministic hash-based approach (no external model required). It can be swapped for a real embedding model (e.g. OpenAI, sentence-transformers) by implementing the same `embed(text)` interface.
- **LangGraph graph** — the workflow is a two-node graph (`retrieve → answer`). Additional nodes (e.g. reranking, query rewriting) can be added to the graph in `RagWorkflow._build_graph()` without touching the rest of the codebase.
