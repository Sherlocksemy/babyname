from __future__ import annotations


CITY_COORDINATES = {
    "汕头": {
        "longitude": 116.681972,
        "latitude": 23.354091,
        "source": "国家基础地理信息中心公开行政区划中心点数据整理；Milestone 2 内置首批城市表。",
    },
    "汕头市": {
        "longitude": 116.681972,
        "latitude": 23.354091,
        "source": "国家基础地理信息中心公开行政区划中心点数据整理；Milestone 2 内置首批城市表。",
    },
    "潮州": {
        "longitude": 116.622603,
        "latitude": 23.65695,
        "source": "国家基础地理信息中心公开行政区划中心点数据整理；Milestone 2 内置首批城市表。",
    },
    "潮州市": {
        "longitude": 116.622603,
        "latitude": 23.65695,
        "source": "国家基础地理信息中心公开行政区划中心点数据整理；Milestone 2 内置首批城市表。",
    },
    "揭阳": {
        "longitude": 116.372831,
        "latitude": 23.549993,
        "source": "国家基础地理信息中心公开行政区划中心点数据整理；Milestone 2 内置首批城市表。",
    },
    "揭阳市": {
        "longitude": 116.372831,
        "latitude": 23.549993,
        "source": "国家基础地理信息中心公开行政区划中心点数据整理；Milestone 2 内置首批城市表。",
    },
}


class LocationAdapter:
    def lookup(self, city: str) -> dict:
        normalized = city.replace("广东省", "").replace("广东", "").strip()
        if normalized in CITY_COORDINATES:
            row = CITY_COORDINATES[normalized].copy()
            row["city"] = normalized
            row["status"] = "COMPLETE"
            return row
        return {
            "city": city,
            "longitude": None,
            "latitude": None,
            "status": "LOCATION_DATA_MISSING",
            "source": "Milestone 2 built-in city table",
            "warnings": ["LOCATION_DATA_MISSING"],
        }
