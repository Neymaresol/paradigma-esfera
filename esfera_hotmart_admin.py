"""Staging diagnostic interface. Password is sent only to the ESFERA backend;
JWT stays in JS memory for the single diagnostic request."""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response

router=APIRouter()

@router.get("/admin/hotmart-diagnostic",response_class=HTMLResponse)
def diagnostic_page():
    return """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ESFERA · Diagnóstico Hotmart</title>
<style>body{font:16px system-ui;background:#071226;color:#eff8ff;max-width:720px;margin:40px auto;padding:20px}
button{padding:14px;background:#67e8f9;color:#071226;border:0;border-radius:8px;font-weight:bold}
input{padding:12px;width:95%;background:#122941;color:white;border:1px solid #567}
pre{white-space:pre-wrap;overflow-wrap:anywhere}label{display:block;margin:20px 0 8px}</style></head>
<body><h1>Diagnóstico OAuth Hotmart · Staging</h1>
<p>Informe somente a senha de operador ESFERA configurada de forma segura no Render.
Não use credenciais Hotmart. Nenhum JWT precisa ser copiado.</p>
<label for="password">Senha administrativa ESFERA</label>
<input id="password" type="password" autocomplete="off" maxlength="256">
<p><button id="run" type="button">Autenticar e testar Hotmart</button></p>
<pre id="result" role="status" aria-live="polite">Nenhum teste realizado.</pre>
<script src="/admin/hotmart-diagnostic.js" defer></script></body></html>"""

@router.get("/admin/hotmart-diagnostic.js")
def diagnostic_js():
    return Response(content=JS,media_type="application/javascript",headers={"Cache-Control":"no-store"})

JS = r"""
document.getElementById('run').addEventListener('click', async () => {
 const field=document.getElementById('password'), out=document.getElementById('result');
 const password=field.value; field.value='';
 if(!password){out.textContent='Senha administrativa obrigatória.';return;}
 out.textContent='Autenticando operador...';
 try {
  const login=await fetch('/api/operator/login',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({password}),cache:'no-store',credentials:'omit'});
  if(!login.ok){out.textContent=login.status===403?'Login administrativo desabilitado.':
    login.status===429?'Muitas tentativas. Aguarde 15 minutos.':
    login.status===503?'Login ainda não configurado.':'Autenticação recusada (HTTP '+login.status+').';return;}
  const {access_token}=await login.json();
  if(!access_token){out.textContent='Resposta de login inválida.';return;}
  const response=await fetch('/api/integrations/hotmart/diagnostic',{method:'POST',
    headers:{Authorization:'Bearer '+access_token},cache:'no-store',credentials:'omit'});
  if(!response.ok){out.textContent='Diagnóstico recusado (HTTP '+response.status+').';return;}
  const data=await response.json();
  const allowed=['status','credentials_present','staging_test_enabled','oauth_authenticated',
    'affiliate_authorization_verified','catalog_synchronized','publication_enabled'];
  out.textContent=allowed.map(k=>k+': '+String(data[k] ?? 'indisponível')).join('\n');
 }catch(_){out.textContent='Não foi possível executar o diagnóstico.';}
});
"""
