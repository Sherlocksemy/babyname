from __future__ import annotations

from fastapi import APIRouter, Request


router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/ready")
def ready(request: Request) -> dict:
    state = request.app.state
    loaded = bool(getattr(state, "knowledge_loaded", False))
    return {
        "status": "ready" if loaded else "not_ready",
        "knowledge_loaded": loaded,
        "datasets": getattr(state, "dataset_counts", {}),
        "engine_version": "MVP_ALPHA_M3",
        "nes_version": "NES_MVP_2.0",
        "startup_elapsed_ms": getattr(state, "startup_elapsed_ms", None),
        "knowledge_load_elapsed_ms": getattr(state, "knowledge_load_elapsed_ms", None),
    }
