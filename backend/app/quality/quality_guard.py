from __future__ import annotations

from backend.app.schemas.name_candidate import NameCandidate


class QualityGuard:
    def accept(self, candidate: NameCandidate, existing: list[NameCandidate]) -> tuple[bool, list[str]]:
        reasons = []
        if any(item.name == candidate.name for item in existing):
            reasons.append("名字重复")
        if candidate.pronunciation.get("homophone_issues"):
            reasons.append("命中谐音风险")
        if candidate.popularity.get("is_hot_name"):
            reasons.append("命中爆款姓名黑名单")
        if candidate.culture_origin and candidate.culture_origin.get("core", {}).get("match_type") == "imagery_related":
            reasons.append("仅意象关联出处，不能展示为直接出处")
        if candidate.score < 60:
            reasons.append("综合评分低于 MVP 阈值")
        if "改命" in candidate.recommendation_reason or "转运" in candidate.recommendation_reason:
            reasons.append("命理表述过度")
        return not reasons, reasons

