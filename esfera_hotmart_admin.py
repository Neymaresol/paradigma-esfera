"""Read-only operator diagnostic page. No tokens in HTML or local storage."""
from html import escape
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response

router = APIRouter()

@router.get("/admin/hotmart-diagnostic", response_class=HTMLResponse)
def hotmart_diagnostic_page():
    return """<!doctype html><html lang="pt-BR"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ESFERA · Diagnóstico Hotmart</title>
<style>body{font:16px system-ui;background:#071226;color:#eff8ff;max-width:720px;margin:40px auto;padding:20px}
button{padding:14px;background:#67e8f9;color:#071226;border:0;border-radius:8px;font-weight:bold}
input{padding:12px;width:95%;background:#122941;color:white;border:1px solid #567}
pre{white-space:pre-wrap;overflow-wrap:anywhere}label{display:block;margin:20px 0 8px}</style>
<h1>Diagnóstico OAuth Hotmart · Staging</h1>
<p>Use somente um JWT de operador de curta duração emitido pelo mecanismo autorizado da ESFERA.
Não cole credenciais Hotmart. O JWT permanece apenas na memória desta página.</p>
<label for="jwt">JWT de operador</label><input id="jwt" type="password" autocomplete="off">
<p><button id="run" type="button">Testar autenticação Hotmart</button></p>
<pre id="result" role="status" aria-live="polite">Nenhum teste realizado.</pre>
<script src="/admin/hotmart-diagnostic.js" defer></script>\n<!--
document.getElementById('run').addEventListener('click', async () => {
 const field=document.getElementById('jwt'), token=field.value.trim(), out=document.getElementById('result');
 field.value='';
 if(!token){out.textContent='JWT de operador obrigatório.';return;}
 out.textContent='Verificando...';
 try {
   const response=await fetch('/api/integrations/hotmart/diagnostic',{
      method:'POST',headers:{'Authorization':'Bearer '+token},
      cache:'no-store',credentials:'omit'});
   const data=await response.json();
   if(!response.ok){out.textContent='Diagnóstico recusado (HTTP '+response.status+'). Verifique autorização do operador.';return;}
   const allowed=['status','credentials_present','staging_test_enabled','oauth_authenticated',
       'affiliate_authorization_verified','catalog_synchronized','publication_enabled'];
   out.textContent=allowed.map(k=>k+': '+String(data[k] ?? 'indisponível')).join('\\n');
 }catch(_){out.textContent='Não foi possível executar o diagnóstico.';}
});
--></html>"""

@router.get('/admin/hotmart-diagnostic.js')
def diagnostic_js():
    return Response(content=DIAGNOSTIC_JS,media_type='application/javascript',headers={'Cache-Control':'no-store'})

DIAGNOSTIC_JS = '''
document.getElementById('run').addEventListener('click', async () => {
 const field=document.getElementById('jwt'), token=field.value.trim(), out=document.getElementById('result');
 field.value='';
 if(!token){out.textContent='JWT de operador obrigatório.';return;}
 out.textContent='Verificando...';
 try {
  const response=await fetch('/api/integrations/hotmart/diagnostic',{method:'POST',headers:{Authorization:'Bearer '+token},cache:'no-store',credentials:'omit'});
  if(!response.ok){out.textContent='Diagnóstico recusado (HTTP '+response.status+').';return;}
  const data=await response.json();
  const allowed=['status','credentials_present','staging_test_enabled','oauth_authenticated','affiliate_authorization_verified','catalog_synchronized','publication_enabled'];
  out.textContent=allowed.map(k=>k+': '+String(data[k] ?? 'indisponível')).join('\\n');
 }catch(_){out.textContent='Não foi possível executar o diagnóstico.';}
});
'''
