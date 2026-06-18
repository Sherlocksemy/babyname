from __future__ import annotations

import os
import subprocess
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")


def _wait_url(url: str, timeout: int = 60) -> None:
    deadline = time.time() + timeout
    last_error = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=3) as response:
                if response.status < 500:
                    return
        except Exception as exc:  # pragma: no cover - diagnostic path
            last_error = exc
        time.sleep(1)
    raise AssertionError(f"{url} not ready: {last_error}")


def _is_ready(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            return response.status < 500
    except Exception:
        return False


def test_frontend_generate_button_clicks_through_to_api():
    if not CHROME.exists():
        raise AssertionError(f"System Chrome not found: {CHROME}")

    env = os.environ.copy()
    env["CHROME_PATH"] = str(CHROME)
    env["FRONTEND_URL"] = "http://127.0.0.1:3000"
    env["NEXT_PUBLIC_API_BASE"] = "http://127.0.0.1:8000"
    backend = None
    frontend = None
    if not _is_ready("http://127.0.0.1:8000/health"):
        backend = subprocess.Popen(
            ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "127.0.0.1", "--port", "8000"],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    if not _is_ready("http://127.0.0.1:3000"):
        frontend = subprocess.Popen(
            ["npm.cmd", "run", "dev"],
            cwd=ROOT / "frontend",
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=False,
        )
    try:
        _wait_url("http://127.0.0.1:8000/health", 90)
        _wait_url("http://127.0.0.1:3000", 90)
        result = subprocess.run(
            ["node", "e2e_frontend_click.mjs"],
            cwd=ROOT / "frontend",
            env=env,
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=90,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        assert '"cardCount": 20' in result.stdout
        assert "/api/names/generate" in result.stdout
    finally:
        if frontend:
            frontend.terminate()
        if backend:
            backend.terminate()
