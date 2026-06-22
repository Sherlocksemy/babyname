from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict
from pathlib import Path
from typing import Any

from app.core.config import KNOWLEDGE_BASE_DIR, REPORTS_DIR, ensure_runtime_dirs
from app.core.dataset_registry import CULTURE_DATASETS, DATASET_SPECS, PLANNED_LAYER_DIRS
from app.core.knowledge_loader import KnowledgeLoadError, KnowledgeLoader
from app.schemas.knowledge import DatasetAudit, LoadedDataset


HANZI_RE = re.compile(r"[\u4e00-\u9fff]")


class KnowledgeAudit:
    def __init__(self, knowledge_base_dir: str | Path = KNOWLEDGE_BASE_DIR) -> None:
        self.knowledge_base_dir = Path(knowledge_base_dir)
        self.loader = KnowledgeLoader(self.knowledge_base_dir)

    def audit(self) -> dict[str, Any]:
        datasets: dict[str, DatasetAudit] = {}
        loaded: dict[str, LoadedDataset] = {}

        for spec in DATASET_SPECS:
            path = spec.resolve(self.knowledge_base_dir)
            item = DatasetAudit(name=spec.name, path=str(path), exists=path.exists())
            if not path.exists():
                item.status = "error" if spec.required else "warning"
                target = item.errors if spec.required else item.warnings
                target.append("dataset file is missing")
                datasets[spec.name] = item
                continue

            try:
                dataset = self.loader.load_dataset(spec)
                if dataset is None:
                    item.status = "warning"
                    item.warnings.append("optional dataset not loaded")
                else:
                    loaded[spec.name] = dataset
                    self._audit_loaded_dataset(item, dataset)
            except KnowledgeLoadError as exc:
                item.status = "error"
                item.parse_failures = 1
                item.errors.append(str(exc))
            datasets[spec.name] = item

        checks = self._run_cross_checks(loaded)
        statuses = [item.status for item in datasets.values()]
        if any(status == "error" for status in statuses) or any(check["status"] == "error" for check in checks):
            overall = "error"
        elif any(status == "warning" for status in statuses) or any(check["status"] == "warning" for check in checks):
            overall = "warning"
        else:
            overall = "ok"

        return {
            "overall_status": overall,
            "datasets": {name: asdict(item) for name, item in datasets.items()},
            "checks": checks,
        }

    def write_reports(self, report: dict[str, Any], output_dir: str | Path = REPORTS_DIR) -> tuple[Path, Path]:
        ensure_runtime_dirs()
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)
        json_path = output / "knowledge_audit.json"
        md_path = output / "knowledge_audit.md"
        json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        md_path.write_text(self._to_markdown(report), encoding="utf-8")
        return json_path, md_path

    def _audit_loaded_dataset(self, item: DatasetAudit, dataset: LoadedDataset) -> None:
        data = dataset.data
        rows = self._rows_for_audit(data)
        item.row_count = dataset.row_count
        item.fields = self._fields_for_audit(data, rows)
        item.null_counts = {field: 0 for field in item.fields}
        for row in rows:
            for field in item.fields:
                value = row.get(field)
                if value is None or value == "" or value == [] or value == {}:
                    item.null_counts[field] += 1
        item.duplicate_primary_keys = self._duplicate_primary_keys(dataset, rows)
        item.warnings.extend(dataset.warnings)
        missing_required = [field for field in dataset.spec.required_fields if field not in item.fields]
        for field in missing_required:
            item.errors.append(f"required field missing: {field}")
        if item.errors:
            item.status = "error"
        elif item.warnings:
            item.status = "warning"
        else:
            item.status = "ok"

    @staticmethod
    def _rows_for_audit(data: Any) -> list[dict[str, Any]]:
        if isinstance(data, list):
            return [row for row in data if isinstance(row, dict)]
        if isinstance(data, dict):
            rows = []
            for key, value in data.items():
                if isinstance(value, dict):
                    row = {"char": key, **value}
                elif isinstance(value, list):
                    row = {"char": key, "items": value}
                else:
                    row = {"key": key, "value": value}
                rows.append(row)
            return rows
        return []

    @staticmethod
    def _fields_for_audit(data: Any, rows: list[dict[str, Any]]) -> list[str]:
        fields: set[str] = set()
        if isinstance(data, dict):
            fields.update(data.keys())
            for value in list(data.values())[:200]:
                if isinstance(value, dict):
                    fields.update(value.keys())
                elif isinstance(value, list):
                    for nested in value[:20]:
                        if isinstance(nested, dict):
                            fields.update(nested.keys())
        for row in rows[:200]:
            fields.update(row.keys())
        return sorted(fields)

    @staticmethod
    def _duplicate_primary_keys(dataset: LoadedDataset, rows: list[dict[str, Any]]) -> int:
        pk = dataset.spec.primary_key
        if not pk:
            return 0
        if isinstance(dataset.data, dict) and pk == "char":
            return 0
        values = [row.get(pk) for row in rows if row.get(pk) not in (None, "")]
        counts = Counter(values)
        return sum(count - 1 for count in counts.values() if count > 1)

    def _run_cross_checks(self, loaded: dict[str, LoadedDataset]) -> list[dict[str, Any]]:
        checks = [
            self._check_character_joinability(loaded),
            self._check_teochew_variants(loaded),
            self._check_culture_schema_and_noise(loaded),
            self._check_popularity_blacklist(loaded),
            self._check_bazi_rules(loaded),
            self._check_planned_layers(),
        ]
        return checks

    @staticmethod
    def _check_character_joinability(loaded: dict[str, LoadedDataset]) -> dict[str, Any]:
        required = ("compliance_hanzi", "char_semantic", "mandarin_pinyin", "kangxi_strokes")
        missing = [name for name in required if name not in loaded]
        if missing:
            return {"name": "character_joinability", "status": "error", "errors": [f"missing loaded dataset: {name}" for name in missing]}
        whitelist = {row["char"] for row in loaded["compliance_hanzi"].data if row.get("char")}
        result = {"name": "character_joinability", "status": "ok", "warnings": [], "errors": [], "details": {}}
        for name in ("char_semantic", "mandarin_pinyin", "kangxi_strokes"):
            keys = set(loaded[name].data.keys())
            missing_chars = sorted(whitelist - keys)
            result["details"][name] = {"missing_from_whitelist": len(missing_chars), "samples": missing_chars[:10]}
            if missing_chars:
                result["status"] = "error"
                result["errors"].append(f"{name} missing {len(missing_chars)} whitelist chars")
        result["details"]["sample_char_zhi"] = {
            "in_compliance": "知" in whitelist,
            "in_semantic": "知" in loaded["char_semantic"].data,
            "in_mandarin": "知" in loaded["mandarin_pinyin"].data,
            "in_kangxi": "知" in loaded["kangxi_strokes"].data,
        }
        return result

    @staticmethod
    def _truthy(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in {"true", "1", "yes", "y"}

    def _check_teochew_variants(self, loaded: dict[str, LoadedDataset]) -> dict[str, Any]:
        if "teochew_pronunciation" not in loaded:
            return {"name": "teochew_variants", "status": "error", "errors": ["teochew dataset not loaded"]}
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in loaded["teochew_pronunciation"].data:
            if row.get("char"):
                grouped[row["char"]].append(row)
        multi_accent = sum(1 for rows in grouped.values() if len({row.get("accent") for row in rows}) > 1)
        multi_reading = sum(1 for rows in grouped.values() if len({(row.get("pinyin_teochew"), row.get("tone")) for row in rows}) > 1)
        literary = sum(1 for rows in grouped.values() if any(self._truthy(row.get("is_literary")) for row in rows))
        colloquial = sum(1 for rows in grouped.values() if any(self._truthy(row.get("is_colloquial")) for row in rows))
        warnings = []
        status = "ok"
        if multi_accent == 0 or multi_reading == 0:
            status = "warning"
            warnings.append("teochew data does not expose multi-accent or multi-reading variants")
        if literary == 0 or colloquial == 0:
            status = "warning"
            warnings.append("teochew literary/colloquial flags are not populated")
        return {
            "name": "teochew_variants",
            "status": status,
            "warnings": warnings,
            "details": {
                "unique_chars": len(grouped),
                "chars_with_multiple_accents": multi_accent,
                "chars_with_multiple_readings": multi_reading,
                "chars_with_literary": literary,
                "chars_with_colloquial": colloquial,
            },
        }

    def _check_culture_schema_and_noise(self, loaded: dict[str, LoadedDataset]) -> dict[str, Any]:
        required = {"id", "title", "author", "dynasty", "chapter", "content", "translation", "keywords", "name_candidates"}
        whitelist = set()
        if "compliance_hanzi" in loaded:
            whitelist = {row["char"] for row in loaded["compliance_hanzi"].data if row.get("char")}
        details: dict[str, Any] = {}
        warnings: list[str] = []
        errors: list[str] = []
        for name in CULTURE_DATASETS:
            if name not in loaded:
                errors.append(f"{name} not loaded")
                continue
            records = loaded[name].data
            missing_fields = 0
            noisy_candidates = []
            for record in records:
                if not required.issubset(record.keys()):
                    missing_fields += 1
                for candidate in record.get("name_candidates") or []:
                    if len(candidate) != 2 or (whitelist and any(char not in whitelist for char in candidate)):
                        noisy_candidates.append(candidate)
            if missing_fields:
                errors.append(f"{name} has {missing_fields} records with non-unified fields")
            if noisy_candidates:
                warnings.append(f"{name} has {len(noisy_candidates)} noisy name_candidates")
            details[name] = {
                "records": len(records),
                "records_with_missing_fields": missing_fields,
                "noisy_name_candidates": len(noisy_candidates),
                "noisy_samples": noisy_candidates[:10],
            }
        status = "error" if errors else "warning" if warnings else "ok"
        return {"name": "culture_schema_and_name_candidates", "status": status, "warnings": warnings, "errors": errors, "details": details}

    @staticmethod
    def _check_popularity_blacklist(loaded: dict[str, LoadedDataset]) -> dict[str, Any]:
        if "top_names_blacklist" not in loaded:
            return {"name": "popularity_blacklist", "status": "error", "errors": ["top_names_blacklist not loaded"]}
        rows = loaded["top_names_blacklist"].data
        warnings = []
        if not rows:
            return {"name": "popularity_blacklist", "status": "error", "errors": ["top_names_blacklist is empty"]}
        if any(not row.get("name") for row in rows):
            warnings.append("blacklist contains empty name values")
        return {
            "name": "popularity_blacklist",
            "status": "warning" if warnings else "ok",
            "warnings": warnings,
            "details": {"records": len(rows), "sample": rows[:3]},
        }

    @staticmethod
    def _check_bazi_rules(loaded: dict[str, LoadedDataset]) -> dict[str, Any]:
        if "bazi_rules" not in loaded:
            return {"name": "bazi_rules_operability", "status": "error", "errors": ["bazi_rules not loaded"]}
        data = loaded["bazi_rules"].data
        required_keys = {"ten_gods", "patterns", "element_rules", "ushen_rules"}
        present = set(data.keys()) if isinstance(data, dict) else set()
        warnings = []
        errors = []
        missing = sorted(required_keys - present)
        if missing:
            errors.append(f"missing rule sections: {missing}")
        concrete_keys = {"heavenly_stems", "earthly_branches", "calendar_rules", "stem_branch_relations"}
        if not (present & concrete_keys):
            warnings.append("bazi_rules is mainly rule description; concrete calendar/stem-branch calculation tables are not present")
        return {
            "name": "bazi_rules_operability",
            "status": "error" if errors else "warning" if warnings else "ok",
            "warnings": warnings,
            "errors": errors,
            "details": {"top_level_keys": sorted(present)},
        }

    def _check_planned_layers(self) -> dict[str, Any]:
        missing = [name for name in PLANNED_LAYER_DIRS if not (self.knowledge_base_dir / name).exists()]
        return {
            "name": "planned_layers",
            "status": "warning" if missing else "ok",
            "warnings": [f"planned layer directory is missing: {name}" for name in missing],
            "details": {"missing_layer_dirs": missing},
        }

    @staticmethod
    def _to_markdown(report: dict[str, Any]) -> str:
        lines = [
            "# Knowledge Audit",
            "",
            f"Overall status: `{report['overall_status']}`",
            "",
            "## Datasets",
            "",
            "| Dataset | Exists | Rows | Status | Warnings | Errors |",
            "| --- | --- | ---: | --- | ---: | ---: |",
        ]
        for item in report["datasets"].values():
            lines.append(
                f"| {item['name']} | {item['exists']} | {item['row_count']} | {item['status']} | "
                f"{len(item['warnings'])} | {len(item['errors'])} |"
            )
        lines.extend(["", "## Checks", ""])
        for check in report["checks"]:
            lines.append(f"### {check['name']}")
            lines.append(f"- status: `{check['status']}`")
            for warning in check.get("warnings", []):
                lines.append(f"- warning: {warning}")
            for error in check.get("errors", []):
                lines.append(f"- error: {error}")
            lines.append("")
        return "\n".join(lines)
