# ESFERA staging Double Check (24 Oct 2026)
1. Use dedicated Neon staging DB; never share Wero1Mercados or Operario databases.
2. Set ESFERA_JWT_SECRET (>=32 random chars), issuer, audience, DATABASE_URL as protected staging secrets.
3. Deploy dev/p0-security-postgres-20261024 to isolated staging service. Current staging tracks main; DO NOT change main or production.
4. Verify unauthenticated /api/ops/* and /api/orders/* return 401; signed operator JWT succeeds; viewer 403; expired token 401.
5. Run pytest, migration and rollback drill, backup restore, logs, /health and /api/readiness.
6. Verify payments, publication, replication and infrastructure purchases remain OFF.
7. Canary and approval required for production. NO-GO until all checks documented.
