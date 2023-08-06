from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Text

from vector_search_api.schema.base import DataclassBase


@dataclass
class Namespace(DataclassBase):
    vector_count: int


@dataclass
class Index(DataclassBase):
    dimension: int
    index_fullness: float
    namespaces: Dict[Text, Namespace]
    total_vector_count: int


@dataclass
class UpsertResult(DataclassBase):
    upserted_count: int


@dataclass
class Match(DataclassBase):
    id: Text
    score: float
    sparseValues: Dict
    values: List[float]
    metadata: Optional[Dict] = None


@dataclass
class QueryResult(DataclassBase):
    matches: List[Match]
    namespace: Text


@dataclass
class FetchRecord(DataclassBase):
    id: Text
    sparseValues: Dict
    values: List[float]
    metadata: Optional[Dict[Text, Any]] = None


@dataclass
class FetchResult(DataclassBase):
    namespace: Text
    vectors: Dict[Text, FetchRecord]
