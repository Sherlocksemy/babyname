#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""项目统一入口。

直接运行本文件可看到完整取名流程演示。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from name_generator import NameGenerator, NameRequest, generate_names


def run_demo() -> dict:
    """命令行演示：构造样例参数并输出候选姓名。"""
    project_root = Path(__file__).resolve().parents[1]
    engine = NameGenerator(project_root)
    request = NameRequest(
        surname="陈",
        gender="N",
        birth_time="2024-05-20 09:30",
        preferred_elements=["木", "水"],
        banned_chars=["伟", "强", "梓"],
        culture_preference="shijing",
        max_heat="高",
        avoid_teochew_homophone=True,
        page=1,
        page_size=10,
        candidate_limit=100,
    )
    return engine.generate(request)


def run_function_demo() -> dict:
    """函数调用示例，便于后续被 API 层复用。"""
    return generate_names(
        surname="林",
        gender="F",
        birth_time="2025-03-12 08:20",
        preferred_elements=["水", "木"],
        banned_chars=["丽", "娜"],
        culture_preference="sishuwujing",
        max_heat="高",
        avoid_teochew_homophone=True,
        page=1,
        page_size=5,
        candidate_limit=80,
    )


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    result = run_demo()
    print("=== 新生儿文化取名系统 Demo ===")
    print(json.dumps(result, ensure_ascii=False, indent=2)[:6000])
    print("\n=== 函数调用示例，前 1000 字 ===")
    print(json.dumps(run_function_demo(), ensure_ascii=False, indent=2)[:1000])
