import os
from fastapi.testclient import TestClient
from app import app

def test_commercial_gate_cannot_be_opened_with_env_flags(monkeypatch):
    monkeypatch.setenv("ESFERA_AFFILIATE_PUBLISH_ENABLED","true")
    monkeypatch.setenv("ESFERA_AFFILIATE_PARTNER_VERIFIED","true")
    client=TestClient(app)
    response=client.get("/api/affiliate/readiness")
    assert response.status_code==200
    assert response.json()["publication_allowed"] is False
    assert response.json()["attribution_verified"] is False
    assert response.json()["financial_claims_allowed"] is False
    response=client.get("/ofertas/hotmart-inicial",follow_redirects=False)
    assert response.status_code==503
    assert "location" not in response.headers
