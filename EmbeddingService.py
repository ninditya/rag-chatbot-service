import random
from typing import List

class EmbeddingService:
    VECTOR_SIZE = 128

    @staticmethod
    def embed(text: str) -> List[float]:
        # Seed derived from hash so the same input always produces the same vector.
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(EmbeddingService.VECTOR_SIZE)]
