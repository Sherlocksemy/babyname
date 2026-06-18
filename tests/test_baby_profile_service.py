from backend.app.schemas.baby_profile import BabyProfileRequest
from backend.app.services.baby_profile_service import BabyProfileService


def test_baby_profile_normalizes_teochew_context():
    profile = BabyProfileService().normalize(BabyProfileRequest(surname="陈", gender="女", birth_datetime="2026-06-18 09:30", birth_place="广东省汕头市"))
    assert profile.gender == "female"
    assert profile.need_teochew_check is True
    assert profile.zodiac
    assert profile.preferred_elements

