"""ESFERA four-cell organism topology, planning only; no live agents or money."""
CELL_ROLES = {
    "market": ("discover", "rank", "quality", "pricing", "regions", "compliance"),
    "affiliates": ("authorizations", "hotlinks", "catalog", "destination", "attribution", "audit"),
    "marketing": ("copy", "localization", "creatives", "channels", "review", "analytics"),
    "finance": ("events", "reconciliation", "commissions", "payouts", "risk", "reporting"),
}

def organism_plan():
    root = {"id":"esfera-central","parent_id":None,"role":"orchestrator",
            "status":"PLANNED","enabled":False}
    nodes = [root]
    links = []
    for index,(cell,agents) in enumerate(CELL_ROLES.items(),1):
        cell_id = f"cell-{index}-{cell}"
        nodes.append({"id":cell_id,"parent_id":root["id"],"role":cell,
                      "status":"PLANNED","enabled":False})
        links.append({"source":root["id"],"target":cell_id,"kind":"control"})
        for number,role in enumerate(agents,1):
            agent_id=f"{cell_id}-agent-{number}"
            nodes.append({"id":agent_id,"parent_id":cell_id,"role":role,
                          "status":"PLANNED","enabled":False})
            links.append({"source":cell_id,"target":agent_id,"kind":"task"})
    return {"nodes":nodes,"links":links,"total":len(nodes),
            "commercial_publication_allowed":False,
            "autonomous_spending_allowed":False,
            "verified_sales":None,"verified_commissions":None}
