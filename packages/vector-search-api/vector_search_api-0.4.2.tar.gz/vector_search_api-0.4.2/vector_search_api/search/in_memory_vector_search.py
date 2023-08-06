from typing import Any, Dict, List, Optional, Text, Tuple, Union

import numpy as np

from vector_search_api.exceptions.search import RecordNotExistsError
from vector_search_api.helper.vector import cosine_similarity
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


class InMemoryVectorSearch(BaseVectorSearch):
    def __init__(self, project: Text, dims: int, **kwargs):
        """Initialize basic attributes project, dims, also the storage of records."""

        super(InMemoryVectorSearch, self).__init__(project=project, dims=dims, **kwargs)

        self._metadata: Dict[Text, Dict[Text, Any]] = {}
        self._ids = np.array([])
        self._vectors = np.empty((0, self.dims))

    def describe(self) -> "Index":
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
                raise RecordNotExistsError(f"ID '{id}' is not found.")

            fetch_result.vectors[self._ids[idx][0]] = FetchRecord(
                id=self._ids[idx][0],
                sparseValues={},
                values=self._vectors[idx].tolist(),
                metadata=self._metadata[id] or {},
            )

        return fetch_result

    def query(
        self,
        vector: List[float],
        top_k: int = 3,
        include_values: bool = False,
        include_metadata: bool = False,
    ) -> "QueryResult":
        """Query vector search.

        Parameters
        ----------
        vector : list[float]
            Query with vector.

        top_k : int
            Top k.

        include_values : bool, default is False
            Return vector or not.

        include_metadata : bool, default is False
            Return metadata or not.

        Returns
        -------
        query_result : dict
            Query result.
        """

        cos_sim = cosine_similarity(np.array(vector), targets=self._vectors)
        top_k_idxs = np.argsort(cos_sim)[-top_k:][::-1]

        result: Dict = QueryResult(
            matches=[
                Match(
                    id=self._ids[idx],
                    score=cos_sim[idx],
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
                for idx in top_k_idxs
            ],
            namespace="",
        )
        return result

    def upsert(self, records: List[Union[Record, Tuple]]) -> "UpsertResult":
        """Upsert records."""

        update_ids = []
        update_vectors = []
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

        self._metadata.update(**update_metadata)
        self._ids = np.append(self._ids, update_ids)
        self._vectors = np.concatenate((self._vectors, update_vectors), axis=0)

        upsert_result = UpsertResult(upserted_count=len(update_ids))
        return upsert_result

    def update(
        self,
        id: Text,
        values: Optional[List[float]] = None,
        set_metadata: Optional[Dict[Text, Any]] = None,
    ) -> None:
        """Update the vector or metadata by ID."""

        idx = np.where(self._ids == id)

        if len(idx) == 0:
            raise RecordNotExistsError(f"ID '{id}' is not found.")

        if values is not None:
            self._vectors[idx] = np.array(values)

        if set_metadata is not None:
            self._metadata[id] = self._metadata[id] or {}
            self._metadata[id].update(**set_metadata)

        return None
