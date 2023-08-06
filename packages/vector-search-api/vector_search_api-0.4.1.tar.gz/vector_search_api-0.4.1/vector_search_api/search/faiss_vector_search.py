from typing import Any, Dict, List, Text, Tuple, Union

import numpy as np

from vector_search_api.config import logger
from vector_search_api.helper.vector import distance_to_similarity
from vector_search_api.schema import (
    FetchRecord,
    FetchResult,
    Index,
    Match,
    Namespace,
    QueryResult,
    Record,
    UpsertResult,
)
from vector_search_api.search.base_vector_search import BaseVectorSearch

try:
    import faiss
except ImportError:
    logger.warning("Trying import faiss but uninstalled.")


class FaissVectorSearch(BaseVectorSearch):
    def __init__(self, project: Text, dims: int, **kwargs):

        super(FaissVectorSearch, self).__init__(project=project, dims=dims, **kwargs)

        self._metadata: Dict[Text, Dict[Text, Any]] = {}
        self._ids = np.array([])
        self._vectors = np.empty((0, self.dims))
        self._index = faiss.IndexFlatL2(self.dims)

    def describe(self) -> Dict:
        """Describe the records."""

        index_stats = Index(
            dimension=self.dims,
            index_fullness=0.0,
            total_vector_count=self._ids.size,
            namespaces={"": Namespace(vector_count=self._ids.size)},
        )
        return index_stats

    def fetch(self, ids: Union[List[Text], Text]) -> "FetchResult":
        """Fetch record by id."""

        fetch_result = FetchResult(namespace="", vectors={})

        if not ids:
            return fetch_result

        if isinstance(ids, List) is False:
            ids = [ids]

        for id in ids:
            idx = np.where(self._ids == id)

            if len(idx) == 0:
                raise ValueError(f"ID '{id}' is not found.")

            fetch_result.vectors[self._ids[idx][0]] = FetchRecord(
                id=self._ids[idx][0],
                sparseValues={},
                values=self._vectors[idx].tolist(),
            )

        return fetch_result

    def query(
        self,
        vector: List[float],
        top_k: int = 3,
        include_values: bool = False,
        include_metadata: bool = False,
    ) -> "QueryResult":
        """Query vector search."""

        vector_np = np.array([vector]).astype("float32")
        top_k = self._index.ntotal if top_k >= self._index.ntotal else top_k

        distances, top_k_idxs = self._index.search(vector_np, top_k)

        result: Dict = QueryResult(
            matches=[
                Match(
                    id=self._ids[idx],
                    score=distance_to_similarity(distance),
                    values=(
                        list(self._vectors[idx]) if include_values is True else None
                    ),
                    metadata=(
                        self._metadata[self._ids[idx]]
                        if include_metadata is True
                        else None
                    ),
                    sparseValues={},
                )
                for distance, idx in zip(distances[0], top_k_idxs[0])
            ],
            namespace="",
        )
        return result

    def upsert(self, records: List[Union[Record, Tuple]]) -> "UpsertResult":
        """Upsert records."""

        update_ids: List[Text] = []
        update_vectors: List[List[float]] = []
        update_metadata = {}
        for doc in records:
            record = Record(*doc)
            if not record.id:
                raise ValueError(f"The value of id '{record.id}' is not validated.")
            if len(record.vector) != self.dims:
                raise ValueError(
                    f"The vector dimension {len(record.vector)} is not validated."
                )
            update_ids.append(str(record.id))
            update_vectors.append(record.vector)
            update_metadata[str(record.id)] = record.metadata or {}

        self._index.add(np.array(update_vectors).astype("float32"))

        self._metadata.update(**update_metadata)
        self._ids = np.append(self._ids, update_ids)
        self._vectors = np.concatenate((self._vectors, update_vectors), axis=0)

        upsert_result = UpsertResult(upserted_count=len(update_ids))
        return upsert_result
