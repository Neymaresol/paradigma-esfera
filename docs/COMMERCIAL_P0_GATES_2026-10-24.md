# ESFERA — Commercial P0 release gates
Date: 2026-10-24. Status: NO GO for commercial publication.

## Verified
- Production Render deployment LIVE, health endpoint previously returned HTTP 200.
- Affiliate storefront uses ESFERA_AFFILIATE_PUBLISH_ENABLED, default false.
- Single hard-coded Hotmart affiliate URL: https://go.hotmart.com/G108129576P.
- Checkout and advertising are disabled. Simulated orders are not real sales.
- Neon project paradigma-esfera-staging has proposal/audit/migration tables; this does not prove the production DATABASE_URL target.
- No confirmed payment/commission reconciliation or partner-side attribution evidence.

## Required release evidence
1. Partner account verifies authorization and ownership of affiliate link, offer eligibility and attribution terms.
2. Staging confirms outbound 302 destination only with authorized publication flag, otherwise 503; no artificial clicks.
3. Render production DATABASE_URL target verified safely by non-secret metadata and database fingerprint; do not disclose credentials.
4. Production logs, security headers, JWT access control, and operational health tested without modifying customer data.
5. Sales and commissions reported only from partner-confirmed records; never derive them from redirects or simulations.
6. Privacy, consent, anti-spam and campaign-platform permissions approved before publication.
7. Canary, rollback and operator sign-off documented.

Do not turn on publication, ads, payments, or automated expansion until every gate passes.
