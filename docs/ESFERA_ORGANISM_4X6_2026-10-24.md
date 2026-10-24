# ESFERA — Organismo digital 4 × 6
Version date: 2026-10-24 (Brasília). Branch: dev/esfera-organism-4x6-20261024.

Based on the user-supplied reference diagram: 1 central orchestrator, 4 primary cells, each with 6 specialized agents (29 planned components).

Market: discovery, ranking, quality, pricing, regions, compliance.
Affiliates: authorizations, HotLinks, catalog, destination, attribution, audit.
Marketing: copy, localization, creatives, channels, review, analytics.
Finance: provider events, reconciliation, commissions, payouts, risk, reporting.

Task flow: Central -> market research -> affiliate approval -> marketing drafts -> compliant publishing review -> provider click/sale attribution -> finance reconciliation -> central dashboard. Cross-cell communication must use a durable, auditable queue with idempotency and quotas. No automatic propagation of unverified data, no artificial clicks, no chain recruitment payments.

Safety: all nodes PLANNED/disabled. Production, marketing, bank transfers, ad spending and revenue claims remain off. Each real integration requires credentials, partner permission, tests, rate limits, approval and rollback. This topology is not a running 24/7 agent system.

Next: implement persistent cell registry, task dispatch/ack, health/heartbeats, dashboard, authenticated operator controls, staging smoke tests and integration with Hotmart 50 PR #5.
