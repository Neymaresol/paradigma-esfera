"""Hotmart affiliate catalog synchronization core.

Requires an authorized connector to supply approved items; does not scrape,
contact Hotmart, write production databases, or publish advertising.
"""
from dataclasses import dataclass
from urllib.parse import urlsplit
import re

CODE = re.compile(r"^[A-Za-z][0-9]{9}[A-Za-z]$")

@dataclass(frozen=True)
class AffiliateOffer:
    code: str
    url: str
    title: str
    partner: str = "hotmart"
    state: str = "pending_review"


def parse_hotlink(url: str) -> str:
    parsed = urlsplit(url.strip())
    if parsed.scheme != "https" or parsed.hostname != "go.hotmart.com":
        raise ValueError("Unapproved Hotmart URL")
    if parsed.username or parsed.password or parsed.port or parsed.query or parsed.fragment:
        raise ValueError("Unexpected Hotmart URL components")
    code = parsed.path.strip("/")
    if "/" in code or not CODE.fullmatch(code):
        raise ValueError("Invalid Hotmart affiliate code")
    return code


def synchronize(items, existing=()):
    """Import only connector-confirmed affiliations; never enable publication.

    items: iterable of mappings from an authenticated/authorized connector.
    Existing offers are preserved by code, preventing duplicate imports.
    """
    registry = {offer.code: offer for offer in existing}
    metrics = {"received": 0, "added": 0, "existing": 0, "rejected": 0}
    for raw in items:
        metrics["received"] += 1
        try:
            if raw.get("affiliate_authorized") is not True:
                raise ValueError("Affiliation not confirmed")
            url = str(raw["affiliate_url"]).strip()
            code = parse_hotlink(url)
            title = str(raw["title"]).strip()
            if not title:
                raise ValueError("Missing product title")
        except (ValueError, KeyError, AttributeError, TypeError):
            metrics["rejected"] += 1
            continue
        if code in registry:
            metrics["existing"] += 1
            continue
        registry[code] = AffiliateOffer(code=code, url=url, title=title)
        metrics["added"] += 1
    return {"offers": tuple(registry.values()), "metrics": metrics,
            "publication_enabled": False, "source_verified_by_application": False}
