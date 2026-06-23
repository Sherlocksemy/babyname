from __future__ import annotations

from collections import Counter

from app.schemas.candidate import NameCandidate


class RankingEngine:
    def rank(self, candidates: list[NameCandidate]) -> dict:
        sorted_candidates = sorted(candidates, key=self._sort_key)
        top20_pool = [candidate for candidate in sorted_candidates if candidate.profile_specificity_score >= 70]
        top20 = self._select_path_balanced(top20_pool, target=20)
        top10_pool = [candidate for candidate in top20 if candidate.profile_specificity_score >= 80]
        top10 = self._select_limited(top10_pool, target=10, max_char_count=1, max_pattern_count=2, max_record_count=2)
        if len(top10) < 10:
            top10.extend(
                self._select_limited(
                    [candidate for candidate in top10_pool if candidate not in top10],
                    target=10 - len(top10),
                    max_char_count=2,
                    max_pattern_count=3,
                    max_record_count=3,
                    existing=top10,
                )
            )
        eligible_top3_pool = [candidate for candidate in top10 if (candidate.score or {}).get("top3_eligible")]
        top3 = self._select_diverse(eligible_top3_pool, target=3, relaxed=False)
        diversity_status = "OK"
        reason = ""
        if len(top3) < 3 or len({item.structure_id for item in top3}) < 2 or len({item.archetype_id for item in top3}) < 2:
            diversity_status = "DEGRADED"
            reason = "insufficient diversity after hard constraints"
        top1 = next((candidate for candidate in top3 if (candidate.score or {}).get("top1_eligible")), None)
        return {
            "top20": top20,
            "top10": top10,
            "top3": top3,
            "top1": top1,
            "top1_status": "OK" if top1 else "NO_S_LEVEL_CANDIDATE",
            "diversity_status": diversity_status,
            "reason": reason,
        }

    @staticmethod
    def _sort_key(candidate: NameCandidate) -> tuple:
        score = (candidate.score or {}).get("normalized_score", 0)
        evidence_strength = max([item.confidence for item in candidate.evidences] or [0])
        profile = candidate.profile_specificity_score
        surname_fit = candidate.surname_fit_score
        path_rank = {"semantic_role_composition": 0, "imagery_transformation": 1, "direct_expression": 2}.get(candidate.generation_mode, 3)
        structure_score = len(candidate.semantic_pattern.split("/"))
        archetype_clarity = 1 if candidate.archetype_id else 0
        phonology = (candidate.score or {}).get("breakdown", {}).get("phonology", 0)
        popularity_penalty = (candidate.score or {}).get("breakdown", {}).get("penalties", 0)
        return (-score, -profile, path_rank, -surname_fit, -evidence_strength, -structure_score, -archetype_clarity, -phonology, popularity_penalty, candidate.given_name)

    def _select_path_balanced(self, candidates: list[NameCandidate], target: int) -> list[NameCandidate]:
        direct_cap = max(1, int(target * 0.40))
        semantic_target = max(1, int(target * 0.40))
        imagery_target = max(1, int(target * 0.20))
        selected: list[NameCandidate] = []
        for mode, count in [
            ("semantic_role_composition", semantic_target),
            ("imagery_transformation", imagery_target),
        ]:
            selected.extend(
                self._select_limited(
                    [candidate for candidate in candidates if candidate.generation_mode == mode and candidate not in selected],
                    target=count,
                    max_char_count=2,
                    max_pattern_count=4,
                    max_record_count=4,
                    existing=selected,
                )
            )
        remaining = [candidate for candidate in candidates if candidate not in selected]
        selected.extend(
            self._select_limited(
                [candidate for candidate in remaining if candidate.generation_mode == "direct_expression"],
                target=direct_cap,
                max_char_count=2,
                max_pattern_count=4,
                max_record_count=4,
                existing=selected,
            )
        )
        if len(selected) < target:
            selected.extend(
                self._select_limited(
                    [candidate for candidate in candidates if candidate not in selected],
                    target=target - len(selected),
                    max_char_count=3,
                    max_pattern_count=5,
                    max_record_count=5,
                    existing=selected,
                )
            )
        return sorted(selected[:target], key=self._sort_key)

    @staticmethod
    def _select_limited(
        candidates: list[NameCandidate],
        target: int,
        max_char_count: int,
        max_pattern_count: int,
        max_record_count: int,
        existing: list[NameCandidate] | None = None,
    ) -> list[NameCandidate]:
        selected: list[NameCandidate] = list(existing or [])
        used_chars: Counter[str] = Counter()
        semantic_patterns: Counter[str] = Counter()
        used_records: Counter[str] = Counter()
        for candidate in selected:
            for char in set(candidate.given_name):
                used_chars[char] += 1
            semantic_patterns[candidate.semantic_pattern] += 1
            record_id = candidate.evidences[0].record_id if candidate.evidences else ""
            if record_id:
                used_records[record_id] += 1
        added: list[NameCandidate] = []
        for candidate in candidates:
            if candidate in selected:
                continue
            chars = set(candidate.given_name)
            if any(used_chars[char] >= max_char_count for char in chars):
                continue
            if semantic_patterns[candidate.semantic_pattern] >= max_pattern_count:
                continue
            record_id = candidate.evidences[0].record_id if candidate.evidences else ""
            if record_id and used_records[record_id] >= max_record_count:
                continue
            selected.append(candidate)
            added.append(candidate)
            for char in chars:
                used_chars[char] += 1
            semantic_patterns[candidate.semantic_pattern] += 1
            if record_id:
                used_records[record_id] += 1
            if len(added) >= target:
                break
        return added

    @staticmethod
    def _select_diverse(candidates: list[NameCandidate], target: int, relaxed: bool) -> list[NameCandidate]:
        selected: list[NameCandidate] = []
        used_chars: Counter[str] = Counter()
        used_records: Counter[str] = Counter()
        semantic_patterns: Counter[str] = Counter()
        for candidate in candidates:
            chars = set(candidate.given_name)
            if not relaxed and any(used_chars[char] >= 1 for char in chars):
                continue
            if not relaxed and candidate.evidences:
                record_id = candidate.evidences[0].record_id or candidate.evidences[0].evidence_id
                if used_records[record_id] >= 1:
                    continue
            if not relaxed and semantic_patterns[candidate.semantic_pattern] >= 1:
                continue
            selected.append(candidate)
            for char in chars:
                used_chars[char] += 1
            if candidate.evidences:
                used_records[candidate.evidences[0].record_id or candidate.evidences[0].evidence_id] += 1
            semantic_patterns[candidate.semantic_pattern] += 1
            if len(selected) >= target:
                return selected
        if relaxed:
            for candidate in candidates:
                if candidate not in selected:
                    selected.append(candidate)
                    if len(selected) >= target:
                        break
        return selected
