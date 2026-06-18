from pathlib import Path


def test_required_modules_and_tests_exist():
    required = [
        "backend/app/core/knowledge_loader.py",
        "backend/app/services/char_service.py",
        "backend/app/services/baby_profile_service.py",
        "backend/app/engines/bazi_engine.py",
        "backend/app/engines/zodiac_engine.py",
        "backend/app/engines/wuge_engine.py",
        "backend/app/engines/char_pool_builder.py",
        "backend/app/engines/culture_retriever.py",
        "backend/app/engines/pronunciation_engine.py",
        "backend/app/engines/name_composer.py",
        "backend/app/engines/name_scorer.py",
        "backend/app/quality/quality_guard.py",
        "backend/app/api/name_routes.py",
        "tests/test_knowledge_loader.py",
        "tests/test_char_service.py",
        "tests/test_baby_profile_service.py",
        "tests/test_bazi_engine.py",
        "tests/test_zodiac_engine.py",
        "tests/test_wuge_engine.py",
        "tests/test_char_pool_builder.py",
        "tests/test_culture_retriever.py",
        "tests/test_pronunciation_engine.py",
        "tests/test_name_composer.py",
        "tests/test_name_scorer.py",
        "tests/test_quality_guard.py",
        "tests/test_name_api.py",
        "tests/test_frontend_e2e.py",
    ]
    missing = [path for path in required if not Path(path).exists()]
    assert missing == []


def test_golden_cases_cover_required_scenarios():
    text = Path("tests/golden_cases.json").read_text(encoding="utf-8")
    for scenario in ["男宝双字名", "女宝双字名", "潮汕地区宝宝", "带辈分字", "禁用爆款字", "喜欢固定字", "单字名", "复姓", "出生时间缺失", "出生地缺失"]:
        assert scenario in text
