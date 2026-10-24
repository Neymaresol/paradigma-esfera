# ESFERA — baseline de configuração e logística

Data: 2026-10-24. Horário exato desta revisão: não aferido.

## Baseline de produção (preservar)
- Repositório: Neymaresol/paradigma-esfera; branch: main
- Render workspace: tea-dao62kn40ujc73e210eg
- Render produção: srv-dbe1e3ks728c738rl4k0
- URL: https://paradigma-esfera.onrender.com
- Deploy live confirmado no Render: dep-dbehfgdg1s2s73fk3jhg
- Commit de produção: 5e416594201b34d0ac27bad314c30dc248c8da00
- Deploy concluído: 2026-10-24 20:41:32 UTC / 17:41:32 Brasília
- Homepage visual original: /; protótipo: /esfera; catálogo demonstrativo: /catalogo
- Rotas e lógica atuais: /health, /api/catalog, /api/readiness, /api/affiliate/readiness, /ofertas, /api/tags/channels, /api/ops/*
- Produção Render: autoDeploy desligado; deploy só após liberação explícita e gates.

## Fronteiras
- ESFERA é independente de Wero1Mercados. Não importar catálogo, banco, jobs ou credenciais de outro robô.
- Banco identificado: paradigma-esfera-staging no Neon (broad-truth-51131093), com tabelas esfera_proposals, esfera_audit e esfera_schema_migrations; conexão efetiva da produção ainda não identificada.
- Hotmart: quatro links históricos preservados em docs/affiliate-recovery-20261024.md. Não presumir autorização ou atribuição.

## Gate para Go Live de multiplicação
1. Snapshot/backup real e validação do banco efetivo.
2. Conector autorizado Hotmart e sincronização incremental idempotente em banco exclusivo ESFERA.
3. Testes unitários + integração + staging, prova de origem e atribuição, publicação legalmente autorizada.
4. Canary/health e rollback para commit de produção acima.
5. Monitoramento separado de saúde operacional e valores financeiros confirmados.

## Estado da revisão
Baseline de produção preservado. Código novo de sincronização em PR de desenvolvimento, não implantado. Publicação automática, vendas e comissões não confirmadas. Este manifesto NÃO substitui snapshot do banco ou export de variáveis seguras.
