"""ESFERA: safe read-only normalization of approved partner offers.
Does not grant affiliation, publish advertisements, or bypass existing release gates.
2026-10-28 BRT.
"""
from urllib.parse import urlsplit
from ipaddress import ip_address

PARTNER_HOSTS = {
    "hotmart": {"go.hotmart.com"},
    "amazon": {"amazon.com.br", "www.amazon.com.br"},
    "shopee": {"s.shopee.com.br", "shopee.com.br", "www.shopee.com.br"},
    "magalu": {"magazineluiza.com.br", "www.magazineluiza.com.br"},
    "mercado_livre": {"mercadolivre.com.br", "www.mercadolivre.com.br", "meli.la"},
}
def normalize_offer(record):
    """Return an approved offer or None. Never infer authorization from URL alone."""
    if not isinstance(record, dict):
        return None
    partner = str(record.get("partner", "")).lower().strip()
    url = record.get("affiliate_url")
    if partner not in PARTNER_HOSTS or not isinstance(url, str):
        return None
    try:
        parsed = urlsplit(url)
        host = (parsed.hostname or "").lower().rstrip(".")
        if parsed.scheme != "https" or host not in PARTNER_HOSTS[partner] or parsed.username or parsed.password or parsed.port not in (None, 443):
            return None
    except ValueError:
        return None
    if record.get("affiliate_authorized") is not True or record.get("attribution_verified") is not True:
        return None
    title = record.get("title")
    external_id = record.get("external_id")
    if not isinstance(title, str) or not title.strip() or not isinstance(external_id, str) or not external_id.strip():
        return None
    return {"partner": partner, "title": title.strip()[:180], "external_id": external_id.strip()[:100], "affiliate_url": url}

def approved_catalog(records):
    """Deduplicate only evidence-backed offers; returns data, not publication approval."""
    result = {}
    for record in records:
        offer = normalize_offer(record)
        if offer:
            result[(offer["partner"], offer["external_id"])] = offer
    return list(result.values())
