"""GET /api/affiliate-catalog/offers must remain strictly read-only."""
import pytest
from fastapi import HTTPException

import affiliate_catalog


class FakeCursor:
    def __init__(self, row=None, rows=None):
        self.row = row
        self.rows = rows or []

    def fetchone(self):
        return self.row

    def fetchall(self):
        return self.rows


class FakeConnection:
    def __init__(self, table_exists=True, rows=None):
        self.table_exists = table_exists
        self.rows = rows or []
        self.statements = []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def execute(self, sql, params=None):
        self.statements.append((sql, params))
        normalized = " ".join(sql.lower().split())
        if "to_regclass" in normalized:
            return FakeCursor({"table_name": "esfera_affiliate_offers" if self.table_exists else None})
        if normalized.startswith("select partner,title"):
            return FakeCursor(rows=self.rows)
        if normalized.startswith("create table"):
            raise AssertionError("GET attempted DDL")
        return FakeCursor()


def test_get_does_not_create_table_when_catalog_is_missing(monkeypatch):
    db = FakeConnection(table_exists=False)
    monkeypatch.setattr(affiliate_catalog, "conn", lambda: db)
    monkeypatch.setattr(
        affiliate_catalog,
        "ensure_table",
        lambda _connection: (_ for _ in ()).throw(AssertionError("GET called ensure_table")),
    )

    result = affiliate_catalog.list_offers()

    assert result["offers"] == []
    assert result["catalog_initialized"] is False
    assert result["commissions_verified"] is False
    assert len(db.statements) == 1
    assert "to_regclass" in db.statements[0][0].lower()


def test_get_reads_approved_offers_without_ddl(monkeypatch):
    expected = [{"partner": "hotmart", "title": "Curso aprovado", "status": "approved"}]
    db = FakeConnection(table_exists=True, rows=expected)
    monkeypatch.setattr(affiliate_catalog, "conn", lambda: db)
    monkeypatch.setattr(
        affiliate_catalog,
        "ensure_table",
        lambda _connection: (_ for _ in ()).throw(AssertionError("GET called ensure_table")),
    )

    result = affiliate_catalog.list_offers("hotmart")

    assert result["offers"] == expected
    assert result["catalog_initialized"] is True
    assert len(db.statements) == 2
    assert all(not sql.lstrip().lower().startswith(("create", "alter", "drop", "insert", "update", "delete"))
               for sql, _ in db.statements)


def test_unknown_partner_is_rejected_before_database_access(monkeypatch):
    monkeypatch.setattr(
        affiliate_catalog,
        "conn",
        lambda: (_ for _ in ()).throw(AssertionError("Database should not be accessed")),
    )

    with pytest.raises(HTTPException) as exc:
        affiliate_catalog.list_offers("unknown-partner")

    assert exc.value.status_code == 422
