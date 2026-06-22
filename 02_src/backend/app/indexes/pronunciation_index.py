from __future__ import annotations

from collections import defaultdict

from app.core.knowledge_loader import KnowledgeLoader


class PronunciationIndex:
    def __init__(self, loader: KnowledgeLoader | None = None) -> None:
        self.loader = loader or KnowledgeLoader()
        self.datasets = self.loader.load_all()
        self.mandarin = self.datasets["mandarin_pinyin"].data
        self.teochew: dict[str, list[dict]] = defaultdict(list)
        self.homophone_risks: dict[str, list[dict]] = defaultdict(list)
        for row in self.datasets["teochew_pronunciation"].data:
            if row.get("char"):
                self.teochew[row["char"]].append(row)
        for row in self.datasets["homophone_blacklist"].data:
            if row.get("char"):
                self.homophone_risks[row["char"]].append(row)

    def get(self, char: str) -> dict:
        return {
            "char": char,
            "mandarin": self.mandarin.get(char, []),
            "teochew": list(self.teochew.get(char, [])),
            "homophone_risks": list(self.homophone_risks.get(char, [])),
        }

    def teochew_readings(self, char: str) -> list[dict]:
        return list(self.teochew.get(char, []))

    def risks(self, char: str) -> list[dict]:
        return list(self.homophone_risks.get(char, []))
