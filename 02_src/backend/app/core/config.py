from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[4]
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "01_knowledge_base"
DOCS_DIR = PROJECT_ROOT / "04_docs_v5"
BACKEND_DIR = PROJECT_ROOT / "02_src" / "backend"
RUNTIME_DIR = BACKEND_DIR / "runtime"
REPORTS_DIR = PROJECT_ROOT / "reports"


def ensure_runtime_dirs() -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
