# ESFERA cell task queue — development plan
Version: 2026-10-24, America/Sao_Paulo.
Branch: dev/esfera-organism-task-queue-20261024.

## Scope
Recreates reference image topology: 1 root, 4 coordinator cells and 24 child agents.
Routes RESEARCH, AFFILIATE_REVIEW, CAMPAIGN_DRAFT and FINANCIAL_RECONCILIATION as review-required tasks. No task performs external calls, social posting, payments, scraping or live advertising.
Provides PostgreSQL schema for cell registry and task queue. Migration is not applied automatically.

## Next steps
1. Integrate this schema with Hotmart 50 PR #5 and Organism PR #7 after merge/rebase review.
2. Create isolated Neon staging branch, apply migration 003 there, verify foreign keys and idempotency.
3. Add operator-authenticated transactional enqueue API and auditable state transitions.
4. Add workers only after rate limiting, heartbeat, retry/dead-letter, scoped secrets, QA and permissions.
5. Verify Hotmart partner authorizations, product identity, click attribution and official commission reconciliation.
6. Double Check CI, staging smoke tests, canary and rollback before any production deploy.
All real sales/commission dashboard values remain unverified until official provider evidence.
