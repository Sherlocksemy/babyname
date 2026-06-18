from __future__ import annotations

import re

from backend.app.core.knowledge_loader import KnowledgeLoader


class PronunciationEngine:
    def __init__(self, loader: KnowledgeLoader | None = None) -> None:
        self.data = (loader or KnowledgeLoader()).load()
        self.mandarin = self.data["mandarin"]
        self.teochew: dict[str, list[dict]] = {}
        for row in self.data["teochew"]:
            self.teochew.setdefault(row.get("char", ""), []).append(row)
        self.blacklist: dict[str, list[dict]] = {}
        for row in self.data["homophone_blacklist"]:
            self.blacklist.setdefault(row.get("char", ""), []).append(row)

    def analyze(self, surname: str, given_name: str, need_teochew: bool = True) -> dict:
        full = surname + given_name
        readings = [self._main_reading(ch) for ch in full]
        tones = [r.get("tone", 0) for r in readings]
        initials = [self._initial(r.get("pinyin", "")) for r in readings]
        issues = []
        for ch in given_name:
            for item in self.blacklist.get(ch, []):
                if need_teochew or item.get("language_type") == "mandarin":
                    issues.append(item)
        same_tone = len(given_name) == 2 and len(set(tones[-2:])) == 1
        same_initial = len(given_name) == 2 and initials[-1] and initials[-1] == initials[-2]
        score = 90
        reasons = ["普通话读音来自本地拼音库。"]
        if same_tone:
            score -= 10
            reasons.append("名用字声调变化较少。")
        if same_initial:
            score -= 8
            reasons.append("名用字声母相同，顺口度略降。")
        if issues:
            score -= min(45, len(issues) * 15)
            reasons.append("命中谐音风险黑名单。")
        teochew_rows = {ch: self.teochew.get(ch, [])[:6] for ch in given_name}
        return {
            "pinyin": " ".join(r.get("pinyin", "") for r in readings).strip(),
            "readings": readings,
            "tones": tones,
            "teochew": teochew_rows,
            "homophone_issues": issues,
            "safe": not issues,
            "score": max(0, min(100, score)),
            "reasons": reasons,
        }

    def _main_reading(self, char: str) -> dict:
        readings = self.mandarin.get(char) or []
        common = next((r for r in readings if r.get("is_common")), readings[0] if readings else {})
        return {"char": char, **common}

    def _initial(self, pinyin: str) -> str:
        plain = re.sub(r"[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]", "", pinyin.lower())
        for initial in ("zh", "ch", "sh"):
            if plain.startswith(initial):
                return initial
        return plain[:1]
