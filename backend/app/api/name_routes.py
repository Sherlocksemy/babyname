from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.app.core.knowledge_loader import KnowledgeLoader
from backend.app.core.store import store
from backend.app.schemas.baby_profile import BabyProfileRequest
from backend.app.schemas.response import FavoriteRequest, RegenerateRequest
from backend.app.services.name_service import NameService


router = APIRouter()
service = NameService()


@router.get("/health")
def health() -> dict:
    audit = KnowledgeLoader().audit(write_report=False)
    return {"ok": audit["status"] in {"ok", "warning"}, "knowledge_status": audit["status"]}


@router.get("/api/knowledge/audit")
def knowledge_audit() -> dict:
    return KnowledgeLoader().audit(write_report=True)


@router.post("/api/names/generate")
def generate_names(payload: BabyProfileRequest):
    try:
        return service.generate(payload)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail={"code": "KNOWLEDGE_MISSING", "message": str(exc)}) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail={"code": "INVALID_INPUT", "message": str(exc)}) from exc


@router.get("/api/names/{request_id}/{name}")
def name_detail(request_id: str, name: str):
    item = service.detail(request_id, name)
    if not item:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "名字详情不存在"})
    return item


@router.post("/api/names/regenerate")
def regenerate(payload: RegenerateRequest):
    response = service.regenerate(payload)
    if not response:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "原请求不存在"})
    return response


@router.post("/api/favorites")
def add_favorite(payload: FavoriteRequest):
    item = service.detail(payload.request_id, payload.name)
    if not item:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "收藏的名字不存在"})
    store.add_favorite({"request_id": payload.request_id, "name": payload.name, "detail": item.model_dump()})
    return {"ok": True}


@router.get("/api/favorites")
def favorites():
    return {"favorites": store.favorites()}

