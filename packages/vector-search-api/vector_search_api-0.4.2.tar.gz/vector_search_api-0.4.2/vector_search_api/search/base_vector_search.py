from typing import Any, Dict, List, Optional, Text, Tuple, Union

from vector_search_api.schema import (
    FetchResult,
    Index,
    QueryResult,
    Record,
    UpsertResult,
)


class BaseVectorSearch:
    """Base Vector Search ABC."""

    def __init__(self, project: Text, dims: Optional[int] = None, **kwargs):
        """Initialize basic attributes project, dims."""

        self.project: Text = project
        self.dims = int(dims) if dims else None
        self.kwargs = kwargs

    def describe(self) -> "Index":
        """Describe the api status."""

        raise NotImplementedError()

    def fetch(self, ids: Union[List[Text], Text]) -> "FetchResult":
        """Fetch record by id."""

        raise NotImplementedError()

    def query(
        self,
        vector: List[float],
        top_k: int = 3,
        include_values: bool = False,
        include_metadata: bool = False,
    ) -> "QueryResult":
        """Query vector search."""

        raise NotImplementedError()

    def upsert(self, records: List[Union[Record, Tuple]]) -> UpsertResult:
        """Upsert records."""

        raise NotImplementedError()

    def update(
        self,
        id: Text,
        values: Optional[List[float]] = None,
        set_metadata: Optional[Dict[Text, Any]] = None,
    ) -> None:
        """Update the vector or metadata by ID."""

        raise NotImplementedError()
