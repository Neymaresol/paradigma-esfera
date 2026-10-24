from fastapi.testclient import TestClient
from app import app
client=TestClient(app)
def test_six_languages():
    for lang in ('pt','en','es','fr','de','ar'):
        r=client.get('/catalogo',params={'lang':lang})
        assert r.status_code==200
        assert f'lang="{lang}"' in r.text
        assert 'no checkout' in r.text

def test_bad_language():
    assert client.get('/catalogo?lang=xx').status_code==400

def test_readiness_closed():
    data=client.get('/api/readiness').json()
    assert data['publish_allowed'] is False
    assert data['payment_provider_connected'] is False

def test_no_fake_sales():
    h=client.get('/health').json()
    assert h['checkout_enabled'] is False
    assert h['live_ads_enabled'] is False
