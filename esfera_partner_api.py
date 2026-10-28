"""Read-only partner catalog API. No publication, checkout or outbound redirects."""
from fastapi import APIRouter
from esfera_partner_catalog import PARTNER_HOSTS

router = APIRouter(prefix="/api/partners", tags=["partners"])

@router.get("/status")
def partner_status():
    return {
        "mode": "read_only",
        "publication_enabled": False,
        "providers": [{"id": key, "allowed_domains": sorted(domains), "integration": "pending_verified_feed"}
                      for key, domains in sorted(PARTNER_HOSTS.items())],
        "verified_offers": 0,
        "verified_sales": None,
        "verified_commissions_brl": None,
        "note": "Allowlisted domains do not prove affiliate authorization or attribution.",
    }

@router.get("/catalog")
def partner_catalog():
    return {
        "items": [],
        "source": "none_verified",
        "affiliate_publication_enabled": False,
        "note": "No external offers shown until provider evidence and feed integration are verified.",
    }
