from __future__ import annotations

from backend.app.core.knowledge_loader import KnowledgeLoader


class CultureRetriever:
    SOURCES = {"shijing": "诗经", "chuci": "楚辞", "tang_poetry": "唐诗", "song_ci": "宋词", "sishuwujing": "四书五经"}

    def __init__(self, loader: KnowledgeLoader | None = None) -> None:
        self.data = (loader or KnowledgeLoader()).load()
        self.items: list[dict] = []
        self.candidate_index: dict[str, list[dict]] = {}
        self.char_index: dict[str, list[dict]] = {}
        for key, label in self.SOURCES.items():
            for item in self.data[key]:
                row = {**item, "source": label, "source_key": key}
                self.items.append(row)
                for candidate in row.get("name_candidates") or []:
                    self.candidate_index.setdefault(candidate, []).append(row)
                for ch in set(row.get("content", "")):
                    self.char_index.setdefault(ch, []).append(row)

    def find_origin(self, given_name: str, styles: list[str] | None = None) -> dict:
        styles = styles or []
        hits: list[dict] = []
        for item in self.candidate_index.get(given_name, []):
            hits.append(self._format(item, given_name, "candidate_source", 0.95))
        if not hits:
            direct = self._direct_phrase(given_name)
            if direct:
                hits.append(self._format(direct, given_name, "direct_phrase", 0.9))
        if not hits:
            hits.extend(self._char_hits(given_name, styles))
        hits.sort(key=lambda x: x["confidence"], reverse=True)
        core = hits[0] if hits and hits[0]["confidence"] >= 0.6 else {}
        return {"core": core, "matches": hits[:3], "has_core_origin": bool(core)}

    def candidate_chars(self, limit: int = 300) -> list[str]:
        chars: list[str] = []
        for name in self.candidate_index:
            for ch in name:
                if "\u4e00" <= ch <= "\u9fff" and ch not in chars:
                    chars.append(ch)
                if len(chars) >= limit:
                    return chars
        return chars

    def candidate_names(self, limit: int = 500) -> list[str]:
        names: list[str] = []
        seen = set()
        for name in self.candidate_index:
            if len(name) != 2 or name in seen:
                continue
            if all("\u4e00" <= ch <= "\u9fff" for ch in name):
                names.append(name)
                seen.add(name)
            if len(names) >= limit:
                break
        return names

    def _direct_phrase(self, phrase: str) -> dict | None:
        for ch in phrase:
            for item in self.char_index.get(ch, [])[:80]:
                if phrase in item.get("content", ""):
                    return item
        return None

    def _char_hits(self, given_name: str, styles: list[str]) -> list[dict]:
        scores: dict[str, tuple[dict, float]] = {}
        for ch in given_name:
            for item in self.char_index.get(ch, [])[:80]:
                confidence = 0.62 if len(given_name) == 1 else 0.55
                keywords = item.get("keywords") or []
                if any(style in keywords for style in styles):
                    confidence += 0.03
                scores[item.get("id", str(id(item)))] = (item, max(confidence, scores.get(item.get("id", ""), ({}, 0))[1] if item.get("id", "") in scores else confidence))
        return [self._format(item, given_name, "direct_char", score) for item, score in scores.values()]

    def _format(self, item: dict, name: str, match_type: str, confidence: float) -> dict:
        content = item.get("content", "")
        quote = content.replace("\n", "。")[:120]
        return {
            "source": item.get("source"),
            "title": item.get("title", ""),
            "author": item.get("author", ""),
            "dynasty": item.get("dynasty", ""),
            "chapter": item.get("chapter", ""),
            "original_text": quote,
            "translation": item.get("translation", ""),
            "matched_chars": [ch for ch in name if ch in content or ch in "".join(item.get("name_candidates") or [])],
            "match_type": match_type,
            "confidence": round(confidence, 2),
            "keywords": item.get("keywords") or [],
            "explanation": "出处来自本地知识库，按直接词组、候选词或单字命中排序。",
        }
