-- Apply in a controlled staging migration only; never auto-run in production.
CREATE TABLE IF NOT EXISTS esfera_hotmart_offers (
  slug VARCHAR(80) PRIMARY KEY,
  title VARCHAR(160) NOT NULL,
  hotlink TEXT NOT NULL UNIQUE,
  status VARCHAR(20) NOT NULL DEFAULT 'PENDING_REVIEW'
    CHECK (status IN ('PENDING_REVIEW','APPROVED','REJECTED','DISABLED')),
  partner_verified BOOLEAN NOT NULL DEFAULT FALSE,
  link_destination_verified BOOLEAN NOT NULL DEFAULT FALSE,
  attribution_verified BOOLEAN NOT NULL DEFAULT FALSE,
  publish_enabled BOOLEAN NOT NULL DEFAULT FALSE,
  source VARCHAR(40) NOT NULL DEFAULT 'operator_import',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_esfera_hotmart_offers_status ON esfera_hotmart_offers(status);
