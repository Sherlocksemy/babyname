from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from backend.app.core.config import KNOWLEDGE_ROOT, REPORTS_DIR


@dataclass(frozen=True)
class KnowledgeFile:
    key: str
    path: Path
    kind: str
    required_fields: tuple[str, ...] = ()


class KnowledgeLoader:
    """Read-only loader for the curated local knowledge base."""

    FILES = (
        KnowledgeFile("compliance", Path("01_compliance_layer/tongyong_guifan_hanzi.csv"), "csv", ("char", "level", "strokes_modern", "radical", "unicode")),
        KnowledgeFile("char_base", Path("02_char_attribute_layer/char_base_info.csv"), "csv", ("char", "pinyin_main", "strokes_modern", "radical", "structure", "wubi")),
        KnowledgeFile("char_semantic", Path("02_char_attribute_layer/char_semantic.json"), "json"),
        KnowledgeFile("kangxi", Path("02_char_attribute_layer/kangxi_strokes.json"), "json"),
        KnowledgeFile("mandarin", Path("03_pronunciation_layer/mandarin_pinyin.json"), "json"),
        KnowledgeFile("teochew", Path("03_pronunciation_layer/teochew_pronunciation.csv"), "csv", ("char", "pinyin_teochew", "tone", "accent", "is_colloquial", "is_literary")),
        KnowledgeFile("homophone_blacklist", Path("03_pronunciation_layer/homophone_blacklist.csv"), "csv", ("char", "homophone_char", "bad_meaning", "language_type")),
        KnowledgeFile("shijing", Path("04_culture_origin_layer/shijing/shijing_full.json"), "json"),
        KnowledgeFile("chuci", Path("04_culture_origin_layer/chuci/chuci_full.json"), "json"),
        KnowledgeFile("tang_poetry", Path("04_culture_origin_layer/tang_poetry/tang_poetry.json"), "json"),
        KnowledgeFile("song_ci", Path("04_culture_origin_layer/song_ci/song_ci.json"), "json"),
        KnowledgeFile("sishuwujing", Path("04_culture_origin_layer/sishuwujing/sishuwujing.json"), "json"),
        KnowledgeFile("char_frequency", Path("05_name_popularity_layer/char_frequency.csv"), "csv", ("char", "gender_tendency", "frequency_rank", "heat_level", "era_tag")),
        KnowledgeFile("top_names_blacklist", Path("05_name_popularity_layer/top_names_blacklist.csv"), "csv", ("name", "gender", "estimated_count", "heat_level")),
        KnowledgeFile("bazi_rules", Path("06_numerology_layer/bazi_rules.json"), "json"),
        KnowledgeFile("wuge_rules", Path("06_numerology_layer/wuge_rules.json"), "json"),
        KnowledgeFile("zodiac_taboo", Path("06_numerology_layer/zodiac_taboo.csv"), "csv", ("zodiac", "good_radicals", "bad_radicals", "good_meaning", "bad_meaning", "lucky_elements")),
    )

    CULTURE_KEYS = ("shijing", "chuci", "tang_poetry", "song_ci", "sishuwujing")
    CULTURE_FIELDS = ("id", "title", "author", "dynasty", "chapter", "content", "translation", "keywords", "name_candidates")

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or KNOWLEDGE_ROOT
        self._bundle: dict[str, Any] | None = None

    def load(self, force: bool = False) -> dict[str, Any]:
        if self._bundle is not None and not force:
            return self._bundle
        bundle: dict[str, Any] = {}
        for spec in self.FILES:
            bundle[spec.key] = self._read_file(spec)
        self._bundle = bundle
        return bundle

    def _read_file(self, spec: KnowledgeFile) -> Any:
        path = self.root / spec.path
        if spec.kind == "json":
            return json.loads(path.read_text(encoding="utf-8-sig"))
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))

    def audit(self, write_report: bool = True) -> dict[str, Any]:
        report: dict[str, Any] = {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "source_root": str(self.root),
            "files": {},
            "row_counts": {},
            "missing_files": [],
            "missing_fields": {},
            "duplicate_counts": {},
            "warnings": [],
            "status": "ok",
        }
        for spec in self.FILES:
            path = self.root / spec.path
            key = spec.key
            report["files"][key] = str(path)
            if not path.exists():
                report["missing_files"].append(str(spec.path))
                continue
            try:
                data = self._read_file(spec)
                report["row_counts"][key] = len(data)
                if spec.kind == "csv":
                    headers = set(data[0].keys()) if data else set()
                    missing = sorted(set(spec.required_fields) - headers)
                    if missing:
                        report["missing_fields"][key] = missing
                    if data and "char" in headers:
                        chars = [row.get("char") for row in data if row.get("char")]
                        report["duplicate_counts"][key] = len(chars) - len(set(chars))
                if key in self.CULTURE_KEYS:
                    self._audit_culture(key, data, report)
            except Exception as exc:
                report["warnings"].append(f"{key} read failed: {exc}")
        if report["missing_files"]:
            report["status"] = "error"
        elif report["missing_fields"] or report["warnings"]:
            report["status"] = "warning"
        if write_report:
            REPORTS_DIR.mkdir(parents=True, exist_ok=True)
            (REPORTS_DIR / "knowledge_audit_report.json").write_text(
                json.dumps(report, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        return report

    def _audit_culture(self, key: str, items: list[dict[str, Any]], report: dict[str, Any]) -> None:
        for field in self.CULTURE_FIELDS:
            if field == "translation":
                continue
            missing = sum(1 for item in items if item.get(field) in (None, "", []))
            if missing:
                report["warnings"].append(f"{key}.{field} missing: {missing}")

