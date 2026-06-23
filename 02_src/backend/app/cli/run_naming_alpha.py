from __future__ import annotations

import json
import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[2]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.core.config import PROJECT_ROOT
from app.orchestration.naming_alpha_orchestrator import NamingAlphaOrchestrator


DEFAULT_INPUT = {
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
}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    orchestrator = NamingAlphaOrchestrator()
    result = orchestrator.run(DEFAULT_INPUT)
    reports_dir = PROJECT_ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_path = reports_dir / "milestone_1_sample_result.json"
    md_path = reports_dir / "milestone_1_sample_result.md"
    before = _legacy_before_result()
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(_to_markdown(result), encoding="utf-8")
    before_after = _before_after(before, result)
    (reports_dir / "milestone_1_1_before_after.json").write_text(json.dumps(before_after, ensure_ascii=False, indent=2), encoding="utf-8")
    (reports_dir / "milestone_1_1_before_after.md").write_text(_before_after_markdown(before_after), encoding="utf-8")
    (reports_dir / "milestone_1_1_rejected_candidates.json").write_text(
        json.dumps(result.get("rejected_candidates", []), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"ok": result.get("ok"), "json": str(json_path), "md": str(md_path), "top3": [item["full_name"] for item in result.get("top3", [])]}, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") and result.get("top3") else 1


def _to_markdown(result: dict) -> str:
    lines = [
        "# Milestone 1 Sample Result",
        "",
        f"- fortune_status: `{result.get('fortune_status')}`",
        f"- generated_candidates_count: {result.get('generated_candidates_count')}",
        f"- passed_candidates_count: {result.get('passed_candidates_count')}",
        f"- filtered_count: {result.get('filtered_count')}",
        f"- diversity_status: `{result.get('diversity_status')}`",
        "",
        "## Top3",
    ]
    for item in result.get("top3", []):
        score = (item.get("score") or {}).get("normalized_score")
        lines.append(f"- {item['full_name']} / {score} / {item['structure_id']} / {item['archetype_id']}")
        for evidence in item.get("evidences", [])[:1]:
            lines.append(f"  - {evidence.get('book')}《{evidence.get('title')}》: {evidence.get('original_text', '')[:80]}")
    return "\n".join(lines)


def _legacy_before_result() -> dict:
    top20 = [
        "林仁贤", "林宜言", "林贤思", "林宇安", "林佑德", "林庭修", "林敬序", "林星序", "林墨书", "林哲嘉",
        "林嘉贤", "林序博", "林庭嘉", "林星嘉", "林泽星", "林言思", "林仁博", "林宜贤", "林川洲", "林泽嘉",
    ]
    return {"top20": top20, "top3": ["林仁贤", "林宜言", "林宇安"], "note": "Milestone 1 sample baseline before quality calibration"}


def _before_after(before: dict, result: dict) -> dict:
    old_names = set(before["top3"])
    rejected = {item["full_name"]: item for item in result.get("rejected_candidates", [])}
    passed = {item["full_name"]: item for item in result.get("top20", [])}
    old_top3_review = {}
    for name in old_names:
        item = rejected.get(name) or passed.get(name)
        if item:
            old_top3_review[name] = {
                "status": "rejected" if name in rejected else "retained_or_downgraded",
                "quality_guard": item.get("quality_guard"),
                "score": item.get("score"),
                "semantic_validation": item.get("semantic_validation"),
                "naturalness": item.get("naturalness"),
                "evidence_level": item.get("evidence_level"),
                "compatibility_level": item.get("compatibility_level"),
            }
        else:
            old_top3_review[name] = {"status": "not_generated_after_calibration"}
    return {
        "before_top20": before["top20"],
        "after_top20": [item["full_name"] for item in result.get("top20", [])],
        "before_top3": before["top3"],
        "after_top3": [item["full_name"] for item in result.get("top3", [])],
        "old_top3_review": old_top3_review,
        "new_top3": result.get("top3", []),
        "filter_reasons": result.get("filter_reasons", {}),
        "top1": result.get("top1"),
        "top1_status": result.get("top1_status"),
    }


def _before_after_markdown(report: dict) -> str:
    lines = ["# Milestone 1.1 Before After", "", "## Before Top3"]
    lines.extend(f"- {name}" for name in report["before_top3"])
    lines.extend(["", "## After Top3"])
    for item in report["new_top3"]:
        lines.append(f"- {item['full_name']} / raw {item['score']['raw_score']} / {item['evidence_level']} / {item['compatibility_level']} / naturalness {item['naturalness_score']}")
        lines.append(f"  - meaning: {item['combined_meaning']}")
        if item.get("evidences"):
            evidence = item["evidences"][0]
            lines.append(f"  - evidence: {evidence['book']}《{evidence['title']}》 {evidence['original_text'][:90]}")
    lines.extend(["", "## Old Top3 Review"])
    for name, item in report["old_top3_review"].items():
        lines.append(f"- {name}: {item.get('status')} / {item.get('evidence_level')} / {item.get('compatibility_level')}")
    lines.extend(["", "## Filter Reasons"])
    for key, value in report["filter_reasons"].items():
        lines.append(f"- {key}: {value}")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
