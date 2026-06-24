from __future__ import annotations

import json
from datetime import datetime

from app.db.base import Base
from app.db.models import NamingRunModel, NamingSessionModel
from app.db.session import engine
from app.db.session import SessionLocal


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    recover_stale_running_records()


def recover_stale_running_records() -> None:
    db = SessionLocal()
    now = datetime.utcnow()
    try:
        for run in db.query(NamingRunModel).filter(NamingRunModel.status == "RUNNING").all():
            run.status = "FAILED"
            run.completed_at = now
            if not run.result_summary_json:
                run.result_summary_json = json.dumps(
                    {
                        "result_status": "GENERATION_FAILED",
                        "error_code": "STALE_RUNNING_RECOVERED",
                        "error_message": "Recovered stale RUNNING run during database startup.",
                        "counts": {"top3": 0, "backup": 0, "qualified": 0, "required": 10},
                    },
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
        for session in db.query(NamingSessionModel).filter(NamingSessionModel.status == "RUNNING").all():
            readable = (
                db.query(NamingRunModel)
                .filter(
                    NamingRunModel.session_id == session.session_id,
                    NamingRunModel.status.in_(("COMPLETED", "PARTIAL")),
                )
                .order_by(NamingRunModel.run_number.desc())
                .first()
            )
            session.status = readable.status if readable else "FAILED"
            session.error_code = "STALE_RUNNING_RECOVERED"
            session.error_message = "Recovered stale RUNNING session during database startup."
            session.updated_at = now
        db.commit()
    finally:
        db.close()
