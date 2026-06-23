from __future__ import annotations

import hashlib

from app.schemas.candidate import NameCandidate
from app.schemas.naming_input import NamingInput


STYLE_RULES: dict[str, dict] = {
    "书卷清雅": {
        "structures": ["S01", "S06", "S08"],
        "archetypes": ["A01", "A02"],
        "imagery": ["竹", "兰", "清", "文", "书"],
        "roles": ["认知", "思辨", "文气", "书卷", "清正"],
        "sources": ["sishuwujing", "tang_poetry", "song_ci"],
    },
    "君子品格": {
        "structures": ["S02", "S07"],
        "archetypes": ["A03", "A07"],
        "imagery": ["德", "仁", "敬", "正", "信"],
        "roles": ["德行", "仁德", "敬慎", "正直", "践行"],
        "sources": ["sishuwujing", "shijing"],
    },
    "温润知性": {
        "structures": ["S08", "S09", "S06"],
        "archetypes": ["A01", "A08", "A09"],
        "imagery": ["清", "灵", "安", "和", "宁", "兰", "芷"],
        "roles": ["清正", "温和", "宁静", "灵秀", "思辨"],
        "sources": ["song_ci", "shijing", "sishuwujing"],
    },
    "民国书卷气": {
        "structures": ["S06", "S08", "S09"],
        "archetypes": ["A01", "A09"],
        "imagery": ["文", "清", "章", "兰", "雅"],
        "roles": ["文气", "清正", "文采", "书卷"],
        "sources": ["song_ci", "tang_poetry"],
    },
    "大气开阔": {
        "structures": ["S03", "S05", "S10"],
        "archetypes": ["A04", "A05", "A06"],
        "imagery": ["岳", "海", "天", "云", "鸿", "远", "岩"],
        "roles": ["远志", "弘阔", "天宇", "山岳", "鸿志"],
        "sources": ["chuci", "tang_poetry"],
    },
    "山水自然": {
        "structures": ["S05", "S11"],
        "archetypes": ["A02", "A07", "A09"],
        "imagery": ["山", "川", "泉", "松", "竹", "云", "岳"],
        "roles": ["山岳", "清泉", "竹节", "云气", "自然"],
        "sources": ["shijing", "tang_poetry", "chuci"],
    },
    "现代高级": {
        "structures": ["S08", "S09", "S11"],
        "archetypes": ["A08", "A09", "A11"],
        "imagery": ["宁", "清", "和", "初", "煦", "朗", "衡"],
        "roles": ["宁静", "清正", "温和", "新生", "平衡"],
        "sources": ["song_ci", "shijing"],
        "avoid": ["S02", "S10", "A04", "CLASSIC_NATURE"],
    },
    "温柔坚定": {
        "structures": ["S08", "S11", "S04"],
        "archetypes": ["A08", "A10", "A11"],
        "imagery": ["宁", "安", "清", "明", "煦", "芷"],
        "roles": ["宁静", "安定", "清正", "光明", "温煦"],
        "sources": ["shijing", "song_ci", "sishuwujing"],
    },
    "雅致": {
        "structures": ["S09", "S08", "S06"],
        "archetypes": ["A09", "A02", "A01"],
        "imagery": ["清", "灵", "兰", "芷", "文", "章"],
        "roles": ["清正", "灵秀", "文采", "雅正"],
        "sources": ["song_ci", "shijing", "tang_poetry"],
    },
    "思想家": {
        "structures": ["S01", "S06", "S10"],
        "archetypes": ["A02", "A06", "A01"],
        "imagery": ["思", "知", "远", "渊", "微", "辨", "闻", "道"],
        "roles": ["认知", "思辨", "深远", "远志"],
        "sources": ["sishuwujing", "chuci"],
    },
}


class ProfileSpecificityEngine:
    def build(self, naming_input: NamingInput) -> dict:
        vector = {"structures": {}, "archetypes": {}, "imagery": {}, "roles": {}, "sources": {}, "avoid": {}}
        for style in naming_input.style_preferences:
            for key, values in STYLE_RULES.get(style, {}).items():
                target = "sources" if key == "sources" else key
                for value in values:
                    vector[target][value] = vector[target].get(value, 0) + 1
        gender_tone = self._gender_tone(naming_input.gender)
        signature_raw = "|".join([naming_input.surname, naming_input.gender, naming_input.region] + naming_input.style_preferences + naming_input.liked_chars + naming_input.blocked_chars)
        return {
            "profile_signature": hashlib.sha1(signature_raw.encode("utf-8")).hexdigest()[:12],
            "gender_tone": gender_tone,
            "style_vector": vector,
            "preferred_structures": sorted(vector["structures"], key=vector["structures"].get, reverse=True),
            "preferred_archetypes": sorted(vector["archetypes"], key=vector["archetypes"].get, reverse=True),
            "preferred_imagery": sorted(vector["imagery"], key=vector["imagery"].get, reverse=True),
            "preferred_semantic_roles": sorted(vector["roles"], key=vector["roles"].get, reverse=True),
            "preferred_culture_sources": sorted(vector["sources"], key=vector["sources"].get, reverse=True),
            "avoid_style_tags": sorted(vector["avoid"], key=vector["avoid"].get, reverse=True),
        }

    def evaluate_candidate(self, candidate: NameCandidate, profile: dict, naming_input: NamingInput) -> dict:
        reasons: list[str] = []
        conflicts: list[str] = []
        style_fit = 54.0
        if candidate.structure_id in profile["preferred_structures"]:
            style_fit += 18
            reasons.append("PROFILE_STRUCTURE_MATCH")
        if candidate.archetype_id in profile["preferred_archetypes"]:
            style_fit += 16
            reasons.append("PROFILE_ARCHETYPE_MATCH")
        role_text = candidate.semantic_role_first + candidate.semantic_role_second + candidate.combined_meaning + candidate.given_name
        role_hits = sum(1 for role in profile["preferred_semantic_roles"] if role and role in role_text)
        imagery_hits = sum(1 for image in profile["preferred_imagery"] if image and image in role_text)
        source_hits = sum(1 for evidence in candidate.evidences[:2] if evidence.source_type in profile["preferred_culture_sources"])
        style_fit += min(16, role_hits * 4)
        imagery_fit = min(100, 62 + imagery_hits * 12 + source_hits * 6)
        if role_hits:
            reasons.append("PROFILE_ROLE_MATCH")
        if imagery_hits:
            reasons.append("PROFILE_IMAGERY_MATCH")
        if source_hits:
            reasons.append("PROFILE_CULTURE_SOURCE_MATCH")
        for avoid in profile["avoid_style_tags"]:
            if candidate.structure_id == avoid or candidate.archetype_id == avoid:
                conflicts.append("AVOID_STYLE_TAG")
                style_fit -= 18
            if avoid == "CLASSIC_NATURE" and any(char in candidate.given_name for char in "泉松竹乔岳山川"):
                conflicts.append("AVOID_CLASSIC_NATURE_IMAGERY")
                style_fit -= 20
        gender = self._gender_score(candidate, naming_input.gender)
        if gender["score"] < 70:
            conflicts.append("GENDER_TONE_CONFLICT")
        universal_risk = max(0, 78 - style_fit) + max(0, 70 - imagery_fit) * 0.4
        if role_hits == 0 and imagery_hits == 0:
            universal_risk += 18
            conflicts.append("LOW_PROFILE_SPECIFICITY")
        source_fit = min(100, source_hits * 50)
        score = 0.42 * max(0, min(100, style_fit)) + 0.18 * gender["score"] + 0.18 * imagery_fit + 0.12 * candidate.surname_fit_score + 0.1 * source_fit
        if len(reasons) >= 4:
            score += 6
        score -= min(18, universal_risk * 0.25)
        return {
            "style_fit_score": round(max(0, min(100, style_fit)), 2),
            "gender_tone_fit_score": gender["score"],
            "gender_tone_reason_codes": gender["reasons"],
            "imagery_fit_score": round(imagery_fit, 2),
            "profile_specificity_score": round(max(0, min(100, score)), 2),
            "profile_fit_reasons": reasons,
            "profile_conflicts": conflicts,
            "universal_candidate_risk": round(min(100, universal_risk), 2),
            "cross_profile_dominance_risk": round(min(100, universal_risk + (12 if not reasons else 0)), 2),
        }

    @staticmethod
    def _gender_tone(gender: str) -> str:
        return {"female": "warm_intellectual", "male": "clear_responsible", "neutral": "modern_neutral"}.get(gender, "neutral")

    @staticmethod
    def _gender_score(candidate: NameCandidate, gender: str) -> dict:
        text = candidate.semantic_role_first + candidate.semantic_role_second + candidate.combined_meaning + candidate.given_name
        score = 78.0
        reasons: list[str] = []
        if gender == "female":
            if any(token in text for token in ["宁", "清", "灵", "和", "芷", "兰", "温"]):
                score += 14
                reasons.append("FEMALE_WARM_INTELLECTUAL")
            if any(token in text for token in ["弘", "毅", "岳", "将", "战"]):
                score -= 12
                reasons.append("FEMALE_OVER_MASCULINE_PENALTY")
        elif gender == "male":
            if any(token in text for token in ["敬", "修", "毅", "岳", "德", "正", "远"]):
                score += 12
                reasons.append("MALE_CLEAR_RESPONSIBLE")
            if any(token in text for token in ["汐", "萱", "兮"]):
                score -= 12
                reasons.append("MALE_SOFT_TEMPLATE_PENALTY")
        else:
            if any(token in text for token in ["清", "安", "思", "云", "灵"]):
                score += 10
                reasons.append("NEUTRAL_MODERN_NATURAL")
            if any(token in text for token in ["弘", "毅", "萱", "汐"]):
                score -= 8
                reasons.append("NEUTRAL_GENDERED_SIGNAL_PENALTY")
        return {"score": round(max(0, min(100, score)), 2), "reasons": reasons or ["GENDER_TONE_BASELINE"]}
