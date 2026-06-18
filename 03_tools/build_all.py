#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run all extractors in dependency order."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

STEPS = [
    "fetch_github_supplements",
    "extract_tongyong_hanzi",
    "extract_char_attributes",
    "extract_pronunciation_data",
    "process_poetry_data",
    "process_name_popularity",
    "extract_numerology_rules",
    "validate_outputs",
]


def main() -> None:
    for step in STEPS:
        print(f"\n==> {step}")
        module = importlib.import_module(step)
        module.main()
    print("\nAll knowledge-base layers built successfully.")


if __name__ == "__main__":
    main()
