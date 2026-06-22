from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal


DatasetKind = Literal["csv", "json"]


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    relative_path: str
    kind: DatasetKind
    required: bool = True
    primary_key: str | None = None
    required_fields: tuple[str, ...] = ()
    category: str = "knowledge"

    def resolve(self, base_dir: Path) -> Path:
        return base_dir / self.relative_path


@dataclass
class LoadedDataset:
    spec: DatasetSpec
    path: Path
    data: Any
    encoding: str
    warnings: list[str] = field(default_factory=list)

    @property
    def row_count(self) -> int:
        if isinstance(self.data, dict):
            return len(self.data)
        if isinstance(self.data, list):
            return len(self.data)
        return 1 if self.data is not None else 0


@dataclass
class DatasetAudit:
    name: str
    path: str
    exists: bool
    row_count: int = 0
    fields: list[str] = field(default_factory=list)
    null_counts: dict[str, int] = field(default_factory=dict)
    duplicate_primary_keys: int = 0
    parse_failures: int = 0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    status: str = "ok"
