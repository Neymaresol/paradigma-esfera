from fastapi.testclient import TestClient
from app import app
from esfera_engine import Gate, expansion_decision

client = TestClient(app)

def test_expansion_fail_closed():
    assert expansion_decision(Gate())['decision'] == 'BLOCKED'

def test_expansion_never_deploys():
    data = {'verified_sales': 10, 'verified_margin_brl': 200, 'fulfilled_orders': 10,
            'unresolved_incidents': 0, 'approved_budget_brl': 100,
            'platform_authorized': True, 'owner_approved': True, 'health_ok': True}
    result = client.post('/api/expansion/evaluate', json=data).json()
    assert result['deployment_allowed'] is False
    assert result['evidence_verified_by_server'] is False

def test_drafts_never_publish():
    data = client.get('/api/campaigns/drafts?channel=facebook').json()
    assert len(data['campaigns']) == 10
    assert data['publication_enabled'] is False
    assert all(x['status'] == 'DRAFT_REVIEW_REQUIRED' for x in data['campaigns'])

def test_unknown_channel_blocked():
    assert client.get('/api/campaigns/drafts?channel=spam').status_code == 400

def test_child_limit():
    assert 'CHILD_LIMIT' in expansion_decision(Gate(), 11)['failures']
