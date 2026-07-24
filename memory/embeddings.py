from __future__ import annotations

from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingModel:
    """
    Wrapper around SentenceTransformer.

    This class isolates the embedding model from the
    rest of the memory system so it can be replaced
    later without changing other components.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.model = SentenceTransformer(model_name)

    def encode(
        self,
        text: str,
    ) -> np.ndarray:
        """
        Generate an embedding for a single string.
        """
        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embedding.astype("float32")

    def encode_batch(
        self,
        texts: list[str],
    ) -> np.ndarray:
        """
        Generate embeddings for multiple strings.
        """
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embeddings.astype("float32")

    @property
    def dimension(self) -> int:
        """
        Returns the embedding dimension.
        """
        return self.model.get_embedding_dimension()