import logging
import uuid
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

logger = logging.getLogger(__name__)


class DocumentStore:
    COLLECTION_NAME = "demo_collection"

    def __init__(self, embedding_service, qdrant_url: str = "http://localhost:6333", qdrant_api_key: str = ""):
        self.embedding_service = embedding_service
        self._docs_memory: List[str] = []
        self._client = None
        self._use_qdrant = False
        self._init_qdrant(qdrant_url, qdrant_api_key)

    def _init_qdrant(self, qdrant_url: str, qdrant_api_key: str = ""):
        try:
            self._client = QdrantClient(
                qdrant_url,
                timeout=5,
                api_key=qdrant_api_key or None,
            )
            if not self._client.collection_exists(self.COLLECTION_NAME):
                self._client.create_collection(
                    collection_name=self.COLLECTION_NAME,
                    vectors_config=VectorParams(size=self.embedding_service.VECTOR_SIZE, distance=Distance.COSINE),
                )
            self._use_qdrant = True
            logger.info("Qdrant connected and ready.")
        except Exception as e:
            logger.warning("Qdrant not available (%s). Falling back to in-memory list.", e)
            self._use_qdrant = False

    def add_document(self, text: str) -> str:
        embedding = self.embedding_service.embed(text)
        doc_id = uuid.uuid4()

        if self._use_qdrant:
            self._client.upsert(
                collection_name=self.COLLECTION_NAME,
                points=[PointStruct(id=str(doc_id), vector=embedding, payload={"text": text})],
            )
        else:
            self._docs_memory.append(text)

        return str(doc_id)

    def search(self, query: str, limit: int = 3, score_threshold: float = 0.4) -> List[str]:
        try:
            embedding = self.embedding_service.embed(query)
        except RuntimeError:
            logger.error("Gagal membuat embedding untuk query '%s'", query[:50])
            raise

        if self._use_qdrant:
            hits = self._client.search(
                collection_name=self.COLLECTION_NAME,
                query_vector=embedding,
                limit=limit,
                score_threshold=score_threshold,
            )
            seen, results = set(), []
            for pt in hits:
                text = pt.payload["text"]
                if text not in seen:
                    seen.add(text)
                    results.append(text)
            return results

        return self._search_memory(query, limit)

    def _search_memory(self, query: str, limit: int) -> List[str]:
        if not self._docs_memory:
            return []

        query_words = set(query.lower().split())

        def score(doc: str) -> int:
            return sum(1 for w in query_words if w in doc.lower())

        ranked = sorted(self._docs_memory, key=score, reverse=True)
        return [doc for doc in ranked if score(doc) > 0][:limit]

    def get_status(self) -> dict:
        return {
            "qdrant_ready": self._use_qdrant,
            "in_memory_docs_count": len(self._docs_memory),
        }
