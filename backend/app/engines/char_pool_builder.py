from __future__ import annotations

from backend.app.engines.culture_retriever import CultureRetriever
from backend.app.schemas.baby_profile import BabyProfile
from backend.app.services.char_service import CharService


class CharPoolBuilder:
    NEGATIVE_HINTS = ("凶", "恶", "病", "死", "灾", "祸", "怨", "哭", "哀", "毒")
    STOP_CHARS = set("之以于其而也者乎矣焉哉兮曰云女男子我你他她它的一了是有在不")
    STYLE_HINTS = {
        "清朗": ("清", "朗", "明", "澄", "皓", "晨"),
        "温润": ("温", "润", "宁", "和", "安", "柔"),
        "儒雅": ("文", "雅", "书", "言", "修", "礼"),
        "大气": ("宇", "远", "泽", "弘", "博", "然"),
        "诗意": ("诗", "云", "月", "溪", "若", "知"),
        "国风": ("子", "君", "之", "怀", "允", "清"),
        "现代": ("一", "辰", "希", "予", "可", "言"),
        "极简": ("一", "宁", "安", "白", "之", "予"),
    }

    def __init__(self, char_service: CharService, culture: CultureRetriever) -> None:
        self.char_service = char_service
        self.culture = culture

    def build(self, profile: BabyProfile, limit: int = 140) -> dict:
        banned = set(profile.surname) | set(profile.banned_chars)
        if profile.generation_char:
            banned.discard(profile.generation_char)
        pools: dict[str, list[dict]] = {"liked_chars": [], "style_chars": [], "culture_chars": [], "core_chars": [], "blocked_chars": []}
        for ch in profile.liked_chars + ([profile.generation_char] if profile.generation_char else []):
            if ch and self._allowed(ch, banned, profile):
                pools["liked_chars"].append(self.char_service.lookup(ch))
        for style in profile.style_preferences:
            for ch in self.STYLE_HINTS.get(style, ()):
                if self._allowed(ch, banned, profile):
                    pools["style_chars"].append(self.char_service.lookup(ch))
        for ch in self.culture.candidate_chars(280):
            if self._allowed(ch, banned, profile):
                pools["culture_chars"].append(self.char_service.lookup(ch))
        for item in self.char_service.iter_nameable_chars():
            if len(pools["core_chars"]) >= limit:
                break
            if self._allowed(item["char"], banned, profile):
                pools["core_chars"].append(item)
            else:
                pools["blocked_chars"].append({"char": item["char"], "reason": "禁用、非合规、负面或热度过滤"})
        merged = []
        seen = set()
        for key in ("liked_chars", "style_chars", "culture_chars", "core_chars"):
            for item in pools[key]:
                ch = item["char"]
                if ch not in seen:
                    merged.append(item)
                    seen.add(ch)
                if len(merged) >= limit:
                    break
        pools["generation_chars"] = merged
        return pools

    def _allowed(self, char: str, banned: set[str], profile: BabyProfile) -> bool:
        if not char or char in banned or char in self.STOP_CHARS or not self.char_service.is_compliant(char):
            return False
        item = self.char_service.lookup(char)
        if any(word in item.get("definition", "") for word in self.NEGATIVE_HINTS):
            return False
        if profile.avoid_hot_names and item.get("heat_level") == "爆款":
            return False
        return item.get("positive_level", 0) >= 3
