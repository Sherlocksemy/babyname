from __future__ import annotations

import re
from collections import defaultdict

from app.core.dataset_registry import CULTURE_DATASETS
from app.core.knowledge_loader import KnowledgeLoader


HANZI_RE = re.compile(r"[\u4e00-\u9fff]")
SENTENCE_SPLIT_RE = re.compile(r"[。！？；，、\n\r]")


class CultureIndex:
    def __init__(self, loader: KnowledgeLoader | None = None) -> None:
        self.loader = loader or KnowledgeLoader()
        self.datasets = self.loader.load_all()
        self.records: list[dict] = []
        self.by_id: dict[str, dict] = {}
        self.char_index: dict[str, list[dict]] = defaultdict(list)
        self.bigram_index: dict[str, list[dict]] = defaultdict(list)
        self.title_index: dict[str, list[dict]] = defaultdict(list)
        self.keyword_index: dict[str, list[dict]] = defaultdict(list)
        self.source_index: dict[str, list[dict]] = defaultdict(list)
        self._build()

    def _build(self) -> None:
        for source in CULTURE_DATASETS:
            dataset = self.datasets[source]
            for record in dataset.data:
                enriched = dict(record)
                enriched["source"] = source
                self.records.append(enriched)
                record_id = str(enriched.get("id") or f"{source}:{len(self.records)}")
                self.by_id[record_id] = enriched
                self.source_index[source].append(enriched)
                if enriched.get("dynasty"):
                    self.source_index[str(enriched["dynasty"])].append(enriched)
                if enriched.get("title"):
                    self.title_index[str(enriched["title"])].append(enriched)
                for keyword in enriched.get("keywords") or []:
                    self.keyword_index[str(keyword)].append(enriched)
                self._index_text(enriched)

    def _index_text(self, record: dict) -> None:
        text = str(record.get("content") or "")
        for candidate in record.get("name_candidates") or []:
            text += str(candidate)
        for char in set(HANZI_RE.findall(text)):
            self.char_index[char].append(record)
        for sentence in SENTENCE_SPLIT_RE.split(str(record.get("content") or "")):
            chars = HANZI_RE.findall(sentence)
            for index in range(len(chars) - 1):
                self.bigram_index[chars[index] + chars[index + 1]].append(record)

    def by_char(self, char: str, limit: int = 10) -> list[dict]:
        return list(self.char_index.get(char, []))[:limit]

    def by_bigram(self, bigram: str, limit: int = 10) -> list[dict]:
        return list(self.bigram_index.get(bigram, []))[:limit]

    def by_title(self, title: str, limit: int = 10) -> list[dict]:
        return list(self.title_index.get(title, []))[:limit]

    def by_keyword(self, keyword: str, limit: int = 10) -> list[dict]:
        return list(self.keyword_index.get(keyword, []))[:limit]

    def by_source(self, source: str, limit: int = 10) -> list[dict]:
        return list(self.source_index.get(source, []))[:limit]
