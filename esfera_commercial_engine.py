"""Pure, fail-closed per-offer commercial readiness logic.

This module does not connect to providers, publish ads, or process payments.
"""
def evaluate_offers(offers, publication_allowed=False):
    items = []
    for offer_id, offer in offers.items():
        configured = bool(offer.get("url"))
        items.append({
            "id": offer_id,
            "partner": offer.get("provider", "Unknown"),
            "title": offer.get("title", ""),
            "destination_configured": configured,
            "outbound_enabled": bool(publication_allowed and configured),
            "needs_partner_evidence": not publication_allowed,
            "needs_destination": not configured,
        })
    return {
        "offers": items,
        "total": len(items),
        "configured": sum(x["destination_configured"] for x in items),
        "enabled": sum(x["outbound_enabled"] for x in items),
        "verified_sales": None,
        "verified_commissions_brl": None,
    }
