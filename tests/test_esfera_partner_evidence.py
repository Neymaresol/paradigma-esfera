from esfera_partner_evidence import PartnerEvidence, eligible, readiness

def test_flags_without_provider_evidence_fail_closed():
    e = PartnerEvidence("hotmart", "offer", "https://go.hotmart.com/example", True, True)
    assert not eligible(e)

def test_unverified_partner_fails_closed():
    e = PartnerEvidence("hotmart", "offer", "https://go.hotmart.com/example")
    assert not eligible(e)
    assert readiness([e])["publication_allowed"] is False

def test_verified_evidence_does_not_bypass_release_gate():
    e = PartnerEvidence("hotmart", "offer", "https://go.hotmart.com/example", True, True, "provider-case-123", True)
    assert eligible(e)
    assert readiness([e])["publication_allowed"] is False
