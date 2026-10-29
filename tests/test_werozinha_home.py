from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_home_renders_werozinha_and_search():
    response = client.get('/')
    assert response.status_code == 200
    assert 'Werozinha' in response.text
    assert 'suggestions' in response.text
    assert 'id="wero-img"' in response.text
    assert 'https://raw.githubusercontent.com/Neymaresol/paradigma-esfera/main/assets/' in response.text
    assert 'id="eventos"' in response.text
    assert 'id="affiliate-rail"' in response.text
    assert 'Próximo gesto' not in response.text
    assert 'script-src' in response.headers['content-security-policy']
    assert 'sha256-' in response.headers['content-security-policy']

def test_werozinha_preview_and_legacy_routes():
    assert client.get('/werozinha').status_code == 200
    assert 'PARADIGMA ESFERA FINANCEIRA' in client.get('/esfera').text
    assert 'Em preparação' in client.get('/catalogo').text

def test_affiliate_links_remain_fail_closed():
    readiness = client.get('/api/affiliate/readiness').json()
    assert readiness['publication_allowed'] is False
    assert client.get('/ofertas/hotmart-inicial').status_code == 503
