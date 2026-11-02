from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_discovery_search_returns_relevant_topic_and_safe_offer_state():
    response = client.get("/api/discovery/search", params={"q": "notebook gamer"})
    assert response.status_code == 200
    data = response.json()
    assert any(item["slug"] == "tecnologia-e-produtos" for item in data["results"])
    assert data["commercial_status"] == "verified_offers_only"
    assert isinstance(data["offers"], list)


def test_discovery_search_supports_services_and_accented_terms():
    response = client.get("/api/discovery/search", params={"q": "serviços de automação"})
    assert response.status_code == 200
    assert any(item["slug"] == "servicos-digitais" for item in response.json()["results"])


def test_discovery_search_links_open_real_topic_pages():
    data = client.get("/api/discovery/search", params={"q": "beleza"}).json()
    topic = next(item for item in data["results"] if item["slug"] == "beleza-e-cuidados")
    page = client.get(topic["url"])
    assert page.status_code == 200
    assert "Beleza e Cuidados" in page.text


def test_discovery_search_rejects_overlong_query():
    assert client.get("/api/discovery/search", params={"q": "x" * 121}).status_code == 422
