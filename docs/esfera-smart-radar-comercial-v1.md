# ESFERA SMART — Célula Radar Comercial v1
Versão: 0.1.0-staging
Registro: 2026-10-28 19:30 BRT (planejamento inicial; confirmar timestamp no commit)
Status: especificação em branch de desenvolvimento; não implantada.

## Objetivo
Antecipar oportunidades de consumo ligadas a eventos futuros, lançamentos, tendências públicas e interesses declarados. Conectar vitrines de produtos e serviços a parceiros autorizados. Não pressupor acesso a pesquisas privadas, público identificado ou dados de compradores de ingressos.

## Fluxo
1. Ingerir fontes públicas/oficiais licenciadas (evento, tipo, artista/equipe, cidade, país, data, URL, verificado_em).
2. Normalizar, deduplicar e descartar eventos sem fonte ou data confirmada.
3. Classificar interesses: rock/pop rock/K-pop/sertanejo/funk, futebol/futsal/basquete/tênis/natação/automobilismo, tecnologia e outros.
4. Mapear categorias comerciais: vestuário, calçados, maquiagem, cosméticos, perfumes, acessórios, celulares, eletrônicos, cursos e serviços.
5. Buscar ofertas de afiliados com URL individual, autorização, região, disponibilidade e rastreamento válidos.
6. Criar campanhas candidatas em janelas configuráveis (60/30/15 dias), com revisão de marcas, licenças, direitos e políticas das plataformas.
7. Publicar somente em canais aprovados e conectados, mediante controles de consentimento e limites de frequência.
8. Registrar impressões, visitas e cliques sem confundir com vendas; reconciliar vendas e comissões exclusivamente com dados oficiais do parceiro.
9. Monitorar saúde, anomalias e qualidade, com Double Check, rollback e nenhuma alteração automática de produção.

## Modelo de dados mínimo
Event(id, source_url, verified_at, starts_at, location, category, entity, status)
Interest(id, category, locale, declared_or_aggregate)
Offer(id, partner, product_url, affiliate_url, authorized, region, checked_at, status)
Campaign(id, event_id_nullable, offer_ids, locale, scheduled_at, approval, channel, status)
Click(id, campaign_id, offer_id, timestamp, anonymous_attribution)
Commission(id, partner_reference, value, currency, verified_at, status)

## Primeira fatia executável (pendente)
- Endpoint read-only /api/radar/opportunities com fontes reais, paginação e estado vazio honesto.
- Endpoint /api/radar/campaigns/preview sem publicação, com recomendações explicáveis.
- Testes de deduplicação, fontes inválidas, links não autorizados e comissões não confirmadas.
- Painel separado para simulação, cliques e comissões confirmadas.
- Integração gradual com Wero1Mercados e UI ESFERA SMART, preservando AJAX, setas e Werozinha.

## Critérios para Go Live
P0 security e testes aprovados; staging healthy; links de afiliados autorizados; fonte real de eventos; verificação visual mobile/desktop; aprovação da publicação; rollback definido. Não alegar vendas, indexação ou campanhas externas sem comprovação.
