from __future__ import annotations

import json
from pathlib import Path

from app.core.config import RUNTIME_DIR


VERSION = "1.0"


STRUCTURES: list[dict] = [
    {
        "id": "S01",
        "name": "智慧型",
        "keywords": ["智慧", "知", "思", "辨", "明", "洞察", "理性", "聪慧"],
        "semantic_roles": ["认知", "洞察"],
        "preferred_culture_sources": ["sishuwujing", "tang_poetry"],
        "source_document": "02D_STRUCTURE_LIBRARY.md",
        "version": VERSION,
    },
    {
        "id": "S02",
        "name": "君子型",
        "keywords": ["君子", "德", "仁", "义", "礼", "信", "品格", "担当"],
        "semantic_roles": ["德行", "责任"],
        "preferred_culture_sources": ["sishuwujing", "shijing"],
        "source_document": "02D_STRUCTURE_LIBRARY.md",
        "version": VERSION,
    },
    {
        "id": "S03",
        "name": "志向型",
        "keywords": ["志", "远", "鸿", "凌", "达", "理想", "志向", "开拓"],
        "semantic_roles": ["理想", "进取"],
        "preferred_culture_sources": ["chuci", "tang_poetry"],
        "source_document": "02D_STRUCTURE_LIBRARY.md",
        "version": VERSION,
    },
    {
        "id": "S04",
        "name": "光明型",
        "keywords": ["明", "昭", "晖", "曜", "晨", "光明", "希望"],
        "semantic_roles": ["光明", "希望"],
        "preferred_culture_sources": ["sishuwujing", "tang_poetry"],
        "source_document": "02D_STRUCTURE_LIBRARY.md",
        "version": VERSION,
    },
    {
        "id": "S05",
        "name": "山水型",
        "keywords": ["山", "川", "河", "云", "泽", "清", "自然", "格局"],
        "semantic_roles": ["自然", "格局"],
        "preferred_culture_sources": ["shijing", "tang_poetry", "song_ci"],
        "source_document": "02D_STRUCTURE_LIBRARY.md",
        "version": VERSION,
    },
    {
        "id": "S06",
        "name": "书卷型",
        "keywords": ["书", "文", "墨", "闻", "思", "学", "书卷", "清雅"],
        "semantic_roles": ["学问", "文气"],
        "preferred_culture_sources": ["sishuwujing", "tang_poetry", "song_ci"],
        "source_document": "02D_STRUCTURE_LIBRARY.md",
        "version": VERSION,
    },
    {
        "id": "S07",
        "name": "修身型",
        "keywords": ["修", "慎", "诚", "敬", "正", "自律", "修身"],
        "semantic_roles": ["自律", "修养"],
        "preferred_culture_sources": ["sishuwujing"],
        "source_document": "02D_STRUCTURE_LIBRARY.md",
        "version": VERSION,
    },
    {
        "id": "S08",
        "name": "温润型",
        "keywords": ["温", "润", "和", "柔", "安", "宁", "品格"],
        "semantic_roles": ["温和", "品格"],
        "preferred_culture_sources": ["shijing", "song_ci"],
        "source_document": "02D_STRUCTURE_LIBRARY.md",
        "version": VERSION,
    },
    {
        "id": "S09",
        "name": "雅致型",
        "keywords": ["雅", "清", "逸", "韵", "竹", "兰", "审美", "清雅"],
        "semantic_roles": ["审美", "雅正"],
        "preferred_culture_sources": ["shijing", "song_ci", "tang_poetry"],
        "source_document": "02D_STRUCTURE_LIBRARY.md",
        "version": VERSION,
    },
    {
        "id": "S10",
        "name": "格局型",
        "keywords": ["衡", "宥", "宇", "怀", "博", "格局", "胸怀"],
        "semantic_roles": ["胸怀", "格局"],
        "preferred_culture_sources": ["sishuwujing", "chuci"],
        "source_document": "02D_STRUCTURE_LIBRARY.md",
        "version": VERSION,
    },
    {
        "id": "S11",
        "name": "生命型",
        "keywords": ["生", "新", "萌", "荣", "华", "成长", "生命"],
        "semantic_roles": ["成长", "生机"],
        "preferred_culture_sources": ["shijing", "chuci"],
        "source_document": "02D_STRUCTURE_LIBRARY.md",
        "version": VERSION,
    },
    {
        "id": "S12",
        "name": "传承型",
        "keywords": ["承", "继", "家", "宗", "祖", "传承", "家风"],
        "semantic_roles": ["传承", "家风"],
        "preferred_culture_sources": ["sishuwujing", "shijing"],
        "source_document": "02D_STRUCTURE_LIBRARY.md",
        "version": VERSION,
    },
]


def get_structure_catalog() -> list[dict]:
    return [dict(item) for item in STRUCTURES]


def ensure_structure_catalog(output_dir: Path | None = None) -> Path:
    derived_dir = output_dir or (RUNTIME_DIR / "derived")
    derived_dir.mkdir(parents=True, exist_ok=True)
    path = derived_dir / "structure_catalog.v1.json"
    path.write_text(json.dumps(STRUCTURES, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
