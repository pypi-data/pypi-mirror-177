from typing import Any, Dict, List, Optional, Text, Tuple, Union

from vector_search_api.schema import (
    Index,
    Match,
    Namespace,
    QueryResult,
    Record,
    UpsertResult,
    FetchResult,
    FetchRecord,
)
from vector_search_api.search.base_vector_search import BaseVectorSearch
from vector_search_api.config import settings


class PineconeVectorSearch(BaseVectorSearch):
    """Pinecone Vector Search."""

    def __init__(
        self,
        project: Text,
        index: Text = settings.pinecone_index_name,
        namespace: Text = settings.pinecone_namespace,
        api_key: Text = settings.pinecone_api_key,
        environment: Text = settings.pinecone_environment,
        dims: Optional[int] = None,
        init_probe: bool = True,
        **kwargs
    ):
        """Initialize basic attributes project, dims, also the storage of records."""

        import pinecone

        pinecone.init(api_key=api_key, environment=environment)

        super(PineconeVectorSearch, self).__init__(project=project, dims=dims, **kwargs)

        self.index = index
        self.namespace = namespace
        self._index = pinecone.Index(self.index)

        if init_probe is True:
            pinecone.whoami()
            self.describe()

    def describe(self) -> "Index":
        """Describe the api status."""

        result: Dict = self._index.describe_index_stats().to_dict()
        namespaces = {
            k: Namespace(**v) for k, v in result.pop("namespaces", {}).items()
        }
        index_stats = Index(namespaces=namespaces, **result)
        self.dims = index_stats.dimension
        return index_stats

    def fetch(self, ids: Union[List[Text], Text]) -> "FetchResult":
        """Fetch record by id."""

        if isinstance(ids, List) is False:
            ids = [ids]

        result = self._index.fetch(ids).to_dict()

        fetch_result = FetchResult(namespace=result["namespace"], vectors={})
        for rec_id, rec_data in result["vectors"].items():
            fetch_result.vectors[rec_id] = FetchRecord(**rec_data)
        return fetch_result

    def query(
        self,
        vector: List[float],
        top_k: int = 3,
        include_values: bool = False,
        include_metadata: bool = False,
        namespace: Optional[Text] = None,
    ) -> "QueryResult":
        """Query vector search."""

        namespace = namespace or self.namespace
        result = self._index.query(
            vector=vector,
            top_k=top_k,
            include_values=include_values,
            include_metadata=include_metadata,
            namespace=namespace,
        ).to_dict()

        query_result = QueryResult(
            matches=[Match(**m) for m in result["matches"]],
            namespace=result["namespace"],
        )

        return query_result

    def upsert(
        self, records: List[Union[Record, Tuple]], namespace: Optional[Text] = None
    ) -> "UpsertResult":
        """Upsert records."""

        namespace = namespace or self.namespace
        result = self._index.upsert(
            [Record(*doc) for doc in records], namespace=namespace
        )
        upsert_result = UpsertResult(**result.to_dict())
        return upsert_result

    def update(
        self,
        id: Text,
        values: Optional[List[float]] = None,
        set_metadata: Optional[Dict[Text, Any]] = None,
    ) -> None:
        """Update the vector or metadata by ID."""

        params = {}
        if values is not None:
            params["values"] = values
        if set_metadata is not None:
            params["set_metadata"] = set_metadata
        self._index.update(id=id, **params)

        return None
