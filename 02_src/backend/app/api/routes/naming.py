from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_indexes, get_orchestrator
from app.schemas.api_request import NamingGenerateRequest, RegenerateRequest
from app.services.naming_application_service import NamingApplicationService


router = APIRouter(prefix="/api/v1/names", tags=["naming"])


@router.post("/generate", status_code=status.HTTP_202_ACCEPTED)
def generate_names(
    request: NamingGenerateRequest,
    db: Session = Depends(get_db),
    orchestrator=Depends(get_orchestrator),
    indexes: dict = Depends(get_indexes),
) -> dict:
    return NamingApplicationService(db, orchestrator, indexes).generate(request)


@router.get("/{request_id}")
def get_result(
    request_id: str,
    db: Session = Depends(get_db),
    orchestrator=Depends(get_orchestrator),
    indexes: dict = Depends(get_indexes),
) -> dict:
    return NamingApplicationService(db, orchestrator, indexes).get_result(request_id)


@router.get("/{request_id}/candidates/{candidate_id}")
def get_candidate_detail(
    request_id: str,
    candidate_id: str,
    db: Session = Depends(get_db),
    orchestrator=Depends(get_orchestrator),
    indexes: dict = Depends(get_indexes),
) -> dict:
    return NamingApplicationService(db, orchestrator, indexes).get_candidate_detail(request_id, candidate_id)


@router.post("/{request_id}/regenerate", status_code=status.HTTP_202_ACCEPTED)
def regenerate_names(
    request_id: str,
    request: RegenerateRequest | None = None,
    db: Session = Depends(get_db),
    orchestrator=Depends(get_orchestrator),
    indexes: dict = Depends(get_indexes),
) -> dict:
    return NamingApplicationService(db, orchestrator, indexes).regenerate(request_id, request or RegenerateRequest())
