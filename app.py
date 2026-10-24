from fastapi import FastAPI, HTTPException, Query, Depends, Request
from esfera_auth import require_operator
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import os
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime, timezone
from html import escape

app = FastAPI(title='PARADIGMA ESFERA 1.0', version='1.3.1-dev', docs_url=None, redoc_url=None, openapi_url=None)
@app.middleware('http')
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'unsafe-inline'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
    return response
CATALOG = [
 {'id':'ia-basica','name':'IA no dia a dia','category':'Cursos','price_brl':9.90,'duration_min':30},
 {'id':'celular','name':'Celular e aplicativos','category':'Cursos','price_brl':9.90,'duration_min':30},
 {'id':'seguranca','name':'Segurança digital','category':'Cursos','price_brl':9.90,'duration_min':30},
 {'id':'planilhas','name':'Planilhas para trabalho','category':'Cursos','price_brl':14.90,'duration_min':45},
 {'id':'vendas','name':'Vendas digitais','category':'Cursos','price_brl':14.90,'duration_min':45},
 {'id':'marketing','name':'Divulgação responsável','category':'Cursos','price_brl':14.90,'duration_min':45},
 {'id':'curriculo','name':'Currículo profissional','category':'Serviços','price_brl':9.90},
 {'id':'catalogo','name':'Catálogo digital','category':'Serviços','price_brl':29.90},
 {'id':'agenda','name':'Agenda inteligente','category':'Serviços','price_brl':14.90},
 {'id':'atendimento','name':'Atendimento com IA','category':'Serviços','price_brl':19.90},
]
# In-memory simulation only; never stores real customer data or processes payments.
ORDERS = {}
class SimulatedOrder(BaseModel):
    product_id: str
    country: str = Field(default='BR', pattern='^(BR|PT|ES|US)$')
@app.get('/health')
def health():
    return {'status':'ok','service':'paradigma-esfera','version':'1.3.1-dev','mode':'simulation','checkout_enabled':False,'live_ads_enabled':False,'auto_replication_enabled':False}
@app.get('/api/catalog')
def catalog():
    return {'currency':'BRL','prices_are_suggested':True,'items':CATALOG}
@app.post('/api/orders/simulate')
def simulate(order:SimulatedOrder, actor: dict = Depends(require_operator)):
    item=next((p for p in CATALOG if p['id']==order.product_id),None)
    if not item: raise HTTPException(404,'Produto não encontrado')
    oid=str(uuid4()); data={'id':oid,'product_id':item['id'],'country':order.country,'status':'SIMULATED_ONLY','payment_confirmed':False,'commission_confirmed':False,'created_at':datetime.now(timezone.utc).isoformat()}
    ORDERS[oid]=data
    return data
@app.get('/api/orders/{order_id}')
def order_status(order_id:str, actor: dict = Depends(require_operator)):
    if order_id not in ORDERS: raise HTTPException(404,'Pedido não encontrado')
    return ORDERS[order_id]
I18N = {
 'pt': {'headline':'Aprenda, crie e evolua','intro':'Cursos e microsserviços digitais para pessoas e negócios.','catalog':'Conheça nossas soluções','course':'Curso','service':'Serviço','price':'Preço ilustrativo','pending':'Em preparação · compra indisponível','notice':'Demonstração: sem pagamentos, assinaturas ou anúncios ativos.'},
 'en': {'headline':'Learn, create and grow','intro':'Digital courses and microservices for people and businesses.','catalog':'Explore our solutions','course':'Course','service':'Service','price':'Illustrative price','pending':'Coming soon · checkout unavailable','notice':'Demo only: no payments, subscriptions or live ads.'},
 'es': {'headline':'Aprende, crea y crece','intro':'Cursos y microservicios digitales para personas y empresas.','catalog':'Explora nuestras soluciones','course':'Curso','service':'Servicio','price':'Precio ilustrativo','pending':'En preparación · compra no disponible','notice':'Demostración: sin pagos, suscripciones ni anuncios activos.'},
 'fr': {'headline':'Apprenez, créez et progressez','intro':'Cours et microservices numériques pour tous.','catalog':'Découvrez nos solutions','course':'Cours','service':'Service','price':'Prix indicatif','pending':'Bientôt disponible · achat désactivé','notice':'Démonstration : aucun paiement ni publicité active.'},
 'de': {'headline':'Lernen, gestalten, wachsen','intro':'Digitale Kurse und Mikroservices für Menschen und Unternehmen.','catalog':'Unsere Angebote','course':'Kurs','service':'Dienstleistung','price':'Beispielpreis','pending':'In Vorbereitung · Kauf nicht verfügbar','notice':'Demo: keine Zahlungen oder aktiven Anzeigen.'},
 'ar': {'headline':'تعلم وابتكر وتطور','intro':'دورات وخدمات رقمية للأفراد والشركات.','catalog':'اكتشف خدماتنا','course':'دورة','service':'خدمة','price':'سعر توضيحي','pending':'قريباً · الشراء غير متاح','notice':'نسخة تجريبية: لا مدفوعات ولا إعلانات نشطة.'}
}

@app.get('/api/i18n/languages')
def languages():
    return {'supported':list(I18N),'default':'pt','other_languages_require_review':True}

@app.get('/api/readiness')
def readiness():
    return {'status':'NOT_READY_FOR_SALES','verified_payments':False,'fulfillment_verified':False,'tax_and_privacy_review':False,'payment_provider_connected':False,'marketing_permissions_verified':False,'publish_allowed':False}

@app.get('/',response_class=HTMLResponse)
def home(lang: str = Query(default='pt')):
    if lang not in I18N: raise HTTPException(400,'Unsupported language')
    t=I18N[lang]
    cards=''.join(f'<article><span>{escape(t["course"] if p["category"]=="Cursos" else t["service"])}</span><h3>{escape(p["name"])}</h3><strong>R$ {p["price_brl"]:.2f}</strong><p>{escape(t["pending"])}</p></article>' for p in CATALOG)
    links=' '.join(f'<a href="/?lang={code}" lang="{code}" aria-label="{code}">{code.upper()}</a>' for code in I18N)
    direction='rtl' if lang=='ar' else 'ltr'
    return f'''<!doctype html><html lang="{lang}" dir="{direction}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PARADIGMA ESFERA 1.2</title><style>body{{margin:0;background:#071226;color:#eaf5ff;font:16px system-ui}}header{{padding:48px 6%;background:radial-gradient(circle at 70% 30%,#154e8d,#071226 55%)}}h1{{font-size:clamp(30px,5vw,60px);margin:12px 0}}p{{color:#a9bdd2}}.tag{{color:#67e8f9;letter-spacing:2px}}main{{padding:28px 6%}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:16px}}article{{background:#10253e;border:1px solid #244565;border-radius:18px;padding:22px}}article span{{color:#67e8f9;font-size:12px}}strong{{font-size:24px}}.notice{{padding:12px;border:1px solid #51718b;border-radius:12px}}nav a{{display:inline-block;padding:8px;margin:3px;color:#a5f3fc;border:1px solid #244565;border-radius:8px;text-decoration:none}}a:focus{{outline:2px solid #67e8f9}}</style></head><body><header><div class="tag">PARADIGMA ESFERA · GLOBAL</div><nav aria-label="Languages">{links}</nav><h1>{escape(t["headline"])}</h1><p>{escape(t["intro"])}</p><p class="notice">{escape(t["notice"])}</p></header><main><h2>{escape(t["catalog"])}</h2><div class="grid">{cards}</div><p>Version 1.2.0-dev · no checkout · no autonomous advertising</p></main></body></html>'''

from esfera_engine import Gate, expansion_decision, campaign_plan

class ExpansionRequest(BaseModel):
    verified_sales: int = Field(default=0, ge=0)
    verified_margin_brl: float = 0
    fulfilled_orders: int = Field(default=0, ge=0)
    unresolved_incidents: int = Field(default=0, ge=0)
    approved_budget_brl: float = Field(default=0, ge=0)
    platform_authorized: bool = False
    owner_approved: bool = False
    health_ok: bool = False
    proposed_children: int = Field(default=10, ge=1, le=10)

@app.post('/api/expansion/evaluate')
def evaluate_expansion(req: ExpansionRequest, actor: dict = Depends(require_operator)):
    values = req.model_dump()
    proposed_children = values.pop('proposed_children')
    # Caller supplied values are NOT trusted evidence. Never allow provisioning from this endpoint.
    result = expansion_decision(Gate(**values), proposed_children)
    result['evidence_verified_by_server'] = False
    result['deployment_allowed'] = False
    return result

@app.get('/api/campaigns/drafts')
def campaign_drafts(channel: str = 'facebook', actor: dict = Depends(require_operator)):
    if channel not in ('facebook', 'instagram', 'tiktok', 'search'):
        raise HTTPException(400, 'Canal não permitido')
    return {'campaigns': [campaign_plan(p, channel) for p in CATALOG],
            'publication_enabled': False, 'advertising_spend_enabled': False}

# Phase 1.3: durable local proposal queue, still fail-closed and not production-ready.
from esfera_ops import propose, proposals, audit

class ProposalRequest(BaseModel):
    kind: str
    product_id: str
    channel: str = 'internal'
    rationale: str = Field(min_length=8, max_length=500)

@app.post('/api/ops/proposals', status_code=201)
def create_proposal(req: ProposalRequest, actor: dict = Depends(require_operator)):
    if req.product_id not in {p['id'] for p in CATALOG}:
        raise HTTPException(404, 'Produto não encontrado')
    if req.kind not in ('CAMPAIGN', 'CELL_EXPANSION', 'INFRA_UPGRADE', 'COURSE'):
        raise HTTPException(400, 'Tipo não permitido')
    if req.channel not in ('internal', 'facebook', 'instagram', 'tiktok', 'search'):
        raise HTTPException(400, 'Canal não permitido')
    return propose(req.kind, {'product_id': req.product_id, 'channel': req.channel, 'rationale': req.rationale})

@app.get('/api/ops/proposals')
def list_proposals(actor: dict = Depends(require_operator)):
    return {'items': proposals(), 'external_actions_enabled': False}

@app.get('/api/ops/audit')
def list_audit(actor: dict = Depends(require_operator)):
    return {'items': audit(), 'external_actions_enabled': False}

@app.get('/api/ops/dashboard')
def ops_dashboard(actor: dict = Depends(require_operator)):
    return {'service': 'paradigma-esfera', 'version': '1.3.1-dev',
            'operational_mode': 'LOCAL_STAGING_ONLY', 'catalog_offers': len(CATALOG),
            'pending_proposals': len(proposals()), 'simulated_orders_in_process': len(ORDERS),
            'verified_sales': None, 'verified_commissions_brl': None,
            'bank_balance_brl': None, 'financial_source_connected': False,
            'payments_enabled': False, 'posting_enabled': False, 'auto_replication_enabled': False,
            'infrastructure_auto_purchase_enabled': False}


# Revenue-first affiliate storefront: disabled until partner authorization is verified.
# No checkout, payment capture, click fabrication, or commission claim occurs here.
from fastapi.responses import RedirectResponse

AFFILIATE_OFFERS = {
    "hotmart-inicial": {
        "title": "Oferta digital na Hotmart",
        "url": "https://go.hotmart.com/G108129576P",
        "provider": "Hotmart",
    }
}

def affiliate_publication_allowed():
    # Two independent release gates: publishing and partner authorization.
    return (os.getenv("ESFERA_AFFILIATE_PUBLISH_ENABLED", "false").lower() == "true"
            and os.getenv("ESFERA_AFFILIATE_PARTNER_VERIFIED", "false").lower() == "true")

@app.get("/api/affiliate/readiness")
def affiliate_readiness():
    return {"publication_allowed": affiliate_publication_allowed(),
            "partner_verified_flag": os.getenv("ESFERA_AFFILIATE_PARTNER_VERIFIED", "false").lower() == "true",
            "attribution_verified": False,
            "commissions_reconciled": False,
            "financial_claims_allowed": False}

@app.get("/ofertas", response_class=HTMLResponse)
def affiliate_storefront():
    enabled = affiliate_publication_allowed()
    if not enabled:
        return '<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ofertas ESFERA</title><body style="font:18px system-ui;background:#071226;color:white;padding:2rem"><h1>ESFERA · Ofertas</h1><p>Ofertas em validação. Nenhuma compra está habilitada nesta página.</p></body></html>'
    cards = ''.join(
        f'<article><h2>{escape(o["title"])}</h2><p>Parceiro: {escape(o["provider"])}</p><p>Publicidade / link de afiliado: podemos receber comissão por compras elegíveis.</p><a href="/ofertas/{escape(k)}" rel="nofollow sponsored">Ver oferta na plataforma parceira</a></article>'
        for k,o in AFFILIATE_OFFERS.items()
    )
    return f'<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ofertas ESFERA</title><body style="font:18px system-ui;background:#071226;color:white;padding:2rem"><h1>ESFERA · Ofertas autorizadas</h1>{cards}</body></html>'

@app.get("/ofertas/{offer_id}")
def affiliate_outbound(offer_id: str):
    if not affiliate_publication_allowed():
        raise HTTPException(503, "Oferta ainda não autorizada para publicação")
    offer = AFFILIATE_OFFERS.get(offer_id)
    if not offer:
        raise HTTPException(404, "Oferta não encontrada")
    return RedirectResponse(url=offer["url"], status_code=302, headers={"Referrer-Policy": "no-referrer"})
