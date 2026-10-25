"""Public discovery assets for the ESFERA global web app.
No affiliate offers or sales claims are activated by this module.
"""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response
from xml.sax.saxutils import escape as xml_escape

router = APIRouter()
PUBLIC_ORIGIN = "https://paradigma-esfera.onrender.com"

@router.get("/manifest.webmanifest")
def manifest():
    import json
    data = {"name":"PARADIGMA ESFERA","short_name":"ESFERA","description":"Educação, tecnologia e serviços digitais","lang":"pt-BR","start_url":"/catalogo","scope":"/","display":"standalone","background_color":"#050b1b","theme_color":"#071226","icons":[{"src":"/esfera-icon.svg","sizes":"any","type":"image/svg+xml","purpose":"any maskable"}]}
    return Response(content=json.dumps(data,ensure_ascii=False),media_type="application/manifest+json",headers={"Cache-Control":"public, max-age=3600"})

@router.get("/esfera-icon.svg")
def icon():
    return Response(content='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" rx="108" fill="#071226"/><circle cx="256" cy="256" r="175" fill="none" stroke="#49baff" stroke-width="22"/><circle cx="256" cy="256" r="112" fill="none" stroke="#eac27c" stroke-width="15"/><path d="M256 120l42 102 94 34-94 34-42 102-42-102-94-34 94-34z" fill="#66dfff"/></svg>''',media_type="image/svg+xml")

@router.get("/robots.txt")
def robots():
    return Response(content="User-agent: *\nAllow: /catalogo\nDisallow: /admin/\nDisallow: /api/\nSitemap: "+PUBLIC_ORIGIN+"/sitemap.xml\n",media_type="text/plain")

@router.get("/sitemap.xml")
def sitemap():
    return Response(content='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+xml_escape(PUBLIC_ORIGIN)+'/catalogo</loc></url></urlset>',media_type="application/xml")

@router.get("/esfera-app",response_class=HTMLResponse)
def app_landing():
    return '''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#071226"><meta name="description" content="PARADIGMA ESFERA: educação, tecnologia e serviços digitais."><link rel="manifest" href="/manifest.webmanifest"><link rel="icon" href="/esfera-icon.svg"><title>ESFERA — Descubra novas possibilidades</title><style>body{font:16px system-ui;background:radial-gradient(circle at 70% 0%,#164b85,#071226 60%);color:#f1f8ff;min-height:100vh;margin:0}main{max-width:960px;margin:auto;padding:80px 24px}h1{font-size:clamp(38px,7vw,76px);line-height:1.1}em{font-style:normal;color:#eac27c}p{color:#c3d6ea;line-height:1.8;max-width:660px}a{display:inline-block;margin:10px 12px 10px 0;padding:15px 20px;border-radius:12px;background:#69cfff;color:#071226;font-weight:700;text-decoration:none}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin-top:50px}article{border:1px solid #355b83;border-radius:14px;padding:22px;background:#0c2141}</style></head><body><main><div>✦ PARADIGMA ESFERA · GLOBAL</div><h1>O futuro é inteligente.<br><em>O alcance é global.</em></h1><p>Explore educação, tecnologia, serviços e novas oportunidades em uma experiência feita para celular, tablet e computador.</p><a href="/catalogo">Explorar cursos e serviços ↗</a><section><article>🎓<h2>Educação</h2><p>Conhecimento para evoluir.</p></article><article>⚙️<h2>Serviços</h2><p>Soluções digitais.</p></article><article>🌐<h2>Comércio</h2><p>Ofertas e parceiros sujeitos à validação.</p></article><article>✨<h2>Expansão</h2><p>Conexões sem fronteiras.</p></article></section><p>Versão inicial de divulgação. Instalação depende do suporte do navegador; vendas e comissões são confirmadas pelos provedores.</p></main></body></html>'''
