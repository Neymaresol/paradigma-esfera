"""Contract tests: preserve the original futuristic ESFERA homepage."""
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_homepage_visual_identity():
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    for required in (
        "PARADIGMA", "IA CENTRAL", "EDUCAÇÃO", "SERVIÇOS",
        "COMÉRCIO", "EXPANSÃO", "MONITORAMENTO",
        "BANCO DE DADOS", "APRENDIZADO", "SEGURANÇA", "MULTIPLICAÇÃO"
    ):
        assert required in html, f"Missing visual identity element: {required}"
    assert 'action="/descobrir"' in html
    assert "discovery-form" in html
    assert "--gold:" in html and "--blue:" in html

def test_esfera_alias_retains_same_visual():
    assert client.get("/esfera").text == client.get("/").text

def test_discovery_keeps_visual_entry_point():
    assert client.get("/descobrir").status_code == 200
    assert client.get("/interesses/inteligencia-artificial").status_code == 200
