"""Search-first discovery for the PARADIGMA ESFERA catalog.

No synthetic prices, unverified checkout links, or simulated sales are shown.
"""
import re
import unicodedata
from html import escape
from urllib.parse import quote
from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse

router = APIRouter()
TOPICS = [
    {"slug":"inteligencia-artificial","title":"Inteligência Artificial","keywords":["ia","inteligencia artificial","automacao","chatbot","tecnologia"],"summary":"Descubra temas e formações em inteligência artificial e automação."},
    {"slug":"marketing-digital","title":"Marketing Digital","keywords":["marketing","vendas","publicidade","empreendedorismo","negocios"],"summary":"Explore marketing, conteúdo e fundamentos de vendas digitais."},
    {"slug":"planilhas-produtividade","title":"Planilhas e Produtividade","keywords":["excel","planilhas","trabalho","produtividade","office"],"summary":"Conheça assuntos relacionados a planilhas e organização do trabalho."},
    {"slug":"seguranca-digital","title":"Segurança Digital","keywords":["seguranca","privacidade","internet","dados","ciberseguranca"],"summary":"Aprenda conceitos de proteção de contas, privacidade e navegação segura."},
    {"slug":"carreira-profissional","title":"Carreira Profissional","keywords":["curriculo","emprego","profissao","carreira","entrevista"],"summary":"Encontre temas de desenvolvimento profissional e preparação de currículo."},
]
def norm(s):
    return "".join(c for c in unicodedata.normalize("NFKD",s.lower()) if not unicodedata.combining(c))
def matches(query,topic):
    q=norm(query).strip()
    if not q:return True
    hay=norm(" ".join([topic["title"],topic["summary"],*topic["keywords"]]))
    return all(word in hay for word in re.findall(r"[\w]+",q)[:8])
def shell(title,description,body):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow"><meta name="description" content="{escape(description,quote=True)}"><title>{escape(title)} | PARADIGMA ESFERA</title><style>body{{background:radial-gradient(ellipse at 50% 20%,#103a76 0%,#04152f 42%,#010714 90%);color:#eef8ff;font:16px system-ui;margin:0;min-height:100vh}}main{{max-width:1100px;margin:auto;padding:50px 22px}}h1{{font-size:clamp(35px,5vw,62px);color:#ffd17a;text-shadow:0 0 18px #bd751f}}p{{color:#b6cce3;line-height:1.7}}a{{color:#7ddaff}}a:hover{{color:#ffd17a}}form{{display:flex;gap:8px;flex-wrap:wrap;margin:25px 0}}input{{padding:15px;background:#102b4b;border:1px solid #47739e;border-radius:10px;color:white;min-width:220px;flex:1}}button{{padding:15px 22px;border:0;border-radius:10px;background:linear-gradient(135deg,#ffe4a1,#d6a54e);color:#061229;font-weight:700}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px}}article{{padding:23px;background:linear-gradient(145deg,#071d49,#020d23);border:2px solid #168dff;border-radius:20px;box-shadow:0 0 22px #0877ed70,inset 0 0 20px #03509b60}}small{{color:#92abc5}}nav{{padding:20px;border-bottom:1px solid #315c83;box-shadow:0 0 22px #0877ed40}}nav a{{color:#ffd17a;text-decoration:none;font-weight:800;letter-spacing:.08em}}.note{{padding:15px;border-left:3px solid #edc57c}}</style></head><body><nav><a href="/">♛ PARADIGMA ESFERA · IA CENTRAL</a> &nbsp; <a href="/descobrir">Explorar interesses</a></nav><main>{body}</main></body></html>"""
@router.get("/api/discovery/topics")
def topics(q: str=Query("",max_length=120)):
    return {"query":q,"results":[{"slug":t["slug"],"title":t["title"],"summary":t["summary"],"url":"/interesses/"+t["slug"]} for t in TOPICS if matches(q,t)],"commerce_status":"no_verified_offers"}
@router.get("/descobrir",response_class=HTMLResponse)
def discover(q: str=Query("",max_length=120)):
    results=[t for t in TOPICS if matches(q,t)]
    cards="".join('<article><h2>'+escape(t["title"])+'</h2><p>'+escape(t["summary"])+'</p><a href="/interesses/'+t["slug"]+'">Explorar tema ↗</a></article>' for t in results)
    if not cards:cards="<p>Nenhum tema encontrado. Experimente outra palavra-chave.</p>"
    body='<small>EDUCAÇÃO · TECNOLOGIA · OPORTUNIDADES</small><h1>O que você quer aprender hoje?</h1><p>Pesquise por assunto e encontre uma trilha de conhecimento.</p><form action="/descobrir" method="get"><input name="q" maxlength="120" aria-label="Pesquisar interesses" placeholder="Ex.: inteligência artificial" value="'+escape(q,quote=True)+'"><button type="submit">Pesquisar</button></form><div class="grid">'+cards+'</div><p class="note">Conteúdo informativo. Ofertas e pagamentos só serão apresentados após autorização e verificação dos parceiros.</p>'
    return shell("Descubra seus interesses","Explore temas de educação, tecnologia e carreira.",body)
@router.get("/interesses/{slug}",response_class=HTMLResponse)
def interest(slug:str):
    from fastapi import HTTPException
    t=next((t for t in TOPICS if t["slug"]==slug),None)
    if not t:raise HTTPException(404,"Tema não encontrado")
    body='<small>TRILHAS DE CONHECIMENTO</small><h1>'+escape(t["title"])+'</h1><p>'+escape(t["summary"])+'</p><p>Explore conceitos, compare formações e escolha opções adequadas ao seu objetivo.</p><p class="note">Ainda não há ofertas comerciais verificadas para este tema. Nenhuma compra é processada nesta página.</p><a href="/descobrir">← Explorar outros interesses</a>'
    return shell(t["title"],t["summary"],body)
