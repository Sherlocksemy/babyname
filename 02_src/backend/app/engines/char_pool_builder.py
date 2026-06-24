from __future__ import annotations

from collections import Counter, defaultdict

from app.catalogs.character_risk_classifier import NEGATIVE_HINTS, UNSUITABLE_CHARS
from app.catalogs.name_char_catalog_builder import ensure_name_char_catalog
from app.indexes.character_index import CharacterIndex
from app.indexes.popularity_index import PopularityIndex
from app.indexes.pronunciation_index import PronunciationIndex
from app.schemas.candidate import CandidateChar, CultureEvidence
from app.schemas.naming_input import NamingInput


class CharPoolBuilder:
    def __init__(
        self,
        character_index: CharacterIndex | None = None,
        pronunciation_index: PronunciationIndex | None = None,
        popularity_index: PopularityIndex | None = None,
    ) -> None:
        self.character_index = character_index or CharacterIndex()
        self.pronunciation_index = pronunciation_index or PronunciationIndex()
        self.popularity_index = popularity_index or PopularityIndex()
        self.catalog = ensure_name_char_catalog()

    def build(
        self,
        naming_input: NamingInput,
        structures: list[dict],
        archetypes: list[dict],
        evidences: list[CultureEvidence],
        fortune_context: dict | None = None,
        first_limit: int = 80,
        second_limit: int = 80,
    ) -> dict:
        evidence_by_char = self._evidence_by_char(evidences)
        role_terms = self._role_terms(structures, archetypes, naming_input)
        blocked = set(naming_input.blocked_chars) | set(naming_input.surname)
        liked = set(naming_input.liked_chars)
        rejected_summary: Counter[str] = Counter()
        candidates: list[CandidateChar] = []

        for record in self.catalog["records"]:
            char = record["char"]
            if char in blocked:
                rejected_summary["USER_BLOCKED_OR_SURNAME_CHAR"] += 1
                continue
            if record["nameability_level"] == "REJECTED":
                rejected_summary["CATALOG_REJECTED"] += 1
                continue
            if record["nameability_level"] == "EXPERIMENTAL" and char not in liked:
                rejected_summary["EXPERIMENTAL_NOT_USER_LIKED"] += 1
                continue
            if "HOMOPHONE_RISK" in record["risk_codes"]:
                rejected_summary["HOMOPHONE_RISK"] += 1
                continue

            profile = self.character_index.get(char)
            score = float(record["nameability_score"])
            risk_flags = list(record["risk_codes"])
            matched_roles: list[str] = []
            search_text = "".join(
                [
                    char,
                    record.get("definition", ""),
                    "".join(record.get("semantic_roles") or []),
                    "".join(record.get("semantic_categories") or []),
                    "".join(record.get("semantic_keywords") or []),
                ]
            )
            for term in role_terms:
                if term and (term in search_text or term == char):
                    score += 4
                    matched_roles.append(term)
            if char in evidence_by_char:
                score += min(18, 4 + len(evidence_by_char[char]) * 2)
            elif record["culture_evidence_count"]:
                score += min(12, record["culture_evidence_count"] * 1.5)
            if char in liked:
                score += 20
            if len(record.get("mandarin") or []) > 1:
                score -= 4
                risk_flags.append("POLYPHONE")

            popularity = self.popularity_index.get_char(char)
            if popularity:
                score += 25
            popularity_penalty = self._popularity_penalty(popularity)
            if popularity_penalty:
                score -= popularity_penalty
                risk_flags.append("POPULAR_CHAR")
            if "FUNCTION" in record.get("semantic_categories", []):
                score -= 8
            if "OBJECT" in record.get("semantic_categories", []):
                score -= 6
            if "OBJECT_OR_TOOL_SEMANTIC" in risk_flags:
                score -= 12
            if "LOW_SOURCE_POSITIVE_LEVEL" in risk_flags:
                score -= 10

            element = self._element_en(record.get("element") or "")
            supportive = set(((fortune_context or {}).get("five_elements") or {}).get("supportive_elements") or [])
            caution = set(((fortune_context or {}).get("five_elements") or {}).get("caution_elements") or [])
            if element in supportive:
                score += 2.0
            if element in caution:
                score -= 1.0

            structure_scores = {item["id"]: self._match_score(char, search_text, item) for item in structures}
            archetype_scores = {item["id"]: self._match_score(char, search_text, item) for item in archetypes}
            catalog_links = self.catalog["culture_links"].get(char, [])
            candidates.append(
                CandidateChar(
                    char=char,
                    semantic_roles=list(dict.fromkeys(matched_roles + list(record.get("semantic_roles") or [])))[:6],
                    semantic_categories=list(record.get("semantic_categories") or []),
                    structure_scores=structure_scores,
                    archetype_scores=archetype_scores,
                    culture_evidence_ids=(evidence_by_char.get(char, []) + record.get("culture_link_ids", []))[:8],
                    culture_links=catalog_links[:4],
                    mandarin=record.get("mandarin") or [],
                    teochew=self.pronunciation_index.teochew_readings(char),
                    popularity_penalty=popularity_penalty,
                    risk_flags=list(dict.fromkeys(risk_flags)),
                    final_score=round(score, 4),
                    element=element,
                    radical=str(record.get("radical") or ""),
                    catalog_level=record["nameability_level"],
                    catalog_score=float(record["nameability_score"]),
                    reason_codes=list(record.get("reason_codes") or []),
                )
            )

        candidates.sort(key=lambda item: (-item.final_score, item.char))
        first_pool = self._position_pool(candidates, structures, position=0, limit=first_limit)
        second_pool = self._position_pool(candidates, structures, position=1, limit=second_limit)
        candidate_by_char = {item.char: item for item in candidates}
        first_pool = self._ensure_liked_chars(first_pool, candidate_by_char, liked, first_limit)
        second_pool = self._ensure_liked_chars(second_pool, candidate_by_char, liked, second_limit)
        return {
            "first_pool": first_pool,
            "second_pool": second_pool,
            "rejected_summary": dict(rejected_summary),
        }

    @staticmethod
    def _role_terms(structures: list[dict], archetypes: list[dict], naming_input: NamingInput) -> list[str]:
        terms: list[str] = []
        for item in structures + archetypes:
            terms.extend(item.get("semantic_roles", []))
            terms.extend(item.get("keywords", []))
        terms.extend(naming_input.style_preferences)
        return list(dict.fromkeys([term for term in terms if term]))

    @staticmethod
    def _evidence_by_char(evidences: list[CultureEvidence]) -> dict[str, list[str]]:
        mapping: dict[str, list[str]] = defaultdict(list)
        for evidence in evidences:
            for char in set(evidence.original_text):
                if "\u4e00" <= char <= "\u9fff":
                    mapping[char].append(evidence.evidence_id)
        return mapping

    @staticmethod
    def _match_score(char: str, text: str, item: dict) -> float:
        score = 0.0
        for keyword in item.get("keywords", []) + item.get("semantic_roles", []):
            if keyword == char:
                score += 5
            elif keyword and keyword in text:
                score += 3
        return score

    @staticmethod
    def _position_pool(candidates: list[CandidateChar], structures: list[dict], position: int, limit: int) -> list[CandidateChar]:
        if not structures:
            return candidates[:limit]
        roles = structures[0].get("semantic_roles", [""])
        role = roles[min(position, len(roles) - 1)]
        ranked = sorted(
            candidates,
            key=lambda item: (-(item.final_score + (4 if role in item.semantic_roles else 0)), item.char),
        )
        return ranked[:limit]

    @staticmethod
    def _popularity_penalty(popularity: dict | None) -> float:
        if not popularity:
            return 0.0
        heat = popularity.get("heat_level")
        if heat == "爆款":
            return 8
        if heat == "高":
            return 5
        if heat == "中":
            return 2
        return 0.0

    @staticmethod
    def _element_en(element: str) -> str:
        return {"木": "wood", "火": "fire", "土": "earth", "金": "metal", "水": "water"}.get(element, element)

    @staticmethod
    def _ensure_liked_chars(pool: list[CandidateChar], candidate_by_char: dict[str, CandidateChar], liked: set[str], limit: int) -> list[CandidateChar]:
        result = list(pool)
        present = {item.char for item in result}
        for char in liked:
            if char in present or char not in candidate_by_char:
                continue
            if len(result) >= limit:
                result[-1] = candidate_by_char[char]
            else:
                result.append(candidate_by_char[char])
            present.add(char)
        return result
