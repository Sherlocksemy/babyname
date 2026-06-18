#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""新生儿取名核心引擎。

固定流水线：合规校验 → 汉字属性筛选 → 读音谐音校验 → 文化出处匹配 → 重名热度分级 → 命理适配。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from itertools import product
from pathlib import Path
from typing import Iterable

from knowledge_loader.char_query import CharQuery
from knowledge_loader.compliance_checker import ComplianceChecker
from knowledge_loader.culture_retriever import CultureRetriever
from knowledge_loader.numerology_calc import NumerologyCalculator
from knowledge_loader.popularity_check import PopularityChecker
from knowledge_loader.pronunciation_check import PronunciationChecker


@dataclass
class NameRequest:
    """取名请求参数。"""

    surname: str
    gender: str = "N"
    birth_time: str = "2024-05-20 09:30"
    preferred_elements: list[str] = field(default_factory=list)
    banned_chars: list[str] = field(default_factory=list)
    culture_preference: str | None = None
    max_heat: str = "高"
    avoid_teochew_homophone: bool = True
    page: int = 1
    page_size: int = 20
    candidate_limit: int = 180


class NameGenerator:
    """串联六层知识库的双字名生成引擎。"""

    UNSUITABLE_NAME_CHARS = set(
        "不无未勿非毋弗否莫没勿乎兮之其而于以与也者"
        "矣焉哉耳乃若所为因则且或及并把被将就很吗呢吧"
        "去来出入上下中内外前后左右东西南北大小多少有是"
        "一二三四五六七八九十百千万亿零凡"
        "凶恶病死灾祸残贼毒怨哭哀厄丧"
    )

    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root) if project_root else Path(__file__).resolve().parents[1]
        self.compliance = ComplianceChecker(self.project_root)
        self.char_query = CharQuery(self.project_root)
        self.pronunciation = PronunciationChecker(self.project_root)
        self.culture = CultureRetriever(self.project_root)
        self.popularity = PopularityChecker(self.project_root)
        self.numerology = NumerologyCalculator(self.project_root)

    def health_check(self) -> dict:
        """检查所有 loader 是否可用。"""
        checks = {
            "compliance": self.compliance.health_check(),
            "char_query": self.char_query.health_check(),
            "pronunciation": self.pronunciation.health_check(),
            "culture": self.culture.health_check(),
            "popularity": self.popularity.health_check(),
            "numerology": self.numerology.health_check(),
        }
        return {"ok": all(item.get("ok") for item in checks.values()), "checks": checks}

    def generate(self, request: NameRequest | dict) -> dict:
        """生成姓名并返回分页后的结构化报告。"""
        try:
            req = request if isinstance(request, NameRequest) else NameRequest(**request)
        except TypeError as exc:
            return {"ok": False, "error": f"请求参数错误: {exc}", "results": []}

        health = self.health_check()
        if not health["ok"]:
            return {"ok": False, "error": "知识库加载失败", "health": health, "results": []}

        surname_check = self.compliance.validate_name(req.surname)
        if not surname_check.get("ok") or not surname_check.get("valid"):
            return {"ok": False, "error": "姓氏包含非合规字", "details": surname_check, "results": []}

        bazi_probe = self.numerology.calculate_bazi(req.birth_time)
        if not bazi_probe.get("ok"):
            return {"ok": False, "error": bazi_probe.get("error"), "results": []}

        candidates = self._build_candidate_chars(req)
        if not candidates:
            return {"ok": True, "total": 0, "page": req.page, "page_size": req.page_size, "results": []}

        results = []
        for first, second in product(candidates, repeat=2):
            if first["char"] == second["char"]:
                continue
            given_name = first["char"] + second["char"]
            full_name = req.surname + given_name
            report = self._evaluate_name(full_name, req.surname, given_name, [first, second], req)
            if not report["passed"]:
                continue
            results.append(report)

        results.sort(key=lambda item: (-item["total_score"], item["name"]))
        total = len(results)
        start = max(req.page - 1, 0) * req.page_size
        end = start + req.page_size
        return {
            "ok": True,
            "request": asdict(req),
            "total": total,
            "page": req.page,
            "page_size": req.page_size,
            "results": results[start:end],
        }

    def _build_candidate_chars(self, req: NameRequest) -> list[dict]:
        """按合规和字属性构造候选字。"""
        banned = set(req.banned_chars) | set(req.surname) | self.UNSUITABLE_NAME_CHARS
        target_count = max(req.candidate_limit, 180)
        raw = self.char_query.filter_chars(
            elements=req.preferred_elements or None,
            positive_min=3,
            common_max=2,
            limit=max(req.candidate_limit * 10, 1000),
        )
        if not raw.get("ok"):
            return []
        chars = []
        for item in raw["chars"]:
            ch = item["char"]
            if ch in banned:
                continue
            definition = item.get("definition", "")
            if any(word in definition for word in ["否定", "语气词", "代词", "介词", "助词", "数词"]):
                continue
            if not self.compliance.is_allowed_char(ch).get("allowed"):
                continue
            heat = self.popularity.get_char_heat(ch)
            if self.popularity.HEAT_ORDER.get(heat.get("heat_level", "低"), 1) > self.popularity.HEAT_ORDER.get(req.max_heat, 3):
                continue
            chars.append(item)
            if len(chars) >= target_count:
                break
        return chars

    def _evaluate_name(self, full_name: str, surname: str, given_name: str, chars: list[dict], req: NameRequest) -> dict:
        """按固定链路计算单个姓名报告。"""
        compliance_report = self.compliance.validate_name(full_name)
        if not compliance_report.get("valid"):
            return self._failed(full_name, "合规校验失败", compliance_report)

        char_scores = [self.char_query.score_char(item["char"], req.preferred_elements) for item in chars]
        attr_score = sum(item.get("score", 0) for item in char_scores) / max(len(char_scores), 1)
        if attr_score < 45:
            return self._failed(full_name, "汉字属性分过低", char_scores)

        pronunciation_report = self.pronunciation.score_pronunciation(given_name, include_teochew=req.avoid_teochew_homophone)
        if not pronunciation_report.get("ok") or not pronunciation_report.get("homophone", {}).get("safe", True):
            return self._failed(full_name, "读音或谐音风险未通过", pronunciation_report)

        culture_report = self.culture.get_name_origins(given_name, preference=req.culture_preference, limit=3)
        popularity_report = self.popularity.score_name(given_name, max_heat=req.max_heat)
        if popularity_report.get("is_hot"):
            return self._failed(full_name, "命中爆款姓名", popularity_report)

        numerology_report = self.numerology.score_numerology(surname, given_name, req.birth_time, chars)
        if not numerology_report.get("ok"):
            return self._failed(full_name, "命理计算失败", numerology_report)

        total_score = (
            compliance_report.get("valid", False) * 10
            + attr_score * 0.25
            + pronunciation_report.get("score", 0) * 0.2
            + culture_report.get("score", 0) * 0.15
            + popularity_report.get("score", 0) * 0.15
            + numerology_report.get("score", 0) * 0.15
        )
        return {
            "name": full_name,
            "given_name": given_name,
            "passed": True,
            "total_score": round(total_score, 2),
            "report": {
                "compliance": compliance_report,
                "char_attribute": {"score": round(attr_score, 2), "chars": char_scores},
                "pronunciation": pronunciation_report,
                "culture": culture_report,
                "popularity": popularity_report,
                "numerology": numerology_report,
            },
        }

    @staticmethod
    def _failed(name: str, reason: str, details) -> dict:
        return {"name": name, "passed": False, "total_score": 0, "reason": reason, "details": details}


def generate_names(**kwargs) -> dict:
    """函数式调用入口。"""
    return NameGenerator().generate(NameRequest(**kwargs))


if __name__ == "__main__":
    engine = NameGenerator()
    demo = NameRequest(
        surname="陈",
        gender="N",
        birth_time="2024-05-20 09:30",
        preferred_elements=["木", "水"],
        banned_chars=["伟", "强"],
        culture_preference="shijing",
        max_heat="高",
        avoid_teochew_homophone=True,
        page_size=5,
    )
    print(engine.generate(demo))
