import inspect
from dataclasses import dataclass
from typing import Dict, List, NamedTuple, Optional, Text


class Record(NamedTuple):
    id: Text
    vector: List[float]
    metadata: Dict = None


@dataclass
class DataclassBase:
    @classmethod
    def from_dict(cls, d: Optional[Dict] = None, **kwargs):
        d = d or {}
        d.update(kwargs)
        return cls(
            **{k: v for k, v in d.items() if k in inspect.signature(cls).parameters}
        )
