from fastapi.testclient import TestClient
from app import app
client=TestClient(app)
def test_manifest_and_icon():
    r=client.get("/manifest.webmanifest")
    assert r.status_code==200
    assert r.json()["start_url"]=="/catalogo"
    assert client.get("/esfera-icon.svg").status_code==200
def test_discovery():
    robots=client.get("/robots.txt")
    assert robots.status_code==200
    assert "Disallow: /admin/" in robots.text
    sitemap=client.get("/sitemap.xml")
    assert sitemap.status_code==200
    assert "/catalogo" in sitemap.text
def test_public_landing():
    r=client.get("/esfera-app")
    assert r.status_code==200
    assert 'rel="manifest"' in r.text
    assert "Comissões confirmadas" not in r.text
