from backend.app.quality.quality_guard import QualityGuard
from backend.app.schemas.name_candidate import NameCandidate, ScoreBreakdown


def _candidate(**overrides):
    base = dict(
        name="陈清柔",
        given_name="清柔",
        group="精选推荐",
        score=86,
        pinyin="chén qīng róu",
        summary="清柔",
        meaning={"chars": [{"char": "清", "common_level": 1, "positive_level": 4}, {"char": "柔", "common_level": 1, "positive_level": 4}]},
        culture_origin={"has_core_origin": True, "core": {"match_type": "direct_phrase"}},
        pronunciation={"homophone_issues": []},
        teochew={},
        bazi={},
        zodiac={},
        wuge={},
        popularity={"heat_level": "低", "is_hot_name": False, "char_heat": {"清": "低", "柔": "低"}},
        score_breakdown=ScoreBreakdown(compliance=15, mandarin=14, teochew=10, meaning=14, culture=15, bazi=8, zodiac=4, popularity=9, style=4, total=93),
        warnings=[],
        recommendation_reason="仅作取名参考。",
    )
    base.update(overrides)
    return NameCandidate(**base)


def test_quality_guard_accepts_good_candidate():
    ok, reasons = QualityGuard().accept(_candidate(), [])
    assert ok is True
    assert reasons == []


def test_quality_guard_rejects_bad_candidate():
    bad = _candidate(given_name="清之", name="陈清之", culture_origin={"has_core_origin": False, "core": {}})
    ok, reasons = QualityGuard().accept(bad, [])
    assert ok is False
    assert reasons
