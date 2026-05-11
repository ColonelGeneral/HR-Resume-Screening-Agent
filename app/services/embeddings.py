from __future__ import annotations

from functools import lru_cache
import math
from typing import Iterable

import numpy as np

from app.core.config import settings

try:
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover - optional dependency fallback
    SentenceTransformer = None


class EmbeddingService:
    def __init__(self, model_name: str | None = None) -> None:
        self.model_name = model_name or settings.embedding_model
        self._model = None
        if SentenceTransformer is not None:
            try:
                self._model = SentenceTransformer(self.model_name)
            except Exception:
                self._model = None

    @property
    def available(self) -> bool:
        return self._model is not None

    def encode(self, texts: Iterable[str]) -> np.ndarray:
        texts = list(texts)
        if self._model is not None:
            vectors = self._model.encode(texts, normalize_embeddings=True)
            return np.asarray(vectors, dtype=np.float32)
        return np.asarray([self._fallback_vector(text) for text in texts], dtype=np.float32)

    def similarity(self, left: str, right: str) -> float:
        vectors = self.encode([left, right])
        left_vec, right_vec = vectors[0], vectors[1]
        denom = float(np.linalg.norm(left_vec) * np.linalg.norm(right_vec))
        if denom == 0:
            return 0.0
        return float(np.dot(left_vec, right_vec) / denom)

    @staticmethod
    @lru_cache(maxsize=2048)
    def _fallback_vector(text: str) -> list[float]:
        tokens = [token for token in text.lower().split() if token]
        buckets = [0.0] * 64
        for token in tokens:
            bucket = sum(ord(char) for char in token) % len(buckets)
            buckets[bucket] += 1.0
        norm = math.sqrt(sum(value * value for value in buckets)) or 1.0
        return [value / norm for value in buckets]


def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()
