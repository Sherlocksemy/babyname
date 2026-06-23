from __future__ import annotations

import json
from pathlib import Path

from app.core.config import RUNTIME_DIR


STRUCTURE_ARCHETYPE_MATRIX: dict[str, list[dict]] = {
    "S01": [{"archetype_id": "A01", "weight": 5}, {"archetype_id": "A02", "weight": 4}],
    "S02": [{"archetype_id": "A03", "weight": 5}, {"archetype_id": "A04", "weight": 3}, {"archetype_id": "A12", "weight": 2}],
    "S03": [{"archetype_id": "A05", "weight": 5}, {"archetype_id": "A10", "weight": 3}],
    "S04": [{"archetype_id": "A08", "weight": 4}, {"archetype_id": "A10", "weight": 4}],
    "S05": [{"archetype_id": "A02", "weight": 3}, {"archetype_id": "A06", "weight": 4}, {"archetype_id": "A07", "weight": 2}, {"archetype_id": "A09", "weight": 3}],
    "S06": [{"archetype_id": "A01", "weight": 5}, {"archetype_id": "A08", "weight": 2}],
    "S07": [{"archetype_id": "A03", "weight": 3}, {"archetype_id": "A07", "weight": 5}, {"archetype_id": "A11", "weight": 2}],
    "S08": [{"archetype_id": "A08", "weight": 5}, {"archetype_id": "A03", "weight": 2}],
    "S09": [{"archetype_id": "A09", "weight": 5}, {"archetype_id": "A02", "weight": 2}],
    "S10": [{"archetype_id": "A04", "weight": 4}, {"archetype_id": "A05", "weight": 3}, {"archetype_id": "A06", "weight": 5}],
    "S11": [{"archetype_id": "A10", "weight": 4}, {"archetype_id": "A11", "weight": 5}],
    "S12": [{"archetype_id": "A12", "weight": 5}, {"archetype_id": "A03", "weight": 2}],
}

ARCHETYPE_CONFLICTS: dict[str, list[str]] = {
    "A01": ["A05"],
    "A04": ["A09"],
    "A05": ["A07"],
    "A06": ["A09"],
    "A10": ["A06"],
}


def get_mapping_catalog() -> dict:
    return {
        "matrix": STRUCTURE_ARCHETYPE_MATRIX,
        "conflicts": ARCHETYPE_CONFLICTS,
        "source_document": "02C_ARCHETYPE_SCORING_MATRIX.md",
        "version": "1.0",
    }


def ensure_mapping_catalog(output_dir: Path | None = None) -> Path:
    derived_dir = output_dir or (RUNTIME_DIR / "derived")
    derived_dir.mkdir(parents=True, exist_ok=True)
    path = derived_dir / "structure_archetype_matrix.v1.json"
    path.write_text(json.dumps(get_mapping_catalog(), ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def ensure_all_catalogs(output_dir: Path | None = None) -> list[Path]:
    from app.catalogs.archetype_catalog import ensure_archetype_catalog
    from app.catalogs.structure_catalog import ensure_structure_catalog

    return [
        ensure_structure_catalog(output_dir),
        ensure_archetype_catalog(output_dir),
        ensure_mapping_catalog(output_dir),
    ]
