# HealthTruth RAG API

API deteksi hoax kesehatan berbasis Retrieval-Augmented Generation (RAG), dibangun dengan FastAPI, LangGraph, Qdrant, dan Gemini 2.5 Flash.

---

## Tech Stack

| Layer | Library / Service |
|---|---|
| API Framework | FastAPI + Uvicorn |
| Workflow Orchestration | LangGraph |
| Vector Store | Qdrant via Docker (fallback ke in-memory) |
| Embedding | Gemini Embedding (`gemini-embedding-001`, 3072-dim) |
| LLM | Gemini 2.5 Flash |

---

## Project Structure

```
.
├── main.py              # Entry point — wiring dependencies + CORS + logging
├── EmbeddingService.py  # Konversi teks ke vektor via Gemini embedding
├── DocumentStore.py     # Penyimpanan dokumen di Qdrant atau in-memory
├── RagWorkflow.py       # LangGraph pipeline: retrieve → answer
├── Routes.py            # FastAPI router: /add, /ask, /fact-check, /status
├── prompts.py           # Prompt templates untuk LLM (fact-check + 3 mode)
├── docker-compose.yml   # Qdrant service
└── .env.example         # Template environment variables
```

---

## How It Works

```
Input pengguna
      │
      ▼
EmbeddingService.embed()   ← Gemini embedding-001
      │
      ▼
DocumentStore.search()     ← Qdrant (cosine similarity) / in-memory fallback
      │
      ▼
RagWorkflow (LangGraph)
  retrieve → answer        ← Gemini 2.5 Flash
      │
      ▼
API response
```

1. **Tambah dokumen** — `POST /add` menyimpan teks sebagai vektor di Qdrant.
2. **Tanya** — `POST /ask` mengambil dokumen relevan dan menghasilkan jawaban via Gemini dengan 3 mode: `ringkas`, `detail`, `sumber`.
3. **Cek fakta** — `POST /fact-check` memverifikasi klaim dan mengembalikan verdict `HOAX / BENAR / TIDAK LENGKAP` dalam format JSON.
4. **Status** — `GET /status` melaporkan backend storage dan kesiapan workflow.

---

## Setup

### Prerequisites

- Python 3.11+
- Docker (untuk Qdrant)
- Gemini API key — dapatkan di [Google AI Studio](https://aistudio.google.com)

### 1. Install dependencies

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 2. Konfigurasi environment

```bash
cp .env.example .env
# Isi GEMINI_API_KEY di .env
```

### 3. Jalankan Qdrant

```bash
docker compose up -d
```

### 4. Jalankan server

```bash
uvicorn main:app --reload
```

API tersedia di `http://localhost:8000`. Interactive docs di `http://localhost:8000/docs`.

---

## API Endpoints

### `POST /add`
Tambah dokumen ke knowledge base.

**Request:**
```json
{ "text": "Vaksin COVID-19 aman dan telah melalui uji klinis WHO." }
```

**Response:**
```json
{ "id": 0, "status": "added" }
```

Batas: maksimal 10.000 karakter per dokumen.

---

### `POST /ask`
Ajukan pertanyaan kesehatan. Mode tersedia: `ringkas` (default), `detail`, `sumber`.

**Request:**
```json
{ "question": "Apakah vaksin COVID-19 aman?", "mode": "detail" }
```

**Response:**
```json
{
  "question": "Apakah vaksin COVID-19 aman?",
  "mode": "detail",
  "answer": "Berdasarkan data WHO dan uji klinis...",
  "context_used": ["Vaksin COVID-19 aman dan telah melalui uji klinis WHO."],
  "latency_sec": 1.243
}
```

---

### `POST /fact-check`
Verifikasi klaim/pesan berantai apakah hoax atau tidak.

**Request:**
```json
{ "claim": "Minum air panas bisa membunuh virus corona" }
```

**Response:**
```json
{
  "claim": "Minum air panas bisa membunuh virus corona",
  "result": {
    "status": "HOAX",
    "summary": "Klaim ini tidak didukung bukti ilmiah.",
    "explanation": "Berdasarkan WHO, suhu air minum tidak cukup tinggi untuk membunuh virus di dalam tubuh.",
    "sources": ["WHO", "Kemenkes"]
  },
  "context_used": ["..."],
  "latency_sec": 1.876
}
```

---

### `GET /status`
Cek status service.

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

- **Qdrant fallback** — jika Qdrant tidak tersedia saat startup, service otomatis fallback ke in-memory search berbasis word overlap. Data tidak persisten saat restart.
- **LangGraph graph** — workflow adalah two-node graph (`retrieve → answer`). Node tambahan (reranking, query rewriting) dapat ditambahkan di `RagWorkflow._build_graph()` tanpa menyentuh bagian lain.
- **CORS** — origins yang diizinkan dikonfigurasi via `ALLOWED_ORIGINS` di `.env`. Default: `localhost:3000` dan `localhost:8501`.
- **Input limit** — pertanyaan dan klaim dibatasi 2.000 karakter; dokumen dibatasi 10.000 karakter.
