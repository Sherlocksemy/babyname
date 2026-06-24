from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CalendarResult:
    solar_datetime: datetime | None
    lunar_date: dict
    is_leap_month: bool
    timezone: str = "Asia/Shanghai"
    calendar_library: str = "lunar-python"
    calendar_library_version: str = "1.4.8"
    calculation_status: str = "COMPLETE"
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "solar_datetime": self.solar_datetime.isoformat(sep=" ") if self.solar_datetime else None,
            "lunar_date": self.lunar_date,
            "is_leap_month": self.is_leap_month,
            "timezone": self.timezone,
            "calendar_library": self.calendar_library,
            "calendar_library_version": self.calendar_library_version,
            "calculation_status": self.calculation_status,
            "warnings": self.warnings,
        }


@dataclass
class TrueSolarTimeResult:
    standard_time: datetime
    longitude: float | None
    standard_meridian: float = 120.0
    longitude_correction_minutes: float | None = None
    equation_of_time_minutes: float | None = None
    true_solar_time: datetime | None = None
    date_shift: int = 0
    method: str = "longitude correction + equation of time"
    status: str = "COMPLETE"
    confidence: float = 0.0
    source: str = ""
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "standard_time": self.standard_time.isoformat(sep=" "),
            "longitude": self.longitude,
            "standard_meridian": self.standard_meridian,
            "longitude_correction_minutes": self.longitude_correction_minutes,
            "equation_of_time_minutes": self.equation_of_time_minutes,
            "true_solar_time": self.true_solar_time.isoformat(sep=" ") if self.true_solar_time else None,
            "date_shift": self.date_shift,
            "method": self.method,
            "status": self.status,
            "confidence": self.confidence,
            "source": self.source,
            "warnings": self.warnings,
        }

