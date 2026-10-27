"""P0 regression checks: read-only routes and fail-closed commercial controls."""
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_is_simulation_only():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["checkout_enabled"] is False
    assert data["live_ads_enabled"] is False
    assert data["auto_replication_enabled"] is False

def test_sales_readiness_is_fail_closed():
    response = client.get("/api/readiness")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "NOT_READY_FOR_SALES"
    assert data["publish_allowed"] is False
    assert data["payment_provider_connected"] is False

def test_affiliate_links_do_not_redirect_without_verification():
    response = client.get("/ofertas/hotmart-inicial", follow_redirects=False)
    assert response.status_code == 503
    readiness = client.get("/api/affiliate/readiness").json()
    assert readiness["publication_allowed"] is False
    assert readiness["attribution_verified"] is False
    assert readiness["commissions_reconciled"] is False

def test_catalog_is_labeled_illustrative():
    response = client.get("/api/catalog")
    assert response.status_code == 200
    assert response.json()["prices_are_suggested"] is True

def test_operator_routes_are_not_public():
    for path in ("/api/ops/dashboard", "/api/ops/audit"):
        assert client.get(path).status_code == 401
