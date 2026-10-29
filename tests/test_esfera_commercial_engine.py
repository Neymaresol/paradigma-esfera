from esfera_commercial_engine import evaluate_offers

def test_missing_evidence_blocks_all():
    offers = {"a": {"provider": "Hotmart", "title": "Course", "url": "https://go.hotmart.com/ABC"},
              "b": {"provider": "Magalu", "title": "Store", "url": ""}}
    result = evaluate_offers(offers)
    assert result["total"] == 2
    assert result["configured"] == 1
    assert result["enabled"] == 0
    assert result["verified_sales"] is None
    assert result["verified_commissions_brl"] is None

def test_missing_destination_remains_blocked():
    result = evaluate_offers({"a": {"provider": "Magalu", "title": "Store", "url": ""}}, publication_allowed=True)
    assert result["enabled"] == 0
    assert result["offers"][0]["needs_destination"] is True
