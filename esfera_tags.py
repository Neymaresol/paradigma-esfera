"""TAG 01/02 channel attribution shared with Wero1Mercados; no private search access or posting."""
from urllib.parse import urlencode

SEARCH = frozenset(("google", "chatgpt", "bing", "organic"))
SOCIAL = frozenset(("instagram", "facebook", "tiktok", "creator"))
ALLOWED = SEARCH | SOCIAL | {"direct"}

def classify_channel(channel: str) -> str:
    value = (channel or "direct").strip().lower()
    return value if value in ALLOWED else "direct"

def tag_for_channel(channel: str) -> str:
    value = classify_channel(channel)
    if value in SEARCH:
        return "TAG_01"
    if value in SOCIAL:
        return "TAG_02"
    return "DIRECT"

def safe_campaign(value: str) -> str:
    value = (value or "").strip()
    return value if 0 < len(value) <= 80 and all(c.isascii() and (c.isalnum() or c in "-_") for c in value) else ""

def landing(offer_id: str, channel: str, campaign: str = "") -> str:
    if not offer_id or not all(c.isascii() and (c.isalnum() or c in "-_") for c in offer_id):
        raise ValueError("invalid offer")
    params = {"channel": classify_channel(channel)}
    if safe_campaign(campaign):
        params["campaign"] = safe_campaign(campaign)
    return "/ofertas/" + offer_id + "?" + urlencode(params)
