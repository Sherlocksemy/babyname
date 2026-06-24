from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.repositories.favorite_repository import FavoriteRepository
from app.repositories.naming_repository import NamingRepository
from app.schemas.api_error import ApiError
from app.schemas.api_request import FavoriteCreateRequest
from app.services.candidate_detail_service import CandidateDetailService


router = APIRouter(prefix="/api/v1/favorites", tags=["favorites"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_favorite(request: FavoriteCreateRequest, db: Session = Depends(get_db)) -> dict:
    naming_repo = NamingRepository(db)
    session = naming_repo.get_session(request.request_id)
    if session is None:
        raise ApiError("SESSION_NOT_FOUND", "Naming session not found.", status_code=404)
    candidate = naming_repo.get_candidate_in_session(request.request_id, request.candidate_id)
    if candidate is None:
        raise ApiError("CANDIDATE_NOT_FOUND", "Candidate not found in this naming session.", status_code=404)
    favorite = FavoriteRepository(db).create(request.request_id, request.candidate_id)
    return {
        "favorite_id": favorite.favorite_id,
        "request_id": favorite.session_id,
        "candidate_id": favorite.candidate_id,
        "created_at": favorite.created_at.isoformat(),
        "candidate": CandidateDetailService().to_card(candidate),
    }


@router.get("")
def list_favorites(request_id: str, db: Session = Depends(get_db)) -> dict:
    naming_repo = NamingRepository(db)
    if naming_repo.get_session(request_id) is None:
        raise ApiError("SESSION_NOT_FOUND", "Naming session not found.", status_code=404)
    favorites = FavoriteRepository(db).list_by_session(request_id)
    items = []
    detail_service = CandidateDetailService()
    for favorite in favorites:
        candidate = naming_repo.get_candidate_in_session(request_id, favorite.candidate_id)
        items.append(
            {
                "favorite_id": favorite.favorite_id,
                "request_id": favorite.session_id,
                "candidate_id": favorite.candidate_id,
                "created_at": favorite.created_at.isoformat(),
                "candidate": detail_service.to_card(candidate) if candidate else None,
            }
        )
    return {"request_id": request_id, "favorites": items}


@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite(favorite_id: str, db: Session = Depends(get_db)) -> Response:
    deleted = FavoriteRepository(db).delete(favorite_id)
    if not deleted:
        raise ApiError("CANDIDATE_NOT_FOUND", "Favorite not found.", status_code=404)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
