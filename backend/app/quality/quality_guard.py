from __future__ import annotations

from backend.app.schemas.name_candidate import NameCandidate


class QualityGuard:
    BAD_NAME_CHARS = set("之以于其而也者乎矣焉哉兮尔何只中上下来去出入左右东西南北为与")

    def accept(self, candidate: NameCandidate, existing: list[NameCandidate]) -> tuple[bool, list[str]]:
        reasons = []
        if any(item.name == candidate.name for item in existing):
            reasons.append("名字重复")
        if any(ch in self.BAD_NAME_CHARS for ch in candidate.given_name):
            reasons.append("包含不适合现代取名的虚词、代词或方位字")
        if candidate.pronunciation.get("homophone_issues"):
            reasons.append("命中谐音风险")
        if candidate.popularity.get("is_hot_name"):
            reasons.append("命中爆款姓名黑名单")
        if candidate.popularity.get("heat_level") == "爆款":
            reasons.append("热度为爆款")
        if list(candidate.popularity.get("char_heat", {}).values()).count("高") >= 2:
            reasons.append("高热单字堆叠")
        if candidate.culture_origin and candidate.culture_origin.get("core", {}).get("match_type") == "imagery_related":
            reasons.append("仅意象关联出处，不能展示为直接出处")
        for item in candidate.meaning.get("chars", []):
            if item.get("common_level", 3) > 2:
                reasons.append(f"{item.get('char')}常用度不足")
            if item.get("positive_level", 0) < 3:
                reasons.append(f"{item.get('char')}正向等级不足")
        if candidate.score < 60:
            reasons.append("综合评分低于 MVP 阈值")
        if "改命" in candidate.recommendation_reason or "转运" in candidate.recommendation_reason:
            reasons.append("命理表述过度")
        return not reasons, reasons
