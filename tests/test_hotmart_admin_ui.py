from fastapi.testclient import TestClient
from app import app

client=TestClient(app)

def test_admin_page_uses_password_not_manual_jwt():
    response=client.get("/admin/hotmart-diagnostic")
    assert response.status_code==200
    assert 'id="password"' in response.text
    assert 'id="jwt"' not in response.text
    assert "HOTMART_CLIENT_SECRET" not in response.text
    assert "localStorage" not in response.text
    assert '<script src="/admin/hotmart-diagnostic.js" defer></script>' in response.text

def test_login_and_diagnostic_wiring():
    js=client.get("/admin/hotmart-diagnostic.js")
    assert js.status_code==200
    assert "/api/operator/login" in js.text
    assert "/api/integrations/hotmart/diagnostic" in js.text
    assert "access_token" in js.text
    assert "localStorage" not in js.text

def test_diagnostic_requires_jwt():
    assert client.post("/api/integrations/hotmart/diagnostic").status_code==401

def test_login_disabled_by_default(monkeypatch):
    monkeypatch.delenv("ESFERA_OPERATOR_LOGIN_ENABLED",raising=False)
    assert client.post("/api/operator/login",json={"password":"example"}).status_code==403
