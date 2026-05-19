# HealthTruth-AI

API pengecekan mitos obat tradisional vs medis berbasis Retrieval-Augmented Generation (RAG), dibangun dengan FastAPI, LangGraph, Qdrant, dan Gemini 2.5 Flash. Dilengkapi chatbot Streamlit dengan personalisasi profil kesehatan.

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

1. **Tambah dokumen** — `POST /add` menyimpan teks referensi ke Qdrant (artikel BPOM, IDI, WHO, Kemenkes, dll).
2. **Tanya** — `POST /ask` mengambil dokumen relevan dan menghasilkan jawaban via Gemini dengan 3 mode: `ringkas`, `detail`, `sumber`.
3. **Cek fakta** — `POST /fact-check` memverifikasi klaim dan mengembalikan verdict `MITOS / FAKTA / PERLU BUKTI LEBIH LANJUT` dalam format JSON.
4. **Status** — `GET /status` melaporkan backend storage dan kesiapan workflow.

---

## Setup

### Prerequisites

- Python 3.11+
- Docker (untuk Qdrant)
- Gemini API key — dapatkan di [Google AI Studio](https://aistudio.google.com)

### Opsi A — Local (development)

```bash
# 1. Virtual environment & dependencies
python -m venv env
source env/bin/activate
pip install -r requirements.txt

# 2. Konfigurasi API key
cp .env.example .env
# Edit .env, isi: GEMINI_API_KEY=key_kamu

# 3. Jalankan Qdrant saja via Docker
docker compose up -d qdrant

# 4. Jalankan server
uvicorn main:app --reload
```

### Opsi B — Full Docker

```bash
cp .env.example .env
# Edit .env, isi: GEMINI_API_KEY=key_kamu

docker compose up
```

API tersedia di `http://localhost:8000`. Interactive docs di `http://localhost:8000/docs`.

---

## API Endpoints

### `POST /add`
Tambah dokumen referensi ke knowledge base (artikel BPOM, IDI, WHO, Kemenkes, dll).

**Request:**
```json
{ "text": "Menurut BPOM, jamu yang tidak terdaftar berisiko mengandung bahan kimia obat berbahaya." }
```

**Response:**
```json
{ "id": 0, "status": "added" }
```

Batas: maksimal 10.000 karakter per dokumen.

---

### `POST /ask`
Ajukan pertanyaan seputar obat tradisional vs medis. Mode: `ringkas` (default), `detail`, `sumber`.

**Request:**
```json
{ "question": "Apakah kunyit bisa menggantikan obat anti-inflamasi?", "mode": "detail" }
```

**Response:**
```json
{
  "question": "Apakah kunyit bisa menggantikan obat anti-inflamasi?",
  "mode": "detail",
  "answer": "Kunyit mengandung kurkumin yang memiliki sifat anti-inflamasi...",
  "context_used": ["..."],
  "latency_sec": 2.1
}
```

---

### `POST /fact-check`
Verifikasi klaim/mitos tentang obat tradisional.

**Request:**
```json
{ "claim": "Minum rebusan daun sirsak bisa menyembuhkan kanker" }
```

**Response:**
```json
{
  "claim": "Minum rebusan daun sirsak bisa menyembuhkan kanker",
  "result": {
    "status": "MITOS",
    "summary": "Belum ada bukti ilmiah yang memadai bahwa daun sirsak menyembuhkan kanker.",
    "explanation": "Berdasarkan BPOM dan IDI, klaim ini tidak didukung uji klinis yang valid...",
    "sources": ["BPOM", "IDI"]
  },
  "context_used": ["..."],
  "latency_sec": 3.1
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

## Deploy ke Production

### Opsi A — VPS (paling simpel, Docker Compose langsung)

```bash
# Di server (Ubuntu/Debian)
git clone <repo>
cd <repo>
cp .env.example .env
# Edit .env: isi GEMINI_API_KEY

docker compose up -d
```

Buka port 8000 (API) dan 8501 (Streamlit) di firewall VPS.

### Opsi B — Railway / Render

1. Push repo ke GitHub
2. Buat dua service terpisah:
   - **App**: Docker build dari repo ini, env `GEMINI_API_KEY`
   - **Qdrant**: gunakan [Qdrant Cloud](https://cloud.qdrant.io) (free tier tersedia), set `QDRANT_URL` ke URL cloud
3. Set `ALLOWED_ORIGINS` ke domain frontend yang diizinkan

### Variabel environment produksi

| Variabel | Wajib | Keterangan |
|----------|-------|------------|
| `GEMINI_API_KEY` | ✓ | Google AI Studio |
| `EMBEDDING_API_KEY` | — | Pisah dari generation key untuk isolasi kuota |
| `QDRANT_URL` | — | Default `http://localhost:6333` |
| `ADD_API_KEY` | — | Proteksi endpoint `/add` dari akses sembarang |
| `ALLOWED_ORIGINS` | — | CORS whitelist, default localhost |

---

## Notes

- **Knowledge base** — isi dengan dokumen dari BPOM, IDI, WHO, Kemenkes, atau jurnal ilmiah terpercaya via `POST /add`. Gunakan `seed_knowledge_base.py` untuk batch insert awal.
- **Qdrant fallback** — jika Qdrant tidak tersedia, otomatis fallback ke in-memory. Data tidak persisten saat restart.
- **LLM fallback** — jika Gemini 503/quota habis, jawaban diambil langsung dari knowledge base tanpa LLM.
- **LangGraph graph** — two-node graph (`retrieve → answer`). Node tambahan bisa ditambahkan di `RagWorkflow._build_graph()`.
- **CORS** — dikonfigurasi via `ALLOWED_ORIGINS` di `.env`.
- **Input limit** — pertanyaan/klaim maks 2.000 karakter; dokumen maks 10.000 karakter.
