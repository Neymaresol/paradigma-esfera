import os
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient
import esfera_ops
from app import app

client = TestClient(app)

def setup_function():
    tmp = tempfile.mkdtemp()
    esfera_ops.DB_PATH = Path(tmp) / 'ops.sqlite3'

def test_proposal_audit_persistence():
    payload = {'kind':'CAMPAIGN','product_id':'ia-basica','channel':'facebook','rationale':'Validar demanda por aulas básicas de IA'}
    r = client.post('/api/ops/proposals', json=payload)
    assert r.status_code == 201
    assert r.json()['status'] == 'REVIEW_REQUIRED'
    assert len(client.get('/api/ops/proposals').json()['items']) == 1
    assert client.get('/api/ops/audit').json()['items'][0]['event'] == 'PROPOSAL_CREATED'

def test_no_real_money_or_posting():
    d = client.get('/api/ops/dashboard').json()
    assert d['verified_sales'] is None
    assert d['posting_enabled'] is False
    assert d['payments_enabled'] is False
    assert d['auto_replication_enabled'] is False

def test_reject_invalid_channel():
    r = client.post('/api/ops/proposals', json={'kind':'CAMPAIGN','product_id':'ia-basica','channel':'spam','rationale':'Teste canal não autorizado'})
    assert r.status_code == 400

def test_reject_invalid_product():
    r = client.post('/api/ops/proposals', json={'kind':'CAMPAIGN','product_id':'missing','rationale':'Teste produto inexistente'})
    assert r.status_code == 404
