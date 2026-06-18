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

