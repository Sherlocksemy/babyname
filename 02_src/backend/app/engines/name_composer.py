from __future__ import annotations

import hashlib
import random
import re

from app.engines.culture_retriever import CultureRetriever
from app.engines.profile_specificity_engine import STYLE_RULES
from app.engines.semantic_composition_validator import SemanticCompositionValidator
from app.engines.structure_archetype_compatibility import evaluate_compatibility
from app.schemas.candidate import CandidateChar, CultureEvidence, NameCandidate
from app.schemas.naming_input import NamingInput


HANZI_RE = re.compile(r"[\u4e00-\u9fff]")


class NameComposer:
    def __init__(self, culture_retriever: CultureRetriever) -> None:
        self.culture_retriever = culture_retriever
        self.semantic_validator = SemanticCompositionValidator()

    def compose(
        self,
        naming_input: NamingInput,
        first_pool: list[CandidateChar],
        second_pool: list[CandidateChar],
        structures: list[dict],
        archetypes: list[dict],
        min_count: int = 60,
        max_count: int = 120,
    ) -> list[NameCandidate]:
        first_map = {item.char: item for item in first_pool}
        second_map = {item.char: item for item in second_pool}
        allowed_first = set(first_map)
        allowed_second = set(second_map)
        rng = random.Random(naming_input.generation_seed)
        candidates: list[NameCandidate] = []
        seen: set[str] = set()
        excluded_given_names = set(naming_input.exclude_given_names)

        evidence_records = self._ordered_culture_records(naming_input, structures, archetypes)
        direct_limit = max(30, int(max_count * 0.42))
        if naming_input.liked_chars:
            self._add_liked_char_candidates(
                naming_input,
                first_map,
                second_map,
                structures,
                archetypes,
                candidates,
                seen,
                min(max_count, direct_limit),
            )
        for record in evidence_records:
            for given_name in self._bigrams_from_record(record):
                if self._mode_count(candidates, "direct_expression") >= direct_limit:
                    break
                if given_name in seen:
                    continue
                if given_name in excluded_given_names:
                    continue
                if given_name[0] not in allowed_first or given_name[1] not in allowed_second:
                    continue
                semantic = self.semantic_validator.validate(given_name)
                if not semantic["passed"]:
                    continue
                structure = self._select_structure(structures, semantic, rng)
                archetype = self._select_archetype(archetypes, structure["id"], rng)
                compatibility = evaluate_compatibility(structure["id"], archetype["id"])
                if compatibility["compatibility_level"] == "CONFLICT":
                    continue
                evidences = self.culture_retriever.evidence_for_name(given_name, limit=4)
                if not evidences:
                    continue
                seen.add(given_name)
                candidates.append(
                    self._create_candidate(
                        naming_input,
                        given_name,
                        first_map,
                        second_map,
                        structure,
                        archetype,
                        semantic,
                        evidences,
                        "direct_expression",
                        "E1" if evidences[0].evidence_level == "E1" else evidences[0].evidence_level,
                        ["DIRECT_EXPRESSION", "CULTURE_TEXT_BIGRAM", "POOL_CHAR_SELECTED"],
                    )
                )
                if len(candidates) >= max_count:
                    return candidates[:max_count]
        self._add_composed_candidates(
            naming_input,
            first_pool,
            second_pool,
            first_map,
            second_map,
            structures,
            archetypes,
            candidates,
            seen,
            max_add=max(18, int(max_count * 0.34)),
            mode="semantic_role_composition",
            evidence_level="E2_COMPOSED",
            reason_codes=["SEMANTIC_ROLE_COMPOSITION", "SEPARATE_CHAR_CULTURE_TRACE"],
        )
        self._add_composed_candidates(
            naming_input,
            first_pool,
            second_pool,
            first_map,
            second_map,
            structures,
            archetypes,
            candidates,
            seen,
            max_add=max(12, int(max_count * 0.24)),
            mode="imagery_transformation",
            evidence_level="E2_IMAGERY",
            reason_codes=["IMAGERY_TRANSFORMATION", "SEPARATE_CHAR_CULTURE_TRACE"],
            imagery_only=True,
        )
        return candidates[:max_count]

    def _add_liked_char_candidates(
        self,
        naming_input: NamingInput,
        first_map: dict[str, CandidateChar],
        second_map: dict[str, CandidateChar],
        structures: list[dict],
        archetypes: list[dict],
        candidates: list[NameCandidate],
        seen: set[str],
        max_count: int,
    ) -> None:
        for liked in naming_input.liked_chars:
            records = self.culture_retriever.index.by_char(liked, limit=80)
            for record in records:
                chars = [char for char in HANZI_RE.findall(str(record.get("content") or "")) if char != liked]
                for other in dict.fromkeys(chars):
                    for given_name in (liked + other, other + liked):
                        if len(candidates) >= max_count:
                            return
                        if given_name in seen:
                            continue
                        if given_name in set(naming_input.exclude_given_names):
                            continue
                        if given_name[0] not in first_map or given_name[1] not in second_map:
                            continue
                        semantic = self.semantic_validator.validate(given_name)
                        if not semantic["passed"]:
                            continue
                        structure = self._select_structure(structures, semantic, random.Random(naming_input.generation_seed))
                        archetype = self._select_archetype(archetypes, structure["id"], random.Random(naming_input.generation_seed))
                        compatibility = evaluate_compatibility(structure["id"], archetype["id"])
                        if compatibility["compatibility_level"] == "CONFLICT":
                            continue
                        evidences = self.culture_retriever.evidence_for_name(given_name, limit=4)
                        if not evidences:
                            continue
                        seen.add(given_name)
                        candidates.append(
                            self._create_candidate(
                                naming_input,
                                given_name,
                                first_map,
                                second_map,
                                structure,
                                archetype,
                                semantic,
                                evidences,
                                "direct_expression",
                                evidences[0].evidence_level,
                                ["LIKED_CHAR_WEIGHTED_DERIVATION", "CULTURE_RECORD_CHAR_SELECTION"],
                            )
                        )

    def _add_composed_candidates(
        self,
        naming_input: NamingInput,
        first_pool: list[CandidateChar],
        second_pool: list[CandidateChar],
        first_map: dict[str, CandidateChar],
        second_map: dict[str, CandidateChar],
        structures: list[dict],
        archetypes: list[dict],
        candidates: list[NameCandidate],
        seen: set[str],
        max_add: int,
        mode: str,
        evidence_level: str,
        reason_codes: list[str],
        imagery_only: bool = False,
    ) -> None:
        added = 0
        style_terms = self._style_terms(naming_input)
        rng = random.Random(naming_input.generation_seed + (17 if imagery_only else 11))
        first_items = sorted(first_pool[:80], key=lambda item: (-self._path_char_score(item, style_terms, imagery_only), item.char))
        second_items = sorted(second_pool[:80], key=lambda item: (-self._path_char_score(item, style_terms, imagery_only), item.char))
        for first in first_items:
            for second in second_items:
                if added >= max_add or len(candidates) >= 120:
                    return
                given_name = first.char + second.char
                if first.char == second.char or given_name in seen:
                    continue
                if given_name in set(naming_input.exclude_given_names):
                    continue
                semantic = self.semantic_validator.validate(given_name)
                if not semantic["passed"]:
                    continue
                if imagery_only and not self._has_imagery_hit(given_name, semantic, style_terms):
                    continue
                structure = self._select_structure(structures, semantic, rng)
                archetype = self._select_archetype(archetypes, structure["id"], rng)
                compatibility = evaluate_compatibility(structure["id"], archetype["id"])
                if compatibility["compatibility_level"] == "CONFLICT":
                    continue
                first_evidences = self.culture_retriever.evidence_for_char(first.char, limit=2) or self._catalog_evidence_for_char(first)
                second_evidences = self.culture_retriever.evidence_for_char(second.char, limit=2) or self._catalog_evidence_for_char(second)
                if not first_evidences or not second_evidences:
                    continue
                evidences = first_evidences[:1] + second_evidences[:1]
                seen.add(given_name)
                added += 1
                candidates.append(
                    self._create_candidate(
                        naming_input,
                        given_name,
                        first_map,
                        second_map,
                        structure,
                        archetype,
                        semantic,
                        evidences,
                        mode,
                        evidence_level,
                        reason_codes,
                    )
                )

    def _ordered_culture_records(self, naming_input: NamingInput, structures: list[dict], archetypes: list[dict]) -> list[dict]:
        preferred_sources = []
        for item in structures + archetypes:
            preferred_sources.extend(item.get("preferred_culture_sources", []))
        source_rank = {source: index for index, source in enumerate(dict.fromkeys(preferred_sources))}
        style_text = "".join(naming_input.style_preferences)

        def key(record: dict) -> tuple:
            source = record.get("source", "")
            keywords = "".join(record.get("keywords") or [])
            style_hit = 0 if any(token and token in keywords + str(record.get("content", "")) for token in naming_input.style_preferences) else 1
            return (source_rank.get(source, 99), style_hit, str(record.get("id", "")))

        records = list(self.culture_retriever.index.records)
        records.sort(key=key)
        return records

    def _create_candidate(
        self,
        naming_input: NamingInput,
        given_name: str,
        first_map: dict[str, CandidateChar],
        second_map: dict[str, CandidateChar],
        structure: dict,
        archetype: dict,
        semantic: dict,
        evidences: list,
        generation_mode: str,
        evidence_level: str,
        reason_codes: list[str],
    ) -> NameCandidate:
        evidence_score = max([(item.suitability or {}).get("evidence_suitability_score", 0) for item in evidences] or [0])
        if evidence_level == "E2_COMPOSED":
            evidence_score = max(evidence_score, 82)
        elif evidence_level == "E2_IMAGERY":
            evidence_score = max(evidence_score, 80)
        return NameCandidate(
            candidate_id=self._candidate_id(naming_input.surname, given_name, naming_input.generation_seed),
            surname=naming_input.surname,
            given_name=given_name,
            full_name=naming_input.surname + given_name,
            structure_id=structure["id"],
            archetype_id=archetype["id"],
            semantic_pattern="/".join([semantic["semantic_role_first"], semantic["semantic_role_second"]]),
            culture_evidence_ids=[item.evidence_id for item in evidences],
            generation_reason_codes=reason_codes + ["POOL_CHAR_SELECTED"],
            generation_seed=naming_input.generation_seed,
            first_char=first_map[given_name[0]],
            second_char=second_map[given_name[1]],
            evidences=evidences,
            semantic_role_first=semantic["semantic_role_first"],
            semantic_role_second=semantic["semantic_role_second"],
            combined_meaning=semantic["combined_meaning"],
            meaning_completeness=semantic["meaning_completeness"],
            evidence_level=evidence_level,
            evidence_suitability_score=evidence_score,
            generation_mode=generation_mode,
            first_char_source=self._char_source(given_name[0], first_map[given_name[0]], evidences),
            second_char_source=self._char_source(given_name[1], second_map[given_name[1]], evidences),
            structure_rule_ids=[structure["id"], "SEMANTIC_ROLE_MATCH"],
            archetype_rule_ids=[archetype["id"], "STRUCTURE_ARCHETYPE_COMPATIBILITY"],
            was_example_name=False,
            was_golden_fixture=False,
            was_direct_name_candidate=False,
            style_affinity_score=self._style_affinity(naming_input, given_name, semantic),
        )

    @staticmethod
    def _bigrams_from_record(record: dict) -> list[str]:
        text = str(record.get("content") or "")
        chars = HANZI_RE.findall(text)
        bigrams = []
        for index in range(len(chars) - 1):
            pair = chars[index] + chars[index + 1]
            if pair[0] != pair[1]:
                bigrams.append(pair)
        return list(dict.fromkeys(bigrams))

    @staticmethod
    def _mode_count(candidates: list[NameCandidate], mode: str) -> int:
        return sum(1 for item in candidates if item.generation_mode == mode)

    @staticmethod
    def _style_terms(naming_input: NamingInput) -> dict[str, set[str]]:
        terms = {"imagery": set(), "roles": set()}
        for style in naming_input.style_preferences:
            rule = STYLE_RULES.get(style, {})
            terms["imagery"].update(rule.get("imagery", []))
            terms["roles"].update(rule.get("roles", []))
        terms["imagery"].update(naming_input.liked_chars)
        return terms

    @staticmethod
    def _path_char_score(item: CandidateChar, style_terms: dict[str, set[str]], imagery_only: bool) -> float:
        text = item.char + "".join(item.semantic_roles) + "".join(item.semantic_categories)
        score = item.final_score
        role_hits = sum(1 for role in style_terms["roles"] if role and role in text)
        imagery_hits = sum(1 for image in style_terms["imagery"] if image and image in text)
        score += role_hits * 8 + imagery_hits * (12 if imagery_only else 6)
        return score

    @staticmethod
    def _has_imagery_hit(given_name: str, semantic: dict, style_terms: dict[str, set[str]]) -> bool:
        text = (
            given_name
            + semantic["semantic_role_first"]
            + semantic["semantic_role_second"]
            + semantic["combined_meaning"]
            + semantic.get("first_category", "")
            + semantic.get("second_category", "")
        )
        if any(image and image in text for image in style_terms["imagery"]):
            return True
        return bool({semantic.get("first_category"), semantic.get("second_category")} & {"AESTHETIC", "LANDSCAPE", "WATER", "BRIGHTNESS", "SPACE", "GROWTH"})

    @staticmethod
    def _catalog_evidence_for_char(candidate_char: CandidateChar) -> list[CultureEvidence]:
        evidences: list[CultureEvidence] = []
        for index, link in enumerate(candidate_char.culture_links[:2]):
            evidences.append(
                CultureEvidence(
                    evidence_id=f"CAT-{candidate_char.char}-{index}-{link.get('source_record_id', '')}",
                    source_type=str(link.get("source_type") or ""),
                    book=str(link.get("source_type") or ""),
                    title=link.get("title") or None,
                    author=link.get("author") or None,
                    original_text=str(link.get("matched_text") or link.get("display_excerpt") or candidate_char.char),
                    matched_chars=[candidate_char.char],
                    matched_keywords=list(link.get("keywords") or []),
                    match_type="catalog_char_evidence",
                    confidence=0.72,
                    record_id=str(link.get("source_record_id") or ""),
                    evidence_level="E2",
                )
            )
        return evidences

    @staticmethod
    def _select_structure(structures: list[dict], semantic: dict, rng: random.Random) -> dict:
        if not structures:
            return {"id": "S06", "semantic_roles": [semantic["semantic_role_first"], semantic["semantic_role_second"]]}
        scored = []
        semantic_text = semantic["semantic_role_first"] + semantic["semantic_role_second"] + semantic["combined_meaning"]
        for item in structures:
            score = 0
            for token in item.get("semantic_roles", []) + item.get("keywords", []):
                if token and token in semantic_text:
                    score += 3
            scored.append((score + rng.random() * 0.0001, item))
        scored.sort(key=lambda row: (-row[0], row[1]["id"]))
        return scored[0][1]

    @staticmethod
    def _select_archetype(archetypes: list[dict], structure_id: str, rng: random.Random) -> dict:
        if not archetypes:
            return {"id": "A01"}
        scored = []
        for item in archetypes:
            compatibility = evaluate_compatibility(structure_id, item["id"])
            score = compatibility["structure_archetype_compatibility"] + rng.random() * 0.0001
            scored.append((score, item))
        scored.sort(key=lambda row: (-row[0], row[1]["id"]))
        return scored[0][1]

    @staticmethod
    def _char_source(char: str, candidate_char: CandidateChar, evidences: list) -> list[str]:
        sources = ["char_pool"]
        if candidate_char.culture_evidence_ids:
            sources.append("culture_evidence_char")
        if any(char in evidence.original_text for evidence in evidences):
            sources.append("selected_culture_text")
        return list(dict.fromkeys(sources))

    @staticmethod
    def _style_affinity(naming_input: NamingInput, given_name: str, semantic: dict) -> float:
        text = "".join(naming_input.style_preferences)
        roles = semantic["semantic_role_first"] + semantic["semantic_role_second"] + semantic["combined_meaning"] + given_name
        score = 0.0
        if any(token in text for token in ["书卷", "知性", "思想"]):
            score += sum(1.2 for token in ["认知", "思辨", "闻学", "道理", "文气"] if token in roles)
        if any(token in text for token in ["君子", "品格"]):
            score += sum(1.2 for token in ["德行", "敬慎", "正直", "仁德", "准则"] if token in roles)
        if any(token in text for token in ["山水", "自然", "开阔", "大气"]):
            score += sum(1.4 for token in ["山", "岳", "云", "星", "海", "岩", "泉", "风", "天宇"] if token in roles)
        if any(token in text for token in ["温润", "温柔", "现代高级", "民国"]):
            score += sum(1.3 for token in ["清", "灵", "安", "宁", "和", "晏", "温", "煦"] if token in roles)
        if naming_input.gender == "female":
            score += sum(0.8 for token in ["清", "灵", "安", "和", "兰", "芷"] if token in roles)
        if naming_input.gender == "male":
            score += sum(0.7 for token in ["弘", "毅", "岳", "修", "敬", "志"] if token in roles)
        if any(char in given_name for char in naming_input.liked_chars):
            score += 3.0
        return round(min(score, 8.0), 2)

    @staticmethod
    def _candidate_id(surname: str, given_name: str, seed: int) -> str:
        raw = f"{surname}:{given_name}:{seed}".encode("utf-8")
        return "NC-" + hashlib.sha1(raw).hexdigest()[:12]
