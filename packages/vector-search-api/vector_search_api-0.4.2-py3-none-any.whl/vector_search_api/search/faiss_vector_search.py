import hashlib
from typing import Any, Dict, List, Optional, Text, Tuple, Union

import numpy as np

from vector_search_api.config import logger
from vector_search_api.exceptions.search import (
    RecordAlreadyExistsError,
    RecordNotExistsError,
)
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
        self._ids_to_index_ids: Dict[Text, int] = {}
        self._index_ids_to_ids: Dict[int, Text] = {}
        self._index = faiss.IndexIDMap2(faiss.IndexFlatIP(self.dims))

    def describe(self) -> Dict:
        """Describe the records."""

        index_stats = Index(
            dimension=self.dims,
            index_fullness=0.0,
            total_vector_count=len(self._ids_to_index_ids),
            namespaces={"": Namespace(vector_count=len(self._ids_to_index_ids))},
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
            if id not in self._ids_to_index_ids:
                raise RecordNotExistsError(f"ID '{id}' is not found.")

            fetch_result.vectors[id] = FetchRecord(
                id=id,
                sparseValues={},
                values=self._index.reconstruct(self.hash_id_to_index_id(id)).tolist(),
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
        """Query vector search."""

        vector_np = np.array([vector]).astype("float32")
        top_k = self._index.ntotal if top_k >= self._index.ntotal else top_k

        distances, top_k_index_ids = self._index.search(vector_np, top_k)

        result = QueryResult(matches=[], namespace="")
        for distance, index_id in zip(distances[0], top_k_index_ids[0]):
            distance: np.float32
            index_id: np.int64

            match_values = None
            if include_values is True:
                match_values = list(self._index.reconstruct(index_id.item()))

            metadata = None
            if include_metadata is True:
                metadata = self._metadata[self._index_ids_to_ids[index_id]]

            match = Match(
                id=self._index_ids_to_ids[index_id],
                score=distance_to_similarity(distance),
                values=match_values,
                metadata=metadata,
                sparseValues={},
            )
            result.matches.append(match)

        return result

    def upsert(self, records: List[Union[Record, Tuple]]) -> "UpsertResult":
        """Upsert records."""

        update_ids: List[Text] = []
        update_index_ids: List[int] = []
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
            if record.id in self._ids_to_index_ids:
                RecordAlreadyExistsError(f"The ID {record.id} is existed.")

            doc_id = str(record.id)
            update_ids.append(doc_id)
            update_index_ids.append(self.hash_id_to_index_id(doc_id))
            update_vectors.append(record.vector)
            update_metadata[str(record.id)] = record.metadata or {}

        self._index.add_with_ids(
            np.array(update_vectors).astype("float32"),
            np.array(update_index_ids).astype("int64"),
        )
        for id, index_id in zip(update_ids, update_index_ids):
            self._ids_to_index_ids[id] = index_id
            self._index_ids_to_ids[index_id] = id
        self._metadata.update(**update_metadata)

        upsert_result = UpsertResult(upserted_count=len(update_ids))
        return upsert_result

    def update(
        self,
        id: Text,
        values: Optional[List[float]] = None,
        set_metadata: Optional[Dict[Text, Any]] = None,
    ) -> None:
        """Update the vector or metadata by ID."""

        if id not in self._ids_to_index_ids:
            raise RecordNotExistsError(f"ID '{id}' is not found.")

        if values is not None:
            index_id = self.hash_id_to_index_id(id)
            index_ids_int64 = np.array([index_id]).astype("int64")
            old_vector = self._index.reconstruct(index_id)
            self._index.remove_ids(index_ids_int64)

            try:
                self._index.add_with_ids(
                    np.array([values]).astype("float32"), index_ids_int64
                )
            except Exception as e:
                self._index.add_with_ids(
                    np.array([old_vector]).astype("float32"), index_ids_int64
                )
                raise e

        if set_metadata is not None:
            self._metadata[id] = self._metadata[id] or {}
            self._metadata[id].update(**set_metadata)

        return None

    def hash_id_to_index_id(self, id: Text) -> int:
        """Hash string ID to integer."""

        return int(hashlib.sha1(id.encode("utf-8")).hexdigest(), 16) % (10**8)
