from __future__ import annotations

import json
from pathlib import Path

import faiss
import numpy as np

from memory.embeddings import EmbeddingModel
from memory.memory_models import MemoryRecord


class VectorStore:
    """
    Persistent FAISS vector store for semantic memory.
    """

    def __init__(
        self,
        index_path: str = "memory/faiss.index",
        metadata_path: str = "memory/metadata.json",
        embedding_model: EmbeddingModel | None = None,
    ):
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)

        self.index_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.embedding_model = (
            embedding_model
            if embedding_model is not None
            else EmbeddingModel()
        )

        self.dimension = self.embedding_model.dimension

        if self.index_path.exists():
            self.index = faiss.read_index(
                str(self.index_path)
            )
        else:
            self.index = faiss.IndexFlatIP(
                self.dimension
            )

        if self.metadata_path.exists():
            with self.metadata_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                self.metadata: list[dict] = json.load(file)
        else:
            self.metadata = []

    def add(
        self,
        memory: MemoryRecord,
    ) -> None:
        embedding = self.embedding_model.encode(
            memory.summary or memory.content
        )

        self.index.add(
            np.expand_dims(
                embedding,
                axis=0,
            )
        )

        self.metadata.append(
            {
                "id": memory.id,
                "content": memory.content,
                "summary": memory.summary,
                "metadata": memory.metadata,
                "created_at": memory.created_at,
            }
        )

        self.save()

    def search(
    self,
    query: str,
    k: int = 5,
    min_score: float = 0.18,
) -> list[dict]:

        if self.index.ntotal == 0 or len(self.metadata) == 0:
            return []

        embedding = self.embedding_model.encode(query)

        distances, indices = self.index.search(
            np.expand_dims(embedding, axis=0),
            min(k, self.index.ntotal),
        )

        results = []

        print("\nRetrieved Memories:")

        for score, idx in zip(distances[0], indices[0]):

            if idx == -1:
                continue

            item = dict(self.metadata[idx])
            item["score"] = float(score)

            print(score, item["summary"])

            if score < min_score:
                continue

            results.append(item)

        return results

    def save(self) -> None:
        faiss.write_index(
            self.index,
            str(self.index_path),
        )

        with self.metadata_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.metadata,
                file,
                indent=4,
                ensure_ascii=False,
            )

    def __len__(self) -> int:
        return self.index.ntotal