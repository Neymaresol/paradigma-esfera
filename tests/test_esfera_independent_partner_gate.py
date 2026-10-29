from fastapi.testclient import TestClient
from app import app, AFFILIATE_OFFERS, AFFILIATE_VERIFIED_EVIDENCE
from esfera_partner_evidence import PartnerEvidence

client = TestClient(app)

def test_global_flags_do_not_prove_provider_authorization(monkeypatch):
    for key in ("ESFERA_AFFILIATE_PUBLISH_ENABLED", "ESFERA_AFFILIATE_PARTNER_VERIFIED", "ESFERA_AFFILIATE_ATTRIBUTION_EVIDENCE_VERIFIED"):
        monkeypatch.setenv(key, "true")
    AFFILIATE_VERIFIED_EVIDENCE.clear()
    response = client.get("/api/affiliate/offers/status")
    assert response.status_code == 200
    assert all(not offer["outbound_enabled"] for offer in response.json()["offers"])
    for offer_id in ("hotmart-inicial", "shopee-inicial", "mercadolivre-inicial"):
        assert client.get("/ofertas/" + offer_id, follow_redirects=False).status_code == 503
    assert "Ver oferta no parceiro" not in client.get("/ofertas").text

def test_only_exact_verified_offer_can_redirect(monkeypatch):
    for key in ("ESFERA_AFFILIATE_PUBLISH_ENABLED", "ESFERA_AFFILIATE_PARTNER_VERIFIED", "ESFERA_AFFILIATE_ATTRIBUTION_EVIDENCE_VERIFIED"):
        monkeypatch.setenv(key, "true")
    AFFILIATE_VERIFIED_EVIDENCE.clear()
    offer = AFFILIATE_OFFERS["hotmart-inicial"]
    AFFILIATE_VERIFIED_EVIDENCE["hotmart-inicial"] = PartnerEvidence(
        provider=offer["provider"], offer_id="hotmart-inicial", affiliate_url=offer["url"],
        authorized_by_provider=True, attribution_confirmed_by_provider=True,
        evidence_reference="test-only-fixture", reviewed=True,
    )
    try:
        assert client.get("/ofertas/hotmart-inicial", follow_redirects=False).status_code in (302, 307)
        assert client.get("/ofertas/shopee-inicial", follow_redirects=False).status_code == 503
        assert client.get("/ofertas/mercadolivre-inicial", follow_redirects=False).status_code == 503
    finally:
        AFFILIATE_VERIFIED_EVIDENCE.clear()
