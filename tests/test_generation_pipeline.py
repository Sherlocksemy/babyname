import json
from pathlib import Path

from backend.app.engines.culture_retriever import CultureRetriever
from backend.app.engines.pronunciation_engine import PronunciationEngine
from backend.app.schemas.baby_profile import BabyProfileRequest
from backend.app.services.name_service import NameService


def test_culture_retriever_never_fakes_core_origin():
    result = CultureRetriever().find_origin("不存在")
    assert result["has_core_origin"] is False
    assert result["core"] == {}


def test_pronunciation_returns_mandarin_and_teochew():
    result = PronunciationEngine().analyze("陈", "清宁", True)
    assert result["pinyin"]
    assert set(result["teochew"]) == {"清", "宁"}
    assert "score" in result


def test_generate_twenty_names_from_golden_case():
    cases = json.loads(Path("tests/golden_cases.json").read_text(encoding="utf-8"))
    response = NameService().generate(BabyProfileRequest(**cases[1]))
    assert len(response.results) == 20
    assert len({item.name for item in response.results}) == 20
    assert all(item.name.startswith("陈") for item in response.results)
    assert all(item.score_breakdown.total == item.score for item in response.results)


def test_all_golden_cases_generate_twenty_quality_names():
    cases = json.loads(Path("tests/golden_cases.json").read_text(encoding="utf-8"))
    stop_chars = set("之以于其而也者乎矣焉哉兮尔何只中上下来去出入左右东西南北零二三四五六七八九十百千万亿人归孙赳见厌羊匪甘乘为与")
    service = NameService()
    for case in cases:
        response = service.generate(BabyProfileRequest(**case))
        assert len(response.results) == 20, case["case"]
        assert len({item.name for item in response.results}) == 20, case["case"]
        assert all(item.name.startswith(case["surname"]) for item in response.results), case["case"]
        assert not [item.name for item in response.results if any(ch in stop_chars for ch in item.given_name)], case["case"]
        assert all(item.recommendation_reason for item in response.results), case["case"]
        assert all("改命" not in item.recommendation_reason and "转运" not in item.recommendation_reason for item in response.results), case["case"]
