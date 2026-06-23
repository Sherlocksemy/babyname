from __future__ import annotations

import hashlib
from collections import OrderedDict

from app.engines.evidence_suitability_evaluator import EvidenceSuitabilityEvaluator
from app.indexes.culture_index import CultureIndex
from app.schemas.candidate import CultureEvidence


class CultureRetriever:
    SOURCE_LABELS = {
        "shijing": "诗经",
        "chuci": "楚辞",
        "tang_poetry": "唐诗",
        "song_ci": "宋词",
        "sishuwujing": "四书五经",
    }

    def __init__(self, culture_index: CultureIndex | None = None) -> None:
        self.index = culture_index or CultureIndex()
        self.suitability_evaluator = EvidenceSuitabilityEvaluator()

    def retrieve(self, structures: list[dict], archetypes: list[dict], style_preferences: list[str], limit: int = 80) -> list[CultureEvidence]:
        keywords: list[str] = []
        sources: list[str] = []
        for item in structures + archetypes:
            keywords.extend(item.get("keywords", []))
            keywords.extend(item.get("semantic_roles", []))
            sources.extend(item.get("preferred_culture_sources", []))
        keywords.extend(style_preferences)
        keywords = self._dedupe([keyword for keyword in keywords if keyword])
        sources = self._dedupe(sources + list(self.SOURCE_LABELS.keys()))

        evidences: OrderedDict[str, CultureEvidence] = OrderedDict()
        for source in sources:
            for record in self.index.by_source(source, limit=10):
                self._add_evidence(evidences, record, [], [], "source_priority", 0.58)
        for keyword in keywords:
            for record in self.index.by_keyword(keyword, limit=12):
                self._add_evidence(evidences, record, [keyword], [], "keyword", 0.78)
        for keyword in keywords:
            if len(keyword) == 1:
                for record in self.index.by_char(keyword, limit=8):
                    self._add_evidence(evidences, record, [], [keyword], "single_char", 0.64)
        return list(evidences.values())[:limit]

    def evidence_for_name(self, given_name: str, limit: int = 5) -> list[CultureEvidence]:
        evidences: OrderedDict[str, CultureEvidence] = OrderedDict()
        direct = self.index.by_bigram(given_name, limit=limit)
        for record in direct:
            self._add_evidence(evidences, record, [], list(given_name), "direct_bigram_same_sentence", 0.95)
        if len(evidences) < limit:
            first_records = {id(record): record for record in self.index.by_char(given_name[0], limit=80)}
            for record in self.index.by_char(given_name[1], limit=80):
                if id(record) in first_records:
                    self._add_evidence(evidences, record, [], list(given_name), "two_chars_same_record", 0.74)
                    if len(evidences) >= limit:
                        break
        ranked = list(evidences.values())[:limit]
        for evidence in ranked:
            result = self.suitability_evaluator.evaluate(given_name, evidence.to_dict(), "", "")
            evidence.evidence_level = result["evidence_level"]
            evidence.suitability = result
            evidence.confidence = max(evidence.confidence, result["evidence_suitability_score"] / 100)
        return ranked

    def evidence_for_char(self, char: str, limit: int = 3) -> list[CultureEvidence]:
        evidences: OrderedDict[str, CultureEvidence] = OrderedDict()
        for record in self.index.by_char(char, limit=limit * 8):
            self._add_evidence(evidences, record, [], [char], "single_char_composition", 0.68)
            if len(evidences) >= limit:
                break
        ranked = list(evidences.values())[:limit]
        for evidence in ranked:
            evidence.evidence_level = "E2"
            evidence.suitability = {
                "evidence_level": "E2",
                "phrase_complete": False,
                "semantic_dependency": False,
                "context_support": True,
                "nameability": True,
                "reason_codes": ["SINGLE_CHAR_CULTURE_TRACE"],
                "passed": True,
                "evidence_suitability_score": 76,
                "semantic": {},
            }
            evidence.confidence = max(evidence.confidence, 0.76)
        return ranked

    def evidence_map(self, evidences: list[CultureEvidence]) -> dict[str, CultureEvidence]:
        return {item.evidence_id: item for item in evidences}

    def _add_evidence(
        self,
        target: OrderedDict[str, CultureEvidence],
        record: dict,
        matched_keywords: list[str],
        matched_chars: list[str],
        match_type: str,
        confidence: float,
    ) -> None:
        content = str(record.get("content") or "")
        if not content:
            return
        source = str(record.get("source") or "")
        record_id = str(record.get("id") or "")
        evidence_id = self._evidence_id(source, record_id, match_type)
        if evidence_id in target:
            existing = target[evidence_id]
            existing.matched_keywords = self._dedupe(existing.matched_keywords + matched_keywords)
            existing.matched_chars = self._dedupe(existing.matched_chars + matched_chars)
            existing.confidence = max(existing.confidence, confidence)
            return
        target[evidence_id] = CultureEvidence(
            evidence_id=evidence_id,
            source_type=source,
            book=self.SOURCE_LABELS.get(source, source),
            title=record.get("title") or None,
            author=record.get("author") or None,
            original_text=content,
            matched_chars=matched_chars,
            matched_keywords=matched_keywords,
            match_type=match_type,
            confidence=confidence,
            record_id=record_id,
        )

    @staticmethod
    def _evidence_id(source: str, record_id: str, match_type: str) -> str:
        raw = f"{source}:{record_id}:{match_type}".encode("utf-8")
        return "EV-" + hashlib.sha1(raw).hexdigest()[:12]

    @staticmethod
    def _dedupe(values: list[str]) -> list[str]:
        return list(dict.fromkeys(values))
