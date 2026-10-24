"""Organic acquisition copy for ESFERA. Never represents verified product claims or paid ads."""
from esfera_tags import classify_channel, tag_for_channel, safe_campaign, landing

CHANNELS = ("google", "chatgpt", "bing", "organic", "instagram", "facebook", "tiktok", "creator")
COPY = {
    "pt": {"headline": "Aprenda habilidades digitais com ofertas selecionadas",
           "description": "Conheça cursos e soluções digitais na plataforma parceira. Confira conteúdo, preço e condições antes de comprar.",
           "disclosure": "Publicidade: podemos receber comissão por compras elegíveis."},
    "en": {"headline": "Explore selected digital learning offers",
           "description": "Check course details, prices and terms on the partner platform before purchasing.",
           "disclosure": "Affiliate disclosure: we may earn a commission on eligible purchases."},
    "es": {"headline": "Descubre ofertas seleccionadas de aprendizaje digital",
           "description": "Consulta detalles, precios y condiciones en la plataforma asociada antes de comprar.",
           "disclosure": "Publicidad: podemos recibir una comisión por compras elegibles."}
}

def draft(channel: str, offer_id: str, campaign: str = "", lang: str = "pt") -> dict:
    channel = classify_channel(channel)
    if channel not in CHANNELS:
        channel = "organic"
    lang = lang if lang in COPY else "pt"
    return {"channel": channel, "tag": tag_for_channel(channel), "language": lang,
            "campaign": safe_campaign(campaign), "copy": COPY[lang],
            "internal_landing": landing(offer_id, channel, campaign),
            "external_posting_enabled": False, "affiliate_link_publication_enabled": False,
            "verified_sales": None, "commission_brl": None}
