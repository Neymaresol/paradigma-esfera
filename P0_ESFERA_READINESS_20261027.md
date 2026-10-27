# P0 ESFERA — readiness verification (2026-10-27)

Scope: development branch only. No production deploy, no payment enablement, no automatic posting.

## Existing verified code gates
- `GET /health`: simulation, checkout disabled, live ads disabled.
- `GET /api/readiness`: NOT_READY_FOR_SALES.
- `GET /api/affiliate/readiness`: attribution and reconciliation false.
- Affiliate redirect deliberately fails closed until independent partner attribution evidence exists.
- Homepage `/` uses Werozinha prototype; `/ajax` and `/visual-oficial` are separate previews.

## Staging acceptance checklist
1. Use dedicated Neon staging database and protected secrets. Never reuse production credentials.
2. Run `pytest -q`; capture failure output and commit SHA.
3. Probe `/health`, `/api/readiness`, `/api/catalog`, `/api/affiliate/readiness`, `/`, `/ajax`, `/visual-oficial`.
4. Verify Werozinha images load; idle transitions, AJAX carousel, both arrows, swipe and mobile viewport work without regressions.
5. Verify anonymous operator routes return 401, invalid role 403, and audit events redact secrets.
6. Check affiliate link ID against approved partner evidence; no redirects until attribution is independently validated.
7. Record simulated visit/click/order only in staging and label SIMULATED_ONLY. No fabricated provider sales or commissions.
8. Review Render logs for HTTP 4xx/5xx and unexpected restarts; verify rollback and backups.
9. Produce a dated go/no-go report. Never merge or deploy to production without separate approval.

## Known blockers
- Affiliate publication hard-disabled pending independent attribution verification.
- No verified financial source, commission reconciliation, or checkout integration.
- Staging service currently follows main; this branch does not deploy automatically to staging.
