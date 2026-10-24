import os
import time
import jwt
import pytest
os.environ["ESFERA_JWT_SECRET"] = "test-only-secret-for-esfera-32-chars-minimum-000"
@pytest.fixture
def auth_headers():
    now = int(time.time())
    token = jwt.encode({"sub":"test-operator","role":"operator","iat":now,"exp":now+300,"iss":"paradigma-esfera","aud":"esfera-admin"}, os.environ["ESFERA_JWT_SECRET"], algorithm="HS256")
    return {"Authorization":f"Bearer {token}"}
