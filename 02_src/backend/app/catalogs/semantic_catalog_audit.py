from __future__ import annotations

import json
import time
from collections import Counter
from pathlib import Path

from app.catalogs.name_char_catalog_builder import ensure_name_char_catalog
from app.core.config import REPORTS_DIR


LEGACY_NAME_FRIENDLY_UNIQUE_COUNT = 113


class SemanticCatalogAudit:
    def __init__(self, reports_dir: Path = REPORTS_DIR) -> None:
        self.reports_dir = reports_dir

    def run(self) -> dict:
        started = time.perf_counter()
        catalog = ensure_name_char_catalog(force=True)
        records = catalog["records"]
        level_counts = Counter(record["nameability_level"] for record in records)
        category_counts = Counter(category for record in records for category in record["semantic_categories"])
        core_extended = level_counts.get("CORE", 0) + level_counts.get("EXTENDED", 0)
        rejected = [record for record in records if record["nameability_level"] == "REJECTED"]
        payload = {
            "catalog_statistics": {
                "total_records": len(records),
                "level_counts": dict(level_counts),
                "core_extended_count": core_extended,
                "legacy_name_friendly_unique_count": LEGACY_NAME_FRIENDLY_UNIQUE_COUNT,
                "minimum_required_core_extended": LEGACY_NAME_FRIENDLY_UNIQUE_COUNT * 4,
                "minimum_coverage_passed": core_extended >= LEGACY_NAME_FRIENDLY_UNIQUE_COUNT * 4,
                "category_counts": dict(category_counts),
            },
            "rejection_audit": {
                "rejected_count": len(rejected),
                "top_rejection_reasons": dict(Counter(reason for record in rejected for reason in record["rejection_reasons"]).most_common(20)),
                "sample": rejected[:50],
            },
            "performance": {
                "catalog_build_seconds": round(time.perf_counter() - started, 4),
            },
        }
        self._write_reports(payload)
        return payload

    def _write_reports(self, payload: dict) -> None:
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        _write_json(self.reports_dir / "milestone_3_2_catalog_statistics.json", payload["catalog_statistics"])
        _write_json(self.reports_dir / "milestone_3_2_catalog_rejection_audit.json", payload["rejection_audit"])
        _write_json(self.reports_dir / "milestone_3_2_performance.json", payload["performance"])


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

