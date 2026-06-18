from backend.app.engines.char_pool_builder import CharPoolBuilder
from backend.app.engines.culture_retriever import CultureRetriever
from backend.app.engines.name_composer import NameComposer
from backend.app.schemas.baby_profile import BabyProfileRequest
from backend.app.services.baby_profile_service import BabyProfileService
from backend.app.services.char_service import CharService


def test_name_composer_generates_unique_single_and_double_names():
    profile = BabyProfileService().normalize(BabyProfileRequest(surname="陈", name_length=2, liked_chars=["清"]))
    pools = CharPoolBuilder(CharService(), CultureRetriever()).build(profile)
    names = NameComposer().compose(profile, pools["generation_chars"], limit=50)
    assert names
    assert all(len(given) == 2 for given, _ in names)
    assert all(chars[0]["char"] != chars[1]["char"] for _, chars in names)

    single_profile = profile.model_copy(update={"name_length": 1})
    single_names = NameComposer().compose(single_profile, pools["generation_chars"], limit=20)
    assert single_names
    assert all(len(given) == 1 for given, _ in single_names)
