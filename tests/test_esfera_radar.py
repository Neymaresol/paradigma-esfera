from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_radar_status_fail_closed():
    response = client.get("/api/radar/status")
    assert response.status_code == 200
    body = response.json()
    assert body["event_sources_connected"] is False
    assert body["automatic_publication"] is False
    assert body["verified_offers"] == 0

def test_no_fabricated_events():
    response = client.get("/api/radar/opportunities?country=BR")
    assert response.status_code == 200
    assert response.json()["items"] == []
    assert response.json()["data_verified"] is False

def test_preview_suggests_categories_without_offers():
    response = client.post("/api/radar/campaigns/preview", json={
        "interest": "rock", "country": "BR", "event_name": "Exemplo hipotético"
    })
    assert response.status_code == 200
    body = response.json()
    assert "jaquetas" in body["product_categories"]
    assert body["event"]["verified"] is False
    assert body["offer_links"] == []
    assert body["publication_enabled"] is False
    assert body["verified_commissions"] is None

def test_unknown_interest_rejected():
    response = client.post("/api/radar/campaigns/preview", json={"interest": "nao-existe"})
    assert response.status_code == 422

def test_invalid_event_date_rejected():
    response = client.post("/api/radar/campaigns/preview", json={
        "interest": "futebol", "event_date": "2030-99-99"
    })
    assert response.status_code == 422

def test_bad_country_rejected():
    response = client.get("/api/radar/opportunities?country=BRASIL")
    assert response.status_code == 422

def test_legacy_homepage_still_available():
    response = client.get("/")
    assert response.status_code == 200
