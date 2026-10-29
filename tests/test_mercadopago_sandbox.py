from esfera_mercadopago import enabled, TEST_ITEMS
from fastapi.testclient import TestClient
from app import app

def test_sandbox_disabled_by_default(monkeypatch):
    monkeypatch.delenv("ESFERA_MP_TEST_CHECKOUT_ENABLED", raising=False)
    assert enabled() is False

def test_no_public_payment_access():
    client = TestClient(app)
    response = client.post("/api/payments/mercadopago/test-preference",
                           json={"product_id": "curriculo"})
    assert response.status_code in (401, 403)

def test_fixed_test_products():
    assert "curriculo" in TEST_ITEMS
    assert all(price > 0 for _, price in TEST_ITEMS.values())

def test_diagnostics_requires_operator():
    client = TestClient(app)
    response = client.get("/api/payments/mercadopago/diagnostics")
    assert response.status_code in (401, 403)

def test_diagnostics_missing_token_is_safe(monkeypatch):
    from esfera_auth import require_operator
    monkeypatch.delenv("MERCADOPAGO_ACCESS_TOKEN_TEST", raising=False)
    app.dependency_overrides[require_operator] = lambda: {"sub": "test", "role": "operator"}
    try:
        response = TestClient(app).get("/api/payments/mercadopago/diagnostics")
        assert response.status_code == 200
        assert response.json() == {
            "credential_present": False,
            "credential_accepted": False,
            "provider_reachable": None,
            "production_checkout_enabled": False,
        }
    finally:
        app.dependency_overrides.pop(require_operator, None)

def test_diagnostics_rejects_non_test_token_without_network(monkeypatch):
    from esfera_auth import require_operator
    monkeypatch.setenv("MERCADOPAGO_ACCESS_TOKEN_TEST", "not-a-test-token")
    app.dependency_overrides[require_operator] = lambda: {"sub": "test", "role": "operator"}
    try:
        response = TestClient(app).get("/api/payments/mercadopago/diagnostics")
        assert response.status_code == 200
        assert response.json()["credential_accepted"] is False
        assert response.json()["production_checkout_enabled"] is False
    finally:
        app.dependency_overrides.pop(require_operator, None)
