from __future__ import annotations

from app.core.knowledge_loader import KnowledgeLoader


class PopularityIndex:
    def __init__(self, loader: KnowledgeLoader | None = None) -> None:
        self.loader = loader or KnowledgeLoader()
        self.datasets = self.loader.load_all()
        self.char_frequency = {row["char"]: row for row in self.datasets["char_frequency"].data if row.get("char")}
        self.name_blacklist = {row["name"]: row for row in self.datasets["top_names_blacklist"].data if row.get("name")}

    def get_char(self, char: str) -> dict | None:
        return self.char_frequency.get(char)

    def get_name(self, name: str) -> dict | None:
        return self.name_blacklist.get(name)

    def is_blacklisted(self, name: str) -> bool:
        return name in self.name_blacklist

    def hot_chars(self, heat_levels: set[str] | None = None) -> list[dict]:
        levels = heat_levels or {"高", "爆款"}
        return [row for row in self.char_frequency.values() if row.get("heat_level") in levels]
