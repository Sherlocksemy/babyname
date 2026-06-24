from app.db.session import SessionLocal
from app.repositories.naming_repository import NamingRepository


def test_sqlite_persistence_can_read_historical_result(api_generated) -> None:
    request_id = api_generated["accepted"]["request_id"]
    db = SessionLocal()
    try:
        repo = NamingRepository(db)
        session = repo.get_session(request_id)
        run = repo.latest_readable_run(request_id)
        assert session is not None
        assert run is not None
        assert repo.list_candidates_for_run(run.run_id)
    finally:
        db.close()
