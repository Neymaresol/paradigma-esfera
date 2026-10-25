from fastapi.testclient import TestClient
from app import app

client=TestClient(app)

def test_search_accents_and_categories():
    r=client.get("/api/discovery/topics",params={"q":"inteligência artificial"})
    assert r.status_code==200
    assert any(x["slug"]=="inteligencia-artificial" for x in r.json()["results"])
    assert r.json()["commerce_status"]=="no_verified_offers"

def test_search_page_escapes_user_input():
    r=client.get("/descobrir",params={"q":'<script>alert(1)</script>'})
    assert r.status_code==200
    assert "<script>alert(1)</script>" not in r.text

def test_topic_page_and_missing_topic():
    assert client.get("/interesses/marketing-digital").status_code==200
    assert client.get("/interesses/nao-existe").status_code==404

def test_no_unverified_checkout():
    r=client.get("/interesses/inteligencia-artificial")
    assert "Nenhuma compra é processada" in r.text
    assert "go.hotmart.com" not in r.text
