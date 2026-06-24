from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.catalogs.character_culture_linker import CharacterCultureLinker
from app.catalogs.nameability_classifier import NameabilityClassifier
from app.catalogs.semantic_role_mapper import (
    ROLE_BY_CATEGORY,
    SEMANTIC_CATEGORIES,
    SEMANTIC_ROLE_VERSION,
    SemanticRoleMapper,
)
from app.core.config import RUNTIME_DIR
from app.core.knowledge_loader import KnowledgeLoader
from app.indexes.character_index import CharacterIndex
from app.indexes.culture_index import CultureIndex
from app.indexes.popularity_index import PopularityIndex
from app.indexes.pronunciation_index import PronunciationIndex


CATALOG_VERSION = "name_char_catalog.v1"
DERIVED_DIR = RUNTIME_DIR / "derived"
CATALOG_PATH = DERIVED_DIR / "name_char_catalog.v1.json"
SEMANTIC_ROLE_PATH = DERIVED_DIR / "semantic_role_catalog.v1.json"
CULTURE_LINK_PATH = DERIVED_DIR / "character_culture_links.v1.json"
REJECTED_PATH = DERIVED_DIR / "rejected_name_chars.v1.json"
METADATA_PATH = DERIVED_DIR / "semantic_catalog_metadata.v1.json"

_CATALOG_CACHE: dict[str, Any] | None = None


class NameCharCatalogBuilder:
    def __init__(self, loader: KnowledgeLoader | None = None) -> None:
        self.loader = loader or KnowledgeLoader()

    def build(self) -> dict:
        datasets = self.loader.load_all()
        character_index = CharacterIndex(self.loader, datasets)
        pronunciation_index = PronunciationIndex(self.loader, datasets)
        popularity_index = PopularityIndex(self.loader, datasets)
        culture_index = CultureIndex(self.loader, datasets)
        culture_linker = CharacterCultureLinker(culture_index)
        role_mapper = SemanticRoleMapper()
        classifier = NameabilityClassifier()

        records: list[dict] = []
        culture_links_by_char: dict[str, list[dict]] = {}
        rejected: list[dict] = []

        compliance_rows = sorted(
            character_index.compliance.values(),
            key=lambda row: (
                int(row.get("level") or 9),
                int(row.get("strokes_modern") or 999),
                str(row.get("unicode") or ""),
            ),
        )
        for row in compliance_rows:
            char = row["char"]
            profile = character_index.get(char)
            links = culture_linker.links_for_char(char)
            culture_links_by_char[char] = links
            semantic_mapping = role_mapper.map_character(profile, links)
            classification = classifier.classify(
                profile,
                semantic_mapping.categories,
                links,
                pronunciation_index.risks(char),
            )
            record = self._record(
                profile,
                semantic_mapping,
                classification,
                links,
                popularity_index.get_char(char),
            )
            records.append(record)
            if record["nameability_level"] == "REJECTED":
                rejected.append(
                    {
                        "char": char,
                        "risk_codes": record["risk_codes"],
                        "rejection_reasons": record["rejection_reasons"],
                        "source": "knowledge_derived_catalog",
                    }
                )

        statistics = self._statistics(records)
        return {
            "version": CATALOG_VERSION,
            "built_at": datetime.now(timezone.utc).isoformat(),
            "source": "01_knowledge_base",
            "records": records,
            "statistics": statistics,
            "culture_links": culture_links_by_char,
            "rejected": rejected,
        }

    def write(self, force: bool = True) -> dict:
        DERIVED_DIR.mkdir(parents=True, exist_ok=True)
        if not force and CATALOG_PATH.exists():
            return load_name_char_catalog()
        payload = self.build()
        catalog_payload = {key: payload[key] for key in ("version", "built_at", "source", "records", "statistics")}
        _write_json(CATALOG_PATH, catalog_payload)
        _write_json(
            SEMANTIC_ROLE_PATH,
            {
                "version": SEMANTIC_ROLE_VERSION,
                "catalog_version": CATALOG_VERSION,
                "categories": SEMANTIC_CATEGORIES,
                "roles_by_category": ROLE_BY_CATEGORY,
            },
        )
        _write_json(CULTURE_LINK_PATH, {"version": CATALOG_VERSION, "links": payload["culture_links"]})
        _write_json(REJECTED_PATH, {"version": CATALOG_VERSION, "records": payload["rejected"]})
        _write_json(
            METADATA_PATH,
            {
                "version": CATALOG_VERSION,
                "built_at": payload["built_at"],
                "source": "01_knowledge_base",
                "statistics": payload["statistics"],
                "files": {
                    "catalog": str(CATALOG_PATH),
                    "semantic_roles": str(SEMANTIC_ROLE_PATH),
                    "culture_links": str(CULTURE_LINK_PATH),
                    "rejected": str(REJECTED_PATH),
                },
            },
        )
        global _CATALOG_CACHE
        _CATALOG_CACHE = None
        return load_name_char_catalog()

    @staticmethod
    def _record(
        profile: dict,
        semantic_mapping,
        classification: dict,
        culture_links: list[dict],
        popularity: dict | None,
    ) -> dict:
        char = profile["char"]
        base = profile.get("base") or {}
        compliance = profile.get("compliance") or {}
        semantic = profile.get("semantic") or {}
        kangxi = profile.get("kangxi") or {}
        mandarin = profile.get("mandarin") or []
        return {
            "char": char,
            "unicode": compliance.get("unicode") or f"U+{ord(char):04X}",
            "compliance_level": int(compliance.get("level") or 0),
            "nameability_level": classification["level"],
            "nameability_score": classification["score"],
            "semantic_categories": semantic_mapping.categories,
            "semantic_roles": semantic_mapping.roles,
            "semantic_keywords": semantic_mapping.keywords,
            "definition": semantic.get("definition") or "",
            "ancient_meaning": semantic.get("ancient_meaning") or "",
            "naming_meaning": NameCharCatalogBuilder._naming_meaning(semantic.get("definition") or "", semantic_mapping.roles),
            "positive_level": int(semantic.get("positive_level") or 0),
            "common_level": int(semantic.get("common_level") or 0),
            "strokes_modern": int(base.get("strokes_modern") or compliance.get("strokes_modern") or 0),
            "kangxi_strokes": int(kangxi.get("kangxi_strokes") or 0),
            "radical": base.get("radical") or kangxi.get("kangxi_radical") or "",
            "kangxi_radical": kangxi.get("kangxi_radical") or "",
            "element": kangxi.get("element") or "",
            "components": list(kangxi.get("components") or []),
            "mandarin": mandarin,
            "teochew_count": len(profile.get("teochew") or []),
            "culture_evidence_count": len(culture_links),
            "culture_link_ids": [f"{item['source_type']}:{item['source_record_id']}" for item in culture_links],
            "popularity": popularity or {},
            "risk_codes": classification["risk_codes"],
            "rejection_reasons": classification["rejection_reasons"],
            "reason_codes": classification["reason_codes"] + semantic_mapping.basis,
            "source_fields": {
                "compliance": "01_compliance_layer/tongyong_guifan_hanzi.csv",
                "base": "02_char_attribute_layer/char_base_info.csv",
                "semantic": "02_char_attribute_layer/char_semantic.json",
                "kangxi": "02_char_attribute_layer/kangxi_strokes.json",
                "pronunciation": "03_pronunciation_layer/mandarin_pinyin.json",
                "culture": "04_culture_origin_layer/*",
            },
        }

    @staticmethod
    def _naming_meaning(definition: str, roles: list[str]) -> str:
        head = str(definition or "").strip()
        for marker in ("。", "；", ";", "\n", "--"):
            if marker in head:
                head = head.split(marker, 1)[0]
        head = head[:48].strip()
        role_text = "、".join(list(dict.fromkeys(roles))[:2])
        if head and role_text:
            return f"{head}；命名语义侧重{role_text}"
        return head or role_text

    @staticmethod
    def _statistics(records: list[dict]) -> dict:
        levels = Counter(record["nameability_level"] for record in records)
        categories = Counter(category for record in records for category in record["semantic_categories"])
        with_culture = sum(1 for record in records if record["culture_evidence_count"])
        return {
            "total_records": len(records),
            "nameability_levels": dict(levels),
            "core_extended_count": levels.get("CORE", 0) + levels.get("EXTENDED", 0),
            "rejected_count": levels.get("REJECTED", 0),
            "with_culture_evidence": with_culture,
            "semantic_categories": dict(categories),
        }


def ensure_name_char_catalog(force: bool = False) -> dict:
    if force or not CATALOG_PATH.exists() or not CULTURE_LINK_PATH.exists():
        return NameCharCatalogBuilder().write(force=True)
    return load_name_char_catalog()


def load_name_char_catalog() -> dict:
    global _CATALOG_CACHE
    if _CATALOG_CACHE is not None:
        return _CATALOG_CACHE
    if not CATALOG_PATH.exists():
        return ensure_name_char_catalog(force=True)
    catalog = _read_json(CATALOG_PATH)
    links = _read_json(CULTURE_LINK_PATH) if CULTURE_LINK_PATH.exists() else {"links": {}}
    records = catalog.get("records") or []
    _CATALOG_CACHE = {
        "version": catalog.get("version") or CATALOG_VERSION,
        "records": records,
        "records_by_char": {record["char"]: record for record in records},
        "culture_links": links.get("links") or {},
        "statistics": catalog.get("statistics") or {},
    }
    return _CATALOG_CACHE


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))
