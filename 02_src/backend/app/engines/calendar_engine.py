from __future__ import annotations

from datetime import datetime

from app.adapters.lunar_calendar_adapter import LunarCalendarAdapter
from app.schemas.baby_profile import BabyProfile
from app.schemas.calendar import CalendarResult


class CalendarEngine:
    def __init__(self, adapter: LunarCalendarAdapter | None = None) -> None:
        self.adapter = adapter or LunarCalendarAdapter()

    def normalize(self, profile: BabyProfile) -> CalendarResult:
        errors = profile.validate()
        if errors:
            raise ValueError("; ".join(errors))
        warnings: list[str] = []
        if profile.calendar_type == "solar":
            solar_dt = datetime(profile.birth_year, profile.birth_month, profile.birth_day, profile.birth_hour, profile.birth_minute)
            lunar_date = self.adapter.solar_to_lunar(solar_dt)
        else:
            try:
                solar_dt = self.adapter.lunar_to_solar(
                    profile.birth_year,
                    profile.birth_month,
                    profile.birth_day,
                    profile.birth_hour,
                    profile.birth_minute,
                    profile.is_leap_month,
                )
            except Exception as exc:
                raise ValueError(f"invalid lunar date: {exc}") from exc
            lunar_date = self.adapter.solar_to_lunar(solar_dt)
            if bool(lunar_date.get("is_leap_month")) != profile.is_leap_month:
                raise ValueError("invalid lunar leap month")
        if not (datetime(1900, 1, 1) <= solar_dt <= datetime(2100, 12, 31, 23, 59)):
            raise ValueError("solar datetime must be within 1900-01-01 to 2100-12-31")
        return CalendarResult(
            solar_datetime=solar_dt,
            lunar_date=lunar_date,
            is_leap_month=bool(lunar_date.get("is_leap_month")),
            timezone=profile.timezone,
            calendar_library=self.adapter.library_name,
            calendar_library_version=self.adapter.library_version,
            calculation_status="COMPLETE",
            warnings=warnings,
        )

