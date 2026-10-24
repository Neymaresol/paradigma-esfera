from fastapi.testclient import TestClient
from app import app

def test_esfera_prototype_renders_safely():
    response = TestClient(app).get('/esfera')
    assert response.status_code == 200
    assert 'PARADIGMA ESFERA FINANCEIRA 1.0' in response.text
    assert 'EDUCAÇÃO' in response.text
    assert 'EXPANSÃO' in response.text
    assert 'Operações comerciais não habilitadas' in response.text
    assert response.headers['content-security-policy']
