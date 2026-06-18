from __future__ import annotations

from datetime import datetime

from backend.app.schemas.baby_profile import BabyProfile, BabyProfileRequest


class BabyProfileService:
    ZODIACS = "鼠牛虎兔龙蛇马羊猴鸡狗猪"

    def normalize(self, request: BabyProfileRequest) -> BabyProfile:
        warnings: list[str] = []
        year = self._parse_year(request.birth_datetime)
        if year is None:
            warnings.append("出生时间缺失或格式无法解析，八字五行仅提供降级参考。")
        zodiac = self.zodiac_from_year(year) if year else None
        preferred = self._preferred_elements(request, year)
        dialect = "teochew" if request.need_teochew_check or self._is_teochew_place(request.birth_place) else None
        weights = self._weights(request.weight_preference)
        return BabyProfile(
            surname=request.surname.strip(),
            gender=request.gender,
            birth_datetime=request.birth_datetime,
            calendar_type=request.calendar_type,
            birth_place=request.birth_place,
            name_length=request.name_length,
            style_preferences=request.style_preferences,
            generation_char=request.generation_char,
            banned_chars=list(dict.fromkeys(request.banned_chars)),
            liked_chars=list(dict.fromkeys(request.liked_chars)),
            expectations=request.expectations,
            avoid_hot_names=request.avoid_hot_names,
            need_teochew_check=bool(dialect),
            need_culture_origin=request.need_culture_origin,
            zodiac=zodiac,
            preferred_elements=preferred,
            dialect_region=dialect,
            preference_weights=weights,
            warnings=warnings,
        )

    def zodiac_from_year(self, year: int) -> str:
        return self.ZODIACS[(year - 4) % 12]

    def _parse_year(self, value: str | None) -> int | None:
        if not value:
            return None
        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d", "%Y/%m/%d %H:%M", "%Y/%m/%d"):
            try:
                return datetime.strptime(value, fmt).year
            except ValueError:
                continue
        return None

    def _preferred_elements(self, request: BabyProfileRequest, year: int | None) -> list[str]:
        text = "".join(request.style_preferences + request.expectations)
        result = []
        mapping = {"清": "水", "温": "水", "朗": "火", "明": "火", "雅": "木", "仁": "木", "稳": "土", "坚": "金", "开阔": "木"}
        for key, element in mapping.items():
            if key in text and element not in result:
                result.append(element)
        if year and not result:
            result.append(["木", "火", "土", "金", "水"][year % 5])
        return result[:2] or ["木", "水"]

    def _weights(self, preference: str | None) -> dict[str, float]:
        weights = {"culture": 1.0, "pronunciation": 1.0, "bazi": 1.0, "modern": 1.0}
        if preference:
            if "文化" in preference:
                weights["culture"] = 1.25
            if "读音" in preference:
                weights["pronunciation"] = 1.25
            if "八字" in preference:
                weights["bazi"] = 1.25
            if "现代" in preference:
                weights["modern"] = 1.25
        return weights

    def _is_teochew_place(self, place: str | None) -> bool:
        return bool(place and any(city in place for city in ("汕头", "潮州", "揭阳", "潮汕", "澄海", "饶平", "潮阳")))

