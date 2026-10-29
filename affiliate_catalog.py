"""ESFERA affiliate catalog: authorized, validated bulk import into staging Neon.
No scraping, credentials, price inference, or automatic publication.
"""
import os
from urllib.parse import urlparse
from datetime import datetime, timezone
import psycopg
from psycopg.rows import dict_row
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from esfera_auth import require_operator

router = APIRouter(prefix="/api/affiliate-catalog", tags=["affiliate-catalog"])
HOSTS = {"hotmart": {"go.hotmart.com"}, "amazon": {"www.amazon.com.br", "amazon.com.br"}, "shopee": {"s.shopee.com.br"}, "mercadolivre": {"meli.la"}, "magalu": {"www.magazinevoce.com.br"}}
class Offer(BaseModel):
    partner: str
    title: str = Field(min_length=5, max_length=240)
    affiliate_url: str = Field(max_length=2000)
    description: str = Field(default="", max_length=500)
    source: str = Field(default="operator_verified", max_length=100)
class Batch(BaseModel):
    offers: list[Offer] = Field(min_length=1, max_length=200)
    dry_run: bool = True

def conn():
    url = os.getenv("ESFERA_CATALOG_DATABASE_URL")
    if not url:
        raise HTTPException(503, "Staging catalog database not configured")
    return psycopg.connect(url, connect_timeout=5, row_factory=dict_row)

def validate(o):
    p = o.partner.lower().strip()
    host = urlparse(o.affiliate_url).hostname
    if p not in HOSTS or host not in HOSTS[p] or urlparse(o.affiliate_url).scheme != "https":
        raise HTTPException(422, "Partner or affiliate link not on approved allowlist")
    if o.source not in ("operator_verified", "partner_api", "authorized_feed"):
        raise HTTPException(422, "Unverified offer source")
    return p

def ensure_table(c):
    c.execute("""CREATE TABLE IF NOT EXISTS esfera_affiliate_offers (
        id BIGSERIAL PRIMARY KEY, partner TEXT NOT NULL, title TEXT NOT NULL,
        affiliate_url TEXT NOT NULL, description TEXT NOT NULL DEFAULT '',
        source TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'review',
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        UNIQUE(partner, affiliate_url))""")

@router.post("/import")
def import_offers(batch: Batch, actor: dict = Depends(require_operator)):
    partners = [validate(o) for o in batch.offers]
    if batch.dry_run:
        return {"status": "validated_only", "count": len(batch.offers), "written": 0, "publication": False}
    with conn() as c:
        ensure_table(c)
        for o, partner in zip(batch.offers, partners):
            c.execute("""INSERT INTO esfera_affiliate_offers (partner,title,affiliate_url,description,source)
                VALUES (%s,%s,%s,%s,%s) ON CONFLICT (partner,affiliate_url)
                DO UPDATE SET title=EXCLUDED.title,description=EXCLUDED.description,
                source=EXCLUDED.source,updated_at=now(),status='review'""",
                (partner,o.title.strip(),o.affiliate_url,o.description,o.source))
    return {"status": "imported_for_review", "count": len(batch.offers), "publication": False}

@router.get("/offers")
def list_offers(partner: str | None = None):
    if partner is not None and partner not in HOSTS:
        raise HTTPException(422, "Unknown partner")
    with conn() as c:
        ensure_table(c)
        rows = c.execute("""SELECT partner,title,affiliate_url,description,status,updated_at
            FROM esfera_affiliate_offers WHERE (%s IS NULL OR partner=%s)
            AND status='approved' ORDER BY partner,updated_at DESC LIMIT 500""",(partner,partner)).fetchall()
    return {"offers": rows, "source": "staging_neon", "commissions_verified": False}
