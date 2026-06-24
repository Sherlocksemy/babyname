from __future__ import annotations

import re
from typing import Any


class EvidenceExcerptBuilder:
    max_display_chars = 240
    default_display_chars = 120

    def build(self, evidence: dict[str, Any] | None, matched_text: str | None) -> dict[str, Any]:
        evidence = evidence or {}
        original_text = str(evidence.get("original_text") or "")
        matched = str(matched_text or "")
        start = original_text.find(matched) if matched and original_text else -1
        exact = start >= 0
        end = start + len(matched) if exact else None
        return {
            "source_record_id": evidence.get("record_id") or evidence.get("evidence_id") or "",
            "source_type": evidence.get("source_type"),
            "book": evidence.get("book"),
            "title": evidence.get("title"),
            "author": evidence.get("author"),
            "original_text": original_text,
            "matched_text": matched,
            "match_start": start if exact else None,
            "match_end": end,
            "display_excerpt": self._excerpt(original_text, matched, start),
            "exact_match": exact,
            "matched_chars": evidence.get("matched_chars", []),
            "matched_keywords": evidence.get("matched_keywords", []),
            "evidence_level": evidence.get("evidence_level"),
            "record_id": evidence.get("record_id"),
        }

    def direct_name_evidence(self, evidence: dict[str, Any] | None, given_name: str | None) -> dict[str, Any] | None:
        excerpt = self.build(evidence, given_name)
        if (
            excerpt["exact_match"]
            and excerpt["matched_text"] == str(given_name or "")
            and excerpt["evidence_level"] == "E1"
            and len(excerpt["matched_text"]) >= 2
        ):
            return excerpt
        return None

    def _excerpt(self, original_text: str, matched_text: str, start: int) -> str:
        if not original_text:
            return ""
        compact = self._compact(original_text)
        if start < 0:
            return self._trim(compact, self.default_display_chars)
        adjusted_start = len(self._compact(original_text[:start]))
        segment = self._sentence_containing(compact, adjusted_start)
        if matched_text and matched_text not in segment:
            segment = compact
        return self._trim_around_match(segment, matched_text)

    @staticmethod
    def _compact(text: str) -> str:
        return re.sub(r"\s+", "", text)

    @staticmethod
    def _sentence_containing(text: str, start: int) -> str:
        boundaries = "。！？；;!?\\n"
        left = max(text.rfind(mark, 0, start) for mark in boundaries)
        right_candidates = [text.find(mark, start) for mark in boundaries if text.find(mark, start) >= 0]
        right = min(right_candidates) + 1 if right_candidates else len(text)
        return text[left + 1 : right].strip()

    def _trim_around_match(self, text: str, matched_text: str) -> str:
        if len(text) <= self.max_display_chars:
            return text
        index = text.find(matched_text) if matched_text else -1
        if index < 0:
            return self._trim(text, self.default_display_chars)
        half = self.default_display_chars // 2
        start = max(0, index - half)
        end = min(len(text), index + len(matched_text) + half)
        return self._trim(text[start:end], self.max_display_chars)

    @staticmethod
    def _trim(text: str, limit: int) -> str:
        if len(text) <= limit:
            return text
        return text[:limit]
