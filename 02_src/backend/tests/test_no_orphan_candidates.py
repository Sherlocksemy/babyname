from app.db.session import SessionLocal
from app.repositories.naming_repository import NamingRepository


def test_no_orphan_candidates() -> None:
    db = SessionLocal()
    try:
        report = NamingRepository(db).integrity_report()
        assert report["orphan_runs"] == 0
        assert report["orphan_candidates"] == 0
    finally:
        db.close()
