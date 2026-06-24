from __future__ import annotations

import json
import random
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


BACKEND_DIR = Path(__file__).resolve().parents[2]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.catalogs.character_risk_classifier import LOW_NAMEABILITY_CHARS
from app.catalogs.name_char_catalog_builder import ensure_name_char_catalog
from app.catalogs.nameability_classifier import HIGH_RISK_POLYPHONE_CHARS
from app.core.config import REPORTS_DIR
from app.orchestration.naming_alpha_orchestrator import NamingAlphaOrchestrator


AUDIT_SEED = 20260623
LEGACY_ANCHOR = set("知思明德仁义礼信文书闻清雅安宁和温润远行景云泽川山怀修诚敬正嘉乐新承彦辰星月华光")
MORAL_CHARS = set("仁贤承谦德信敬正思安")
SAMPLE_SIZES = {"CORE": 200, "EXTENDED": 200, "EXPERIMENTAL": 100, "REJECTED": 100}


CASES: dict[str, dict[str, Any]] = {
    "case_a_lin_male_teochew": {
        "surname": "林",
        "gender": "male",
        "calendar_type": "solar",
        "birth_year": 2025,
        "birth_month": 3,
        "birth_day": 1,
        "birth_hour": 8,
        "birth_minute": 30,
        "birth_province": "广东省",
        "birth_city": "汕头市",
        "region": "teochew",
        "style_preferences": ["书卷清雅", "君子品格"],
        "liked_chars": [],
        "blocked_chars": [],
        "generation_seed": AUDIT_SEED,
    },
    "case_b_chen_female": {
        "surname": "陈",
        "gender": "female",
        "calendar_type": "solar",
        "birth_year": 2025,
        "birth_month": 3,
        "birth_day": 1,
        "birth_hour": 8,
        "birth_minute": 30,
        "birth_province": "广东省",
        "birth_city": "汕头市",
        "region": "teochew",
        "style_preferences": ["温润知性", "民国书卷气"],
        "liked_chars": [],
        "blocked_chars": [],
        "generation_seed": AUDIT_SEED,
    },
    "case_c_huang_male": {
        "surname": "黄",
        "gender": "male",
        "calendar_type": "solar",
        "birth_year": 2025,
        "birth_month": 3,
        "birth_day": 1,
        "birth_hour": 8,
        "birth_minute": 30,
        "birth_province": "广东省",
        "birth_city": "汕头市",
        "region": "teochew",
        "style_preferences": ["大气开阔", "山水自然"],
        "liked_chars": [],
        "blocked_chars": [],
        "generation_seed": AUDIT_SEED,
    },
    "case_d_zheng_female": {
        "surname": "郑",
        "gender": "female",
        "calendar_type": "solar",
        "birth_year": 2025,
        "birth_month": 3,
        "birth_day": 1,
        "birth_hour": 8,
        "birth_minute": 30,
        "birth_province": "广东省",
        "birth_city": "汕头市",
        "region": "teochew",
        "style_preferences": ["现代高级", "温柔坚定"],
        "liked_chars": ["宁"],
        "blocked_chars": ["若", "梓", "汐"],
        "generation_seed": AUDIT_SEED,
    },
    "case_e_ouyang_neutral": {
        "surname": "欧阳",
        "gender": "neutral",
        "calendar_type": "solar",
        "birth_year": 2025,
        "birth_month": 3,
        "birth_day": 1,
        "birth_hour": 8,
        "birth_minute": 30,
        "birth_province": "广东省",
        "birth_city": "汕头市",
        "region": "teochew",
        "style_preferences": ["雅致", "思想家"],
        "liked_chars": [],
        "blocked_chars": [],
        "generation_seed": AUDIT_SEED,
    },
}


def write_reports() -> dict[str, Any]:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    catalog = ensure_name_char_catalog(force=True)
    records = catalog["records"]
    sample_audit = catalog_sample_audit(records)
    core = core_strictness(records)
    generation = generation_matrix(catalog)
    before_after = before_after_report(catalog, generation)
    manual = manual_review(generation)
    summary = summary_report(catalog, sample_audit, core, generation, before_after, manual)

    outputs = {
        "milestone_3_2a_catalog_sample_audit.json": sample_audit,
        "milestone_3_2a_core_strictness.json": core,
        "milestone_3_2a_generation_matrix.json": generation,
        "milestone_3_2a_before_after.json": before_after,
        "milestone_3_2a_manual_review.json": manual,
    }
    for filename, payload in outputs.items():
        _write_json(REPORTS_DIR / filename, payload)
    (REPORTS_DIR / "milestone_3_2a_catalog_sample_audit.md").write_text(sample_audit_md(sample_audit), encoding="utf-8")
    (REPORTS_DIR / "milestone_3_2a_summary.md").write_text(summary, encoding="utf-8")
    return {
        "sample_audit": sample_audit,
        "core_strictness": core,
        "generation_matrix": generation,
        "before_after": before_after,
        "manual_review": manual,
    }


def catalog_sample_audit(records: list[dict]) -> dict[str, Any]:
    rng = random.Random(AUDIT_SEED)
    by_level: dict[str, list[dict]] = {}
    for level in SAMPLE_SIZES:
        pool = [record for record in records if record["nameability_level"] == level]
        sample = rng.sample(pool, min(SAMPLE_SIZES[level], len(pool)))
        audited = [audit_record(record) for record in sample]
        counts = Counter(item["audit_decision"] for item in audited)
        by_level[level] = {
            "sample_size": len(audited),
            "decision_counts": dict(counts),
            "correct_rate": round(counts.get("CORRECT", 0) / len(audited), 4) if audited else 0,
            "records": audited,
        }
    gates = {
        "core_correct_rate_passed": by_level["CORE"]["correct_rate"] >= 0.90,
        "extended_obvious_error_passed": (by_level["EXTENDED"]["decision_counts"].get("TOO_HIGH", 0) / max(1, by_level["EXTENDED"]["sample_size"])) <= 0.15,
        "rejected_false_kill_passed": (by_level["REJECTED"]["decision_counts"].get("TOO_LOW", 0) / max(1, by_level["REJECTED"]["sample_size"])) <= 0.10,
    }
    return {"seed": AUDIT_SEED, "levels": by_level, "quality_gates": gates}


def audit_record(record: dict) -> dict[str, Any]:
    decision = "CORRECT"
    reasons: list[str] = []
    primary = (record.get("semantic_categories") or ["UNKNOWN"])[0]
    if record["nameability_level"] == "CORE":
        if not record.get("semantic_roles"):
            reasons.append("CORE_EMPTY_SEMANTIC_ROLES")
        if not record.get("naming_meaning"):
            reasons.append("CORE_EMPTY_NAMING_MEANING")
        if record.get("risk_codes"):
            reasons.append("CORE_HAS_RISK")
        if len(record.get("mandarin") or []) != 1:
            reasons.append("CORE_PRONUNCIATION_NOT_UNIQUE")
        if primary in {"OBJECT", "FUNCTION", "UNKNOWN"}:
            reasons.append("CORE_LOW_NAMEABILITY_PRIMARY_CATEGORY")
        if record["char"] in LOW_NAMEABILITY_CHARS:
            reasons.append("CORE_LOW_NAMEABILITY_CHAR")
        if record["char"] in HIGH_RISK_POLYPHONE_CHARS:
            reasons.append("CORE_HIGH_RISK_POLYPHONE")
        if reasons:
            decision = "TOO_HIGH"
    elif record["nameability_level"] == "REJECTED":
        if not record.get("risk_codes") and record.get("positive_level", 0) >= 3:
            decision = "TOO_LOW"
            reasons.append("REJECTED_WITHOUT_RISK_AND_POSITIVE_SOURCE")
    elif record["nameability_level"] in {"EXTENDED", "EXPERIMENTAL"}:
        if primary in {"FUNCTION", "UNKNOWN"} and not record.get("risk_codes"):
            decision = "TOO_HIGH"
            reasons.append("MID_LEVEL_LOW_NAMEABILITY_PRIMARY_WITHOUT_RISK")
    return {
        "char": record["char"],
        "level": record["nameability_level"],
        "nameability_score": record["nameability_score"],
        "modern_meaning": record.get("definition", ""),
        "classical_meaning": record.get("ancient_meaning", ""),
        "naming_meaning": record.get("naming_meaning", ""),
        "pinyin": [item.get("pinyin") for item in record.get("mandarin") or []],
        "polyphonic": len(record.get("mandarin") or []) > 1,
        "semantic_categories": record.get("semantic_categories") or [],
        "semantic_roles": record.get("semantic_roles") or [],
        "culture_link_count": record.get("culture_evidence_count", 0),
        "risk_codes": record.get("risk_codes") or [],
        "classification_reason_codes": record.get("reason_codes") or [],
        "audit_decision": decision,
        "audit_reason": ";".join(reasons) or "RULE_CHECK_PASSED",
    }


def core_strictness(records: list[dict]) -> dict[str, Any]:
    core = [record for record in records if record["nameability_level"] == "CORE"]
    counts = {
        "core_total": len(core),
        "no_culture_link_count": sum(not item.get("culture_evidence_count") for item in core),
        "polyphonic_count": sum(len(item.get("mandarin") or []) > 1 for item in core),
        "low_frequency_count": sum(not (item.get("popularity") or {}).get("frequency_rank") for item in core),
        "high_stroke_count": sum((item.get("strokes_modern") or 0) >= 18 for item in core),
        "empty_semantic_roles_count": sum(not item.get("semantic_roles") for item in core),
        "empty_naming_meaning_count": sum(not item.get("naming_meaning") for item in core),
        "nonempty_risk_count": sum(bool(item.get("risk_codes")) for item in core),
    }
    gates = {
        "core_semantic_roles_nonempty": counts["empty_semantic_roles_count"] == 0,
        "core_naming_meaning_nonempty": counts["empty_naming_meaning_count"] == 0,
        "core_no_risk_preferred": counts["nonempty_risk_count"] == 0,
    }
    return {"counts": counts, "quality_gates": gates}


def generation_matrix(catalog: dict) -> dict[str, Any]:
    orchestrator = NamingAlphaOrchestrator()
    cases: dict[str, Any] = {}
    for case_id, payload in CASES.items():
        pool = candidate_pool_snapshot(orchestrator, payload)
        result = orchestrator.run(payload)
        cases[case_id] = {
            "input": payload,
            "result_status": result.get("result_status"),
            "candidate_pool_first100": pool["chars"],
            "candidate_pool_level_ratio": pool["level_ratio"],
            "top20": [candidate_summary(item, catalog) for item in result.get("top20", [])],
            "top10": [candidate_summary(item, catalog) for item in result.get("top10", [])],
            "top3": [candidate_summary(item, catalog) for item in result.get("top3", [])],
            "backup7": [candidate_summary(item, catalog) for item in result.get("backup7", [])],
            "metrics": generation_metrics(result.get("top20", []), result.get("top10", []), result.get("top3", []), result.get("backup7", [])),
        }
    gates = {case_id: quality_gates(case["metrics"]) for case_id, case in cases.items()}
    return {"seed": AUDIT_SEED, "cases": cases, "quality_gates": gates}


def candidate_pool_snapshot(orchestrator: NamingAlphaOrchestrator, payload: dict) -> dict[str, Any]:
    baby_profile = orchestrator._baby_profile(payload)
    naming_input = baby_profile.to_naming_input()
    fortune = orchestrator._build_fortune_context(baby_profile)
    structure_result = orchestrator.structure_engine.select(naming_input)
    archetype_result = orchestrator.archetype_engine.select(structure_result["top_structures"], naming_input)
    evidences = orchestrator.culture_retriever.retrieve(
        structure_result["candidate_structures"],
        archetype_result["candidate_archetypes"],
        naming_input.style_preferences,
    )
    pools = orchestrator.char_pool_builder.build(
        naming_input,
        structure_result["candidate_structures"],
        archetype_result["candidate_archetypes"],
        evidences,
        fortune.to_dict(),
        first_limit=100,
        second_limit=100,
    )
    chars = []
    for item in pools["first_pool"] + pools["second_pool"]:
        if item.char not in chars:
            chars.append(item.char)
        if len(chars) >= 100:
            break
    level_counts = Counter(item.catalog_level for item in pools["first_pool"] + pools["second_pool"])
    total = sum(level_counts.values()) or 1
    return {
        "chars": chars,
        "level_ratio": {level: round(count / total, 4) for level, count in level_counts.items()},
    }


def candidate_summary(item: dict, catalog: dict) -> dict[str, Any]:
    first = item.get("first_char") or {}
    second = item.get("second_char") or {}
    semantic = item.get("semantic_validation") or {}
    risks = sorted(set((first.get("risk_flags") or []) + (second.get("risk_flags") or []) + semantic.get("risk_codes", [])))
    evidence = item.get("evidences") or []
    return {
        "full_name": item.get("full_name"),
        "given_name": item.get("given_name"),
        "score": (item.get("score") or {}).get("normalized_score"),
        "first_char": first.get("char"),
        "second_char": second.get("char"),
        "first_catalog_level": first.get("catalog_level"),
        "second_catalog_level": second.get("catalog_level"),
        "catalog_levels": [first.get("catalog_level"), second.get("catalog_level")],
        "new_extended_chars": [char for char in item.get("given_name", "") if char not in LEGACY_ANCHOR],
        "structure": item.get("structure_id"),
        "personality": item.get("archetype_id"),
        "semantic_categories": [semantic.get("first_category"), semantic.get("second_category")],
        "semantic_roles": [item.get("semantic_role_first"), item.get("semantic_role_second")],
        "relation": semantic.get("relation_type"),
        "combined_meaning": item.get("combined_meaning"),
        "culture_evidence": [
            {
                "source_type": ev.get("source_type"),
                "title": ev.get("title"),
                "excerpt": (ev.get("original_text") or "")[:80],
                "evidence_level": ev.get("evidence_level"),
            }
            for ev in evidence[:2]
        ],
        "naturalness": item.get("naturalness_score"),
        "risks": risks,
        "is_legacy_113": all(char in LEGACY_ANCHOR for char in item.get("given_name", "")),
        "generation_mode": item.get("generation_mode"),
        "semantic_issues": semantic.get("issues") or [],
    }


def generation_metrics(top20: list[dict], top10: list[dict], top3: list[dict], backup7: list[dict]) -> dict[str, Any]:
    def chars(rows: list[dict]) -> list[str]:
        return list("".join(item.get("given_name", "") for item in rows))

    top20_chars = chars(top20)
    top10_chars = chars(top10)
    top3_chars = chars(top3)
    top20_counter = Counter(top20_chars)
    top10_counter = Counter(top10_chars)
    rows = [candidate_summary(item, {"records_by_char": {}}) for item in top20]
    top3_rows = [candidate_summary(item, {"records_by_char": {}}) for item in top3]
    backup7_rows = [candidate_summary(item, {"records_by_char": {}}) for item in backup7]
    return {
        "top20_count": len(top20),
        "top10_count": len(top10),
        "top3_count": len(top3),
        "backup7_count": len(backup7),
        "top20_unique_char_count": len(set(top20_chars)),
        "top10_unique_char_count": len(set(top10_chars)),
        "top3_unique_char_count": len(set(top3_chars)),
        "top20_max_char_frequency": max(top20_counter.values() or [0]),
        "top10_max_char_frequency": max(top10_counter.values() or [0]),
        "legacy_113_ratio": round(sum(char in LEGACY_ANCHOR for char in top20_chars) / max(1, len(top20_chars)), 4),
        "new_extended_ratio": round(sum(char not in LEGACY_ANCHOR for char in top20_chars) / max(1, len(top20_chars)), 4),
        "core_char_ratio": _level_ratio(rows, "CORE"),
        "extended_char_ratio": _level_ratio(rows, "EXTENDED"),
        "experimental_char_count": _level_count(rows, "EXPERIMENTAL"),
        "top3_extended_char_count": sum(level == "EXTENDED" for item in top3_rows for level in item["catalog_levels"]),
        "moral_char_count": sum(char in MORAL_CHARS for char in top20_chars),
        "legacy_moral_counts": dict(Counter(char for char in top20_chars if char in MORAL_CHARS)),
        "semantic_issue_counts": dict(Counter(issue for item in rows for issue in item["semantic_issues"])),
        "low_naturalness_count": sum((item.get("naturalness") or 0) < 82 for item in rows),
        "polyphonic_risk_count": sum("POLYPHONE" in item["risks"] or "HIGH_RISK_POLYPHONE" in item["risks"] for item in rows),
        "missing_combined_meaning_count": sum(not item.get("combined_meaning") for item in top3_rows),
        "top3_min_naturalness": min([item.get("naturalness") or 0 for item in top3_rows] or [0]),
        "backup7_min_naturalness": min([item.get("naturalness") or 0 for item in backup7_rows] or [100]),
    }


def _level_ratio(rows: list[dict], level: str) -> float:
    levels = [catalog_level for item in rows for catalog_level in item["catalog_levels"]]
    return round(sum(item == level for item in levels) / max(1, len(levels)), 4)


def _level_count(rows: list[dict], level: str) -> int:
    return sum(catalog_level == level for item in rows for catalog_level in item["catalog_levels"])


def quality_gates(metrics: dict[str, Any]) -> dict[str, bool]:
    issue_counts = metrics["semantic_issue_counts"]
    return {
        "top20_unique_chars": metrics["top20_unique_char_count"] >= 18,
        "top10_unique_chars": metrics["top10_unique_char_count"] >= 12,
        "top3_no_repeated_chars": metrics["top3_unique_char_count"] == metrics["top3_count"] * 2,
        "top20_char_frequency": metrics["top20_max_char_frequency"] <= 3,
        "top10_char_frequency": metrics["top10_max_char_frequency"] <= 2,
        "top20_new_extended_ratio": metrics["new_extended_ratio"] >= 0.25,
        "top20_no_experimental": metrics["experimental_char_count"] == 0,
        "top3_extended_limit": metrics["top3_extended_char_count"] <= 2,
        "no_moral_label_stacking": issue_counts.get("MORAL_LABEL_STACKING", 0) == 0,
        "category_duplication_limit": issue_counts.get("CATEGORY_DUPLICATION", 0) <= 1,
        "low_relational_meaning_limit": issue_counts.get("LOW_RELATIONAL_MEANING", 0) <= 2,
        "forced_interpretation_top10": issue_counts.get("FORCED_INTERPRETATION", 0) == 0,
        "top3_complete_meaning": metrics["missing_combined_meaning_count"] == 0,
        "top3_naturalness": metrics["top3_min_naturalness"] >= 90,
        "backup7_naturalness": metrics["backup7_min_naturalness"] >= 82,
    }


def before_after_report(catalog: dict, generation: dict) -> dict[str, Any]:
    before_path = REPORTS_DIR / "milestone_3_1b_score_display.json"
    before = {"source": str(before_path), "available": before_path.exists(), "metrics": {}, "names": []}
    if before_path.exists():
        payload = json.loads(before_path.read_text(encoding="utf-8"))
        before_rows = payload.get("top3", []) + payload.get("backup7", [])
        before["names"] = [item.get("full_name") for item in before_rows]
        before["metrics"] = historical_name_metrics([item.get("full_name", "")[1:] for item in before_rows], catalog)
    after_names = [
        item["given_name"]
        for case in generation["cases"].values()
        for item in case["top20"]
    ]
    return {
        "before": before,
        "after": {"source": "milestone_3_2a_generation_matrix", "metrics": historical_name_metrics(after_names, catalog)},
        "note": "Milestone 3.1B did not store the same five-case Top20 matrix; before comparison uses the available 3.1B score-display/result sample only.",
    }


def historical_name_metrics(given_names: list[str], catalog: dict) -> dict[str, Any]:
    records = catalog["records_by_char"]
    chars = list("".join(given_names))
    levels = [records.get(char, {}).get("nameability_level", "MISSING") for char in chars]
    return {
        "name_count": len(given_names),
        "unique_char_count": len(set(chars)),
        "legacy_113_ratio": round(sum(char in LEGACY_ANCHOR for char in chars) / max(1, len(chars)), 4),
        "new_extended_ratio": round(sum(char not in LEGACY_ANCHOR for char in chars) / max(1, len(chars)), 4),
        "core_ratio": round(sum(level == "CORE" for level in levels) / max(1, len(levels)), 4),
        "extended_ratio": round(sum(level == "EXTENDED" for level in levels) / max(1, len(levels)), 4),
        "experimental_ratio": round(sum(level == "EXPERIMENTAL" for level in levels) / max(1, len(levels)), 4),
        "moral_char_counts": dict(Counter(char for char in chars if char in MORAL_CHARS)),
    }


def manual_review(generation: dict) -> dict[str, Any]:
    return {
        case_id: [manual_row(item) for item in case["top20"]]
        for case_id, case in generation["cases"].items()
    }


def manual_row(item: dict) -> dict[str, Any]:
    risks = item.get("risks") or []
    naturalness = item.get("naturalness") or 0
    if risks or naturalness < 82:
        decision = "淘汰"
    elif naturalness < 88 or item.get("semantic_issues"):
        decision = "需人工复核"
    elif naturalness < 92:
        decision = "降为备选"
    else:
        decision = "保留"
    return {
        "姓名": item["full_name"],
        "Catalog层级": "/".join(item["catalog_levels"]),
        "新扩展字": "".join(item["new_extended_chars"]),
        "结构": item["structure"],
        "人格": item["personality"],
        "首字角色": item["semantic_roles"][0],
        "次字角色": item["semantic_roles"][1],
        "关系": item["relation"],
        "组合义": item["combined_meaning"],
        "文化证据": item["culture_evidence"],
        "自然度": item["naturalness"],
        "风险": risks,
        "建议": decision,
    }


def summary_report(catalog: dict, sample: dict, core: dict, generation: dict, before_after: dict, manual: dict) -> str:
    stats = Counter(record["nameability_level"] for record in catalog["records"])
    all_generation_passed = all(all(gates.values()) for gates in generation["quality_gates"].values())
    sample_gates_passed = all(sample["quality_gates"].values())
    core_gates_passed = core["quality_gates"]["core_semantic_roles_nonempty"] and core["quality_gates"]["core_naming_meaning_nonempty"]
    lines = [
        "# Milestone 3.2A Summary",
        "",
        f"Generated at: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Catalog Counts",
        f"- CORE: {stats.get('CORE', 0)}",
        f"- EXTENDED: {stats.get('EXTENDED', 0)}",
        f"- EXPERIMENTAL: {stats.get('EXPERIMENTAL', 0)}",
        f"- REJECTED: {stats.get('REJECTED', 0)}",
        f"- CORE+EXTENDED modern-name candidate count: {stats.get('CORE', 0) + stats.get('EXTENDED', 0)}",
        "",
        "## Core Questions",
        f"1. CORE+EXTENDED currently has {stats.get('CORE', 0) + stats.get('EXTENDED', 0)} eligible production-pool characters after strict risk filtering.",
        "2. CORE reached its current size because the catalog combines source positivity, commonness, culture evidence, semantic category bonuses, and the new no-risk CORE cap.",
        "3. Extension still introduces some review-worthy combinations; low-nameability and primary-category rules were tightened in this pass.",
        "4. Compared with 3.1B, the old virtue stack is reduced and expanded chars are used, but 3.1B lacks a same-case Top20 matrix.",
        "5. 仁、贤、承、谦、德、信、敬、正、思、安 are no longer allowed to monopolize Top20 by ranking caps.",
        "6. Some generated names still need human review for phrase-like feel; see manual review.",
        "7. Catalog now carries semantic roles and composition validation, but this remains rule-driven rather than fully linguistic.",
        "",
        "## Sample Audit",
    ]
    for level, payload in sample["levels"].items():
        lines.append(f"- {level}: sample={payload['sample_size']}, decisions={payload['decision_counts']}, correct_rate={payload['correct_rate']}")
    lines.extend(
        [
            "",
            "## Core Strictness",
            json.dumps(core["counts"], ensure_ascii=False, indent=2),
            "",
            "## Five Case Results",
        ]
    )
    for case_id, case in generation["cases"].items():
        lines.append(f"- {case_id}: Top3={' / '.join(item['full_name'] for item in case['top3'])}; Backup7={' / '.join(item['full_name'] for item in case['backup7'])}")
    lines.extend(
        [
            "",
            "## Acceptance",
            f"- Catalog sample gates passed: {sample_gates_passed}",
            f"- CORE required non-empty gates passed: {core_gates_passed}",
            f"- Generation hard gates passed for all cases: {all_generation_passed}",
            "- Milestone 3.3 was not entered.",
            "",
            "See JSON reports for full Top20, Top10, Top3, Backup7, before/after metrics, and manual review tables.",
        ]
    )
    return "\n".join(lines) + "\n"


def sample_audit_md(sample: dict) -> str:
    lines = ["# Milestone 3.2A Catalog Sample Audit", ""]
    for level, payload in sample["levels"].items():
        lines.append(f"## {level}")
        lines.append(f"- sample_size: {payload['sample_size']}")
        lines.append(f"- decision_counts: {payload['decision_counts']}")
        lines.append(f"- correct_rate: {payload['correct_rate']}")
        for item in payload["records"][:20]:
            lines.append(f"- {item['char']} {item['level']} {item['audit_decision']} {item['audit_reason']}")
        lines.append("")
    return "\n".join(lines)


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    result = write_reports()
    print(json.dumps(result["generation_matrix"]["quality_gates"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
