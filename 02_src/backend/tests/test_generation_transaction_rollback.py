def test_generation_transaction_rollback_on_candidate_save_failure(api_client, api_payload, monkeypatch) -> None:
    from app.repositories import naming_repository

    original = naming_repository.NamingRepository.save_candidates

    def fail_save(self, *args, **kwargs):
        raise RuntimeError("forced save failure")

    monkeypatch.setattr(naming_repository.NamingRepository, "save_candidates", fail_save)
    response = api_client.post("/api/v1/names/generate", json={**api_payload, "generation_seed": 20260801})
    assert response.status_code == 500
    monkeypatch.setattr(naming_repository.NamingRepository, "save_candidates", original)
