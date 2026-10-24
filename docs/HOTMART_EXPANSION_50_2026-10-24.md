# PARADIGMA ESFERA — Hotmart 50 expansion
Date: 2026-10-24 (America/Sao_Paulo). Development branch: dev/hotmart-50-import-20261024.

## Scope and architecture
1. Up to 50 affiliate offers per operator-controlled batch, with unique slugs and HotLinks.
2. Source must be account-authorized HotLinks; marketplace recommendations are not proof of affiliation.
3. The parser validates HTTPS, exact go.hotmart.com host, path shape, duplicates and batch size. This is syntactic validation only, not proof of ownership, destination safety, authorization or attribution.
4. Import into PostgreSQL table esfera_hotmart_offers after migration review, using parameterized upsert, transaction, operator JWT and audit trail. Import endpoint must never mark offers approved. **Importer persistence endpoint not implemented in this PR.**
5. Individual release gates: partner verified, link destination verified, attribution verified, explicit publish approval, plus global publish switch. Default all FALSE.
6. Check the Hotmart official account and partner authorization manually or through a documented, permitted API. Do not scrape or bypass approval.
7. Redirect validation in isolated staging without generating artificial affiliate clicks or sales. Confirm destination and product identity through account evidence and approved test methods.
8. Do not assert sales, commissions, balances or transfers until independently reconciled with official provider records.
9. Draft campaigns by niche/language only; no social posting, bulk email, ads spend or automatic replication without platform permissions and operator review.
10. Rollout 3 verified candidate offers -> 10 -> 25 -> 50, with CI, database migration tests, staging smoke tests, canary, health and rollback.
11. Monitor per-offer health, status, attribution evidence, verified sales/commissions and incidents. Financial numbers remain NULL if source unconnected.
12. Never use staging database as evidence of effective production database.

## Current evidence and limits
Three HotLinks and product names were supplied and matched by the account owner in chat: G108129576P (Lembrancinhas e Flores em E.V.A), A107958015J (Leadlovers), J107828590U (Viva Sempre com Dinheiro). Screenshot shows confirmed affiliations but does not establish per-link attribution. PR #4 is separately preparing three static offers.
This PR adds validation, schema and tests; it does not import records, run migrations, change deployment, connect Hotmart APIs, or publish campaigns.

## Release gates
P0: CI tests pass; schema reviewed/migrated in staging; importer with audit, operator auth, idempotency and transaction; HotLinks and products verified; no unsafe redirects; approved API permissions; attribution evidence; production DB mapping verified; consent/compliance review; operator sign-off.
GO only after all P0 gates are green; deploy behind disabled flags, smoke test, canary, rollback.
