from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[2]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.core.config import PROJECT_ROOT
from app.orchestration.naming_alpha_orchestrator import NamingAlphaOrchestrator


GOLDEN_NAMES = {"知微", "景行", "弘毅", "怀瑾", "若谷", "修远", "慎思", "清晏", "牧之", "守仁"}
DOCUMENT_EXAMPLE_NAMES = GOLDEN_NAMES | {"明德", "致知", "明辨", "闻道"}

CASES = {
    "A": {
        "surname": "林",
        "gender": "male",
        "birth_date": "2025-03-01",
        "birth_time": "08:30",
        "birth_location": "广东省汕头市",
        "region": "teochew",
        "style_preferences": ["书卷清雅", "君子品格"],
        "liked_chars": [],
        "blocked_chars": [],
        "generation_seed": 20260622,
    },
    "B": {
        "surname": "陈",
        "gender": "female",
        "birth_date": "2025-03-01",
        "birth_time": "08:30",
        "birth_location": "广东省潮州市",
        "region": "teochew",
        "style_preferences": ["温润知性", "民国书卷气"],
        "liked_chars": [],
        "blocked_chars": [],
        "generation_seed": 20260622,
    },
    "C": {
        "surname": "黄",
        "gender": "male",
        "birth_date": "2025-03-01",
        "birth_time": "08:30",
        "birth_location": "广东省揭阳市",
        "region": "teochew",
        "style_preferences": ["大气开阔", "山水自然"],
        "liked_chars": [],
        "blocked_chars": [],
        "generation_seed": 20260622,
    },
    "D": {
        "surname": "郑",
        "gender": "female",
        "birth_date": "2025-03-01",
        "birth_time": "08:30",
        "birth_location": "广东省汕头市",
        "region": "teochew",
        "style_preferences": ["现代高级", "温柔坚定"],
        "liked_chars": ["宁"],
        "blocked_chars": ["若", "梓", "汐"],
        "generation_seed": 20260622,
    },
    "E": {
        "surname": "欧阳",
        "gender": "neutral",
        "birth_date": "2025-03-01",
        "birth_time": "08:30",
        "birth_location": "广东省汕头市",
        "region": "teochew",
        "style_preferences": ["雅致", "思想家"],
        "liked_chars": [],
        "blocked_chars": [],
        "generation_seed": 20260622,
    },
}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    reports_dir = PROJECT_ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    audit = provenance_audit()
    matrix = run_matrix()
    distribution = score_distribution(matrix)

    (reports_dir / "milestone_1_2_provenance_audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    (reports_dir / "milestone_1_2_provenance_audit.md").write_text(provenance_markdown(audit), encoding="utf-8")
    (reports_dir / "milestone_1_2_personalization_matrix.json").write_text(json.dumps(matrix, ensure_ascii=False, indent=2), encoding="utf-8")
    (reports_dir / "milestone_1_2_personalization_matrix.md").write_text(matrix_markdown(matrix), encoding="utf-8")
    (reports_dir / "milestone_1_2_score_distribution.json").write_text(json.dumps(distribution, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"audit_polluted": audit["polluted"], "cases": list(matrix["cases"]), "max_overlap": matrix["max_top20_overlap"], "score_distribution": distribution["summary"]}, ensure_ascii=False, indent=2))
    return 0 if not audit["polluted"] and matrix["max_top20_overlap"] <= 0.25 else 1


def provenance_audit() -> dict:
    app_dir = PROJECT_ROOT / "02_src" / "backend" / "app"
    checks = []
    patterns = {
        "golden_fixture_import": "golden_names.v1.json",
        "weak_fixture_import": "weak_names.v1.json",
        "golden_symbol": "GOLDEN_MEANINGS",
        "direct_representative_name": "preferred =",
        "direct_name_candidates_use": "name_candidates",
    }
    polluted = False
    for path in app_dir.rglob("*.py"):
        if path.name == "run_milestone_1_2.py":
            continue
        text = path.read_text(encoding="utf-8")
        hits = [name for name, pattern in patterns.items() if pattern in text]
        runtime_dependency = bool(hits)
        is_pollution = any(hit in {"golden_fixture_import", "weak_fixture_import", "golden_symbol", "direct_representative_name"} for hit in hits)
        if "culture_index.py" in str(path) and "name_candidates" in hits:
            is_pollution = True
        if hits:
            polluted = polluted or is_pollution
            checks.append(
                {
                    "file": str(path),
                    "import_chain": [],
                    "runtime_dependency": runtime_dependency,
                    "hits": hits,
                    "pollutes_production": is_pollution,
                    "fix_action": "remove direct fixture/example/name_candidates production dependency" if is_pollution else "schema/audit reference only",
                }
            )
    return {
        "polluted": polluted,
        "checks": checks,
        "fixture_policy": "tests/fixtures files are pytest-only and must not be read by production code",
    }


def run_matrix() -> dict:
    orchestrator = NamingAlphaOrchestrator()
    results = {}
    for case_id, payload in CASES.items():
        result = orchestrator.run(payload)
        top20 = result.get("top20", [])
        top10 = result.get("top10", [])
        top3 = result.get("top3", [])
        given_top20 = [item["given_name"] for item in top20]
        results[case_id] = {
            "input": payload,
            "top20": [item["full_name"] for item in top20],
            "top10": [item["full_name"] for item in top10],
            "top3": [item["full_name"] for item in top3],
            "primary_structure": result["structure_result"]["primary_structure"]["id"],
            "primary_archetype": result["archetype_result"]["primary_archetype"]["id"],
            "structure_distribution": dict(Counter(item["structure_id"] for item in top20)),
            "archetype_distribution": dict(Counter(item["archetype_id"] for item in top20)),
            "culture_source_distribution": dict(Counter(ev["source_type"] for item in top20 for ev in item.get("evidences", [])[:1])),
            "char_distribution": dict(Counter(char for item in top20 for char in item["given_name"])),
            "golden_overlap_rate": round(len(set(given_top20) & GOLDEN_NAMES) / max(len(given_top20), 1), 4),
            "document_example_overlap_rate": round(len(set(given_top20) & DOCUMENT_EXAMPLE_NAMES) / max(len(given_top20), 1), 4),
            "blocked_char_hits": [name for name in given_top20 if any(char in name for char in payload.get("blocked_chars", []))],
            "liked_char_appearances": [name for name in given_top20 if any(char in name for char in payload.get("liked_chars", []))],
            "raw_scores": [item["score"]["raw_score"] for item in top10],
            "naturalness_scores": [item["naturalness_score"] for item in top10],
            "reconstruction_success_rate": round(sum(1 for item in top20 if item.get("reconstruction", {}).get("reconstructable")) / max(len(top20), 1), 4),
            "fortune_status": result.get("fortune_status"),
        }
    overlap = {}
    max_overlap = 0.0
    for left, right in itertools.combinations(results, 2):
        left_set = set(results[left]["top20"])
        right_set = set(results[right]["top20"])
        rate = round(len(left_set & right_set) / max(min(len(left_set), len(right_set)), 1), 4)
        overlap[f"{left}-{right}"] = rate
        max_overlap = max(max_overlap, rate)
    return {"cases": results, "top20_overlap_matrix": overlap, "max_top20_overlap": max_overlap}


def score_distribution(matrix: dict) -> dict:
    case_summaries = {}
    for case_id, data in matrix["cases"].items():
        raw = data["raw_scores"]
        naturalness = data["naturalness_scores"]
        case_summaries[case_id] = {
            "raw_scores": raw,
            "unique_raw_scores": len(set(raw)),
            "top3_raw_scores": raw[:3],
            "naturalness_scores": naturalness,
            "unique_naturalness_scores": len(set(naturalness)),
        }
    return {"summary": case_summaries}


def provenance_markdown(audit: dict) -> str:
    lines = ["# Milestone 1.2 Provenance Audit", "", f"- polluted: `{audit['polluted']}`", ""]
    for item in audit["checks"]:
        lines.append(f"- {item['file']}: hits={item['hits']}, polluted={item['pollutes_production']}, fix={item['fix_action']}")
    return "\n".join(lines)


def matrix_markdown(matrix: dict) -> str:
    lines = ["# Milestone 1.2 Personalization Matrix", "", f"- max_top20_overlap: {matrix['max_top20_overlap']}", ""]
    for case_id, item in matrix["cases"].items():
        lines.append(f"## Case {case_id}")
        lines.append(f"- primary_structure: {item['primary_structure']}")
        lines.append(f"- primary_archetype: {item['primary_archetype']}")
        lines.append(f"- golden_overlap_rate: {item['golden_overlap_rate']}")
        lines.append(f"- top3: {', '.join(item['top3'])}")
        lines.append(f"- top20: {', '.join(item['top20'])}")
        lines.append("")
    lines.append("## Overlap")
    for pair, rate in matrix["top20_overlap_matrix"].items():
        lines.append(f"- {pair}: {rate}")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
