"""Hotmart OAuth client for ESFERA. No secrets or tokens are logged or persisted.

Production use requires validated scopes and a separate server-side authorization
check before any affiliate link is published.
"""
import base64
import json
import os
from urllib import error, parse, request

TOKEN_URL = "https://api-sec-vlc.hotmart.com/security/oauth/token"


class HotmartAuthError(RuntimeError):
    pass


def credentials_configured(env=None):
    env = os.environ if env is None else env
    return all(bool(env.get(k, "").strip()) for k in (
        "HOTMART_CLIENT_ID", "HOTMART_CLIENT_SECRET", "HOTMART_CLIENT_TOKEN"))


def request_access_token(env=None, opener=None, timeout=10):
    """Obtain an OAuth token using server-side secrets; never return secrets in errors."""
    env = os.environ if env is None else env
    if not credentials_configured(env):
        raise HotmartAuthError("Hotmart credentials are not configured")
    client_id = env["HOTMART_CLIENT_ID"].strip()
    client_secret = env["HOTMART_CLIENT_SECRET"].strip()
    client_token = env["HOTMART_CLIENT_TOKEN"].strip()
    # Hotmart's Basic client token is used as supplied by the credential portal.
    if not client_token.startswith("Basic "):
        raise HotmartAuthError("Invalid client token format")
    payload = parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode("ascii")
    req = request.Request(TOKEN_URL, data=payload, method="POST", headers={
        "Authorization": client_token,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    })
    opener = opener or request.urlopen
    try:
        with opener(req, timeout=timeout) as response:
            data = json.loads(response.read(32768))
    except (error.HTTPError, error.URLError, TimeoutError, ValueError, OSError):
        raise HotmartAuthError("Hotmart OAuth request failed") from None
    if not isinstance(data, dict) or not isinstance(data.get("access_token"), str) or not data["access_token"]:
        raise HotmartAuthError("Hotmart OAuth response missing access token")
    return data["access_token"]
