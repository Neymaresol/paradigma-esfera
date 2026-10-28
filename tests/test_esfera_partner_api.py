"""Partner API contract tests; no provider calls."""
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_partner_status_fail_closed():
    response = client.get("/api/partners/status")
    assert response.status_code == 200
    data = response.json()
    assert data["publication_enabled"] is False
    assert data["verified_sales"] is None
    assert {p["id"] for p in data["providers"]} == {"hotmart", "amazon", "shopee", "magalu", "mercado_livre"}

def test_partner_catalog_has_no_unverified_offers():
    response = client.get("/api/partners/catalog")
    assert response.status_code == 200
    assert response.json()["items"] == []
    assert response.json()["affiliate_publication_enabled"] is False
