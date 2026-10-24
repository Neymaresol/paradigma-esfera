"""Protected ESFERA Hotmart connectivity diagnostic.

Never returns access tokens, credential values, raw provider errors or account data.
Staging-only execution is gated by explicit operator authorization and environment.
"""
import os
from hotmart_auth import credentials_configured, request_access_token, HotmartAuthError


def hotmart_diagnostic(env=None, token_request=request_access_token):
    env = os.environ if env is None else env
    configured = credentials_configured(env)
    allowed = env.get("ESFERA_HOTMART_STAGING_TEST_ENABLED", "").lower() == "true"
    production = env.get("RENDER_SERVICE_ID") == "srv-dbe1e3ks728c738rl4k0"
    result = {
        "service": "paradigma-esfera",
        "credentials_present": configured,
        "staging_test_enabled": allowed and not production,
        "oauth_authenticated": False,
        "affiliate_authorization_verified": False,
        "catalog_synchronized": False,
        "publication_enabled": False,
    }
    if not configured or not allowed or production:
        result["status"] = "BLOCKED"
        return result
    try:
        token = token_request(env=env)
        result["oauth_authenticated"] = bool(token)
        result["status"] = "AUTHENTICATED" if token else "FAILED"
    except (HotmartAuthError, Exception):
        result["status"] = "FAILED"
    return result
