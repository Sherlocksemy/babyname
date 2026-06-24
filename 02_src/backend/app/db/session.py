from __future__ import annotations

import os

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.core.config import RUNTIME_DIR, ensure_runtime_dirs


def default_database_url() -> str:
    ensure_runtime_dirs()
    return f"sqlite:///{(RUNTIME_DIR / 'yiyuan_mvp.sqlite3').as_posix()}"


DATABASE_URL = os.getenv("DATABASE_URL", default_database_url())
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)


@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record) -> None:
    if DATABASE_URL.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
