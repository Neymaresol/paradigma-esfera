# ESFERA — Hierarquia de células
Version date: 2026-10-24 (Brasília). Branch: dev/esfera-cell-tree-20261024.

## Design
One parent controller, binary fanout of two worker children per node, maximum 5 levels below root and 63 total nodes. Planning is deterministic, without background jobs or external side effects. 50 nodes are supported as a plan; this does not mean 50 live workers, Hotmart authorizations, products or sales.

## Separation of responsibilities
Root: configuration, audit, Double Check, rollout/rollback approvals, consolidated operational and financial dashboard.
Level 1: product categories/regions. Level 2: approved affiliate offers. Level 3+: campaign drafts, localization, analytics, QA.
Parent-child IDs are explicit. Each worker must have a unique identity, quota, idempotent task ID, lease, heartbeat, rate limits, retries, dead-letter queue and human-approved publishing permissions before execution.
No chain referral compensation, recruiting, artificial traffic, self-purchases, or fabricated sales.

## Gates
- Every node starts PLANNED, deploy_allowed=false, ads_allowed=false.
- Separate partner authorization, link/destination validation, attribution evidence, campaign permissions, data privacy, financial reconciliation and owner approval.
- Start with 3 verified offer candidates, stage up to 10/25/50 only after measured safe outcomes.
- No financial totals without official Hotmart reconciliation. Parent aggregates confirmed numbers without double-counting child transactions.
- Production unchanged; no deploy or advertisements performed.

## Next implementation
Authenticated DB-backed cell registry, foreign keys, unique parent-child relations, task queue, worker heartbeats, audit and observability. Integrate with the Hotmart 50 import branch after both PRs pass review. CI tests and staging-only canary before production.
