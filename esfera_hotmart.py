"""Fail-closed Hotmart offer import staging module. No network, advertising or payments."""
import re
from urllib.parse import urlsplit

MAX_BATCH = 50
HOTLINK = re.compile(r"^/[A-Za-z][0-9]{9}[A-Za-z]$")
STATES = ("PENDING_REVIEW", "APPROVED", "REJECTED", "DISABLED")

def validate_hotlink(value):
    if not isinstance(value, str):
        raise ValueError("HotLink must be a string")
    parts = urlsplit(value)
    if parts.scheme != "https" or parts.netloc != "go.hotmart.com" or not HOTLINK.fullmatch(parts.path) or parts.query or parts.fragment or parts.username or parts.password:
        raise ValueError("Invalid Hotmart affiliate link")
    return value

def normalize_offer(row):
    if not isinstance(row, dict):
        raise ValueError("Offer must be an object")
    slug = row.get("slug")
    title = row.get("title")
    if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or len(slug) > 80:
        raise ValueError("Invalid slug")
    if not isinstance(title, str) or not (3 <= len(title.strip()) <= 160):
        raise ValueError("Invalid title")
    link = validate_hotlink(row.get("hotlink"))
    return {"slug": slug, "title": title.strip(), "hotlink": link,
            "status": "PENDING_REVIEW", "partner_verified": False,
            "link_destination_verified": False, "attribution_verified": False,
            "publish_enabled": False}

def validate_batch(items):
    if not isinstance(items, list) or not (1 <= len(items) <= MAX_BATCH):
        raise ValueError("Batch must contain 1 to 50 offers")
    result = [normalize_offer(x) for x in items]
    if len({x["slug"] for x in result}) != len(result):
        raise ValueError("Duplicate slugs")
    if len({x["hotlink"] for x in result}) != len(result):
        raise ValueError("Duplicate HotLinks")
    return result

def eligible_for_publication(row, global_publish_enabled=False):
    return bool(global_publish_enabled and row["status"] == "APPROVED"
                and row["partner_verified"] and row["link_destination_verified"]
                and row["attribution_verified"] and row["publish_enabled"])
