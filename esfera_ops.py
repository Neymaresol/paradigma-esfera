"""Local, non-financial audit trail and approval queue for PARADIGMA ESFERA.
No external effects: no payment, social publication, deploy or infrastructure spending.
"""
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

DB_PATH = Path(os.environ.get('ESFERA_DB_PATH', '/tmp/paradigma_esfera_dev.sqlite3'))

def connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute('CREATE TABLE IF NOT EXISTS audit (id TEXT PRIMARY KEY, at TEXT NOT NULL, event TEXT NOT NULL, payload TEXT NOT NULL)')
    db.execute('CREATE TABLE IF NOT EXISTS proposals (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, type TEXT NOT NULL, status TEXT NOT NULL, payload TEXT NOT NULL)')
    db.commit()
    return db

def record(event, payload):
    data = {'id': str(uuid4()), 'at': datetime.now(timezone.utc).isoformat(), 'event': event, 'payload': payload}
    with connection() as db:
        db.execute('INSERT INTO audit VALUES (?,?,?,?)', (data['id'], data['at'], event, json.dumps(payload, ensure_ascii=False)))
    return data

def propose(kind, payload):
    if kind not in ('CAMPAIGN', 'CELL_EXPANSION', 'INFRA_UPGRADE', 'COURSE'):
        raise ValueError('Invalid proposal type')
    data = {'id': str(uuid4()), 'created_at': datetime.now(timezone.utc).isoformat(), 'type': kind, 'status': 'REVIEW_REQUIRED', 'payload': payload}
    with connection() as db:
        db.execute('INSERT INTO proposals VALUES (?,?,?,?,?)', (data['id'], data['created_at'], kind, data['status'], json.dumps(payload, ensure_ascii=False)))
    record('PROPOSAL_CREATED', {'proposal_id': data['id'], 'type': kind})
    return data

def proposals():
    with connection() as db:
        rows = db.execute('SELECT * FROM proposals ORDER BY created_at DESC LIMIT 100').fetchall()
    return [{**dict(row), 'payload': json.loads(row['payload'])} for row in rows]

def audit():
    with connection() as db:
        rows = db.execute('SELECT * FROM audit ORDER BY at DESC LIMIT 100').fetchall()
    return [{**dict(row), 'payload': json.loads(row['payload'])} for row in rows]
