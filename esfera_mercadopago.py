"""Mercado Pago Checkout Pro sandbox-only integration. No production charges.
Operator-authenticated preference creation; no local claims of confirmed payments.
"""
import os
from uuid import uuid4
from urllib.parse import urlparse
import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from esfera_auth import require_operator

router = APIRouter(prefix="/api/payments/mercadopago", tags=["mercadopago"])
SANDBOX_API = "https://api.mercadopago.com/checkout/preferences"
# Fixed sandbox prices only, not a live commercial catalog.
TEST_ITEMS = {
    "curriculo": ("Currículo profissional - TESTE", 9.90),
    "catalogo": ("Catálogo digital - TESTE", 29.90),
    "agenda": ("Agenda inteligente - TESTE", 14.90),
}
class TestCheckout(BaseModel):
    product_id: str

def enabled():
    return os.getenv("ESFERA_MP_TEST_CHECKOUT_ENABLED", "false").lower() == "true"

@router.get("/readiness")
def readiness(actor: dict = Depends(require_operator)):
    return {
        "sandbox_enabled": enabled(),
        "test_token_configured": bool(os.getenv("MERCADOPAGO_ACCESS_TOKEN_TEST")),
        "production_checkout_enabled": False,
        "webhook_verified": False,
        "payments_confirmed": False,
    }

@router.post("/test-preference")
async def test_preference(data: TestCheckout, actor: dict = Depends(require_operator)):
    if not enabled():
        raise HTTPException(503, "Sandbox checkout disabled")
    token = os.getenv("MERCADOPAGO_ACCESS_TOKEN_TEST", "")
    if not token or not token.startswith("TEST-"):
        raise HTTPException(503, "Valid Mercado Pago TEST token not configured")
    item = TEST_ITEMS.get(data.product_id)
    if not item:
        raise HTTPException(422, "Unknown sandbox product")
    title, price = item
    payload = {
        "items": [{"id": data.product_id, "title": title, "quantity": 1,
                   "unit_price": price, "currency_id": "BRL"}],
        "external_reference": "ESFERA-TEST-" + uuid4().hex,
    }
    try:
        async with httpx.AsyncClient(timeout=12.0) as client:
            response = await client.post(
                SANDBOX_API, json=payload,
                headers={"Authorization": "Bearer " + token,
                         "X-Idempotency-Key": str(uuid4())})
    except httpx.RequestError:
        raise HTTPException(502, "Mercado Pago sandbox unavailable")
    if response.status_code not in (200, 201):
        raise HTTPException(502, "Mercado Pago sandbox rejected preference")
    result = response.json()
    url = result.get("sandbox_init_point")
    if not url or urlparse(url).scheme != "https" or urlparse(url).hostname not in {
        "www.mercadopago.com.br", "mercadopago.com.br",
        "www.mercadopago.com", "mercadopago.com"
    }:
        raise HTTPException(502, "Sandbox checkout URL not validated")
    return {"status": "TEST_ONLY", "sandbox_checkout_url": url,
            "preference_id": result.get("id"), "payment_confirmed": False}

@router.get("/diagnostics")
async def diagnostics(actor: dict = Depends(require_operator)):
    """Read-only provider credential check; never exposes secrets or customer data."""
    token = os.getenv("MERCADOPAGO_ACCESS_TOKEN_TEST", "")
    if not token:
        return {"credential_present": False, "credential_accepted": False,
                "provider_reachable": None, "production_checkout_enabled": False}
    if not token.startswith("TEST-"):
        return {"credential_present": True, "credential_accepted": False,
                "provider_reachable": None, "production_checkout_enabled": False}
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.get(
                "https://api.mercadopago.com/users/me",
                headers={"Authorization": "Bearer " + token})
    except httpx.RequestError:
        return {"credential_present": True, "credential_accepted": False,
                "provider_reachable": False, "production_checkout_enabled": False}
    return {"credential_present": True, "credential_accepted": response.status_code == 200,
            "provider_reachable": True, "production_checkout_enabled": False}
