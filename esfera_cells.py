"""Bounded, fail-closed hierarchical cell planner; no deployments or sales."""
from collections import deque

MAX_CELLS = 63
MAX_DEPTH = 5
FANOUT = 2

def plan_cells(total=15):
    if not isinstance(total, int) or isinstance(total, bool) or not 1 <= total <= MAX_CELLS:
        raise ValueError("total must be between 1 and 63")
    cells = [{"id":"esfera-root","parent_id":None,"depth":0,"role":"CONTROL",
              "status":"PLANNED","deploy_allowed":False,"ads_allowed":False}]
    queue = deque([cells[0]])
    while len(cells) < total:
        if not queue:
            raise ValueError("capacity exceeded")
        parent = queue.popleft()
        if parent["depth"] >= MAX_DEPTH:
            continue
        for child_number in (1,2):
            if len(cells) >= total:
                break
            child = {"id":f'{parent["id"]}-{child_number}',
                     "parent_id":parent["id"],"depth":parent["depth"]+1,
                     "role":"WORKER","status":"PLANNED",
                     "deploy_allowed":False,"ads_allowed":False}
            cells.append(child)
            queue.append(child)
    return {"cells":cells,"total":len(cells),"max_depth":MAX_DEPTH,
            "fanout":FANOUT,"deploy_allowed":False,"ads_allowed":False,
            "financial_claims_allowed":False}

def check_tree(cells):
    ids = {c["id"] for c in cells}
    if len(ids) != len(cells) or len(cells) > MAX_CELLS:
        return False
    roots = [c for c in cells if c["parent_id"] is None]
    if len(roots) != 1:
        return False
    for cell in cells:
        if cell["depth"] > MAX_DEPTH or cell["status"] != "PLANNED":
            return False
        if cell["parent_id"] is not None:
            parents = [p for p in cells if p["id"] == cell["parent_id"]]
            if len(parents) != 1 or parents[0]["depth"]+1 != cell["depth"]:
                return False
            if sum(x["parent_id"] == cell["parent_id"] for x in cells) > FANOUT:
                return False
    return True
