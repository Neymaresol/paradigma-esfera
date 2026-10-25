"""Protect Hotmart inventory and commercial release gates."""
from fastapi.testclient import TestClient
from app import app, AFFILIATE_OFFERS, affiliate_publication_allowed

def test_four_recovered_offers_preserved():
    assert len(AFFILIATE_OFFERS) == 4
    assert {offer["url"] for offer in AFFILIATE_OFFERS.values()} == {
        "https://go.hotmart.com/G108129576P",
        "https://go.hotmart.com/A107958015J",
        "https://go.hotmart.com/O107910953Y",
        "https://go.hotmart.com/J107828590U",
    }

def test_unverified_offers_not_published():
    assert affiliate_publication_allowed() is False
    client = TestClient(app)
    assert client.get("/api/affiliate/readiness").json()["publication_allowed"] is False
    assert client.get("/ofertas").status_code == 200
    for offer_id in AFFILIATE_OFFERS:
        assert client.get(f"/ofertas/{offer_id}", follow_redirects=False).status_code == 503
