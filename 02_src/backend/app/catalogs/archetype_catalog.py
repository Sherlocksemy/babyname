from __future__ import annotations

import json
from pathlib import Path

from app.core.config import RUNTIME_DIR


VERSION = "1.0"


ARCHETYPES: list[dict] = [
    {"id": "A01", "name": "书卷学者", "keywords": ["书卷", "学问", "知性", "深度", "理性"], "semantic_roles": ["学问", "洞察"], "preferred_culture_sources": ["sishuwujing"], "source_document": "02C_ARCHETYPE_SCORING_MATRIX.md", "version": VERSION},
    {"id": "A02", "name": "思想家", "keywords": ["思想", "洞察", "远见", "山水"], "semantic_roles": ["洞察", "思辨"], "preferred_culture_sources": ["sishuwujing", "tang_poetry"], "source_document": "02C_ARCHETYPE_SCORING_MATRIX.md", "version": VERSION},
    {"id": "A03", "name": "君子人格", "keywords": ["君子", "德行", "责任", "修养"], "semantic_roles": ["德行", "修养"], "preferred_culture_sources": ["sishuwujing", "shijing"], "source_document": "02C_ARCHETYPE_SCORING_MATRIX.md", "version": VERSION},
    {"id": "A04", "name": "领导者", "keywords": ["担当", "责任", "格局", "领导"], "semantic_roles": ["担当", "格局"], "preferred_culture_sources": ["sishuwujing"], "source_document": "02C_ARCHETYPE_SCORING_MATRIX.md", "version": VERSION},
    {"id": "A05", "name": "开拓者", "keywords": ["创造", "志向", "开拓", "进取"], "semantic_roles": ["创造", "进取"], "preferred_culture_sources": ["chuci", "tang_poetry"], "source_document": "02C_ARCHETYPE_SCORING_MATRIX.md", "version": VERSION},
    {"id": "A06", "name": "战略家", "keywords": ["战略", "远见", "山水", "格局"], "semantic_roles": ["远见", "布局"], "preferred_culture_sources": ["chuci", "sishuwujing"], "source_document": "02C_ARCHETYPE_SCORING_MATRIX.md", "version": VERSION},
    {"id": "A07", "name": "修行者", "keywords": ["修行", "精进", "自律", "山水"], "semantic_roles": ["精进", "自律"], "preferred_culture_sources": ["sishuwujing", "shijing"], "source_document": "02C_ARCHETYPE_SCORING_MATRIX.md", "version": VERSION},
    {"id": "A08", "name": "教育者", "keywords": ["启发", "光明", "温润", "教育"], "semantic_roles": ["启发", "温和"], "preferred_culture_sources": ["sishuwujing"], "source_document": "02C_ARCHETYPE_SCORING_MATRIX.md", "version": VERSION},
    {"id": "A09", "name": "雅士人格", "keywords": ["雅士", "审美", "清雅", "山水"], "semantic_roles": ["审美", "雅正"], "preferred_culture_sources": ["shijing", "song_ci"], "source_document": "02C_ARCHETYPE_SCORING_MATRIX.md", "version": VERSION},
    {"id": "A10", "name": "理想主义者", "keywords": ["理想", "希望", "光明", "生命"], "semantic_roles": ["希望", "理想"], "preferred_culture_sources": ["chuci", "tang_poetry"], "source_document": "02C_ARCHETYPE_SCORING_MATRIX.md", "version": VERSION},
    {"id": "A11", "name": "成长者", "keywords": ["成长", "生命力", "修身"], "semantic_roles": ["成长", "修养"], "preferred_culture_sources": ["shijing", "chuci"], "source_document": "02C_ARCHETYPE_SCORING_MATRIX.md", "version": VERSION},
    {"id": "A12", "name": "家族传承者", "keywords": ["传承", "家族", "家风", "君子"], "semantic_roles": ["传承", "家风"], "preferred_culture_sources": ["sishuwujing", "shijing"], "source_document": "02C_ARCHETYPE_SCORING_MATRIX.md", "version": VERSION},
]


def get_archetype_catalog() -> list[dict]:
    return [dict(item) for item in ARCHETYPES]


def ensure_archetype_catalog(output_dir: Path | None = None) -> Path:
    derived_dir = output_dir or (RUNTIME_DIR / "derived")
    derived_dir.mkdir(parents=True, exist_ok=True)
    path = derived_dir / "archetype_catalog.v1.json"
    path.write_text(json.dumps(ARCHETYPES, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
