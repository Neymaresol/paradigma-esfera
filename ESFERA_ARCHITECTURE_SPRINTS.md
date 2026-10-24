# PARADIGMA ESFERA FINANCEIRA 1.0 — Arquitetura e sprints
Atualizado em 2026-10-24 (horário de Brasília; horário exato de gravação não registrado).
Referência visual: diagrama fornecido pelo proprietário em 24/10/2026.

## Núcleo de IA
A IA central orquestra quatro frentes: (1) Educação, (2) Serviços, (3) Comércio e (4) Expansão. Componentes transversais: monitoramento, PostgreSQL, melhoria contínua, Double Check e multiplicação. Agentes geram propostas; publicação, compras, pagamentos e replicação são bloqueados por padrão e dependem de autorização verificável e testes.

## Estratégia receita primeiro
Começar com UMA oferta de afiliação autorizada e um link de atribuição verificado; publicação orgânica somente em canais permitidos. Medir visitantes, cliques legítimos, conversões reportadas pelo parceiro, comissões confirmadas e valores efetivamente recebidos. Nunca confundir simulações, cliques ou deploy LIVE com vendas.

## Multiplicação 1 → 10 → 100 → 1000
1: validar operação comercial e primeira atribuição real.
10: replicar campanhas/ofertas aprovadas, com limite de canais e revisão.
100: escalar apenas com indicadores confiáveis de conversão, margem, custos e incidentes.
1000: células internacionais com autorizações locais, isolamento, rate limits, orçamento e rollback.
Nenhuma etapa garante volume de vendas ou retorno financeiro.

## Sprints de entrega (meta de planejamento: 72h; não garantia)
- S01 0–12h: conexão Neon staging/Render, migrations, backup e health. Aceite: leitura/gravação real comprovada.
- S02 12–24h: autenticação, testes negativos, logs, segurança, rollback. Aceite: P0 zerados.
- S03 24–36h: uma oferta afiliada autorizada, link e destino verificados. Aceite: redirecionamento correto sem cliques artificiais.
- S04 36–48h: vitrine, métricas e conciliação. Aceite: distinguir cliques, vendas e comissões confirmadas.
- S05 48–60h: revisão legal e comercial, homologação, decisão GO/NO-GO. Aceite: evidências auditáveis.
- S06 60–72h: publicação controlada e monitoramento. Aceite: canary, health, rollback, aprovação.
Em caso de bloqueio P0, parar publicação e preservar produção.

## Status verificado
Render produção LIVE em commit 23995d7 (versão antiga); staging LIVE em c0a952b (segurança). Código atual informa NOT_READY_FOR_SALES, checkout e publicidade automática desativados. Banco Neon staging criado e migração 001 aplicada; conexão protegida Render↔Neon ainda não comprovada. Sem vendas ou comissões reais verificadas.

## Indicadores do dashboard
Versão de produção, data/hora e health no topo; estado por robô/célula; ofertas autorizadas; cliques reais; vendas e comissões somente com confirmação da plataforma; saldos e repasses somente com confirmação financeira; falhas, gates, canary e rollback.
