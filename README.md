# PARADIGMA ESFERA 1.0 — Loja de Microsserviços e Educação Digital

MVP de demonstração local. Não conectado a pagamentos, afiliados, publicidade ou produção.

## Iniciar

```bash
pip install -r requirements.txt
uvicorn app:app --reload
pytest -q
```

Acesse http://localhost:8000 para a vitrine, /docs para API e /health para segurança.

## Modelo
- 10 ofertas iniciais, preços sugeridos BRL (não validados por pesquisa de mercado).
- Catálogo preparado conceitualmente para BR, PT, ES, US; preços e idiomas internacionais ainda NÃO implementados.
- Pedidos simulados, sem cobrança nem comprovação financeira.
- Expansão celular, publicidade automática e integrações sociais DESABILITADAS.
- Antes de produção: banco persistente, autenticação, LGPD/GDPR, pagamentos reais via provedor autorizado, gestão de consentimento, antifraude, atendimento, direitos autorais dos cursos, avaliações pedagógicas, qualidade e Double Check.

## Referências de mercado
- World Economic Forum, Future of Jobs 2025.
- Comissão Europeia, DigComp 3.0 (2025).
- UNESCO, Global Education Monitoring Report 2026.

Versão: 1.0.0-dev, 2026-10-23 (data de referência do projeto).

## Motor celular 1.1.0-dev (2026-10-24 UTC)

- `GET /api/campaigns/drafts?channel=facebook`: 10 propostas de divulgação em rascunho; nenhuma publicação.
- `POST /api/expansion/evaluate`: simulação de gates pai/filhos (máximo 10 por pai).
- Nenhum dado enviado pelo cliente conta como venda verificada; endpoint nunca libera deploy.
- Faltam integrações autenticadas de pagamento, entrega, autorização de canais, persistência, auditoria e publicação.
- Divulgação pública deve esperar serviço entregue e checkout real aprovado.
