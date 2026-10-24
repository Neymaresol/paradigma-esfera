import pytest
from esfera_cell_persistence import enqueue_review_task

def test_nonproduction_gate(monkeypatch):
    monkeypatch.setenv("ESFERA_ENV","production")
    with pytest.raises(RuntimeError):
        enqueue_review_task("RESEARCH","lembrancinhas-flores-eva","request-12345678")

def test_staging_requires_postgres(monkeypatch):
    monkeypatch.setenv("ESFERA_ENV","test")
    monkeypatch.delenv("DATABASE_URL",raising=False)
    with pytest.raises(RuntimeError):
        enqueue_review_task("RESEARCH","lembrancinhas-flores-eva","request-12345678")
