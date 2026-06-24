from __future__ import annotations

from app.schemas.baby_profile import BabyProfile


def test_baby_profile_normalizes_structured_input() -> None:
    profile = BabyProfile.from_dict(
        {
            "surname": "欧阳",
            "gender": "neutral",
            "calendar_type": "solar",
            "birth_year": 2025,
            "birth_month": 3,
            "birth_day": 1,
            "birth_hour": 8,
            "birth_minute": 30,
            "birth_city": "汕头市",
        }
    )
    assert profile.validate() == []
    assert profile.to_naming_input().surname == "欧阳"


def test_baby_profile_rejects_out_of_range_year() -> None:
    profile = BabyProfile.from_dict({"surname": "林", "birth_year": 1899})
    assert any("1900-2100" in item for item in profile.validate())

