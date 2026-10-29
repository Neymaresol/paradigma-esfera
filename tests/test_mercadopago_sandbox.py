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
