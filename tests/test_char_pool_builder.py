from backend.app.engines.char_pool_builder import CharPoolBuilder
from backend.app.engines.culture_retriever import CultureRetriever
from backend.app.schemas.baby_profile import BabyProfileRequest
from backend.app.services.baby_profile_service import BabyProfileService
from backend.app.services.char_service import CharService


def test_char_pool_filters_stop_chars_and_hot_chars():
    profile = BabyProfileService().normalize(
        BabyProfileRequest(surname="陈", style_preferences=["温润", "诗意"], banned_chars=["梓", "轩"], liked_chars=["清"])
    )
    pool = CharPoolBuilder(CharService(), CultureRetriever()).build(profile)
    chars = {item["char"] for item in pool["generation_chars"]}
    assert chars
    assert not (chars & CharPoolBuilder.STOP_CHARS)
    assert all(item["heat_level"] != "爆款" for item in pool["generation_chars"])
