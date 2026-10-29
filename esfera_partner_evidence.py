"""Independent evidence gate for ESFERA affiliate publishing.

Do not infer authorization or attribution from operator flags, link format,
a successful HTTP redirect, or a recorded click.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class PartnerEvidence:
    provider: str
    offer_id: str
    affiliate_url: str
    authorized_by_provider: bool = False
    attribution_confirmed_by_provider: bool = False
    evidence_reference: str = ""
    reviewed: bool = False

def eligible(e: PartnerEvidence) -> bool:
    return bool(
        e.provider.strip() and e.offer_id.strip() and
        e.affiliate_url.startswith("https://") and
        e.authorized_by_provider and
        e.attribution_confirmed_by_provider and
        e.evidence_reference.strip() and e.reviewed
    )

def readiness(evidence: list[PartnerEvidence]) -> dict:
    return {
        "verified_offers": sum(eligible(e) for e in evidence),
        "blocked_offers": sum(not eligible(e) for e in evidence),
        "publication_allowed": False,  # separate deployment/release gate required
        "external_actions_enabled": False,
    }
