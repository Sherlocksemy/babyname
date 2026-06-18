from backend.app.engines.name_scorer import NameScorer


def test_name_scorer_breakdown_sums_to_total():
    breakdown = NameScorer().score(
        [{"is_compliant": True, "positive_level": 4, "element": "水"}],
        {"score": 90, "homophone_issues": [], "safe": True},
        {"has_core_origin": True},
        {"preferred_elements": ["水"]},
        {"score": 4},
        {"score": 8},
        {"heat_level": "低"},
        True,
    )
    parts = [
        breakdown.compliance,
        breakdown.mandarin,
        breakdown.teochew,
        breakdown.meaning,
        breakdown.culture,
        breakdown.bazi,
        breakdown.zodiac,
        breakdown.popularity,
        breakdown.style,
    ]
    assert sum(parts) == breakdown.total
