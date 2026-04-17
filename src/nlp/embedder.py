import numpy as np
from loguru import logger
from sentence_transformers import SentenceTransformer
from src.utils.config import load_settings


class SkillEmbedder:
    def __init__(self):
        settings = load_settings()
        model_name = settings["model"]["sbert_model"]
        logger.info(f"Loading SBERT model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self._cache: dict[str, np.ndarray] = {}

    def embed(self, texts: list[str]) -> np.ndarray:
        uncached = [t for t in texts if t not in self._cache]
        if uncached:
            vectors = self.model.encode(uncached, show_progress_bar=False, normalize_embeddings=True)
            for text, vec in zip(uncached, vectors):
                self._cache[text] = vec
        return np.array([self._cache[t] for t in texts])

    def embed_single(self, text: str) -> np.ndarray:
        return self.embed([text])[0]

    def similarity(self, a: str | np.ndarray, b: str | np.ndarray) -> float:
        if isinstance(a, str):
            a = self.embed_single(a)
        if isinstance(b, str):
            b = self.embed_single(b)
        return float(np.dot(a, b))

    def pairwise_similarity(self, skills_a: list[str], skills_b: list[str]) -> np.ndarray:
        vecs_a = self.embed(skills_a)
        vecs_b = self.embed(skills_b)
        return vecs_a @ vecs_b.T