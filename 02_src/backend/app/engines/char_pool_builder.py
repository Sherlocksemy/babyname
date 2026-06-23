from __future__ import annotations

from collections import Counter, defaultdict

from app.indexes.character_index import CharacterIndex
from app.indexes.popularity_index import PopularityIndex
from app.indexes.pronunciation_index import PronunciationIndex
from app.schemas.candidate import CandidateChar, CultureEvidence
from app.schemas.naming_input import NamingInput


UNSUITABLE_CHARS = set(
    "乂乜儿几卜了么也兮乎哉矣焉其之而于以与或且及并把被将就很吗呢啊吧呀"
    "一二三四五六七八九十百千万亿零不无未非否勿莫没旧帝王夫女民臣父母鸟虫鱼菜草犬马口手目耳穷细"
)
NAME_FRIENDLY_CHARS = set(
    "知思明德仁义礼信文书闻清雅安宁和温润远行景云泽川山怀修诚敬正嘉乐新承彦谦然"
    "微言道贤哲睿朗昭晖晨曜煦衡宥博达鸿凌志望庭序家祐佑宜初南乔松竹兰芷洲汀沅湘"
    "辰星月华光若沐汐涵轩宸萱桐墨子雨浩宇梓能毅瑾弘则灵均容维闻辨昭章"
    "天地海波岳岩泉风雨洲渊"
)
NEGATIVE_HINTS = ("贬义", "恶", "病", "死", "灾", "祸", "残", "败", "毒", "怨", "哭", "哀", "凶", "杀", "亡")


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

    def build(
        self,
        naming_input: NamingInput,
        structures: list[dict],
        archetypes: list[dict],
        evidences: list[CultureEvidence],
        first_limit: int = 80,
        second_limit: int = 80,
    ) -> dict:
        evidence_by_char = self._evidence_by_char(evidences)
        role_terms = self._role_terms(structures, archetypes, naming_input)
        blocked = set(naming_input.blocked_chars) | set(naming_input.surname)
        liked = set(naming_input.liked_chars)
        candidates: list[CandidateChar] = []

        for char in self.character_index.compliance:
            if char in blocked or char in UNSUITABLE_CHARS:
                continue
            profile = self.character_index.get(char)
            semantic = profile.get("semantic") or {}
            definition = str(semantic.get("definition") or "")
            if not definition:
                continue
            if any(hint in definition for hint in NEGATIVE_HINTS):
                continue
            if not profile.get("mandarin"):
                continue
            risks = self.pronunciation_index.risks(char)
            if risks:
                continue
            positive_level = int(semantic.get("positive_level") or 0)
            common_level = int(semantic.get("common_level") or 3)
            if positive_level < 3 or common_level > 2:
                continue

            score = positive_level * 4 + (4 - common_level) * 3
            risk_flags: list[str] = []
            matched_roles: list[str] = []
            for term in role_terms:
                if term and (term in definition or term == char):
                    score += 4
                    matched_roles.append(term)
            if char not in NAME_FRIENDLY_CHARS and char not in liked:
                continue
            if char in NAME_FRIENDLY_CHARS:
                score += 6
            if char in evidence_by_char:
                score += min(18, 4 + len(evidence_by_char[char]) * 2)
            if char in liked:
                score += 20
            if len(profile.get("mandarin") or []) > 1:
                score -= 4
                risk_flags.append("POLYPHONE")
            popularity = self.popularity_index.get_char(char)
            popularity_penalty = 0.0
            if popularity:
                heat = popularity.get("heat_level")
                if heat == "爆款":
                    popularity_penalty = 8
                elif heat == "高":
                    popularity_penalty = 5
                elif heat == "中":
                    popularity_penalty = 2
                score -= popularity_penalty
                if popularity_penalty:
                    risk_flags.append("POPULAR_CHAR")
            teochew = self.pronunciation_index.teochew_readings(char)
            if teochew:
                score += 1.5

            structure_scores = {item["id"]: self._match_score(char, definition, item) for item in structures}
            archetype_scores = {item["id"]: self._match_score(char, definition, item) for item in archetypes}
            candidate = CandidateChar(
                char=char,
                semantic_roles=matched_roles or role_terms[:2],
                structure_scores=structure_scores,
                archetype_scores=archetype_scores,
                culture_evidence_ids=evidence_by_char.get(char, [])[:8],
                mandarin=profile.get("mandarin") or [],
                teochew=teochew,
                popularity_penalty=popularity_penalty,
                risk_flags=risk_flags,
                final_score=round(score, 4),
            )
            candidates.append(candidate)

        candidates.sort(key=lambda item: (-item.final_score, item.char))
        first_pool = self._position_pool(candidates, structures, position=0, limit=first_limit)
        second_pool = self._position_pool(candidates, structures, position=1, limit=second_limit)
        return {
            "first_pool": first_pool,
            "second_pool": second_pool,
            "rejected_summary": dict(Counter()),
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
    def _match_score(char: str, definition: str, item: dict) -> float:
        score = 0.0
        for keyword in item.get("keywords", []) + item.get("semantic_roles", []):
            if keyword == char:
                score += 5
            elif keyword and keyword in definition:
                score += 3
        return score

    @staticmethod
    def _position_pool(candidates: list[CandidateChar], structures: list[dict], position: int, limit: int) -> list[CandidateChar]:
        if not structures:
            return candidates[:limit]
        role = structures[0].get("semantic_roles", [""])[min(position, len(structures[0].get("semantic_roles", [""])) - 1)]
        ranked = sorted(
            candidates,
            key=lambda item: (-(item.final_score + (4 if role in item.semantic_roles else 0)), item.char),
        )
        return ranked[:limit]
