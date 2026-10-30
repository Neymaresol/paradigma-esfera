"""Regression tests for affiliate discovery query tokenization."""
from esfera_discovery import norm
import re


def test_portuguese_search_terms_tokenize():
    query = "Curso de Inteligência Artificial"
    words = [w for w in re.findall(r"\w+", norm(query)) if w not in {"curso", "cursos", "de", "da", "do", "para", "quero", "aprender"}]
    assert words == ["inteligencia", "artificial"]


def test_service_search_terms_tokenize():
    assert re.findall(r"\w+", norm("consultoria de automação")) == ["consultoria", "de", "automacao"]
