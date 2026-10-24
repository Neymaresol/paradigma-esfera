import pytest
from esfera_cell_queue import topology, plan_task, assert_safe_task

def test_print_topology():
    nodes=topology()
    assert len(nodes)==29
    assert len({n["id"] for n in nodes})==29
    assert sum(n["parent_id"]=="esfera-central" for n in nodes)==4
    for cell in [n for n in nodes if n["parent_id"]=="esfera-central"]:
        assert sum(n["parent_id"]==cell["id"] for n in nodes)==6

@pytest.mark.parametrize("kind,cell",[
    ("RESEARCH","market"),("AFFILIATE_REVIEW","affiliates"),
    ("CAMPAIGN_DRAFT","marketing"),("FINANCIAL_RECONCILIATION","finance")
])
def test_task_routing_fail_closed(kind,cell):
    task=plan_task(kind,"lembrancinhas-flores-eva","request-12345678")
    assert task["target_cell"]==cell
    assert assert_safe_task(task)
    assert task["external_actions_enabled"] is False

@pytest.mark.parametrize("kind,slug,key",[
    ("POST_AD","offer-one","request-12345678"),
    ("RESEARCH","https://evil.example","request-12345678"),
    ("RESEARCH","offer-one","bad")
])
def test_reject_invalid(kind,slug,key):
    with pytest.raises(ValueError):
        plan_task(kind,slug,key)
