from __future__ import annotations

from typing import Any

from app.catalogs.archetype_catalog import ARCHETYPES
from app.catalogs.structure_catalog import STRUCTURES
from app.repositories.naming_repository import loads
from app.services.evidence_excerpt_builder import EvidenceExcerptBuilder


DISCLAIMER = "传统命理、生肖及五格内容仅供文化参考，不构成对个人命运、健康、教育或职业发展的现实承诺。"
STRUCTURE_LABELS = {item["id"]: item["name"] for item in STRUCTURES}
ARCHETYPE_LABELS = {item["id"]: item["name"] for item in ARCHETYPES}
GENERATION_LABELS = {
    "direct_expression": "整体出处",
    "semantic_role_composition": "双字文化组合推导",
    "imagery_transformation": "意象转化推导",
}


class CandidateDetailService:
    def __init__(self, indexes: dict[str, Any] | None = None) -> None:
        self.indexes = indexes or {}
        self.excerpts = EvidenceExcerptBuilder()

    def to_card(self, candidate_row) -> dict:
        payload = loads(candidate_row.candidate_payload_json) or {}
        score = payload.get("score") or {}
        origin = self._origin(payload)
        display_score = self._score_contract(candidate_row, payload)
        return {
            "candidate_id": candidate_row.candidate_id,
            "engine_candidate_id": payload.get("candidate_id"),
            "rank_type": candidate_row.rank_type,
            "rank_position": candidate_row.rank_position,
            "full_name": candidate_row.full_name,
            "given_name": candidate_row.given_name,
            "score": candidate_row.score,
            "display_score": display_score,
            "nes_score": display_score["nes_score"],
            "ranking_score": display_score["ranking_score"],
            "structure": payload.get("structure_id"),
            "structure_label": STRUCTURE_LABELS.get(payload.get("structure_id"), "未归类"),
            "archetype": payload.get("archetype_id"),
            "archetype_label": ARCHETYPE_LABELS.get(payload.get("archetype_id"), "未归类"),
            "generation_label": GENERATION_LABELS.get(payload.get("generation_mode"), "文化推导"),
            "origin": origin,
            "culture_source": origin["display_label"],
            "culture_evidence": origin["name_level_evidence"],
            "one_sentence_meaning": payload.get("combined_meaning") or self._fallback_meaning(payload),
            "pinyin": self._pinyin(payload),
            "teochew_pronunciation": self._teochew_contract(payload),
            "popularity_template_risk": self._popularity_template_risk(payload),
            "quality_guard": payload.get("quality_guard"),
            "nes_breakdown": score.get("breakdown", {}),
        }

    def to_detail(self, candidate_row, request_id: str) -> dict:
        payload = loads(candidate_row.candidate_payload_json) or {}
        first = payload.get("first_char") or {}
        second = payload.get("second_char") or {}
        chars = [char for char in [first.get("char"), second.get("char")] if char]
        char_details = [self._char_detail(char) for char in chars]
        origin = self._origin(payload)
        fortune = payload.get("fortune_evaluation") or {}
        metadata = fortune.get("metadata") or {}
        score = payload.get("score") or {}
        display_score = self._score_contract(candidate_row, payload)
        return {
            "request_id": request_id,
            "candidate_id": candidate_row.candidate_id,
            "engine_candidate_id": payload.get("candidate_id"),
            "name": {
                "surname": payload.get("surname"),
                "given_name": payload.get("given_name"),
                "full_name": payload.get("full_name"),
                "pinyin": self._pinyin(payload),
            },
            "recommendation": {
                "score": candidate_row.score,
                "display_score": display_score,
                "grade": score.get("alpha_grade"),
                "summary": payload.get("combined_meaning") or self._fallback_meaning(payload),
            },
            "structure": {
                "structure_id": payload.get("structure_id"),
                "label": STRUCTURE_LABELS.get(payload.get("structure_id"), "未归类"),
                "semantic_pattern": payload.get("semantic_pattern"),
                "semantic_roles": [payload.get("semantic_role_first"), payload.get("semantic_role_second")],
                "compatibility_level": payload.get("compatibility_level"),
                "compatibility_reason_codes": payload.get("compatibility_reason_codes", []),
            },
            "archetype": {
                "archetype_id": payload.get("archetype_id"),
                "label": ARCHETYPE_LABELS.get(payload.get("archetype_id"), "未归类"),
                "profile_fit_reasons": payload.get("profile_fit_reasons", []),
                "profile_conflicts": payload.get("profile_conflicts", []),
            },
            "imagery": {
                "first_char_source": payload.get("first_char_source", []),
                "second_char_source": payload.get("second_char_source", []),
                "generation_mode": payload.get("generation_mode"),
                "generation_label": GENERATION_LABELS.get(payload.get("generation_mode"), "文化推导"),
            },
            "origin": origin,
            "culture": origin,
            "meaning": {
                "chars": char_details,
                "combined_meaning": payload.get("combined_meaning"),
                "meaning_completeness": payload.get("meaning_completeness"),
            },
            "pronunciation": {
                "mandarin": [self._pronunciation(char).get("mandarin", []) for char in chars],
                "teochew": [self._pronunciation(char).get("teochew", []) for char in chars],
                "teochew_pronunciation": self._teochew_contract(payload),
                "homophone_risks": [risk for char in chars for risk in self._pronunciation(char).get("homophone_risks", [])],
                "risk_level": self._teochew_contract(payload)["risk_level"],
            },
            "fortune": {
                "five_elements": {
                    "score": fortune.get("score"),
                    "recommended_elements": fortune.get("recommended_elements", []),
                    "caution_elements": fortune.get("caution_elements", []),
                    "char_elements": metadata.get("char_elements", []),
                    "status": fortune.get("status"),
                },
                "zodiac": metadata.get("zodiac"),
                "wuge": {
                    **(metadata.get("wuge") or {}),
                    "interpretation_status": (metadata.get("wuge") or {}).get("interpretation_status", "DATA_INCOMPLETE"),
                },
            },
            "scores": {
                "nes_total": candidate_row.score,
                "ranking_score": display_score["ranking_score"],
                "selection_reasons": display_score["selection_reasons"],
                "diversity_reasons": display_score["diversity_reasons"],
                "nes_version": score.get("score_version"),
                "breakdown": score.get("breakdown", {}),
                "sub_breakdown": score.get("sub_breakdown", {}),
                "naturalness": payload.get("naturalness_score"),
                "profile_specificity": payload.get("profile_specificity_score"),
                "surname_fit": payload.get("surname_fit"),
                "popularity_template_risk": self._popularity_template_risk(payload),
            },
            "quality_guard": payload.get("quality_guard"),
            "generation_path": payload.get("generation_reason_codes", []),
            "limitations": list((fortune.get("limitations") or [])) + ["五格吉凶断语数据不足时仅展示计算值。"],
            "disclaimer": DISCLAIMER,
        }

    def _char_detail(self, char: str) -> dict:
        index = self.indexes.get("character")
        data = index.get(char) if index else {"char": char}
        return {
            "char": char,
            "semantic": data.get("semantic"),
            "kangxi": data.get("kangxi"),
            "base": data.get("base"),
        }

    def _pronunciation(self, char: str) -> dict:
        index = self.indexes.get("pronunciation")
        return index.get(char) if index else {"char": char, "mandarin": [], "teochew": [], "homophone_risks": []}

    @staticmethod
    def _culture_label(evidence: dict) -> str:
        parts = [evidence.get("book"), evidence.get("title")]
        return " / ".join(str(item) for item in parts if item) or str(evidence.get("source_type") or "")

    def _origin(self, payload: dict) -> dict:
        mode_map = {
            "direct_expression": "DIRECT_EXPRESSION",
            "semantic_role_composition": "SEMANTIC_ROLE_COMPOSITION",
            "imagery_transformation": "IMAGERY_TRANSFORMATION",
        }
        mode = mode_map.get(str(payload.get("generation_mode") or ""), "IMAGERY_TRANSFORMATION")
        evidences = payload.get("evidences") or []
        if mode == "DIRECT_EXPRESSION":
            evidence = self.excerpts.direct_name_evidence(evidences[0] if evidences else {}, payload.get("given_name"))
            if evidence:
                return {
                    "mode": mode,
                    "display_label": f"整体出处：{self._culture_label(evidence)}",
                    "name_level_evidence": evidence,
                    "component_evidences": [],
                    "composition_reason": None,
                    "combined_meaning": payload.get("combined_meaning"),
                    "disclaimer": None,
                }
            mode = "SEMANTIC_ROLE_COMPOSITION"
        first = (payload.get("first_char") or {}).get("char") or (str(payload.get("given_name") or "")[:1])
        second = (payload.get("second_char") or {}).get("char") or (str(payload.get("given_name") or "")[1:2])
        component_evidences = []
        for position, char, evidence in [
            ("FIRST", first, evidences[0] if len(evidences) > 0 else {}),
            ("SECOND", second, evidences[1] if len(evidences) > 1 else {}),
        ]:
            if char:
                component_evidences.append(
                    {
                        "position": position,
                        "char": char,
                        **self._evidence_payload(evidence, matched_text=char),
                    }
                )
        if mode == "SEMANTIC_ROLE_COMPOSITION":
            label = "双字文化组合推导"
        else:
            label = "意象转化推导"
        return {
            "mode": mode,
            "display_label": label,
            "name_level_evidence": None,
            "component_evidences": component_evidences,
            "composition_reason": self._composition_reason(payload),
            "combined_meaning": payload.get("combined_meaning"),
            "disclaimer": "该姓名由多个文化证据与命名结构组合推导，并非古籍原文中的固定双字姓名表达。",
        }

    def _evidence_payload(self, evidence: dict, matched_text: str | None = None) -> dict:
        return self.excerpts.build(evidence, matched_text)

    @staticmethod
    def _composition_reason(payload: dict) -> str:
        roles = [payload.get("semantic_role_first"), payload.get("semantic_role_second")]
        roles = [str(item) for item in roles if item]
        if roles:
            return f"结合“{'、'.join(roles)}”的语义角色形成双字命名表达。"
        return "结合两个字的文化证据、字义和姓名结构形成命名表达。"

    @staticmethod
    def _fallback_meaning(payload: dict) -> str:
        roles = [payload.get("semantic_role_first"), payload.get("semantic_role_second")]
        roles = [str(item) for item in roles if item]
        return "、".join(roles) if roles else "基于结构、字义与出处综合推荐。"

    @staticmethod
    def _pinyin(payload: dict) -> str:
        result: list[str] = []
        for key in ("first_char", "second_char"):
            readings = ((payload.get(key) or {}).get("mandarin") or [])
            if readings:
                result.append(str(readings[0].get("pinyin") or ""))
        return " ".join(item for item in result if item)

    @staticmethod
    def _risk_level(payload: dict) -> str:
        guard = payload.get("quality_guard") or {}
        failures = guard.get("hard_failures") or []
        warnings = guard.get("soft_warnings") or []
        if failures:
            return "HIGH"
        if warnings:
            return "NOTICE"
        return "LOW"

    def _teochew_contract(self, payload: dict) -> dict:
        characters = []
        for key in ("first_char", "second_char"):
            data = payload.get(key) or {}
            char = data.get("char")
            readings = data.get("teochew") or []
            if char:
                characters.append({"char": char, "readings": readings})
        queried = any(item["readings"] for item in characters)
        return {
            "characters": characters,
            "full_name_reading_status": "PARTIAL" if queried else "NOT_EVALUATED",
            "risk_level": "UNKNOWN",
            "risk_reasons": [],
            "limitations": ["潮汕单字读音：已查询" if queried else "潮汕单字读音：暂未查询", "姓名连读及变调风险：暂未完整评估"],
        }

    @staticmethod
    def _popularity_template_risk(payload: dict) -> dict:
        score = payload.get("score") or {}
        uniqueness = (score.get("breakdown") or {}).get("uniqueness")
        collision = payload.get("historical_name_collision")
        level = "UNKNOWN"
        reasons: list[str] = []
        if isinstance(uniqueness, (int, float)):
            if uniqueness >= 8:
                level = "LOW"
            elif uniqueness >= 5:
                level = "MEDIUM"
            else:
                level = "HIGH"
            reasons.append("根据热门字、模板名和内部避雷规则综合评估。")
        if collision and collision != "UNKNOWN":
            reasons.append(f"历史姓名碰撞标记：{collision}")
        labels = {"LOW": "低", "MEDIUM": "中", "HIGH": "高", "UNKNOWN": "暂无法评估"}
        return {"level": level, "label": labels[level], "reasons": reasons}

    @staticmethod
    def _score_contract(candidate_row, payload: dict) -> dict:
        score = payload.get("score") or {}
        nes = round(float(candidate_row.score or 0), 1)
        if candidate_row.rank_type == "TOP3":
            ranking = round(max(90.0, 100.0 - (candidate_row.rank_position - 1) * 2.5), 1)
            selection = ["进入精品方案：综合考虑基础质量、画像适配和多样性。"]
            diversity: list[str] = []
        else:
            ranking = round(max(70.0, 88.0 - (candidate_row.rank_position - 1) * 1.2), 1)
            selection = ["列入备选方案：基础质量达标，可作为补充选择。"]
            diversity = ["该名字基础质量较高，但为保持精品方案在人格、结构和用字上的差异性，列入备选方案。"]
        return {
            "nes_score": nes,
            "ranking_score": ranking,
            "rank_type": candidate_row.rank_type,
            "selection_reasons": selection,
            "diversity_reasons": diversity,
            "grade": score.get("alpha_grade") or ("卓越" if nes >= 90 else "优秀" if nes >= 85 else "良好"),
        }
