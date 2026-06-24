from __future__ import annotations

import json
import sys
import time
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[2]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.catalogs.name_char_catalog_builder import ensure_name_char_catalog
from app.catalogs.semantic_catalog_audit import SemanticCatalogAudit
from app.core.config import PROJECT_ROOT, REPORTS_DIR
from app.engines.semantic_composition_validator import SemanticCompositionValidator
from app.orchestration.naming_alpha_orchestrator import NamingAlphaOrchestrator


SAMPLE_PAYLOADS = [
    ("default_male", {"surname": "林", "gender": "male", "birth_date": "2025-03-01", "birth_time": "08:30", "birth_location": "广东省汕头市", "region": "teochew", "style_preferences": ["书卷清雅", "君子品格"], "generation_seed": 20260622}),
    ("gentle_female", {"surname": "陈", "gender": "female", "birth_date": "2025-03-01", "birth_time": "08:30", "birth_location": "广东省汕头市", "region": "teochew", "style_preferences": ["温润知性", "民国书卷气"], "generation_seed": 20260622}),
    ("landscape_male", {"surname": "黄", "gender": "male", "birth_date": "2025-03-01", "birth_time": "08:30", "birth_location": "广东省汕头市", "region": "teochew", "style_preferences": ["大气开阔", "山水自然"], "generation_seed": 20260622}),
]


def write_reports() -> dict:
    started = time.perf_counter()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    catalog = ensure_name_char_catalog(force=True)
    audit_payload = SemanticCatalogAudit(REPORTS_DIR).run()
    hardcoded = hardcoded_dependency_audit()
    generation = generation_report()
    diversity = diversity_report(generation["cases"])
    manual = manual_review_report(catalog)
    performance = {
        **audit_payload["performance"],
        "end_to_end_report_seconds": round(time.perf_counter() - started, 4),
        "sample_case_count": len(generation["cases"]),
    }
    outputs = {
        "milestone_3_2_hardcoded_dependency_audit.json": hardcoded,
        "milestone_3_2_generation_before_after.json": generation,
        "milestone_3_2_diversity_matrix.json": diversity,
        "milestone_3_2_manual_review.json": manual,
        "milestone_3_2_performance.json": performance,
    }
    for filename, payload in outputs.items():
        _write_json(REPORTS_DIR / filename, payload)
    summary = summary_markdown(catalog, hardcoded, generation, diversity, performance)
    (REPORTS_DIR / "milestone_3_2_summary.md").write_text(summary, encoding="utf-8")
    return {
        "catalog_statistics": catalog["statistics"],
        "hardcoded": hardcoded,
        "generation": generation,
        "diversity": diversity,
        "performance": performance,
    }


def hardcoded_dependency_audit() -> dict:
    targets = {
        "NAME_FRIENDLY_CHARS": "must_not_be_runtime_source",
        "CHAR_INFO": "must_not_be_runtime_source",
    }
    findings = []
    for path in (PROJECT_ROOT / "02_src" / "backend" / "app" / "engines").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for token, rule in targets.items():
            if token in text:
                findings.append({"file": str(path), "token": token, "rule": rule})
    return {
        "status": "PASS" if not findings else "FAIL",
        "findings": findings,
        "allowed_rule_tables": [
            "template name filters",
            "negative semantic hints",
            "semantic category compatibility matrix",
            "structure and archetype definitions",
        ],
    }


def generation_report() -> dict:
    orchestrator = NamingAlphaOrchestrator()
    cases = {}
    for case_id, payload in SAMPLE_PAYLOADS:
        result = orchestrator.run(payload)
        cases[case_id] = {
            "input": payload,
            "result_status": result.get("result_status"),
            "char_pool_counts": result.get("char_pool_counts"),
            "generated_candidates_count": result.get("generated_candidates_count"),
            "passed_candidates_count": result.get("passed_candidates_count"),
            "qualified_count": result.get("qualified_count"),
            "top3": [item["given_name"] for item in result.get("top3", [])],
            "top20": [item["given_name"] for item in result.get("top20", [])],
            "path_distribution": path_distribution(result.get("top20", [])),
            "filter_reasons": result.get("filter_reasons", {}),
        }
    return {
        "before": {
            "legacy_positive_source": "NAME_FRIENDLY_CHARS",
            "legacy_unique_count": 113,
        },
        "after": {
            "positive_source": "name_char_catalog.v1.json",
            "catalog_total": ensure_name_char_catalog()["statistics"]["total_records"],
            "core_extended_count": ensure_name_char_catalog()["statistics"]["core_extended_count"],
        },
        "cases": cases,
    }


def diversity_report(cases: dict) -> dict:
    top3_names = [name for case in cases.values() for name in case["top3"]]
    top20_names = [name for case in cases.values() for name in case["top20"]]
    return {
        "case_count": len(cases),
        "top3_slot_count": len(top3_names),
        "top3_unique_given_name_count": len(set(top3_names)),
        "top20_unique_given_name_count": len(set(top20_names)),
        "all_cases_have_top3": all(len(case["top3"]) == 3 for case in cases.values()),
        "path_distribution": {case_id: case["path_distribution"] for case_id, case in cases.items()},
    }


def manual_review_report(catalog: dict) -> dict:
    validator = SemanticCompositionValidator()
    records = catalog["records_by_char"]
    sample_chars = ["知", "微", "仁", "贤", "诗", "楚", "乂", "罪", "山"]
    return {
        "sample_chars": {
            char: {
                "nameability_level": records[char]["nameability_level"],
                "nameability_score": records[char]["nameability_score"],
                "semantic_categories": records[char]["semantic_categories"],
                "risk_codes": records[char]["risk_codes"],
            }
            for char in sample_chars
            if char in records
        },
        "sample_compositions": {
            name: validator.validate(name)
            for name in ["知微", "仁贤", "诗楚", "峰山"]
        },
    }


def path_distribution(candidates: list[dict]) -> dict:
    counts: dict[str, int] = {}
    for item in candidates:
        mode = item.get("generation_mode") or "UNKNOWN"
        counts[mode] = counts.get(mode, 0) + 1
    total = len(candidates)
    return {
        "total": total,
        "counts": counts,
        "ratios": {key: round(value / total, 4) for key, value in counts.items()} if total else {},
    }


def summary_markdown(catalog: dict, hardcoded: dict, generation: dict, diversity: dict, performance: dict) -> str:
    stats = catalog["statistics"]
    lines = [
        "# Milestone 3.2 Summary",
        "",
        f"- Catalog records: {stats['total_records']}",
        f"- CORE+EXTENDED: {stats['core_extended_count']}",
        f"- Rejected: {stats['rejected_count']}",
        f"- Hardcoded dependency audit: {hardcoded['status']}",
        f"- All sample cases have Top3: {diversity['all_cases_have_top3']}",
        f"- Report runtime seconds: {performance['end_to_end_report_seconds']}",
        "",
        "## Sample Top3",
    ]
    for case_id, case in generation["cases"].items():
        lines.append(f"- {case_id}: {' / '.join(case['top3'])}")
    return "\n".join(lines) + "\n"


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    result = write_reports()
    print(json.dumps(result["catalog_statistics"], ensure_ascii=False, indent=2))
    return 0 if result["hardcoded"]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
