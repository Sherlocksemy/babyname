from __future__ import annotations

from fastapi import Request

from app.db.session import get_db_session
from app.schemas.api_error import ApiError


def get_db():
    yield from get_db_session()


def get_orchestrator(request: Request):
    orchestrator = getattr(request.app.state, "orchestrator", None)
    if orchestrator is None or not getattr(request.app.state, "knowledge_loaded", False):
        raise ApiError("KNOWLEDGE_NOT_READY", "Knowledge base is not ready.", status_code=503)
    return orchestrator


def get_indexes(request: Request) -> dict:
    return getattr(request.app.state, "indexes", {})
