from app.db.session import SessionLocal
from app.repositories.naming_repository import NamingRepository


def test_regenerate_session_not_stuck_running(api_generated) -> None:
    request_id = api_generated["accepted"]["request_id"]
    db = SessionLocal()
    try:
        session = NamingRepository(db).get_session(request_id)
        assert session is not None
        assert session.status != "RUNNING"
    finally:
        db.close()
