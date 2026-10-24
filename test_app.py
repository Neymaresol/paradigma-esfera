from fastapi.testclient import TestClient
from app import app
client=TestClient(app)
def test_health_fail_closed():
    h=client.get('/health').json()
    assert h['status']=='ok' and h['checkout_enabled'] is False
    assert h['live_ads_enabled'] is False and h['auto_replication_enabled'] is False
def test_catalog():
    assert len(client.get('/api/catalog').json()['items'])==10
def test_simulated_order_not_real():
    r=client.post('/api/orders/simulate',json={'product_id':'ia-basica'})
    assert r.status_code==200
    data=r.json()
    assert data['payment_confirmed'] is False and data['status']=='SIMULATED_ONLY'
    assert client.get('/api/orders/'+data['id']).json()['commission_confirmed'] is False
def test_invalid_product():
    assert client.post('/api/orders/simulate',json={'product_id':'invalid'}).status_code==404
def test_home():
    r=client.get('/')
    assert r.status_code==200 and 'PARADIGMA ESFERA' in r.text
