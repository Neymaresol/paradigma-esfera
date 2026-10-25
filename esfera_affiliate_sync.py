"""Safe ingestion and reconciliation of authorized affiliate course records.

A scheduled worker can call reconcile with records from an approved provider API.
Never assume an arbitrary product is affiliated or publish unverified URLs.
"""
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

ALLOWED_HOSTS = {"go.hotmart.com"}
REQUIRED = ("provider", "provider_product_id", "title", "affiliate_url", "affiliate_authorized", "attribution_verified")

def validate_course(item):
    if not isinstance(item, dict) or any(key not in item for key in REQUIRED):
        return None
    if item["provider"] != "hotmart":
        return None
    if not isinstance(item["title"], str) or not item["title"].strip():
        return None
    if not isinstance(item["provider_product_id"], str) or not item["provider_product_id"].strip():
        return None
    if item["affiliate_authorized"] is not True or item["attribution_verified"] is not True:
        return None
    url = item["affiliate_url"]
    if not isinstance(url, str):
        return None
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS or not re.fullmatch(r"/[A-Za-z0-9]+/?",parsed.path):
        return None
    return {"id": "hotmart:"+item["provider_product_id"],"title":item["title"].strip()[:180],
            "url":url,"provider":"Hotmart","verified":True,
            "category":str(item.get("category") or "Cursos")[:80],
            "updated_at":datetime.now(timezone.utc).isoformat()}

def reconcile(existing, incoming):
    """Pure function: no network access, publication or database writes."""
    updated = dict(existing)
    rejected = 0
    for record in incoming:
        item = validate_course(record)
        if item is None:
            rejected += 1
            continue
        updated[item["id"]] = item
    return {"catalog":updated,"accepted":len(updated)-len(existing),"rejected":rejected}
