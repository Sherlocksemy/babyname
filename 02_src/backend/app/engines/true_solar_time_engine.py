from __future__ import annotations

import math
from datetime import datetime, timedelta

from app.adapters.location_adapter import LocationAdapter
from app.schemas.calendar import TrueSolarTimeResult


class TrueSolarTimeEngine:
    def __init__(self, location_adapter: LocationAdapter | None = None) -> None:
        self.location_adapter = location_adapter or LocationAdapter()

    def calculate(self, standard_time: datetime, birth_city: str) -> TrueSolarTimeResult:
        location = self.location_adapter.lookup(birth_city)
        if location.get("status") == "LOCATION_DATA_MISSING":
            return TrueSolarTimeResult(
                standard_time=standard_time,
                longitude=None,
                true_solar_time=None,
                status="LOCATION_DATA_MISSING",
                confidence=0,
                source=location.get("source", ""),
                warnings=["LOCATION_DATA_MISSING"],
            )
        longitude = float(location["longitude"])
        longitude_correction = (longitude - 120.0) * 4.0
        equation = self._equation_of_time_minutes(standard_time)
        true_time = standard_time + timedelta(minutes=longitude_correction + equation)
        date_shift = (true_time.date() - standard_time.date()).days
        return TrueSolarTimeResult(
            standard_time=standard_time,
            longitude=longitude,
            longitude_correction_minutes=round(longitude_correction, 4),
            equation_of_time_minutes=round(equation, 4),
            true_solar_time=true_time,
            date_shift=date_shift,
            status="COMPLETE",
            confidence=0.86,
            source=location.get("source", ""),
            warnings=[],
        )

    @staticmethod
    def _equation_of_time_minutes(dt: datetime) -> float:
        day_of_year = dt.timetuple().tm_yday
        b = math.radians((360 / 365) * (day_of_year - 81))
        return 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)

