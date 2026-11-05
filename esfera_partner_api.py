"""Read-only partner catalog API. No publication, checkout or outbound redirects."""
from fastapi import APIRouter, HTTPException
from affiliate_catalog import approved_catalog_read
from esfera_partner_catalog import PARTNER_HOSTS

router = APIRouter(prefix="/api/partners", tags=["partners"])

@router.get("/status")
def partner_status():
    try:
        offers = approved_catalog_read()
        catalog_status = "staging_catalog_connected"
        count = len(offers)
    except Exception:
        catalog_status = "staging_catalog_unavailable"
        count = 0
    return {
        "mode": "read_only",
        "publication_enabled": False,
        "providers": [{"id": key, "allowed_domains": sorted(domains), "integration": "approved_catalog_only"}
                      for key, domains in sorted(PARTNER_HOSTS.items())],
        "catalog_status": catalog_status,
        "verified_offers": count,
        "verified_sales": None,
        "verified_commissions_brl": None,
        "note": "Only offers manually approved in the staging catalog are returned; sales and commissions remain unverified.",
    }

@router.get("/catalog")
def partner_catalog(partner: str | None = None):
    if partner is not None and partner not in PARTNER_HOSTS:
        raise HTTPException(422, "Unknown partner")
    try:
        items = approved_catalog_read(partner)
    except Exception:
        return {
            "items": [],
            "source": "staging_catalog_unavailable",
            "affiliate_publication_enabled": False,
            "note": "Staging catalog is not connected. No fallback or unverified offer is shown.",
        }
    return {
        "items": items,
        "source": "staging_approved_catalog",
        "affiliate_publication_enabled": False,
        "note": "Offers are visible for review only; public affiliate publication remains disabled.",
    }
