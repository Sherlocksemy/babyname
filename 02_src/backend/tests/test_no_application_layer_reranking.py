import pytest

from app.services.naming_application_service import NamingApplicationService


def test_application_layer_reranking_is_disabled() -> None:
    with pytest.raises(RuntimeError):
        NamingApplicationService._select_visible_candidates({"top20": []}, set())
