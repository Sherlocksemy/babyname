from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.db.models import FavoriteModel


class FavoriteRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, session_id: str, candidate_id: str) -> FavoriteModel:
        existing = self.get_by_session_candidate(session_id, candidate_id)
        if existing:
            return existing
        row = FavoriteModel(
            favorite_id=f"fav_{uuid.uuid4().hex}",
            session_id=session_id,
            candidate_id=candidate_id,
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def list_by_session(self, session_id: str) -> list[FavoriteModel]:
        return (
            self.db.query(FavoriteModel)
            .filter(FavoriteModel.session_id == session_id)
            .order_by(FavoriteModel.created_at.asc())
            .all()
        )

    def get(self, favorite_id: str) -> FavoriteModel | None:
        return self.db.get(FavoriteModel, favorite_id)

    def get_by_session_candidate(self, session_id: str, candidate_id: str) -> FavoriteModel | None:
        return (
            self.db.query(FavoriteModel)
            .filter(FavoriteModel.session_id == session_id, FavoriteModel.candidate_id == candidate_id)
            .first()
        )

    def delete(self, favorite_id: str) -> bool:
        row = self.get(favorite_id)
        if row is None:
            return False
        self.db.delete(row)
        self.db.commit()
        return True
