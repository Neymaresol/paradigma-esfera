# ESFERA P0 — preflight / 2026-10-27 09:40 BRT

Baseline production and staging: 6c6d1d1d01d4e498f6146366c5ed132d978a10b7. No production changes, no merge, no deploy.

## Verified by source inspection
- `prototypes/werozinha-idle-v1.html`: six Werozinha assets, five-second idle cycle, pause control, AJAX fetch to `/api/discovery/topics`, carousel arrows with scrollBy, responsive mobile CSS.
- `esfera_discovery.py`: topics are informational, not commercial offers. `/api/discovery/offers` returns verified offers only.
- `app.py`: checkout and ads disabled; affiliate publication explicitly fail-closed; initial Hotmart URL registered but not publicly published.
- `hotmart_diagnostic.py`: protected, operator-triggered OAuth test restricted to staging, returns no credentials or tokens.
- Neon `esfera_staging` main: audit_rows=0, proposal_rows=0 at 2026-10-27T12:37:31Z. This does not prove production DB connectivity.

## P0 acceptance checklist (not yet executed in browser)
- [ ] Mobile and desktop: compare actual screenshot to approved Werozinha layout; image within central dark panel, not floating lower-right.
- [ ] All six /assets/werozinha-*.webp load with HTTP 200, correct MIME type, and no console errors.
- [ ] Idle gesture advances every 5 seconds; pauses when requested; clicking image opens chat; reduced-motion preference respected.
- [ ] GET /api/discovery/topics?q=ingles and empty query return expected cards; debounce and error state work; no cross-site requests.
- [ ] Left/right buttons scroll exactly one card; disabled at bounds; touch swipe and keyboard focus work.
- [ ] GET /api/catalog and /api/discovery/offers: differentiate illustrative courses from authorized commercial offers; no simulated commissions.
- [ ] GET /api/affiliate/readiness: publication_allowed remains false until independently verified attribution and partner permission.
- [ ] Operator-only staging Hotmart diagnostic after explicit operator login; inspect redacted OAuth status only. Do not expose tokens.
- [ ] Verify staging /health, /api/readiness, build logs, request errors and effective DB connection without printing secrets.
- [ ] Ensure production and staging remain on baseline commit; no branch promotion without approved tests.

## Proposed isolated P0 fixes
1. Add browser automation smoke tests (Playwright) with assertions on image loading, timed pose, arrow movement, AJAX, mobile viewport, and browser console errors.
2. Add API contract tests for catalog, discovery, readiness, and Hotmart fail-closed behavior.
3. Ensure staging-only test routes never alter real Hotmart data and never send outbound affiliate redirects before verified permission.
4. Resolve actual failures only after evidence is captured; do not replace approved homepage or disable existing carousel.

## Release gate
Do not merge, deploy, or claim sales readiness. Require green automated tests, screenshot review, health checks, verified affiliate authorization and attribution, and explicit production approval.
