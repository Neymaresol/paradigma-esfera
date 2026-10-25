from esfera_ai_routing import classify, fallback
from esfera_discovery import route_search, discover

def test_fallback_routes_courses():
    result=fallback("quero aprender IA em um curso")
    assert "educacao" in result["fronts"]
    assert result["commercial_verified"] is False

def test_fallback_routes_commerce():
    assert "comercio" in fallback("comprar computador")["fronts"]

def test_api_without_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result=route_search("curso de inteligencia artificial")
    assert result["engine"] == "keywords"
    assert result["theme"] == "curso de inteligencia artificial"

def test_page_displays_theme(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    response=discover("Inteligência Artificial")
    assert "Tema pesquisado: Inteligência Artificial" in response
    assert "Educação" in response
