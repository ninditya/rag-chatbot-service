from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

class DocumentStore:
    COLLECTION_NAME = "demo_collection"

    def __init__(self, embedding_service, qdrant_url: str = "http://localhost:6333"):
        self.embedding_service = embedding_service
        self._docs_memory: List[str] = []
        self._next_id = 0
        self._client = None
        self._use_qdrant = False
        self._init_qdrant(qdrant_url)

    def _init_qdrant(self, qdrant_url: str):
        # Preserve existing data on restart — use collection_exists instead of recreate.
        try:
            self._client = QdrantClient(qdrant_url)
            if not self._client.collection_exists(self.COLLECTION_NAME):
                self._client.create_collection(
                    collection_name=self.COLLECTION_NAME,
                    vectors_config=VectorParams(size=self.embedding_service.VECTOR_SIZE, distance=Distance.COSINE),
                )
            self._next_id = self._client.count(
                collection_name=self.COLLECTION_NAME,
                exact=True,
            ).count
            self._use_qdrant = True
            print("Qdrant connected and ready.")
        except Exception:
            print("Qdrant not available. Falling back to in-memory list.")
            self._use_qdrant = False

    def add_document(self, text: str) -> int:
        embedding = self.embedding_service.embed(text)
        doc_id = self._next_id
        self._next_id += 1

        if self._use_qdrant:
            self._client.upsert(
                collection_name=self.COLLECTION_NAME,
                points=[PointStruct(id=doc_id, vector=embedding, payload={"text": text})],
            )
        else:
            self._docs_memory.append(text)

        return doc_id

    def search(self, query: str, limit: int = 2) -> List[str]:
        embedding = self.embedding_service.embed(query)

        if self._use_qdrant:
            hits = self._client.search(
                collection_name=self.COLLECTION_NAME,
                query_vector=embedding,
                limit=limit,
            )
            return [hit.payload["text"] for hit in hits]

        results = [doc for doc in self._docs_memory if query.lower() in doc.lower()]
        if not results and self._docs_memory:
            return [self._docs_memory[0]]
        return results

    def get_status(self) -> dict:
        return {
            "qdrant_ready": self._use_qdrant,
            "in_memory_docs_count": len(self._docs_memory),
        }
