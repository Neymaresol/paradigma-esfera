"""Deterministic task routing for ESFERA cells. No network or execution side effects."""
from datetime import datetime, timezone
from uuid import uuid4

CELL_AGENTS = {
    "market": ("discover","rank","quality","pricing","regions","compliance"),
    "affiliates": ("authorizations","hotlinks","catalog","destination","attribution","audit"),
    "marketing": ("copy","localization","creatives","channels","review","analytics"),
    "finance": ("events","reconciliation","commissions","payouts","risk","reporting"),
}
ALLOWED_KINDS = {
    "RESEARCH": "market", "AFFILIATE_REVIEW": "affiliates",
    "CAMPAIGN_DRAFT": "marketing", "FINANCIAL_RECONCILIATION": "finance",
}

def topology():
    nodes = [{"id":"esfera-central","parent_id":None,"role":"orchestrator","status":"PLANNED"}]
    for index,(cell,agents) in enumerate(CELL_AGENTS.items(),1):
        cid=f"cell-{index}-{cell}"
        nodes.append({"id":cid,"parent_id":"esfera-central","role":cell,"status":"PLANNED"})
        for number,role in enumerate(agents,1):
            nodes.append({"id":f"{cid}-agent-{number}","parent_id":cid,
                          "role":role,"status":"PLANNED"})
    return nodes

def plan_task(kind, offer_slug, idempotency_key):
    if kind not in ALLOWED_KINDS:
        raise ValueError("Unsupported task kind")
    import re
    if not isinstance(offer_slug,str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",offer_slug) or len(offer_slug)>80:
        raise ValueError("Invalid offer slug")
    if not isinstance(idempotency_key,str) or not re.fullmatch(r"[A-Za-z0-9_-]{8,100}",idempotency_key):
        raise ValueError("Invalid idempotency key")
    cell = ALLOWED_KINDS[kind]
    return {"id":str(uuid4()),"kind":kind,"offer_slug":offer_slug,
            "idempotency_key":idempotency_key,"target_cell":cell,
            "status":"REVIEW_REQUIRED","external_actions_enabled":False,
            "created_at":datetime.now(timezone.utc).isoformat()}

def assert_safe_task(task):
    return (task.get("status")=="REVIEW_REQUIRED"
            and task.get("external_actions_enabled") is False
            and task.get("kind") in ALLOWED_KINDS)
