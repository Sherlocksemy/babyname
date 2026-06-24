from __future__ import annotations

from app.core.knowledge_loader import KnowledgeLoader


class CharacterIndex:
    def __init__(self, loader: KnowledgeLoader | None = None, datasets: dict | None = None) -> None:
        self.loader = loader or KnowledgeLoader()
        self.datasets = datasets or self.loader.load_all()
        self.compliance = {row["char"]: row for row in self.datasets["compliance_hanzi"].data if row.get("char")}
        self.base = {row["char"]: row for row in self.datasets["char_base_info"].data if row.get("char")}
        self.semantic = self.datasets["char_semantic"].data
        self.kangxi = self.datasets["kangxi_strokes"].data
        self.mandarin = self.datasets["mandarin_pinyin"].data
        self.popularity = {row["char"]: row for row in self.datasets["char_frequency"].data if row.get("char")}

    def get(self, char: str) -> dict:
        return {
            "char": char,
            "is_compliant": char in self.compliance,
            "compliance": self.compliance.get(char),
            "base": self.base.get(char),
            "semantic": self.semantic.get(char),
            "kangxi": self.kangxi.get(char),
            "mandarin": self.mandarin.get(char, []),
            "popularity": self.popularity.get(char),
        }

    def is_compliant(self, char: str) -> bool:
        return char in self.compliance
