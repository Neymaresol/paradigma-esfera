from esfera_affiliate_sync import validate_course, reconcile

def valid():
    return {"provider":"hotmart","provider_product_id":"123","title":"Curso de Inglês",
            "affiliate_url":"https://go.hotmart.com/G108129576P",
            "affiliate_authorized":True,"attribution_verified":True}

def test_verified_course_is_accepted():
    assert validate_course(valid())["title"]=="Curso de Inglês"

def test_unverified_course_is_rejected():
    item=valid()
    item["attribution_verified"]=False
    assert validate_course(item) is None

def test_external_redirect_is_rejected():
    item=valid()
    item["affiliate_url"]="https://evil.example/redirect"
    assert validate_course(item) is None

def test_reconciliation_is_idempotent():
    first=reconcile({},[valid()])
    second=reconcile(first["catalog"],[valid()])
    assert first["accepted"]==1
    assert second["accepted"]==0
