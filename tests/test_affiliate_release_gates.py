import os
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_affiliate_default_fail_closed(monkeypatch):
    monkeypatch.delenv("ESFERA_AFFILIATE_PUBLISH_ENABLED", raising=False)
    monkeypatch.delenv("ESFERA_AFFILIATE_PARTNER_VERIFIED", raising=False)
    assert client.get("/api/affiliate/readiness").json()["publication_allowed"] is False
    assert client.get("/ofertas/hotmart-inicial", follow_redirects=False).status_code == 503

def test_publish_flag_alone_is_insufficient(monkeypatch):
    monkeypatch.setenv("ESFERA_AFFILIATE_PUBLISH_ENABLED", "true")
    monkeypatch.delenv("ESFERA_AFFILIATE_PARTNER_VERIFIED", raising=False)
    assert client.get("/ofertas/hotmart-inicial", follow_redirects=False).status_code == 503

def test_both_flags_still_block_redirect_without_attribution(monkeypatch):
    monkeypatch.setenv("ESFERA_AFFILIATE_PUBLISH_ENABLED", "true")
    monkeypatch.setenv("ESFERA_AFFILIATE_PARTNER_VERIFIED", "true")
    response = client.get("/ofertas/hotmart-inicial", follow_redirects=False)
    assert response.status_code == 503
    assert "location" not in response.headers
    readiness = client.get("/api/affiliate/readiness").json()
    assert readiness["publication_allowed"] is False
    assert readiness["financial_claims_allowed"] is False
    assert readiness["attribution_verified"] is False

def test_unknown_offer_is_blocked_without_publication(monkeypatch):
    monkeypatch.setenv("ESFERA_AFFILIATE_PUBLISH_ENABLED", "true")
    monkeypatch.setenv("ESFERA_AFFILIATE_PARTNER_VERIFIED", "true")
    assert client.get("/ofertas/inexistente", follow_redirects=False).status_code == 503
