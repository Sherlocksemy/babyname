def test_health_api(api_client) -> None:
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_swagger_is_accessible(api_client) -> None:
    response = api_client.get("/docs")
    assert response.status_code == 200
