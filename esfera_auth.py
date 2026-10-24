"""ESFERA authentication: signed JWTs from a configured issuer, fail closed."""
import os
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer = HTTPBearer(auto_error=False)
def require_operator(credentials: HTTPAuthorizationCredentials | None = Security(bearer)):
    secret = os.getenv("ESFERA_JWT_SECRET", "")
    issuer = os.getenv("ESFERA_JWT_ISSUER", "paradigma-esfera")
    audience = os.getenv("ESFERA_JWT_AUDIENCE", "esfera-admin")
    if not credentials or credentials.scheme.lower() != "bearer" or len(secret) < 32:
        raise HTTPException(status_code=401, detail="Authentication required", headers={"WWW-Authenticate":"Bearer"})
    try:
        claims = jwt.decode(credentials.credentials, secret, algorithms=["HS256"], issuer=issuer, audience=audience, options={"require":["exp","iat","iss","aud","sub"]}, leeway=15)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate":"Bearer"})
    if claims.get("role") not in ("operator", "admin"):
        raise HTTPException(status_code=403, detail="Insufficient role")
    return {"sub": claims["sub"], "role": claims["role"]}
