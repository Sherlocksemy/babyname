from __future__ import annotations

import json
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.db.models import CandidateModel, NamingRunModel, NamingSessionModel


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


def dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def loads(data: str | None) -> Any:
    return json.loads(data) if data else None


class NamingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_session(self, payload: dict, *, commit: bool = True) -> NamingSessionModel:
        row = NamingSessionModel(
            session_id=new_id("req"),
            status="PENDING",
            request_payload_json=dumps(payload),
        )
        self.db.add(row)
        self.db.flush()
        if commit:
            self.db.commit()
            self.db.refresh(row)
        return row

    def update_session_status(
        self,
        session_id: str,
        status: str,
        *,
        error_code: str | None = None,
        error_message: str | None = None,
        commit: bool = True,
    ) -> NamingSessionModel | None:
        row = self.get_session(session_id)
        if not row:
            return None
        row.status = status
        row.error_code = error_code
        row.error_message = error_message
        row.updated_at = datetime.utcnow()
        self.db.flush()
        if commit:
            self.db.commit()
            self.db.refresh(row)
        return row

    def create_run(self, session_id: str, run_number: int, seed: int, *, status: str = "RUNNING", commit: bool = True) -> NamingRunModel:
        row = NamingRunModel(
            run_id=new_id("run"),
            session_id=session_id,
            run_number=run_number,
            generation_seed=seed,
            status=status,
        )
        self.db.add(row)
        self.db.flush()
        if commit:
            self.db.commit()
            self.db.refresh(row)
        return row

    def complete_run(self, run_id: str, result_summary: dict, status: str = "COMPLETED", *, commit: bool = True) -> NamingRunModel:
        row = self.get_run(run_id)
        if row is None:
            raise RuntimeError(f"run not found: {run_id}")
        row.status = status
        row.result_summary_json = dumps(result_summary)
        row.completed_at = datetime.utcnow()
        self.db.flush()
        if commit:
            self.db.commit()
            self.db.refresh(row)
        return row

    def save_candidates(self, run_id: str, top3: list[dict], backup7: list[dict], *, commit: bool = True) -> list[CandidateModel]:
        rows: list[CandidateModel] = []
        for rank_type, candidates in (("TOP3", top3), ("BACKUP7", backup7)):
            for index, payload in enumerate(candidates, start=1):
                score = float((payload.get("score") or {}).get("normalized_score") or (payload.get("score") or {}).get("raw_score") or 0)
                row = CandidateModel(
                    candidate_id=new_id("cand"),
                    run_id=run_id,
                    rank_type=rank_type,
                    rank_position=index,
                    full_name=str(payload.get("full_name") or ""),
                    given_name=str(payload.get("given_name") or ""),
                    score=score,
                    candidate_payload_json=dumps(payload),
                )
                self.db.add(row)
                rows.append(row)
        self.db.flush()
        if commit:
            self.db.commit()
            for row in rows:
                self.db.refresh(row)
        return rows

    def record_failed_run(
        self,
        session_id: str,
        run_number: int,
        seed: int,
        error_code: str,
        error_message: str,
        *,
        session_status: str,
    ) -> NamingRunModel:
        run = self.create_run(session_id, run_number, seed, status="FAILED", commit=False)
        run.result_summary_json = dumps(
            {
                "result_status": "GENERATION_FAILED",
                "error_code": error_code,
                "error_message": error_message,
                "counts": {"top3": 0, "backup": 0, "qualified": 0, "required": 10},
            }
        )
        run.completed_at = datetime.utcnow()
        self.update_session_status(session_id, session_status, error_code=error_code, error_message=error_message, commit=False)
        self.db.commit()
        self.db.refresh(run)
        return run

    def get_session(self, session_id: str) -> NamingSessionModel | None:
        return self.db.get(NamingSessionModel, session_id)

    def get_run(self, run_id: str) -> NamingRunModel | None:
        return self.db.get(NamingRunModel, run_id)

    def list_runs(self, session_id: str) -> list[NamingRunModel]:
        return (
            self.db.query(NamingRunModel)
            .filter(NamingRunModel.session_id == session_id)
            .order_by(NamingRunModel.run_number.asc())
            .all()
        )

    def latest_run(self, session_id: str) -> NamingRunModel | None:
        return (
            self.db.query(NamingRunModel)
            .filter(NamingRunModel.session_id == session_id)
            .order_by(NamingRunModel.run_number.desc())
            .first()
        )

    def latest_readable_run(self, session_id: str) -> NamingRunModel | None:
        return (
            self.db.query(NamingRunModel)
            .filter(NamingRunModel.session_id == session_id, NamingRunModel.status.in_(("COMPLETED", "PARTIAL")))
            .order_by(NamingRunModel.run_number.desc())
            .first()
        )

    def list_candidates_for_run(self, run_id: str) -> list[CandidateModel]:
        return (
            self.db.query(CandidateModel)
            .filter(CandidateModel.run_id == run_id)
            .order_by(CandidateModel.rank_type.desc(), CandidateModel.rank_position.asc())
            .all()
        )

    def list_candidates_for_session(self, session_id: str) -> list[CandidateModel]:
        return (
            self.db.query(CandidateModel)
            .join(NamingRunModel, CandidateModel.run_id == NamingRunModel.run_id)
            .filter(NamingRunModel.session_id == session_id)
            .order_by(NamingRunModel.run_number.asc(), CandidateModel.rank_type.desc(), CandidateModel.rank_position.asc())
            .all()
        )

    def get_candidate_in_session(self, session_id: str, candidate_id: str) -> CandidateModel | None:
        return (
            self.db.query(CandidateModel)
            .join(NamingRunModel, CandidateModel.run_id == NamingRunModel.run_id)
            .filter(NamingRunModel.session_id == session_id, CandidateModel.candidate_id == candidate_id)
            .first()
        )

    def integrity_report(self) -> dict:
        orphan_runs = (
            self.db.query(NamingRunModel)
            .outerjoin(NamingSessionModel, NamingRunModel.session_id == NamingSessionModel.session_id)
            .filter(NamingSessionModel.session_id.is_(None))
            .count()
        )
        orphan_candidates = (
            self.db.query(CandidateModel)
            .outerjoin(NamingRunModel, CandidateModel.run_id == NamingRunModel.run_id)
            .filter(NamingRunModel.run_id.is_(None))
            .count()
        )
        empty_completed_runs = (
            self.db.query(NamingRunModel)
            .outerjoin(CandidateModel, CandidateModel.run_id == NamingRunModel.run_id)
            .filter(NamingRunModel.status.in_(("COMPLETED", "PARTIAL")))
            .group_by(NamingRunModel.run_id)
            .having(CandidateModel.candidate_id.is_(None))
            .count()
        )
        running_sessions = self.db.query(NamingSessionModel).filter(NamingSessionModel.status == "RUNNING").count()
        return {
            "orphan_runs": orphan_runs,
            "orphan_candidates": orphan_candidates,
            "empty_completed_runs": empty_completed_runs,
            "running_sessions": running_sessions,
        }
