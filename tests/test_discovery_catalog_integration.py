"""Read-only commercial discovery contract tests."""
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_unified_catalog_does_not_invent_affiliate_offers():
    response = client.get("/api/discovery/catalog", params={"q": "Curso de Inteligência Artificial"})
    assert response.status_code == 200
    payload = response.json()
    assert "offers" in payload and "topics" in payload and "fronts" in payload
    assert payload["verified_only"] is True
    assert any(t["slug"] == "inteligencia-artificial" for t in payload["topics"])


def test_services_are_classified():
    payload = client.get("/api/discovery/catalog", params={"q": "consultoria"}).json()
    assert "servicos" in payload["fronts"]


def test_homepage_calls_unified_catalog():
    html = client.get("/").text
    assert "/api/discovery/catalog?q=" in html
    assert "Ver oferta afiliada" in html
