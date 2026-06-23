from __future__ import annotations

import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = PROJECT_ROOT / "02_src"
BACKEND_DIR = SRC_DIR / "backend"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


@pytest.fixture(scope="session")
def alpha_input() -> dict:
    return {
        "surname": "林",
        "gender": "male",
        "birth_date": "2025-03-01",
        "birth_time": "08:30",
        "birth_location": "广东省汕头市",
        "region": "teochew",
        "style_preferences": ["书卷清雅", "君子品格"],
        "liked_chars": [],
        "blocked_chars": [],
        "generation_seed": 20260622,
    }


@pytest.fixture(scope="session")
def alpha_result(alpha_input):
    from app.orchestration.naming_alpha_orchestrator import NamingAlphaOrchestrator

    return NamingAlphaOrchestrator().run(alpha_input)


@pytest.fixture(scope="session")
def milestone_1_3_results():
    from app.cli.run_milestone_1_3 import MATRIX_A_CASES, MATRIX_B_CASES, overlap_metrics, run_cases
    from app.orchestration.naming_alpha_orchestrator import NamingAlphaOrchestrator

    orchestrator = NamingAlphaOrchestrator()
    matrix_a = run_cases(MATRIX_A_CASES, orchestrator)
    matrix_b = run_cases(MATRIX_B_CASES, orchestrator)
    return {
        "matrix_a": matrix_a,
        "matrix_b": matrix_b,
        "matrix_a_overlap": overlap_metrics(matrix_a),
        "matrix_b_overlap": overlap_metrics(matrix_b),
    }
