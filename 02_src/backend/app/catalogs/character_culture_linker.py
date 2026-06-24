from __future__ import annotations

import re

from app.indexes.culture_index import CultureIndex


SENTENCE_SPLIT_RE = re.compile(r"[。！？；，、\n\r]")


class CharacterCultureLinker:
    def __init__(self, culture_index: CultureIndex | None = None) -> None:
        self.culture_index = culture_index or CultureIndex()

    def links_for_char(self, char: str, limit: int = 6) -> list[dict]:
        links: list[dict] = []
        for record in self.culture_index.by_char(char, limit=limit * 3):
            content = str(record.get("content") or "")
            if char not in content:
                continue
            source_record_id = str(record.get("id") or "")
            matched_text = self._sentence_with_char(content, char)
            links.append(
                {
                    "char": char,
                    "source_type": str(record.get("source") or ""),
                    "source_record_id": source_record_id,
                    "title": record.get("title") or "",
                    "author": record.get("author") or "",
                    "dynasty": record.get("dynasty") or "",
                    "matched_text": matched_text,
                    "display_excerpt": self._excerpt(matched_text, char),
                    "exact_match": True,
                    "keywords": list(record.get("keywords") or []),
                }
            )
            if len(links) >= limit:
                break
        return links

    @staticmethod
    def _sentence_with_char(content: str, char: str) -> str:
        for sentence in SENTENCE_SPLIT_RE.split(content):
            if char in sentence:
                return sentence.strip()
        index = content.find(char)
        if index < 0:
            return ""
        start = max(0, index - 18)
        end = min(len(content), index + 19)
        return content[start:end]

    @staticmethod
    def _excerpt(text: str, char: str, radius: int = 16) -> str:
        if len(text) <= radius * 2 + 1:
            return text
        index = text.find(char)
        if index < 0:
            return text[: radius * 2 + 1]
        start = max(0, index - radius)
        end = min(len(text), index + radius + 1)
        prefix = "..." if start else ""
        suffix = "..." if end < len(text) else ""
        return f"{prefix}{text[start:end]}{suffix}"

