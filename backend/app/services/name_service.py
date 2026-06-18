from __future__ import annotations

from uuid import uuid4

from backend.app.core.knowledge_loader import KnowledgeLoader
from backend.app.core.store import store
from backend.app.engines.bazi_engine import BaziEngine
from backend.app.engines.char_pool_builder import CharPoolBuilder
from backend.app.engines.culture_retriever import CultureRetriever
from backend.app.engines.name_composer import NameComposer
from backend.app.engines.name_scorer import NameScorer
from backend.app.engines.pronunciation_engine import PronunciationEngine
from backend.app.engines.wuge_engine import WugeEngine
from backend.app.engines.zodiac_engine import ZodiacEngine
from backend.app.schemas.baby_profile import BabyProfileRequest
from backend.app.schemas.name_candidate import NameCandidate
from backend.app.schemas.response import GenerateNamesResponse, RegenerateRequest
from backend.app.services.baby_profile_service import BabyProfileService
from backend.app.services.char_service import CharService
from backend.app.quality.quality_guard import QualityGuard


class NameService:
    def __init__(self, loader: KnowledgeLoader | None = None) -> None:
        self.loader = loader or KnowledgeLoader()
        self.char_service = CharService(self.loader)
        self.profile_service = BabyProfileService()
        self.bazi = BaziEngine()
        self.zodiac = ZodiacEngine(self.loader)
        self.wuge = WugeEngine(self.loader)
        self.culture = CultureRetriever(self.loader)
        self.pronunciation = PronunciationEngine(self.loader)
        self.pool_builder = CharPoolBuilder(self.char_service, self.culture)
        self.composer = NameComposer()
        self.scorer = NameScorer()
        self.guard = QualityGuard()
        self.hot_names = {row["name"]: row for row in self.loader.load()["top_names_blacklist"]}

    def generate(self, request: BabyProfileRequest, request_id: str | None = None, locked_chars: list[str] | None = None, excluded_names: set[str] | None = None) -> GenerateNamesResponse:
        request_id = request_id or str(uuid4())
        profile = self.profile_service.normalize(request)
        bazi_report = self.bazi.analyze(profile.birth_datetime)
        if bazi_report.get("preferred_elements"):
            profile.preferred_elements[:] = bazi_report["preferred_elements"]
        pools = self.pool_builder.build(profile)
        preferred_names = self.culture.candidate_names(800)
        composed = self.composer.compose(
            profile,
            pools["generation_chars"],
            excluded_names=excluded_names,
            locked_chars=locked_chars,
            preferred_names=preferred_names,
        )
        results: list[NameCandidate] = []
        for given_name, chars in composed:
            candidate = self._evaluate(profile, given_name, chars, bazi_report, pools)
            ok, reasons = self.guard.accept(candidate, results)
            if not ok:
                continue
            results.append(candidate)
            if len(results) >= 20:
                break
        if len(results) < 20:
            for given_name, chars in composed:
                if any(item.given_name == given_name for item in results):
                    continue
                candidate = self._evaluate(profile, given_name, chars, bazi_report, pools, relaxed=True)
                ok, _ = self.guard.accept(candidate, results)
                if ok and candidate.score >= 50 and not candidate.pronunciation.get("homophone_issues"):
                    results.append(candidate)
                if len(results) >= 20:
                    break
        results.sort(key=lambda item: item.score, reverse=True)
        for i, item in enumerate(results):
            item.group = "精选推荐" if i < 5 else "风格备选" if i < 15 else "创意探索"
        response = GenerateNamesResponse(request_id=request_id, profile=profile, results=results[:20])
        store.save_request(request_id, {"request": request.model_dump(), "response": response.model_dump()})
        return response

    def detail(self, request_id: str, name: str) -> NameCandidate | None:
        saved = store.get_request(request_id)
        if not saved:
            return None
        for item in saved["response"]["results"]:
            if item["name"] == name:
                return NameCandidate(**item)
        return None

    def regenerate(self, payload: RegenerateRequest) -> GenerateNamesResponse | None:
        saved = store.get_request(payload.request_id)
        if not saved:
            return None
        request = BabyProfileRequest(**saved["request"])
        banned = list(dict.fromkeys(request.banned_chars + payload.excluded_chars))
        request.banned_chars = banned
        excluded = {item["name"] for item in saved["response"]["results"]} | set(payload.excluded_names)
        return self.generate(request, request_id=str(uuid4()), locked_chars=payload.locked_chars, excluded_names=excluded)

    def _evaluate(self, profile, given_name: str, chars: list[dict], bazi_report: dict, pools: dict, relaxed: bool = False) -> NameCandidate:
        full_name = profile.surname + given_name
        pronunciation = self.pronunciation.analyze(profile.surname, given_name, profile.need_teochew_check)
        culture = self.culture.find_origin(given_name, profile.style_preferences) if profile.need_culture_origin else {"core": {}, "matches": [], "has_core_origin": False}
        zodiac = self.zodiac.analyze(profile.zodiac, chars)
        wuge = self.wuge.analyze(profile.surname, given_name)
        popularity = self._popularity(given_name, full_name)
        style_hit = any(item["char"] in {c["char"] for c in pools.get("style_chars", [])} for item in chars)
        breakdown = self.scorer.score(chars, pronunciation, culture, bazi_report, zodiac, wuge, popularity, style_hit)
        if relaxed and not culture.get("has_core_origin"):
            breakdown.total = max(50, breakdown.total)
        summary = self._summary(chars)
        warnings = list(profile.warnings) + breakdown.reasons
        if not culture.get("has_core_origin"):
            warnings.append("未找到高置信度核心出处，未伪造出处。")
        return NameCandidate(
            name=full_name,
            given_name=given_name,
            score=breakdown.total,
            pinyin=pronunciation.get("pinyin", ""),
            summary=summary,
            meaning={"chars": chars, "summary": summary},
            culture_origin=culture,
            pronunciation={k: v for k, v in pronunciation.items() if k != "teochew"},
            teochew=pronunciation.get("teochew", {}),
            bazi=bazi_report,
            zodiac=zodiac,
            wuge=wuge,
            popularity=popularity,
            score_breakdown=breakdown,
            warnings=list(dict.fromkeys(warnings)),
            recommendation_reason=self._reason(given_name, chars, culture, bazi_report),
        )

    def _popularity(self, given_name: str, full_name: str) -> dict:
        hot = self.hot_names.get(given_name) or self.hot_names.get(full_name)
        levels = [self.char_service.lookup(ch).get("heat_level", "低") for ch in given_name]
        order = {"极低": 0, "低": 1, "中": 2, "高": 3, "爆款": 4}
        heat = max(levels, key=lambda x: order.get(x, 1)) if levels else "低"
        if hot:
            heat = hot.get("heat_level", heat)
        return {"heat_level": heat, "char_heat": dict(zip(given_name, levels)), "is_hot_name": bool(hot), "hot_name_record": hot or {}}

    def _summary(self, chars: list[dict]) -> str:
        parts = []
        for item in chars:
            definition = item.get("definition", "")
            parts.append(f"{item['char']}：{definition[:34]}".strip())
        return "；".join(parts)

    def _reason(self, given_name: str, chars: list[dict], culture: dict, bazi: dict) -> str:
        elements = "、".join(filter(None, [item.get("element") for item in chars]))
        origin = culture.get("core", {}).get("title")
        if origin:
            return f"{given_name}兼顾字义、读音与本地典籍出处《{origin}》，五行属性为{elements}，仅作取名参考。"
        return f"{given_name}通过合规、字义、读音和热度检查，五行属性为{elements}；未伪造文化出处。"
