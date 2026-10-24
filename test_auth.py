from fastapi.testclient import TestClient
from app import app
import jwt, os, time
client = TestClient(app)
PRIVATE = [("/api/ops/proposals","get"),("/api/ops/audit","get"),("/api/ops/dashboard","get"),("/api/campaigns/drafts","get"),("/api/expansion/evaluate","post"),("/api/orders/simulate","post")]
def test_private_endpoints_require_auth():
    for path, method in PRIVATE:
        assert getattr(client,method)(path).status_code == 401
def test_viewer_denied():
    now=int(time.time())
    token=jwt.encode({"sub":"viewer","role":"viewer","iat":now,"exp":now+100,"iss":"paradigma-esfera","aud":"esfera-admin"},os.environ["ESFERA_JWT_SECRET"],algorithm="HS256")
    assert client.get("/api/ops/dashboard",headers={"Authorization":"Bearer "+token}).status_code==403
def test_bad_signature_denied():
    assert client.get("/api/ops/dashboard",headers={"Authorization":"Bearer invalid"}).status_code==401
def test_no_public_docs():
    assert client.get("/docs").status_code==404
def test_security_headers():
    r=client.get("/health")
    assert r.headers["x-content-type-options"]=="nosniff"
    assert r.headers["x-frame-options"]=="DENY"
