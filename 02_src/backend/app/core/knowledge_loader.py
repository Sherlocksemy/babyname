from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable

from app.core.config import KNOWLEDGE_BASE_DIR
from app.core.dataset_registry import DATASET_SPECS
from app.schemas.knowledge import DatasetSpec, LoadedDataset


class KnowledgeLoadError(RuntimeError):
    pass


class KnowledgeLoader:
    def __init__(
        self,
        knowledge_base_dir: str | Path = KNOWLEDGE_BASE_DIR,
        dataset_specs: Iterable[DatasetSpec] = DATASET_SPECS,
    ) -> None:
        self.knowledge_base_dir = Path(knowledge_base_dir)
        self.dataset_specs = tuple(dataset_specs)
        self.warnings: list[str] = []

    def load_all(self) -> dict[str, LoadedDataset]:
        loaded: dict[str, LoadedDataset] = {}
        self.warnings.clear()
        for spec in self.dataset_specs:
            result = self.load_dataset(spec)
            if result is not None:
                loaded[spec.name] = result
        return loaded

    def load_dataset(self, spec_or_name: DatasetSpec | str) -> LoadedDataset | None:
        spec = self._resolve_spec(spec_or_name)
        path = spec.resolve(self.knowledge_base_dir)
        if not path.exists():
            message = f"Missing dataset {spec.name}: {path}"
            if spec.required:
                raise KnowledgeLoadError(message)
            self.warnings.append(message)
            return None

        try:
            if spec.kind == "csv":
                data, encoding = self.read_csv(path)
            elif spec.kind == "json":
                data, encoding = self.read_json(path)
            else:
                raise KnowledgeLoadError(f"Unsupported dataset kind for {spec.name}: {spec.kind}")
        except Exception as exc:
            raise KnowledgeLoadError(f"Failed to parse dataset {spec.name} at {path}: {exc}") from exc

        warnings = self._validate_required_fields(spec, data)
        self.warnings.extend(f"{spec.name}: {item}" for item in warnings)
        return LoadedDataset(spec=spec, path=path, data=data, encoding=encoding, warnings=warnings)

    @staticmethod
    def read_csv(path: Path) -> tuple[list[dict[str, str]], str]:
        last_error: Exception | None = None
        for encoding in ("utf-8-sig", "utf-8"):
            try:
                with path.open("r", encoding=encoding, newline="") as handle:
                    return list(csv.DictReader(handle)), encoding
            except UnicodeDecodeError as exc:
                last_error = exc
        raise KnowledgeLoadError(f"CSV decode failed: {path}: {last_error}")

    @staticmethod
    def read_json(path: Path) -> tuple[Any, str]:
        last_error: Exception | None = None
        for encoding in ("utf-8-sig", "utf-8"):
            try:
                with path.open("r", encoding=encoding) as handle:
                    return json.load(handle), encoding
            except UnicodeDecodeError as exc:
                last_error = exc
        raise KnowledgeLoadError(f"JSON decode failed: {path}: {last_error}")

    def _resolve_spec(self, spec_or_name: DatasetSpec | str) -> DatasetSpec:
        if isinstance(spec_or_name, DatasetSpec):
            return spec_or_name
        for spec in self.dataset_specs:
            if spec.name == spec_or_name:
                return spec
        raise KnowledgeLoadError(f"Unknown dataset: {spec_or_name}")

    @staticmethod
    def _validate_required_fields(spec: DatasetSpec, data: Any) -> list[str]:
        if not spec.required_fields:
            return []
        fields = set()
        if isinstance(data, list):
            for row in data[:20]:
                if isinstance(row, dict):
                    fields.update(row.keys())
        elif isinstance(data, dict):
            fields.update(data.keys())
            for value in list(data.values())[:20]:
                if isinstance(value, dict):
                    fields.update(value.keys())
                elif isinstance(value, list) and value and isinstance(value[0], dict):
                    fields.update(value[0].keys())
        missing = [field for field in spec.required_fields if field not in fields]
        return [f"missing expected field: {field}" for field in missing]
