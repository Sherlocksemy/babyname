from __future__ import annotations

from datetime import datetime

from lunar_python import Lunar, Solar


class LunarCalendarAdapter:
    library_name = "lunar-python"
    library_version = "1.4.8"

    def solar_to_lunar(self, dt: datetime) -> dict:
        solar = Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        lunar = solar.getLunar()
        return self._lunar_to_dict(lunar)

    def lunar_to_solar(self, year: int, month: int, day: int, hour: int, minute: int, is_leap_month: bool) -> datetime:
        lunar_month = -month if is_leap_month else month
        lunar = Lunar.fromYmdHms(year, lunar_month, day, hour, minute, 0)
        solar = lunar.getSolar()
        return datetime(solar.getYear(), solar.getMonth(), solar.getDay(), solar.getHour(), solar.getMinute(), solar.getSecond())

    def eight_char(self, dt: datetime, sect: int = 2) -> dict:
        lunar = Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second).getLunar()
        eight = lunar.getEightChar()
        eight.setSect(sect)
        return {
            "year": eight.getYear(),
            "month": eight.getMonth(),
            "day": eight.getDay(),
            "time": eight.getTime(),
            "year_gan": eight.getYearGan(),
            "year_zhi": eight.getYearZhi(),
            "month_gan": eight.getMonthGan(),
            "month_zhi": eight.getMonthZhi(),
            "day_gan": eight.getDayGan(),
            "day_zhi": eight.getDayZhi(),
            "time_gan": eight.getTimeGan(),
            "time_zhi": eight.getTimeZhi(),
            "sect": eight.getSect(),
        }

    def jieqi_table(self, year: int) -> dict[str, datetime]:
        lunar = Solar.fromYmdHms(year, 6, 1, 0, 0, 0).getLunar()
        table = {}
        for name, solar in lunar.getJieQiTable().items():
            if len(name) <= 3:
                table[name] = datetime(solar.getYear(), solar.getMonth(), solar.getDay(), solar.getHour(), solar.getMinute(), solar.getSecond())
        return table

    @staticmethod
    def _lunar_to_dict(lunar) -> dict:
        return {
            "year": lunar.getYear(),
            "month": abs(lunar.getMonth()),
            "day": lunar.getDay(),
            "raw_month": lunar.getMonth(),
            "is_leap_month": lunar.getMonth() < 0,
            "month_cn": lunar.getMonthInChinese(),
            "day_cn": lunar.getDayInChinese(),
            "year_ganzhi": lunar.getYearInGanZhi(),
            "month_ganzhi": lunar.getMonthInGanZhi(),
            "day_ganzhi": lunar.getDayInGanZhi(),
            "time_ganzhi": lunar.getTimeInGanZhi(),
            "zodiac": lunar.getYearShengXiao(),
        }

