# ESFERA P0 remediation — 2026-10-24

Status: DEVELOPMENT ONLY; NO-GO for commercial production.

## P0-1 Auth & security
- Require server-validated authentication and role-based authorization for all /api/ops/*, /api/orders/* and expansion/campaign endpoints.
- Do not trust caller-supplied verified_sales, budget, health or approval flags as authorization evidence.
- Restrict CORS, add rate limiting, security headers, request size limits, audit redaction and structured logs.
- Disable or gate API documentation and interactive endpoints on public production.
- Never store secrets in source control. Test 401/403, role boundaries, replay and abuse scenarios.

## P0-2 PostgreSQL
- Provision an isolated ESFERA Neon staging database after approval; do not reuse another robot's database.
- Add versioned schema migrations, least-privilege DB roles, transactional proposals/audit and health probes.
- Enforce DATABASE_URL in non-test environments, no SQLite fallback in production.
- Test migrations, restore, connection failures and concurrency. Never log credentials.

## P0-3 Financial & marketing controls
- Keep checkout, transfers, advertising, auto-provisioning and auto-replication disabled.
- Future payments require provider contracts, signed webhooks, idempotency, reconciliation and verified ledger.
- Future marketing requires channel authorization, approvals, compliant assets and budgets.

## P0-4 Release gates
- Unit, integration, authorization, security and load tests in CI.
- Dedicated staging branch/environment, no automatic deploy from main until verified.
- Double Check: deploy commit SHA, /health, /api/readiness, logs, migrations, access control and rollback.
- Production only via separately approved PR, canary and health confirmation.

## Findings
Current public Render production exposes a development demonstration with unauthenticated simulation and operations endpoints. This is a confirmed P0. The code declares version 1.3.0-dev and mode simulation. The staging service tracks main, not this development branch.

No production changes authorized.
