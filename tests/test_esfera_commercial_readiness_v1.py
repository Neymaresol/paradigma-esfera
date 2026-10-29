from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_all_five_partner_cards_visible_without_checkout(monkeypatch):
    for key in ("ESFERA_AFFILIATE_PUBLISH_ENABLED", "ESFERA_AFFILIATE_PARTNER_VERIFIED", "ESFERA_AFFILIATE_ATTRIBUTION_EVIDENCE_VERIFIED"):
        monkeypatch.delenv(key, raising=False)
    response = client.get("/ofertas")
    assert response.status_code == 200
    for name in ("Hotmart", "Shopee", "Mercado Livre", "Amazon Brasil", "Magalu"):
        assert name in response.text
    assert "Ver oferta no parceiro" not in response.text

def test_public_readiness_is_truthful_and_no_financial_fabrication(monkeypatch):
    for key in ("ESFERA_AFFILIATE_PUBLISH_ENABLED", "ESFERA_AFFILIATE_PARTNER_VERIFIED", "ESFERA_AFFILIATE_ATTRIBUTION_EVIDENCE_VERIFIED"):
        monkeypatch.delenv(key, raising=False)
    response = client.get("/api/affiliate/offers/status")
    assert response.status_code == 200
    data = response.json()
    assert len(data["offers"]) == 5
    assert all(not item["outbound_enabled"] for item in data["offers"])
    assert data["verified_sales"] is None
    assert data["verified_commissions_brl"] is None
    assert sum(item["destination_configured"] for item in data["offers"]) == 3

def test_unconfigured_partner_cannot_redirect_even_with_flags(monkeypatch):
    for key in ("ESFERA_AFFILIATE_PUBLISH_ENABLED", "ESFERA_AFFILIATE_PARTNER_VERIFIED", "ESFERA_AFFILIATE_ATTRIBUTION_EVIDENCE_VERIFIED"):
        monkeypatch.setenv(key, "true")
    response = client.get("/ofertas/amazon-inicial", follow_redirects=False)
    assert response.status_code == 503
    assert "location" not in response.headers
