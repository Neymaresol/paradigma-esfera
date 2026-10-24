from esfera_organism import organism_plan

def test_exact_print_topology():
    plan=organism_plan()
    assert plan["total"] == 29
    assert len(plan["links"]) == 28
    assert sum(n["parent_id"]=="esfera-central" for n in plan["nodes"]) == 4
    for cell in (n for n in plan["nodes"] if n["parent_id"]=="esfera-central"):
        assert sum(n["parent_id"]==cell["id"] for n in plan["nodes"]) == 6
    assert len({n["id"] for n in plan["nodes"]}) == 29

def test_fail_closed():
    plan=organism_plan()
    assert all(not n["enabled"] for n in plan["nodes"])
    assert plan["commercial_publication_allowed"] is False
    assert plan["autonomous_spending_allowed"] is False
    assert plan["verified_sales"] is None
    assert plan["verified_commissions"] is None
