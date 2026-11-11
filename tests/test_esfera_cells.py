import pytest
from esfera_cells import plan_cells, check_tree

@pytest.mark.parametrize("count", [1,3,7,15,31,50,63])
def test_valid_bounded_tree(count):
    result=plan_cells(count)
    assert result["total"] == count
    assert check_tree(result["cells"])
    assert all(not x["deploy_allowed"] and not x["ads_allowed"] for x in result["cells"])

@pytest.mark.parametrize("count", [0,64,-1,True,1.5])
def test_invalid_size(count):
    with pytest.raises(ValueError):
        plan_cells(count)

def test_no_financial_claims():
    result=plan_cells(50)
    assert result["financial_claims_allowed"] is False
