from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def now_utc() -> datetime:
    return datetime.utcnow()


class NamingSessionModel(Base):
    __tablename__ = "naming_sessions"

    session_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    status: Mapped[str] = mapped_column(String(24), index=True)
    request_payload_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc, onupdate=now_utc)
    error_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    runs: Mapped[list["NamingRunModel"]] = relationship(back_populates="session", cascade="all, delete-orphan")


class NamingRunModel(Base):
    __tablename__ = "naming_runs"

    run_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("naming_sessions.session_id", ondelete="CASCADE"), index=True)
    run_number: Mapped[int] = mapped_column(Integer)
    generation_seed: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(24), index=True)
    result_summary_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    session: Mapped[NamingSessionModel] = relationship(back_populates="runs")
    candidates: Mapped[list["CandidateModel"]] = relationship(back_populates="run", cascade="all, delete-orphan")


class CandidateModel(Base):
    __tablename__ = "candidates"

    candidate_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("naming_runs.run_id", ondelete="CASCADE"), index=True)
    rank_type: Mapped[str] = mapped_column(String(16), index=True)
    rank_position: Mapped[int] = mapped_column(Integer)
    full_name: Mapped[str] = mapped_column(String(16), index=True)
    given_name: Mapped[str] = mapped_column(String(8), index=True)
    score: Mapped[float] = mapped_column()
    candidate_payload_json: Mapped[str] = mapped_column(Text)

    run: Mapped[NamingRunModel] = relationship(back_populates="candidates")


class FavoriteModel(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("session_id", "candidate_id", name="uq_favorite_session_candidate"),)

    favorite_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("naming_sessions.session_id", ondelete="CASCADE"), index=True)
    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.candidate_id", ondelete="CASCADE"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)
