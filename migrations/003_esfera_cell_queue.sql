-- Staging-only manual migration. No automatic execution.
CREATE TABLE IF NOT EXISTS esfera_cells (
  id VARCHAR(100) PRIMARY KEY,
  parent_id VARCHAR(100) REFERENCES esfera_cells(id),
  role VARCHAR(60) NOT NULL,
  status VARCHAR(24) NOT NULL DEFAULT 'PLANNED' CHECK (status IN ('PLANNED','DISABLED','READY','RUNNING','ERROR')),
  enabled BOOLEAN NOT NULL DEFAULT FALSE,
  last_heartbeat TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS esfera_cell_tasks (
  id UUID PRIMARY KEY,
  idempotency_key VARCHAR(100) NOT NULL UNIQUE,
  offer_slug VARCHAR(80) NOT NULL,
  kind VARCHAR(40) NOT NULL CHECK (kind IN ('RESEARCH','AFFILIATE_REVIEW','CAMPAIGN_DRAFT','FINANCIAL_RECONCILIATION')),
  target_cell VARCHAR(30) NOT NULL,
  status VARCHAR(24) NOT NULL DEFAULT 'REVIEW_REQUIRED' CHECK (status IN ('REVIEW_REQUIRED','APPROVED','RUNNING','SUCCEEDED','FAILED','CANCELLED')),
  external_actions_enabled BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_esfera_cell_tasks_status ON esfera_cell_tasks(status,created_at);
