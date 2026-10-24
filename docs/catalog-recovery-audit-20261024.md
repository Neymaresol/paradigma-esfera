# Recuperação de catálogo e auditoria de persistência — 2026-10-24

Versão do relatório: 1.0 — data 2026-10-24; horário exato de geração não aferido.

## Fontes inspecionadas (somente leitura)
- GitHub: Neymaresol/paradigma-esfera e Neymaresol/wero1mercados (branch main).
- Render: serviços paradigma-esfera e wero1mercados; logs consultados.
- Neon: projetos paradigma-esfera-staging, wero1mercados-staging e wero1mercados-production (listagem de tabelas e contagens).

## Evidências
- wero1mercados-staging (Neon floral-hat-53843763): 19 linhas em products; 20 em offers; 0 em product_offers; 2 em partners. Contagens são registros, não validação de status, afiliação ou publicação.
- paradigma-esfera-staging (Neon broad-truth-51131093): 0 em esfera_proposals e 0 em esfera_audit.
- Projeto Neon denominado wero1mercados-production (long-tooth-35390946): consulta information_schema.tables não retornou tabelas públicas; isso NÃO identifica necessariamente o banco efetivo do Render.
- wero1mercados/catalog_discovery.py: normaliza candidatos, deduplica, contabiliza páginas e rejeitados, mas NÃO grava no banco nem publica ofertas.
- wero1mercados/docs/hotmart-tiktok-automation-20261021.md: documentação classifica automação como design/development only; nenhuma implantação comercial comprovada.
- paradigma-esfera/app.py: apenas um link Hotmart no registro AFFILIATE_OFFERS e publicação bloqueada por fail-closed.
- Logs Render examinados não forneceram evidência suficiente de uma análise persistida de exatamente 50 produtos.

## Resultado
**Não foi comprovada a existência de 50 produtos analisados e armazenados** nas fontes verificadas. Há 19 produtos e 20 ofertas no staging do Wero1Mercados, que devem ser preservados e reconciliados sem supor que sejam 39 produtos distintos.

## Preservação e próximas etapas
1. Não alterar produção, segredos, links ou banco sem snapshot e confirmação do banco efetivo.
2. Identificar DATABASE_URL efetivo por metadados seguros (sem exibir credenciais).
3. Fazer backup/snapshot e inventário de IDs, parceiros, status e URLs sem exposição de dados pessoais.
4. Buscar evidências dos 50 em branches, commits, exports, logs e banco efetivo.
5. Implementar importação incremental idempotente de fonte autorizada, com testes, double check e rollback.
6. Preservar visual original ESFERA e versão live 5e416594201b34d0ac27bad314c30dc248c8da00.

Este arquivo é um registro de auditoria versionado, NÃO um backup completo do banco e NÃO prova de 50 produtos.
