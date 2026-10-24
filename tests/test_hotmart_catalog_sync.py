from hotmart_catalog_sync import AffiliateOffer, parse_hotlink, synchronize
import pytest

def test_code_validation():
    assert parse_hotlink("https://go.hotmart.com/G108129576P") == "G108129576P"
    for url in ("http://go.hotmart.com/G108129576P", "https://evil.com/G108129576P",
                "https://go.hotmart.com/G108129576P?x=1",
                "https://go.hotmart.com/../G108129576P"):
        with pytest.raises(ValueError):
            parse_hotlink(url)

def test_import_is_idempotent_and_fail_closed():
    item = {"affiliate_authorized": True, "affiliate_url": "https://go.hotmart.com/A107958015J", "title": "Curso autorizado"}
    result = synchronize([item, item, {"affiliate_authorized": False, "affiliate_url": "https://go.hotmart.com/O107910953Y", "title": "Sem autorização"}])
    assert result["metrics"] == {"received": 3, "added": 1, "existing": 1, "rejected": 1}
    assert len(result["offers"]) == 1
    assert result["offers"][0].state == "pending_review"
    assert result["publication_enabled"] is False
    again = synchronize([item], existing=result["offers"])
    assert again["metrics"]["added"] == 0
    assert again["metrics"]["existing"] == 1

def test_existing_configuration_preserved():
    existing = AffiliateOffer("G108129576P", "https://go.hotmart.com/G108129576P", "Original")
    result = synchronize([], existing=[existing])
    assert result["offers"] == (existing,)
