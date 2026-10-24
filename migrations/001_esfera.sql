-- ESFERA isolated PostgreSQL schema; apply manually to a dedicated staging database first.
BEGIN;
CREATE TABLE IF NOT EXISTS esfera_schema_migrations(version integer PRIMARY KEY, applied_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS esfera_proposals(
  id uuid PRIMARY KEY, created_at timestamptz NOT NULL DEFAULT now(),
  type text NOT NULL CHECK(type IN ('CAMPAIGN','CELL_EXPANSION','INFRA_UPGRADE','COURSE')),
  status text NOT NULL DEFAULT 'REVIEW_REQUIRED', payload jsonb NOT NULL
);
CREATE TABLE IF NOT EXISTS esfera_audit(
  id uuid PRIMARY KEY, at timestamptz NOT NULL DEFAULT now(),
  event text NOT NULL, payload jsonb NOT NULL
);
CREATE INDEX IF NOT EXISTS esfera_proposals_created_idx ON esfera_proposals(created_at DESC);
CREATE INDEX IF NOT EXISTS esfera_audit_at_idx ON esfera_audit(at DESC);
INSERT INTO esfera_schema_migrations(version) VALUES (1) ON CONFLICT DO NOTHING;
COMMIT;
