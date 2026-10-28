"""ESFERA SMART radar: read-only, fail-closed opportunity planner.

No external source ingestion, outbound publishing, affiliate redirects or financial claims.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/radar", tags=["radar"])

INTERESTS = {
    "rock": ("jaquetas", "botas", "camisetas", "maquiagem", "acessorios"),
    "pop-rock": ("jaquetas", "tenis", "maquiagem", "acessorios"),
    "k-pop": ("streetwear", "tenis", "mochilas", "acessorios"),
    "sertanejo": ("botas", "chapeus", "cintos", "jeans"),
    "country": ("botas", "chapeus", "cintos", "jeans"),
    "funk": ("streetwear", "tenis", "bones", "oculos"),
    "futebol": ("camisas-licenciadas", "chuteiras", "bolas", "acessorios"),
    "futsal": ("chuteiras-indoor", "bolas", "uniformes"),
    "basquete": ("tenis", "regatas", "bolas", "streetwear"),
    "tenis": ("raquetes", "bolas", "calcados", "roupas-esportivas"),
    "natacao": ("oculos", "toucas", "roupas-de-banho"),
    "automobilismo": ("bones", "jaquetas", "miniaturas-licenciadas"),
    "celulares": ("smartphones", "capas", "carregadores", "fones"),
    "beleza": ("perfumes", "shampoo", "maquiagem", "skincare"),
    "servicos": ("cursos", "design", "sites", "atendimento-digital"),
}

class PreviewRequest(BaseModel):
    interest: str = Field(min_length=2, max_length=40)
    country: str = Field(default="BR", pattern=r"^[A-Z]{2}$")
    event_name: str | None = Field(default=None, max_length=120)
    event_date: str | None = Field(default=None, max_length=10)

def build_preview(interest: str, country: str, event_name=None, event_date=None):
    key = interest.strip().lower()
    if key not in INTERESTS:
        raise ValueError("Interesse não suportado")
    if event_date:
        try:
            date = datetime.strptime(event_date, "%Y-%m-%d").date()
        except ValueError as exc:
            raise ValueError("Data inválida; use YYYY-MM-DD") from exc
        if date < datetime.now(timezone.utc).date():
            raise ValueError("Evento precisa ter data futura")
    return {
        "interest": key, "country": country,
        "event": {"name": event_name, "date": event_date, "verified": False} if event_name else None,
        "product_categories": list(INTERESTS[key]),
        "offer_links": [], "affiliate_attribution_verified": False,
        "publication_enabled": False, "ads_enabled": False,
        "verified_sales": None, "verified_commissions": None,
        "status": "PREVIEW_ONLY",
        "note": "Sugestões de categorias, não produtos/ofertas reais. Evento informado não foi verificado.",
    }

@router.get("/status")
def radar_status():
    return {
        "service": "esfera-smart-radar", "version": "0.1.0-staging",
        "mode": "PREVIEW_ONLY", "event_sources_connected": False,
        "verified_events": 0, "verified_offers": 0,
        "automatic_publication": False, "commission_provider_connected": False,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

@router.get("/interests")
def interests():
    return {"items": [{"id": key, "categories": list(value)} for key, value in INTERESTS.items()]}

@router.get("/opportunities")
def opportunities(country: str = Query(default="BR", pattern=r"^[A-Z]{2}$"),
                  limit: int = Query(default=20, ge=1, le=100)):
    # Never invent events: source ingestion is not yet configured.
    return {"country": country, "items": [], "count": 0, "limit": limit,
            "sources_connected": False, "data_verified": False,
            "note": "Nenhuma agenda oficial integrada; não há eventos verificados."}

@router.post("/campaigns/preview")
def preview(request: PreviewRequest):
    try:
        return build_preview(request.interest, request.country, request.event_name, request.event_date)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
