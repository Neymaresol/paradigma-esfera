"""ESFERA proposal/audit storage. No financial or external actions."""
import json
import os
import sqlite3
from pathlib import Path
from uuid import uuid4
from datetime import datetime, timezone

KINDS = ('CAMPAIGN', 'CELL_EXPANSION', 'INFRA_UPGRADE', 'COURSE')
def backend():
    if os.getenv('DATABASE_URL'):
        return 'postgres'
    if os.getenv('ESFERA_ENV', 'development') not in ('development', 'test'):
        raise RuntimeError('DATABASE_URL is mandatory outside development')
    return 'sqlite'

def connection():
    if backend() == 'postgres':
        import psycopg
        return psycopg.connect(os.environ['DATABASE_URL'])
    path = Path(os.environ.get('ESFERA_DB_PATH', '/tmp/paradigma_esfera_dev.sqlite3'))
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute('CREATE TABLE IF NOT EXISTS audit (id TEXT PRIMARY KEY, at TEXT NOT NULL, event TEXT NOT NULL, payload TEXT NOT NULL)')
    db.execute('CREATE TABLE IF NOT EXISTS proposals (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, type TEXT NOT NULL, status TEXT NOT NULL, payload TEXT NOT NULL)')
    db.commit()
    return db

def _insert(table, values):
    pg = backend() == 'postgres'
    table = ('esfera_' if pg else '') + table
    placeholders = ','.join(['%s' if pg else '?'] * len(values))
    with connection() as db:
        db.execute(f'INSERT INTO {table} VALUES ({placeholders})', values)

def record(event, payload):
    data = {'id': str(uuid4()), 'at': datetime.now(timezone.utc).isoformat(), 'event': event, 'payload': payload}
    _insert('audit', (data['id'], data['at'], event, json.dumps(payload, ensure_ascii=False)))
    return data

def propose(kind, payload):
    if kind not in KINDS:
        raise ValueError('Invalid proposal type')
    data = {'id': str(uuid4()), 'created_at': datetime.now(timezone.utc).isoformat(), 'type': kind, 'status': 'REVIEW_REQUIRED', 'payload': payload}
    _insert('proposals', (data['id'], data['created_at'], kind, data['status'], json.dumps(payload, ensure_ascii=False)))
    record('PROPOSAL_CREATED', {'proposal_id': data['id'], 'type': kind})
    return data

def _read(table, timecol):
    pg = backend() == 'postgres'
    table = ('esfera_' if pg else '') + table
    with connection() as db:
        rows = db.execute(f'SELECT * FROM {table} ORDER BY {timecol} DESC LIMIT 100').fetchall()
        if pg:
            cols = [x.name for x in db.execute(f'SELECT * FROM {table} LIMIT 0').description]
            data = [dict(zip(cols, row)) for row in rows]
        else:
            data = [dict(row) for row in rows]
    for row in data:
        if isinstance(row['payload'], str):
            row['payload'] = json.loads(row['payload'])
    return data

def proposals():
    return _read('proposals', 'created_at')

def audit():
    return _read('audit', 'at')
