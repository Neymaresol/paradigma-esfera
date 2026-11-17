"""Search-first discovery using relevant topics and approved staging offers only."""
import re, unicodedata
from html import escape
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import HTMLResponse
from esfera_ai_routing import classify
router = APIRouter()
TOPICS = [
{"slug":"inteligencia-artificial","title":"Inteligência Artificial","keywords":["ia","inteligencia artificial","automacao","chatbot","tecnologia","chatgpt","gpt","robotica"],"summary":"Temas e formações em inteligência artificial e automação."},
{"slug":"marketing-digital","title":"Marketing Digital","keywords":["marketing","vendas","publicidade","empreendedorismo","negocios","instagram","tiktok","afiliados","trafego","ecommerce"],"summary":"Marketing, conteúdo, redes sociais e vendas digitais."},
{"slug":"planilhas-produtividade","title":"Planilhas e Produtividade","keywords":["excel","planilhas","trabalho","produtividade","office","formulas","google sheets"],"summary":"Planilhas, dados e organização do trabalho."},
{"slug":"seguranca-digital","title":"Segurança Digital","keywords":["seguranca","privacidade","internet","dados","ciberseguranca","senha","golpe","fraude"],"summary":"Proteção de contas, privacidade e navegação segura."},
{"slug":"curso-ingles","title":"Curso de Inglês","keywords":["ingles","english","idiomas","lingua inglesa","conversacao","fluencia","traducao"],"summary":"Trilhas de idiomas, do básico à conversação."},
{"slug":"carreira-profissional","title":"Carreira Profissional","keywords":["curriculo","emprego","profissao","carreira","entrevista","sap","oracle","prodesp","vaga"],"summary":"Desenvolvimento profissional e preparação para o trabalho."},
]
def norm(s):
    return "".join(c for c in unicodedata.normalize("NFKD", str(s).lower()) if not unicodedata.combining(c))
def terms(q):
    stop={"curso","cursos","de","da","do","das","dos","para","um","uma","quero","aprender","estudar","sobre","como","com"}
    return [w for w in re.findall(r"[\w]+",norm(q)) if w not in stop][:12]
def score(q,t):
    ts=terms(q)
    if not ts: return 1
    hay=norm(" ".join([t["title"],t["summary"],*t["keywords"]]))
    return sum(1 for w in ts if w in hay or any(w in x or x in w for x in hay.split()))
def shell(title,body):
    return "<!doctype html><html lang=\"pt-BR\"><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>"+escape(title)+" | PARADIGMA ESFERA</title><style>body{background:#061229;color:#eef8ff;font:16px system-ui;margin:0}main{max-width:1100px;margin:auto;padding:40px 22px}p{color:#b6cce3;line-height:1.6}a{color:#7ddaff}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px}article{padding:22px;background:#0e2544;border:1px solid #315c83;border-radius:16px}input{padding:14px;min-width:220px}button{padding:14px}</style><main><a href=\"/descobrir\">✦ PARADIGMA ESFERA</a>"+body+"</main></html>"
def approved_offers(q):
    ts=terms(q)
    if not ts: return []
    try:
        from affiliate_catalog import approved_catalog_read
        rows=approved_catalog_read()
    except Exception:
        return []
    found=[]
    for row in rows:
        hay=norm(" ".join([str(row.get("title","")),str(row.get("description","")),str(row.get("partner",""))]))
        matched=[w for w in ts if w in hay or any(w in x or x in w for x in hay.split())]
        if matched: found.append({"title":row.get("title",""),"provider":row.get("partner",""),"description":row.get("description",""),"matched_terms":matched,"commercial_link_enabled":False})
    return found
@router.get("/api/discovery/offers")
def discovery_offers(q:str=Query("",max_length=120)):
    offers=approved_offers(q)
    return {"query":q,"offers":offers,"count":len(offers),"verified_catalog_only":True,"commercial_links_enabled":False}
@router.get("/api/discovery/topics")
def topics(q:str=Query("",max_length=120)):
    results=sorted([t for t in TOPICS if score(q,t)>0],key=lambda t:score(q,t),reverse=True)
    return {"query":q,"results":[{"slug":t["slug"],"title":t["title"],"summary":t["summary"],"url":"/interesses/"+t["slug"],"relevance":score(q,t)} for t in results],"commerce_status":"approved_catalog_review_only"}
@router.get("/api/discovery/route")
def route_search(q:str=Query("",max_length=120)):
    return classify(q)
@router.get("/descobrir",response_class=HTMLResponse)
def discover(q:str=Query("",max_length=120)):
    intent=classify(q)
    results=sorted([t for t in TOPICS if score(q,t)>0],key=lambda t:score(q,t),reverse=True)
    cards="".join("<article><h2>"+escape(t["title"])+"</h2><p>"+escape(t["summary"])+"</p><a href=\"/interesses/"+t["slug"]+"\">Explorar tema</a></article>" for t in results)
    if not cards: cards="<article><h2>Pesquisa recebida: "+escape(q)+"</h2><p>Não encontramos uma categoria exata. Tente termos como tecnologia, cursos, trabalho, música, esportes ou turismo. Ofertas só aparecem após aprovação.</p></article>"
    offers=approved_offers(q)
    offer_cards="".join("<article><h3>"+escape(o["title"])+"</h3><p>Parceiro: "+escape(o["provider"])+"</p><p>Oferta aprovada para consulta. Link comercial desativado.</p></article>" for o in offers)
    body="<h1>O que você quer encontrar?</h1><p>Pesquise por assunto, curso, serviço ou interesse.</p><form action=\"/descobrir\" method=\"get\"><input name=\"q\" maxlength=\"120\" placeholder=\"Ex.: Excel, rock, turismo, inteligência artificial\" value=\""+escape(q,quote=True)+"\"><button>Pesquisar</button></form><div class=\"grid\">"+cards+"</div>"+("<h2>Ofertas relacionadas</h2><div class=\"grid\">"+offer_cards+"</div>" if offer_cards else "")+"<p>Motor: "+escape(str(intent.get("engine","ESFERA"))) +". Links comerciais e publicação permanecem desativados durante a validação.</p>"
    return shell("Descobrir",body)
@router.get("/interesses/{slug}",response_class=HTMLResponse)
def interest(slug:str):
    t=next((x for x in TOPICS if x["slug"]==slug),None)
    if not t: raise HTTPException(404,"Tema não encontrado")
    return shell(t["title"],"<h1>"+escape(t["title"])+"</h1><p>"+escape(t["summary"])+"</p><p>Ofertas comerciais dependem de aprovação e validação dos parceiros.</p><a href=\"/descobrir\">Voltar à busca</a>")
