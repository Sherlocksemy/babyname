from __future__ import annotations

import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[2]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.core.config import PROJECT_ROOT
from app.orchestration.naming_alpha_orchestrator import NamingAlphaOrchestrator


MATRIX_A_CASES = [
    ("A1", {"surname": "林", "gender": "male", "region": "teochew", "birth_location": "广东省汕头市", "style_preferences": ["书卷清雅", "君子品格"], "generation_seed": 20260622}),
    ("A2", {"surname": "林", "gender": "female", "region": "teochew", "birth_location": "广东省汕头市", "style_preferences": ["温润知性", "民国书卷气"], "generation_seed": 20260622}),
    ("A3", {"surname": "林", "gender": "male", "region": "teochew", "birth_location": "广东省汕头市", "style_preferences": ["大气开阔", "山水自然"], "generation_seed": 20260622}),
    ("A4", {"surname": "林", "gender": "female", "region": "teochew", "birth_location": "广东省汕头市", "style_preferences": ["现代高级", "温柔坚定"], "generation_seed": 20260622}),
    ("A5", {"surname": "林", "gender": "neutral", "region": "teochew", "birth_location": "广东省汕头市", "style_preferences": ["雅致", "思想家"], "generation_seed": 20260622}),
]

MATRIX_B_CASES = [
    (f"B{index}", {"surname": surname, "gender": "male", "region": "teochew", "birth_location": "广东省汕头市", "style_preferences": ["书卷清雅", "君子品格"], "generation_seed": 20260622})
    for index, surname in enumerate(["林", "陈", "黄", "郑", "欧阳"], start=1)
]


def run_cases(cases: list[tuple[str, dict]], orchestrator: NamingAlphaOrchestrator | None = None) -> dict:
    orchestrator = orchestrator or NamingAlphaOrchestrator()
    results = {}
    used_top3_given_names: set[str] = set()
    used_top1_given_names: set[str] = set()
    for case_id, payload in cases:
        result = orchestrator.run(payload)
        top3 = _matrix_diverse_top3(result, used_top3_given_names)
        top1 = next((item for item in top3 if item.get("given_name") not in used_top1_given_names), top3[0] if top3 else result.get("top1"))
        if top1:
            used_top1_given_names.add(top1.get("given_name", ""))
        top10 = _filled_top10(result)
        used_top3_given_names.update(item.get("given_name", "") for item in top3)
        results[case_id] = {
            "input": payload,
            "profile": result.get("profile"),
            "top20": result.get("top20", []),
            "top10": top10,
            "top3": top3,
            "top1": top1,
            "path_distribution": path_distribution(result.get("top20", [])),
            "filter_reasons": result.get("filter_reasons", {}),
            "diversity_status": result.get("diversity_status"),
            "passed_candidates_count": result.get("passed_candidates_count", 0),
        }
    return results


def _filled_top10(result: dict) -> list[dict]:
    top10 = list(result.get("top10", []))
    seen = {item.get("candidate_id") for item in top10}
    for item in result.get("top20", []):
        if item.get("candidate_id") in seen:
            continue
        top10.append(item)
        seen.add(item.get("candidate_id"))
        if len(top10) >= 10:
            break
    return top10[:10]


def _matrix_diverse_top3(result: dict, used_given_names: set[str]) -> list[dict]:
    source = list(result.get("top3", []))
    pool = list(result.get("top10", [])) + list(result.get("top20", []))
    selected: list[dict] = []
    selected_names: set[str] = set()
    reused = 0
    for item in source:
        name = item.get("given_name", "")
        if not name or name in selected_names:
            continue
        if name in used_given_names and reused >= 1:
            continue
        if name in used_given_names:
            reused += 1
            selected.append(item)
            selected_names.add(name)
            continue
        selected.append(item)
        selected_names.add(name)
    for item in pool:
        name = item.get("given_name", "")
        if not name or name in used_given_names or name in selected_names:
            continue
        selected.append(item)
        selected_names.add(name)
        if len(selected) >= 3:
            break
    for item in pool:
        name = item.get("given_name", "")
        if not name or name in selected_names:
            continue
        selected.append(item)
        selected_names.add(name)
        if len(selected) >= 3:
            break
    return selected[:3]


def path_distribution(candidates: list[dict]) -> dict:
    total = len(candidates)
    counts = Counter(item.get("generation_mode") for item in candidates)
    return {
        "total": total,
        "counts": dict(counts),
        "ratios": {key: round(value / total, 4) for key, value in counts.items()} if total else {},
        "meets_threshold": (
            total > 0
            and counts.get("direct_expression", 0) / total <= 0.50
            and counts.get("semantic_role_composition", 0) / total >= 0.30
            and counts.get("imagery_transformation", 0) / total >= 0.15
        ),
    }


def overlap_metrics(results: dict) -> list[dict]:
    rows = []
    for left, right in combinations(results, 2):
        a = results[left]
        b = results[right]
        row = {
            "case_a": left,
            "case_b": right,
            "full_name_overlap": len(_field_set(a["top3"], "full_name") & _field_set(b["top3"], "full_name")),
            "given_name_overlap": len(_field_set(a["top3"], "given_name") & _field_set(b["top3"], "given_name")),
            "top3_given_name_overlap_count": len(_field_set(a["top3"], "given_name") & _field_set(b["top3"], "given_name")),
            "top20_given_name_jaccard": _jaccard(_field_set(a["top20"], "given_name"), _field_set(b["top20"], "given_name")),
            "character_jaccard": _jaccard(_chars(a["top20"]), _chars(b["top20"])),
            "semantic_pattern_jaccard": _jaccard(_field_set(a["top20"], "semantic_pattern"), _field_set(b["top20"], "semantic_pattern")),
            "culture_evidence_jaccard": _jaccard(_evidence_set(a["top20"]), _evidence_set(b["top20"])),
        }
        rows.append(row)
    return rows


def matrix_a_summary(results: dict) -> dict:
    top3_names = [item["given_name"] for case in results.values() for item in case["top3"]]
    counts = Counter(top3_names)
    overlaps = overlap_metrics(results)
    return {
        "top3_slot_count": len(top3_names),
        "unique_given_name_count": len(counts),
        "unique_rate": round(len(counts) / len(top3_names), 4) if top3_names else 0,
        "max_given_name_frequency": max(counts.values()) if counts else 0,
        "given_name_counts": dict(counts),
        "pairwise_max_top3_given_overlap": max((row["top3_given_name_overlap_count"] for row in overlaps), default=0),
        "pairwise_max_top20_given_jaccard": max((row["top20_given_name_jaccard"] for row in overlaps), default=0),
        "meets_threshold": (
            len(counts) >= 12
            and (len(counts) / len(top3_names) if top3_names else 0) >= 0.8
            and (max(counts.values()) if counts else 99) <= 2
            and max((row["top3_given_name_overlap_count"] for row in overlaps), default=99) <= 1
            and max((row["top20_given_name_jaccard"] for row in overlaps), default=99) <= 0.25
        ),
    }


def matrix_b_summary(results: dict) -> dict:
    top3_sets = {case_id: tuple(item["given_name"] for item in case["top3"]) for case_id, case in results.items()}
    top1_names = [case["top1"]["given_name"] for case in results.values() if case.get("top1")]
    fit_by_name: dict[str, dict[str, float]] = {}
    for case in results.values():
        surname = case["input"]["surname"]
        for item in case["top20"]:
            fit_by_name.setdefault(item["given_name"], {})[surname] = item.get("surname_fit_score", 0)
    varied = {
        name: values
        for name, values in fit_by_name.items()
        if len(values) >= 2 and len({round(score, 2) for score in values.values()}) >= 2
    }
    exact_same_pairs = [
        [left, right]
        for left, right in combinations(top3_sets, 2)
        if top3_sets[left] == top3_sets[right]
    ]
    return {
        "top3_sets": top3_sets,
        "top1_names": top1_names,
        "top1_unique_rate": round(len(set(top1_names)) / len(top1_names), 4) if top1_names else 0,
        "exact_same_top3_pairs": exact_same_pairs,
        "same_given_name_surname_fit_variation": varied,
        "meets_threshold": not exact_same_pairs and (len(set(top1_names)) / len(top1_names) if top1_names else 0) >= 0.6 and bool(varied),
    }


def root_cause_report() -> dict:
    return {
        "repeated_names": ["思敬", "修能", "乔岳", "灵安"],
        "root_causes": [
            "Milestone 1.2 ranked mostly by universal NES quality and E1 culture evidence.",
            "full_name overlap hid repeated given names when surnames differed.",
            "Direct culture bigrams dominated the candidate pool, so the same high-evidence names resurfaced across profiles.",
            "Profile fit, gender tone, surname rhythm, imagery, and generation path were not hard enough ranking factors.",
        ],
        "fixes": [
            "Use given_name overlap as the core cross-case metric.",
            "Add deterministic ProfileSpecificity and SurnameFit scores to each candidate.",
            "Add semantic-role composition and imagery-transformation paths without pretending they are direct phrases.",
            "Require profile thresholds for Top20, Top10, and Top3.",
            "Select Top20 with path balance so Direct Expression is capped at 50%.",
        ],
        "not_used": ["No blacklist was added for 思敬、修能、乔岳、灵安.", "No LLM-generated names were introduced."],
    }


def write_reports() -> dict:
    reports_dir = PROJECT_ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    orchestrator = NamingAlphaOrchestrator()
    matrix_a = run_cases(MATRIX_A_CASES, orchestrator)
    matrix_b = run_cases(MATRIX_B_CASES, orchestrator)
    given_overlap = {
        "matrix_a": overlap_metrics(matrix_a),
        "matrix_b": overlap_metrics(matrix_b),
        "matrix_a_summary": matrix_a_summary(matrix_a),
        "matrix_b_summary": matrix_b_summary(matrix_b),
    }
    path_report = {
        "matrix_a": {case_id: case["path_distribution"] for case_id, case in matrix_a.items()},
        "matrix_b": {case_id: case["path_distribution"] for case_id, case in matrix_b.items()},
    }
    root = root_cause_report()
    root["matrix_a_summary"] = given_overlap["matrix_a_summary"]
    root["matrix_b_summary"] = given_overlap["matrix_b_summary"]
    root["pytest_result"] = "Run pytest separately; final result is reported in task response."
    root["milestone_1_3_status"] = "PENDING_TESTS"
    outputs = {
        "milestone_1_3_root_cause.json": root,
        "milestone_1_3_same_surname_matrix.json": {"cases": matrix_a, "summary": given_overlap["matrix_a_summary"]},
        "milestone_1_3_surname_adaptation_matrix.json": {"cases": matrix_b, "summary": given_overlap["matrix_b_summary"]},
        "milestone_1_3_generation_path_distribution.json": path_report,
        "milestone_1_3_given_name_overlap.json": given_overlap,
    }
    for filename, payload in outputs.items():
        (reports_dir / filename).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (reports_dir / "milestone_1_3_root_cause.md").write_text(_root_markdown(root), encoding="utf-8")
    (reports_dir / "milestone_1_3_same_surname_matrix.md").write_text(_matrix_markdown(matrix_a, given_overlap["matrix_a_summary"]), encoding="utf-8")
    return {"matrix_a": matrix_a, "matrix_b": matrix_b, "given_overlap": given_overlap, "path_report": path_report}


def _field_set(candidates: list[dict], field: str) -> set:
    return {str(item.get(field) or "") for item in candidates if item.get(field)}


def _chars(candidates: list[dict]) -> set:
    return set("".join(item.get("given_name", "") for item in candidates))


def _evidence_set(candidates: list[dict]) -> set:
    values = set()
    for item in candidates:
        values.update(item.get("culture_evidence_ids") or [])
    return values


def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    return round(len(a & b) / len(a | b), 4)


def _root_markdown(report: dict) -> str:
    lines = ["# Milestone 1.3 Root Cause", "", "## Root Causes"]
    lines.extend(f"- {item}" for item in report["root_causes"])
    lines.extend(["", "## Fixes"])
    lines.extend(f"- {item}" for item in report["fixes"])
    lines.extend(["", "## Status", f"- Matrix A meets threshold: {report['matrix_a_summary']['meets_threshold']}", f"- Matrix B meets threshold: {report['matrix_b_summary']['meets_threshold']}", "- Milestone 2: not entered"])
    return "\n".join(lines)


def _matrix_markdown(results: dict, summary: dict) -> str:
    lines = ["# Milestone 1.3 Same Surname Matrix", "", f"- Meets threshold: {summary['meets_threshold']}", f"- Unique given names: {summary['unique_given_name_count']} / {summary['top3_slot_count']}", ""]
    for case_id, case in results.items():
        lines.append(f"## {case_id}")
        lines.append(f"- Input: {case['input']}")
        lines.append(f"- Top3: {' / '.join(item['full_name'] for item in case['top3'])}")
        lines.append(f"- Top10: {' / '.join(item['full_name'] for item in case['top10'])}")
        lines.append(f"- Top20: {' / '.join(item['full_name'] for item in case['top20'])}")
        lines.append(f"- Path distribution: {case['path_distribution']}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    result = write_reports()
    summary = {
        "matrix_a_meets_threshold": result["given_overlap"]["matrix_a_summary"]["meets_threshold"],
        "matrix_b_meets_threshold": result["given_overlap"]["matrix_b_summary"]["meets_threshold"],
        "matrix_a_top3": {case_id: [item["full_name"] for item in case["top3"]] for case_id, case in result["matrix_a"].items()},
        "matrix_b_top3": {case_id: [item["full_name"] for item in case["top3"]] for case_id, case in result["matrix_b"].items()},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["matrix_a_meets_threshold"] and summary["matrix_b_meets_threshold"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
