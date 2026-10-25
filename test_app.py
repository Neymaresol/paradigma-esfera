from fastapi.testclient import TestClient
from app import app
client=TestClient(app)
def test_health_fail_closed():
    h=client.get('/health').json()
    assert h['status']=='ok' and h['checkout_enabled'] is False
    assert h['live_ads_enabled'] is False and h['auto_replication_enabled'] is False
def test_catalog():
    assert len(client.get('/api/catalog').json()['items'])==10
def test_simulated_order_not_real(auth_headers):
    r=client.post('/api/orders/simulate',json={'product_id':'ia-basica'},headers=auth_headers)
    assert r.status_code==200
    data=r.json()
    assert data['payment_confirmed'] is False and data['status']=='SIMULATED_ONLY'
    assert client.get('/api/orders/'+data['id'],headers=auth_headers).json()['commission_confirmed'] is False
def test_invalid_product(auth_headers):
    assert client.post('/api/orders/simulate',json={'product_id':'invalid'},headers=auth_headers).status_code==404
def test_home():
    r=client.get('/')
    assert r.status_code == 200
    assert 'Werozinha' in r.text
    assert 'suggestions' in r.text
    assert 'sha256-' in r.headers['content-security-policy']
