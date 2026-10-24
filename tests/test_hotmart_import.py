import pytest
from esfera_hotmart import validate_batch, validate_hotlink, eligible_for_publication

def offer(n):
    return {"slug": f"offer-{n}", "title": f"Produto {n}",
            "hotlink": f"https://go.hotmart.com/A{100000000+n:09d}J"}

def test_accept_fifty_and_fail_closed():
    rows = validate_batch([offer(i) for i in range(50)])
    assert len(rows) == 50
    assert all(not eligible_for_publication(x, True) for x in rows)

def test_reject_fifty_one():
    with pytest.raises(ValueError):
        validate_batch([offer(i) for i in range(51)])

@pytest.mark.parametrize("link", [
    "http://go.hotmart.com/A107958015J",
    "https://evil.example/A107958015J",
    "https://go.hotmart.com.evil.example/A107958015J",
    "https://go.hotmart.com/A107958015J?redirect=evil",
    "https://go.hotmart.com/A107958015J#frag",
    "https://go.hotmart.com/../A107958015J",
])
def test_reject_unsafe_links(link):
    with pytest.raises(ValueError):
        validate_hotlink(link)

def test_duplicate_rejected():
    with pytest.raises(ValueError):
        validate_batch([offer(1), offer(1)])

def test_approval_requires_all_gates():
    row = validate_batch([offer(1)])[0]
    row.update(status="APPROVED", partner_verified=True,
               link_destination_verified=True, attribution_verified=True,
               publish_enabled=True)
    assert eligible_for_publication(row, False) is False
    assert eligible_for_publication(row, True) is True
