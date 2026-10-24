"""Staging-only operator login, fail-closed and short lived.
Configure ESFERA_OPERATOR_PASSWORD_SCRYPT as base64(salt[16] + hashlib.scrypt(password,
salt=salt, n=2**14, r=8, p=1, dklen=32)). Never store plaintext passwords.
"""
import base64
import hashlib
import hmac
import os
import time
import threading
from collections import defaultdict, deque
import jwt
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

router = APIRouter()
_attempts = defaultdict(deque)
_attempt_lock = threading.Lock()

def _rate_limit(key, now):
    # Per-instance defense in depth; enforce distributed rate limits at the edge too.
    with _attempt_lock:
        hits = _attempts[key]
        while hits and hits[0] <= now - 900:
            hits.popleft()
        if len(hits) >= 5:
            raise HTTPException(429, 'Too many attempts')
        hits.append(now)

class LoginRequest(BaseModel):
    password: str = Field(min_length=1, max_length=256)

@router.post("/api/operator/login")
def operator_login(body: LoginRequest, request: Request):
    # No public login in production. External rate limiting is REQUIRED before enabling.
    if os.getenv("RENDER_SERVICE_ID") != "srv-dbe16ejrjlhs738mgokg" or os.getenv("ESFERA_OPERATOR_LOGIN_ENABLED") != "true":
        raise HTTPException(403, "Operator login disabled")
    _rate_limit(request.client.host if request.client else 'unknown', time.monotonic())
    secret = os.getenv("ESFERA_JWT_SECRET", "")
    verifier = os.getenv("ESFERA_OPERATOR_PASSWORD_SCRYPT", "")
    if len(secret) < 32 or not verifier:
        raise HTTPException(503, "Operator login not configured")
    try:
        blob = base64.b64decode(verifier, validate=True)
        if len(blob) != 48:
            raise ValueError("Invalid verifier")
        derived = hashlib.scrypt(body.password.encode(), salt=blob[:16], n=2**14, r=8, p=1, dklen=32)
        valid = hmac.compare_digest(derived, blob[16:])
    except (ValueError, TypeError):
        raise HTTPException(503, "Operator login not configured") from None
    if not valid:
        raise HTTPException(401, "Invalid credentials")
    now = int(time.time())
    token = jwt.encode({"sub":"staging-operator","role":"operator","iss":os.getenv("ESFERA_JWT_ISSUER","paradigma-esfera"),
        "aud":os.getenv("ESFERA_JWT_AUDIENCE","esfera-admin"),"iat":now,"exp":now+300},secret,algorithm="HS256")
    return {"access_token":token,"token_type":"bearer","expires_in":300}
