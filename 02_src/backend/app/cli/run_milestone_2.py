from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[2]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.adapters.lunar_calendar_adapter import LunarCalendarAdapter
from app.core.config import KNOWLEDGE_BASE_DIR, PROJECT_ROOT, REPORTS_DIR
from app.engines.calendar_engine import CalendarEngine
from app.engines.four_pillars_engine import FourPillarsEngine
from app.engines.true_solar_time_engine import TrueSolarTimeEngine
from app.orchestration.naming_alpha_orchestrator import NamingAlphaOrchestrator
from app.schemas.baby_profile import BabyProfile


READ_DOCS = [
    "04_docs_v5/01_PRD.md",
    "04_docs_v5/02_SPEC.md",
    "04_docs_v5/02A_NAMING_PHILOSOPHY.md",
    "04_docs_v5/02B_NAMING_EVALUATION_SYSTEM.md",
    "04_docs_v5/03_DATA_SCHEMA.md",
    "04_docs_v5/04_DEV_PLAN.md",
    "01_knowledge_base/06_numerology_layer/README.md",
    "reports/knowledge_audit.json",
]


SAMPLE_CASES = [
    ("shantou_solar", {"surname": "林", "gender": "male", "calendar_type": "solar", "birth_year": 2025, "birth_month": 3, "birth_day": 1, "birth_hour": 8, "birth_minute": 30, "birth_province": "广东省", "birth_city": "汕头市", "timezone": "Asia/Shanghai", "region": "teochew", "style_preferences": ["书卷清雅", "君子品格"], "generation_seed": 20260623}),
    ("chaozhou_lunar", {"surname": "陈", "gender": "female", "calendar_type": "lunar", "birth_year": 2025, "birth_month": 2, "birth_day": 2, "birth_hour": 9, "birth_minute": 10, "birth_province": "广东省", "birth_city": "潮州市", "timezone": "Asia/Shanghai", "region": "teochew", "style_preferences": ["温润知性", "民国书卷气"], "generation_seed": 20260623}),
    ("jieyang_lunar_leap", {"surname": "黄", "gender": "neutral", "calendar_type": "lunar", "birth_year": 2025, "birth_month": 6, "birth_day": 1, "birth_hour": 10, "birth_minute": 0, "is_leap_month": True, "birth_province": "广东省", "birth_city": "揭阳市", "timezone": "Asia/Shanghai", "region": "teochew", "style_preferences": ["雅致", "思想家"], "generation_seed": 20260623}),
    ("before_lichun", {"surname": "郑", "gender": "male", "calendar_type": "solar", "birth_year": 2025, "birth_month": 2, "birth_day": 3, "birth_hour": 20, "birth_minute": 0, "birth_city": "汕头市", "timezone": "Asia/Shanghai", "region": "teochew", "style_preferences": ["大气开阔", "山水自然"], "generation_seed": 20260623}),
    ("after_lichun", {"surname": "郑", "gender": "male", "calendar_type": "solar", "birth_year": 2025, "birth_month": 2, "birth_day": 4, "birth_hour": 12, "birth_minute": 0, "birth_city": "汕头市", "timezone": "Asia/Shanghai", "region": "teochew", "style_preferences": ["大气开阔", "山水自然"], "generation_seed": 20260623}),
    ("before_23", {"surname": "欧阳", "gender": "female", "calendar_type": "solar", "birth_year": 2025, "birth_month": 3, "birth_day": 1, "birth_hour": 22, "birth_minute": 50, "birth_city": "潮州市", "timezone": "Asia/Shanghai", "region": "teochew", "style_preferences": ["现代高级", "温柔坚定"], "generation_seed": 20260623}),
    ("after_23", {"surname": "欧阳", "gender": "female", "calendar_type": "solar", "birth_year": 2025, "birth_month": 3, "birth_day": 1, "birth_hour": 23, "birth_minute": 10, "birth_city": "潮州市", "timezone": "Asia/Shanghai", "region": "teochew", "style_preferences": ["现代高级", "温柔坚定"], "generation_seed": 20260623}),
]


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    reports = build_reports()
    print(json.dumps({"ok": True, "reports": list(reports), "sample_top3": reports["milestone_2_naming_integration.json"]["sample_top3"]}, ensure_ascii=False, indent=2))
    return 0


def build_reports() -> dict:
    data_audit = audit_numerology_data()
    calendar_validation = validate_calendar()
    true_solar_validation = validate_true_solar_time()
    four_pillars_validation = validate_four_pillars()
    fortune_matrix = run_fortune_matrix()
    naming_integration = run_naming_integration()
    summary = build_summary(data_audit, naming_integration)
    outputs = {
        "milestone_2_data_audit.json": data_audit,
        "milestone_2_calendar_validation.json": calendar_validation,
        "milestone_2_true_solar_time_validation.json": true_solar_validation,
        "milestone_2_four_pillars_validation.json": four_pillars_validation,
        "milestone_2_fortune_matrix.json": fortune_matrix,
        "milestone_2_naming_integration.json": naming_integration,
    }
    for name, payload in outputs.items():
        (REPORTS_DIR / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (REPORTS_DIR / "milestone_2_summary.md").write_text(summary, encoding="utf-8")
    return outputs


def audit_numerology_data() -> dict:
    wuge = json.loads((KNOWLEDGE_BASE_DIR / "06_numerology_layer" / "wuge_rules.json").read_text(encoding="utf-8"))
    bazi = json.loads((KNOWLEDGE_BASE_DIR / "06_numerology_layer" / "bazi_rules.json").read_text(encoding="utf-8"))
    with (KNOWLEDGE_BASE_DIR / "06_numerology_layer" / "zodiac_taboo.csv").open(encoding="utf-8-sig", newline="") as handle:
        zodiac_rows = list(csv.DictReader(handle))
    return {
        "read_documents": READ_DOCS,
        "bazi_rules": {"keys": list(bazi), "status": "RULE_TEXT_ONLY_FOR_ADVANCED_PATTERNS"},
        "wuge_rules": {
            "stroke_math_count": len(wuge.get("stroke_math", {})),
            "sancai_config_count": len(wuge.get("sancai_config", {})),
            "interpretation_status": "DATA_INCOMPLETE",
            "note": "81数理文本为占位式派生说明，本轮只使用五格数值，不生成吉凶断语。",
        },
        "zodiac_rules": {"row_count": len(zodiac_rows), "status": "COMPLETE_FOR_AUXILIARY_RADICALS"},
        "calendar_dependency": {"name": "lunar-python", "version": "1.4.8", "sxtwl_status": "FAILED_BUILD_ON_CURRENT_WINDOWS_PY314"},
    }


def validate_calendar() -> dict:
    engine = CalendarEngine()
    solar = engine.normalize(BabyProfile.from_dict(SAMPLE_CASES[0][1]))
    lunar_payload = SAMPLE_CASES[1][1]
    lunar = engine.normalize(BabyProfile.from_dict(lunar_payload))
    leap = engine.normalize(BabyProfile.from_dict(SAMPLE_CASES[2][1]))
    invalid_leap_error = ""
    try:
        bad = dict(SAMPLE_CASES[2][1])
        bad["birth_month"] = 2
        engine.normalize(BabyProfile.from_dict(bad))
    except ValueError as exc:
        invalid_leap_error = str(exc)
    return {
        "solar_to_lunar": solar.to_dict(),
        "lunar_to_solar": lunar.to_dict(),
        "leap_month": leap.to_dict(),
        "invalid_leap_month_rejected": bool(invalid_leap_error),
        "invalid_leap_month_error": invalid_leap_error,
        "cross_validation_vectors": [
            {"solar": "2025-03-01", "expected_lunar": "2025-02-02", "passed": solar.lunar_date["month"] == 2 and solar.lunar_date["day"] == 2},
            {"lunar": "2025 leap 6-1", "expected_solar": "2025-07-25", "passed": leap.solar_datetime.strftime("%Y-%m-%d") == "2025-07-25"},
        ],
    }


def validate_true_solar_time() -> dict:
    engine = TrueSolarTimeEngine()
    profile = BabyProfile.from_dict(SAMPLE_CASES[0][1])
    standard = CalendarEngine().normalize(profile).solar_datetime
    normal = engine.calculate(standard, profile.birth_city)
    missing = engine.calculate(standard, "不存在城市")
    cross_day = engine.calculate(standard.replace(hour=0, minute=5), "揭阳市")
    return {
        "normal": normal.to_dict(),
        "missing_city": missing.to_dict(),
        "cross_day": cross_day.to_dict(),
        "method": "true solar time = standard time + (longitude - 120E) * 4 minutes + equation of time",
    }


def validate_four_pillars() -> dict:
    adapter = LunarCalendarAdapter()
    engine = FourPillarsEngine(adapter)
    before = engine.calculate(adapter.jieqi_table(2025)["立春"].replace(minute=0) if False else CalendarEngine().normalize(BabyProfile.from_dict(SAMPLE_CASES[3][1])).solar_datetime)
    after = engine.calculate(CalendarEngine().normalize(BabyProfile.from_dict(SAMPLE_CASES[4][1])).solar_datetime)
    before_23 = engine.calculate(CalendarEngine().normalize(BabyProfile.from_dict(SAMPLE_CASES[5][1])).solar_datetime, zi_hour_rule="SAME_DAY")
    after_23_next = engine.calculate(CalendarEngine().normalize(BabyProfile.from_dict(SAMPLE_CASES[6][1])).solar_datetime, zi_hour_rule="NEXT_DAY_AT_23")
    return {
        "before_lichun": before,
        "after_lichun": after,
        "zi_rule_same_day": before_23,
        "zi_rule_next_day_at_23": after_23_next,
        "cross_validation": {
            "method": "lunar-python EightChar plus independent day pillar sequence anchored at 2000-01-01 戊午",
            "passed": all(item["cross_validation"]["passed"] for item in [before, after, before_23, after_23_next]),
        },
    }


def run_fortune_matrix() -> dict:
    engine = NamingAlphaOrchestrator()
    rows = {}
    for case_id, payload in SAMPLE_CASES:
        result = engine.run(payload)
        rows[case_id] = {
            "baby_profile": result.get("baby_profile"),
            "calendar": result.get("fortune", {}).get("calendar"),
            "true_solar_time": result.get("fortune", {}).get("true_solar_time"),
            "four_pillars": result.get("fortune", {}).get("four_pillars"),
            "five_elements": result.get("fortune", {}).get("five_elements"),
            "zodiac": result.get("fortune", {}).get("zodiac"),
            "top3": [item["full_name"] for item in result.get("top3", [])],
            "backup7": [item["full_name"] for item in result.get("backup7", [])],
        }
    return rows


def run_naming_integration() -> dict:
    result = NamingAlphaOrchestrator().run(SAMPLE_CASES[0][1])
    return {
        "result_status": result.get("result_status"),
        "qualified_count": result.get("qualified_count"),
        "fortune_status": result.get("fortune_status"),
        "sample_top3": [item["full_name"] for item in result.get("top3", [])],
        "sample_backup7": [item["full_name"] for item in result.get("backup7", [])],
        "top3_scores": [item["score"] for item in result.get("top3", [])],
        "quality_guard_not_weakened": all(not item["quality_guard"].get("hard_failures") for item in result.get("top3", []) + result.get("backup7", [])),
        "max_fortune_score": max([item.get("fortune_score") or 0 for item in result.get("top20", [])] or [0]),
    }


def build_summary(data_audit: dict, naming_integration: dict) -> str:
    lines = [
        "# Milestone 2 Summary",
        "",
        "## Read Documents",
        *[f"- {item}" for item in READ_DOCS],
        "",
        "## Numerology Data Audit",
        f"- Bazi rules: {data_audit['bazi_rules']['status']}",
        f"- Wuge interpretation: {data_audit['wuge_rules']['interpretation_status']}",
        f"- Zodiac rows: {data_audit['zodiac_rules']['row_count']}",
        "",
        "## Dependency",
        "- `lunar-python==1.4.8` for lunar calendar, solar terms, and EightChar adapter.",
        "- `sxtwl==2.0.7` was not used because it requires local C++ build tools in this environment.",
        "",
        "## Methods",
        "- Calendar: `lunar-python` behind `LunarCalendarAdapter`.",
        "- True solar time: longitude correction plus equation of time.",
        "- Four pillars: Lichun year boundary, jieqi month boundary, true-solar-time hour basis.",
        "- Five elements: objective stems, branches, and hidden stems counting only.",
        "- Zodiac: bazi zodiac uses Lichun year branch; folk zodiac uses lunar year.",
        "- Wuge: Kangxi strokes only; interpretation marked `DATA_INCOMPLETE`.",
        "",
        "## Naming Integration",
        f"- Top3: {' / '.join(naming_integration['sample_top3'])}",
        f"- Backup7: {' / '.join(naming_integration['sample_backup7'])}",
        f"- Max fortune score in Top20: {naming_integration['max_fortune_score']}",
        "- Fortune can add at most 10 points and cannot rescue QualityGuard failures.",
        "",
        "## Status",
        "- Pytest: run separately and recorded in final task response.",
        "- Milestone 2 acceptance: pending full tests.",
        "- API/frontend development: not entered.",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
