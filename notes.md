# Design Notes — RAG Service Refactor

## Main Design Decisions

The original `main.py` mixed HTTP routing, document storage, embedding generation, and the LangGraph workflow into a single file with global state. The refactor splits these into four focused classes: `EmbeddingService`, `DocumentStore`, `RagWorkflow`, and a `Routes` factory — each with a single clear responsibility. Dependencies are passed explicitly through constructors rather than shared via globals, making it straightforward to swap any component (e.g., replace the fake embedder with a real model) without touching the rest.

## Trade-off Considered

Splitting into multiple files adds a small navigation overhead for a project this size — a single well-organised file could feel simpler for a demo. The multi-file structure was chosen anyway because it mirrors how the service would grow in practice: a real embedding model, a persistent Qdrant setup, or additional workflow nodes can each be changed in isolation without risk of breaking the other layers. The upfront cost is low; the long-term maintenance benefit compounds quickly.

## How This Improves Maintainability

Because each component owns its own state and exposes a narrow interface (`embed`, `add_document`/`search`/`get_status`, `ask`/`is_ready`), changes stay local and tests can target individual units without standing up the full API. The `DocumentStore` initialises Qdrant safely on startup — preserving existing data instead of recreating the collection — and seeds auto-incrementing IDs from the live collection count, fixing the unsafe `len(docs_memory)` ID from the original. The `/status` endpoint now calls `get_status()` and `is_ready` on the respective objects rather than reaching into their internals, keeping encapsulation intact.
