from fastapi.testclient import TestClient
from app import app
from esfera_operator_login import _attempts

client=TestClient(app)

def test_diagnostic_script_external_and_csp_compatible():
    page=client.get('/admin/hotmart-diagnostic')
    assert page.status_code==200
    assert '<script src="/admin/hotmart-diagnostic.js" defer></script>' in page.text
    assert '<script>' not in page.text
    script=client.get('/admin/hotmart-diagnostic.js')
    assert script.status_code==200
    assert "addEventListener('click'" in script.text

def test_login_rate_limit_is_fail_closed(monkeypatch):
    _attempts.clear()
    monkeypatch.setenv('RENDER_SERVICE_ID','srv-dbe16ejrjlhs738mgokg')
    monkeypatch.setenv('ESFERA_OPERATOR_LOGIN_ENABLED','true')
    monkeypatch.setenv('ESFERA_JWT_SECRET','x'*40)
    monkeypatch.delenv('ESFERA_OPERATOR_PASSWORD_SCRYPT',raising=False)
    statuses=[client.post('/api/operator/login',json={'password':'invalid'}).status_code for _ in range(6)]
    assert statuses[:5]==[503]*5
    assert statuses[5]==429
    _attempts.clear()
