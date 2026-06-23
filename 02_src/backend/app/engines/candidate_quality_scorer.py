from __future__ import annotations

from app.schemas.candidate import NameCandidate


class CandidateQualityScorer:
    SCORE_VERSION = "NES_ALPHA_1.3"
    AVAILABLE_MAX_SCORE = 90

    def score(self, candidate: NameCandidate) -> dict:
        first = candidate.first_char
        second = candidate.second_char
        tones = [self._first_tone(first), self._first_tone(second)]
        polyphone_count = sum(1 for item in [first, second] if item and len(item.mandarin) > 1)
        popularity_penalty = sum(item.popularity_penalty for item in [first, second] if item)
        semantic = candidate.semantic_validation or {}
        naturalness = candidate.naturalness or {}

        phonology_sub = {
            "tone_variation": 3.0 if tones[0] != tones[1] else 1.8,
            "initial_conflict": self._initial_score(first, second),
            "final_conflict": self._final_score(first, second),
            "surname_link": self._surname_link_score(candidate.surname, candidate.given_name),
            "internal_flow": max(1.8, 3.0 - polyphone_count * 0.55),
        }
        phonology = min(15, sum(phonology_sub.values()))

        char_quality = ((first.final_score if first else 20) + (second.final_score if second else 20)) / 8.5
        completeness = candidate.meaning_completeness / 100 * 4.2
        complementarity = 3.2 if not semantic.get("issues") else max(1.2, 3.2 - len(semantic.get("issues", [])) * 0.55)
        modern_understanding = min(2.6, candidate.naturalness_score / 100 * 2.6)
        effective_level = self._effective_evidence_level(candidate)
        time_stability = 2.1 if effective_level == "E1" else 1.7
        meaning_sub = {
            "char_meaning_quality": min(2.9, char_quality),
            "composition_completeness": completeness,
            "semantic_complementarity": complementarity,
            "modern_understanding": modern_understanding,
            "time_stability": time_stability,
        }
        meaning = min(15, sum(meaning_sub.values()))

        level_score = {"E1": 4.1, "E2": 3.35, "E3": 1.8, "E0": 0.4}.get(effective_level, 0.4)
        expression = min(3.2, candidate.evidence_suitability_score / 100 * 3.2)
        source_depth = {"sishuwujing": 2.7, "shijing": 2.6, "chuci": 2.5, "tang_poetry": 2.2, "song_ci": 2.0}.get(
            candidate.evidences[0].source_type if candidate.evidences else "", 1.6
        )
        evidence_unique = max(1.0, 2.4 - max(0, candidate.corpus_copy_risk) * 0.9)
        culture_sub = {
            "evidence_level": level_score,
            "original_text_relevance": min(2.8, candidate.evidence_suitability_score / 100 * 2.8),
            "expression_completeness": expression,
            "source_depth": source_depth,
            "evidence_uniqueness": evidence_unique,
        }
        culture = min(15, sum(culture_sub.values()))

        structure_sub = {
            "two_semantic_roles": 4.0 if candidate.semantic_role_first and candidate.semantic_role_second else 1.5,
            "structure_integrity": min(4.4, candidate.meaning_completeness / 100 * 4.4),
            "structure_rarity": self._rarity_score(candidate.structure_id),
            "explainability": 4.0 if candidate.combined_meaning else 1.5,
            "structure_match": min(4.4, candidate.structure_archetype_compatibility / 100 * 4.4),
        }
        structure = min(20, sum(structure_sub.values()))

        archetype_sub = {
            "archetype_clarity": 3.4 if candidate.archetype_id else 1.0,
            "archetype_consistency": min(3.4, candidate.structure_archetype_compatibility / 100 * 3.4),
            "archetype_match": 3.2 if candidate.compatibility_level == "HIGH" else 2.1 if candidate.compatibility_level == "MEDIUM" else 0.8,
        }
        archetype = min(10, sum(archetype_sub.values()))

        uniqueness_sub = {
            "hot_char_risk": max(0.6, 2.0 - popularity_penalty / 5),
            "hot_combo_risk": 1.5 if not candidate.was_direct_name_candidate else 0.6,
            "template_risk": 1.5 if not self._has_template_warning(candidate) else 0.4,
        }
        uniqueness = min(5, sum(uniqueness_sub.values()))

        aesthetic_sub = {
            "restraint": min(2.0, naturalness.get("adult_usability", candidate.naturalness_score) / 100 * 2.0),
            "real_name_feel": min(2.2, candidate.naturalness_score / 100 * 2.2),
            "adult_usability": min(1.9, naturalness.get("adult_usability", 80) / 100 * 1.9),
            "conceptualization_risk": max(0.6, 1.8 - naturalness.get("conceptualization_risk", 20) / 100 * 1.8),
            "surname_fit": min(2.1, naturalness.get("full_name_fit", candidate.naturalness_score) / 100 * 2.1),
        }
        aesthetic = min(10, sum(aesthetic_sub.values()))

        penalties = sum((candidate.quality_guard or {}).get("penalties", {}).values())
        style_bonus = min(3.5, candidate.style_affinity_score * 0.45)
        profile_adjustment = self._profile_adjustment(candidate)
        raw_score = max(0, phonology + meaning + culture + structure + archetype + uniqueness + aesthetic + style_bonus + profile_adjustment - penalties)
        raw_score = min(self.AVAILABLE_MAX_SCORE, self._apply_caps(raw_score, candidate))
        normalized = raw_score / self.AVAILABLE_MAX_SCORE * 100
        breakdown = {
            "phonology": round(phonology, 2),
            "meaning": round(meaning, 2),
            "culture": round(culture, 2),
            "structure": round(structure, 2),
            "archetype": round(archetype, 2),
            "uniqueness": round(uniqueness, 2),
            "aesthetic": round(aesthetic, 2),
            "naturalness": round(candidate.naturalness_score, 2),
            "penalties": round(penalties, 2),
            "style_affinity_bonus": round(style_bonus, 2),
            "profile_specificity": round(candidate.profile_specificity_score, 2),
            "surname_fit": round(candidate.surname_fit_score, 2),
            "profile_adjustment": round(profile_adjustment, 2),
        }
        sub_breakdown = {
            "phonology": {key: round(value, 2) for key, value in phonology_sub.items()},
            "meaning": {key: round(value, 2) for key, value in meaning_sub.items()},
            "culture": {key: round(value, 2) for key, value in culture_sub.items()},
            "structure": {key: round(value, 2) for key, value in structure_sub.items()},
            "archetype": {key: round(value, 2) for key, value in archetype_sub.items()},
            "uniqueness": {key: round(value, 2) for key, value in uniqueness_sub.items()},
            "aesthetic": {key: round(value, 2) for key, value in aesthetic_sub.items()},
            "style_affinity": {"input_style_match": round(style_bonus, 2), "source": "style_preferences and liked_chars"},
            "profile_specificity": {
                "style_fit_score": round(candidate.style_fit_score, 2),
                "gender_tone_fit_score": round(candidate.gender_tone_fit_score, 2),
                "imagery_fit_score": round(candidate.imagery_fit_score, 2),
                "surname_fit_score": round(candidate.surname_fit_score, 2),
                "universal_candidate_risk": round(candidate.universal_candidate_risk, 2),
            },
        }
        return {
            "raw_score": round(raw_score, 2),
            "available_max_score": self.AVAILABLE_MAX_SCORE,
            "normalized_score": round(normalized, 2),
            "alpha_grade": self._grade(raw_score),
            "fortune_score": None,
            "fortune_status": "NOT_EVALUATED",
            "fortune_max_score": 10,
            "score_version": self.SCORE_VERSION,
            "breakdown": breakdown,
            "sub_breakdown": sub_breakdown,
            "top3_eligible": self._top3_eligible(raw_score, breakdown, candidate),
            "top1_eligible": self._top1_eligible(raw_score, breakdown, candidate),
        }

    @staticmethod
    def _first_tone(item) -> int:
        if not item or not item.mandarin:
            return 0
        return int(item.mandarin[0].get("tone") or 0)

    @staticmethod
    def _initial_score(first, second) -> float:
        fp = (first.mandarin[0].get("pinyin", "") if first and first.mandarin else "")
        sp = (second.mandarin[0].get("pinyin", "") if second and second.mandarin else "")
        return 2.2 if fp[:1] and fp[:1] == sp[:1] else 3.0

    @staticmethod
    def _final_score(first, second) -> float:
        fp = (first.mandarin[0].get("pinyin", "") if first and first.mandarin else "")
        sp = (second.mandarin[0].get("pinyin", "") if second and second.mandarin else "")
        return 2.0 if fp[-1:] and fp[-1:] == sp[-1:] else 3.0

    @staticmethod
    def _surname_link_score(surname: str, given_name: str) -> float:
        if surname[-1:] == given_name[:1]:
            return 1.4
        if len(surname) > 1:
            return 2.7
        return 3.0

    @staticmethod
    def _rarity_score(structure_id: str) -> float:
        return {"S01": 3.5, "S02": 3.2, "S03": 3.6, "S04": 3.1, "S05": 3.4, "S06": 3.2, "S07": 3.7, "S08": 3.3, "S09": 3.5, "S10": 3.6, "S11": 3.4, "S12": 3.1}.get(structure_id, 2.8)

    @staticmethod
    def _has_template_warning(candidate: NameCandidate) -> bool:
        return "TEMPLATE_NAME_PATTERN" in (candidate.quality_guard or {}).get("soft_warnings", [])

    @staticmethod
    def _apply_caps(raw_score: float, candidate: NameCandidate) -> float:
        capped = raw_score
        effective_level = CandidateQualityScorer._effective_evidence_level(candidate)
        if effective_level == "E3":
            capped = min(capped, 65)
        if effective_level == "E2" and candidate.evidence_suitability_score < 78:
            capped = min(capped, 71)
        if candidate.compatibility_level == "MEDIUM":
            capped = min(capped, 76)
        if candidate.naturalness_score < 85:
            capped = min(capped, 71)
        issues = (candidate.semantic_validation or {}).get("issues", [])
        if "FORCED_INTERPRETATION" in issues:
            capped = min(capped, 62)
        return capped

    @staticmethod
    def _effective_evidence_level(candidate: NameCandidate) -> str:
        if candidate.evidence_level in {"E2_COMPOSED", "E2_IMAGERY"}:
            return "E2"
        return candidate.evidence_level

    @staticmethod
    def _profile_adjustment(candidate: NameCandidate) -> float:
        profile = candidate.profile_specificity_score or 0
        surname = candidate.surname_fit_score or 0
        gender = candidate.gender_tone_fit_score or 0
        surname_affinity = ((candidate.surname_fit or {}).get("surname_affinity_score") or 72) if candidate.surname_fit else 72
        bonus = max(-5.0, (profile - 78) * 0.12)
        bonus += max(-4.0, (surname - 82) * 0.16)
        bonus += max(0.0, (surname_affinity - 72) * 0.18)
        bonus += max(-2.0, (gender - 78) * 0.035)
        bonus -= min(5.0, candidate.universal_candidate_risk * 0.045)
        return max(-8.0, min(12.0, bonus))

    @staticmethod
    def _grade(raw_score: float) -> str:
        if raw_score >= 81:
            return "S"
        if raw_score >= 72:
            return "A"
        if raw_score >= 63:
            return "B"
        if raw_score >= 54:
            return "C"
        return "D"

    @staticmethod
    def _top3_eligible(raw_score: float, breakdown: dict, candidate: NameCandidate) -> bool:
        return (
            raw_score >= 72
            and breakdown["structure"] >= 15
            and breakdown["culture"] >= 11
            and breakdown["meaning"] >= 12
            and breakdown["aesthetic"] >= 8
            and candidate.naturalness_score >= 88
            and candidate.evidence_level in {"E1", "E2", "E2_COMPOSED", "E2_IMAGERY"}
            and candidate.profile_specificity_score >= 88
            and not candidate.profile_conflicts
            and not (candidate.quality_guard or {}).get("hard_failures")
            and candidate.compatibility_level == "HIGH"
            and candidate.reconstruction
            and candidate.reconstruction.get("reconstructable")
        )

    @staticmethod
    def _top1_eligible(raw_score: float, breakdown: dict, candidate: NameCandidate) -> bool:
        return (
            raw_score >= 81
            and breakdown["structure"] >= 16
            and breakdown["culture"] >= 12
            and breakdown["meaning"] >= 13
            and breakdown["aesthetic"] >= 8
            and candidate.naturalness_score >= 90
            and candidate.evidence_level in {"E1", "E2_COMPOSED", "E2_IMAGERY"}
            and candidate.profile_specificity_score >= 90
        )
