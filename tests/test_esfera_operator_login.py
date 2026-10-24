import base64
import hashlib
import os
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_login_disabled_by_default(monkeypatch):
    monkeypatch.delenv("ESFERA_OPERATOR_LOGIN_ENABLED", raising=False)
    assert client.post("/api/operator/login", json={"password":"dummy"}).status_code == 403

def test_login_refuses_missing_verifier(monkeypatch):
    monkeypatch.setenv("RENDER_SERVICE_ID","srv-dbe16ejrjlhs738mgokg")
    monkeypatch.setenv("ESFERA_OPERATOR_LOGIN_ENABLED","true")
    monkeypatch.setenv("ESFERA_JWT_SECRET","s"*40)
    monkeypatch.delenv("ESFERA_OPERATOR_PASSWORD_SCRYPT",raising=False)
    assert client.post("/api/operator/login",json={"password":"dummy"}).status_code == 503

def test_login_issues_short_lived_token_only_for_valid_password(monkeypatch):
    import jwt
    password="test-only-password"
    salt=b"0123456789abcdef"
    verifier=base64.b64encode(salt+hashlib.scrypt(password.encode(),salt=salt,n=2**14,r=8,p=1,dklen=32)).decode()
    monkeypatch.setenv("RENDER_SERVICE_ID","srv-dbe16ejrjlhs738mgokg")
    monkeypatch.setenv("ESFERA_OPERATOR_LOGIN_ENABLED","true")
    monkeypatch.setenv("ESFERA_JWT_SECRET","s"*40)
    monkeypatch.setenv("ESFERA_OPERATOR_PASSWORD_SCRYPT",verifier)
    assert client.post("/api/operator/login",json={"password":"wrong"}).status_code == 401
    response=client.post("/api/operator/login",json={"password":password})
    assert response.status_code == 200
    token=response.json()["access_token"]
    claims=jwt.decode(token,"s"*40,algorithms=["HS256"],audience="esfera-admin",issuer="paradigma-esfera")
    assert claims["role"]=="operator"
    assert claims["exp"]-claims["iat"]==300
