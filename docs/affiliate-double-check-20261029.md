# ESFERA — Double Check de afiliados

Data: 2026-10-29, 14:47 BRT (horário da última implantação confirmada). Auditoria realizada após o deploy.

Produção auditada: commit `dd7dea22e71bc5112e57382fc3035167aa1dedbf`.
Backup de código: `backup/esfera-live-20261029-dd7dea22`.

## Constatações

| Parceiro | Destino configurado | Autorização oficial | Atribuição oficial | Liberação |
|---|---|---|---|---|
| Hotmart | Sim | Não comprovada nesta auditoria | Não comprovada | Bloqueada |
| Shopee | Sim | Não comprovada nesta auditoria | Não comprovada | Bloqueada |
| Mercado Livre | Sim | Não comprovada nesta auditoria | Não comprovada | Bloqueada |

O código `app.py` usa as variáveis `ESFERA_AFFILIATE_PUBLISH_ENABLED`, `ESFERA_AFFILIATE_PARTNER_VERIFIED` e `ESFERA_AFFILIATE_ATTRIBUTION_EVIDENCE_VERIFIED` como gates globais. A existência ou ativação desses flags não comprova evidência independente nem verificação individual de parceiro.

O módulo `esfera_partner_evidence.py` exige autorização, atribuição, referência de evidência e revisão para cada oferta, mas a vitrine atual ainda não consome essas provas individuais para publicação.

O documento `docs/affiliate-recovery-20261024.md` registra links Hotmart sem comprovação de aprovação ou atribuição. `esfera_partner_api.py` retorna catálogo verificado vazio e publicação desabilitada.

Render: deploy `dep-dbhocus9v7es73bffl80` live; logs de inicialização e health check 200. A consulta filtrada de logs de ofertas não trouxe registros; não é prova de zero visitas.

## Bloqueios P0 e liberação

1. Obter da conta oficial de cada parceiro a autorização vigente da oferta, URL exata e evidência de atribuição.
2. Guardar referência verificável e data da prova, sem segredos no GitHub.
3. Implementar gate individual por oferta baseado em `PartnerEvidence.eligible`, não apenas em flags globais.
4. Testar redirecionamentos autorizados e rejeição de URLs não autorizadas em staging.
5. Promover somente ofertas aprovadas com canary, health e rollback; reconciliar vendas/comissões apenas com dados do parceiro.

**Decisão desta auditoria:** nenhuma oferta comercial liberada sem comprovação. Nenhuma alteração de flags de produção, checkout ou publicidade.
