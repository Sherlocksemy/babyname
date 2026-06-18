#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch and verify small GitHub supplement sources used by the build.

Large corpus downloads are intentionally not handled through MCP or this file.
The GitHub MCP service is used interactively to confirm repositories and key
files; this script keeps local raw-file caches reproducible and cheap.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SUP = ROOT / "00_raw_repos" / "07_github_supplement"

RAW_FILES = [
    {
        "name": "johnwu1114/chinese-name ChineseCharacters.json",
        "url": "https://raw.githubusercontent.com/johnwu1114/chinese-name/master/ChineseCharacters.json",
        "path": SUP / "johnwu1114-chinese-name" / "ChineseCharacters.json",
        "sha256": None,
    },
]

LOCAL_REQUIRED = [
    SUP / "shuowenjiezi-shuowen" / "data",
    SUP / "NiuTrans-Classical-Modern-bilingual",
    SUP / "yht050511-gushiwen" / "gushiwen.json.gz",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def valid_json(path: Path) -> bool:
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except Exception:
        return False


def fetch(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "baby-name-system-data-builder"})
    with urlopen(req, timeout=60) as resp:
        return resp.read()


def handle_raw_file(item: dict[str, object], dry_run: bool) -> dict[str, object]:
    path = Path(item["path"])
    exists = path.exists()
    current_sha = sha256(path) if exists else ""
    status = "cached" if exists else "missing"
    if exists and path.suffix == ".json" and not valid_json(path):
        status = "invalid-json"
    if item.get("sha256") and current_sha and current_sha != item["sha256"]:
        status = "sha-mismatch"

    if status != "cached" and not dry_run:
        data = fetch(str(item["url"]))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        status = "downloaded"
        current_sha = sha256(path)

    return {
        "name": item["name"],
        "path": str(path),
        "status": status,
        "sha256": current_sha,
        "bytes": path.stat().st_size if path.exists() else 0,
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Report cache state without downloading.")
    args = parser.parse_args(argv)

    SUP.mkdir(parents=True, exist_ok=True)
    report = {"raw_files": [], "local_required": []}
    for item in RAW_FILES:
        report["raw_files"].append(handle_raw_file(item, args.dry_run))
    for path in LOCAL_REQUIRED:
        report["local_required"].append(
            {
                "path": str(path),
                "exists": path.exists(),
                "files": sum(1 for _ in path.rglob("*") if _.is_file()) if path.is_dir() else (1 if path.exists() else 0),
            }
        )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
