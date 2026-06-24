from __future__ import annotations

import os
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[2]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.error_handlers import install_error_handlers
from app.api.routes.favorites import router as favorites_router
from app.api.routes.health import router as health_router
from app.api.routes.naming import router as naming_router
from app.core.knowledge_loader import KnowledgeLoader
from app.db.init_db import init_db
from app.indexes.character_index import CharacterIndex
from app.indexes.culture_index import CultureIndex
from app.indexes.popularity_index import PopularityIndex
from app.indexes.pronunciation_index import PronunciationIndex
from app.orchestration.naming_alpha_orchestrator import NamingAlphaOrchestrator


@asynccontextmanager
async def lifespan(app: FastAPI):
    startup_started = time.perf_counter()
    app.state.knowledge_loaded = False
    app.state.startup_error = None
    init_db()
    try:
        knowledge_started = time.perf_counter()
        loader = KnowledgeLoader()
        datasets = loader.load_all()
        app.state.knowledge_load_elapsed_ms = round((time.perf_counter() - knowledge_started) * 1000, 2)
        app.state.dataset_counts = {name: dataset.row_count for name, dataset in datasets.items()}
        app.state.indexes = {
            "character": CharacterIndex(loader, datasets),
            "culture": CultureIndex(loader, datasets),
            "pronunciation": PronunciationIndex(loader, datasets),
            "popularity": PopularityIndex(loader, datasets),
        }
        app.state.orchestrator = NamingAlphaOrchestrator()
        app.state.knowledge_loaded = True
    except Exception as exc:
        app.state.startup_error = str(exc)
        app.state.indexes = {}
        app.state.orchestrator = None
    app.state.startup_elapsed_ms = round((time.perf_counter() - startup_started) * 1000, 2)
    yield


app = FastAPI(title="Yiyuan Naming Pro MVP", version="0.3.0", lifespan=lifespan)
frontend_origins = [
    origin.strip()
    for origin in os.getenv("FRONTEND_ORIGIN", "http://localhost:3000,http://127.0.0.1:3000").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
install_error_handlers(app)
app.include_router(health_router)
app.include_router(naming_router)
app.include_router(favorites_router)
