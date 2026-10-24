from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_operator_diagnostic_page_does_not_embed_secrets():
    response = client.get("/admin/hotmart-diagnostic")
    assert response.status_code == 200
    assert "Testar autenticação Hotmart" in response.text
    assert "HOTMART_CLIENT_SECRET" not in response.text
    assert "localStorage" not in response.text

def test_diagnostic_endpoint_requires_operator_jwt():
    response = client.post("/api/integrations/hotmart/diagnostic")
    assert response.status_code == 401

def test_page_has_no_automatic_diagnostic_request():
    response = client.get("/admin/hotmart-diagnostic")
    assert "addEventListener('click'" in response.text
    assert "credentials:'omit'" in response.text
