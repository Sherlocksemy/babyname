from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_generate_detail_and_favorite_api():
    payload = {
        "surname": "陈",
        "gender": "female",
        "birth_datetime": "2026-06-18 09:30",
        "birth_place": "广东省汕头市",
        "name_length": 2,
        "style_preferences": ["温润", "诗意"],
        "banned_chars": ["梓", "轩"],
        "liked_chars": ["清"],
        "avoid_hot_names": True,
        "need_teochew_check": True,
        "need_culture_origin": True,
    }
    res = client.post("/api/names/generate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["results"]) == 20
    name = data["results"][0]["name"]
    detail = client.get(f"/api/names/{data['request_id']}/{name}")
    assert detail.status_code == 200
    fav = client.post("/api/favorites", json={"request_id": data["request_id"], "name": name})
    assert fav.status_code == 200
    assert client.get("/api/favorites").json()["favorites"]

