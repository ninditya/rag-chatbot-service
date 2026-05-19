import logging
from typing import List
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)


class EmbeddingService:
    VECTOR_SIZE = 3072

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def embed(self, text: str) -> List[float]:
        try:
            res = self.client.models.embed_content(
                model="gemini-embedding-001",
                contents=[text],
                config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY"),
            )
            return list(res.embeddings[0].values)
        except Exception as e:
            logger.error("Gagal membuat embedding: %s", e, exc_info=True)
            raise RuntimeError("Gagal menghubungi embedding model. Coba lagi nanti.") from e
