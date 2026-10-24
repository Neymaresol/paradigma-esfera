from hotmart_diagnostic import hotmart_diagnostic

def test_blocked_without_credentials():
    result = hotmart_diagnostic({})
    assert result["status"] == "BLOCKED"
    assert not result["oauth_authenticated"]

def test_staging_can_validate_without_leaking_token():
    env = {
        "HOTMART_CLIENT_ID": "example",
        "HOTMART_CLIENT_SECRET": "private",
        "HOTMART_CLIENT_TOKEN": "Basic private",
        "ESFERA_HOTMART_STAGING_TEST_ENABLED": "true",
        "RENDER_SERVICE_ID": "srv-staging",
    }
    result = hotmart_diagnostic(env, token_request=lambda env: "sensitive-token")
    assert result["status"] == "AUTHENTICATED"
    assert result["oauth_authenticated"]
    assert "sensitive-token" not in str(result)
    assert "private" not in str(result)
    assert not result["publication_enabled"]

def test_production_is_blocked_even_if_enabled():
    env = {
        "HOTMART_CLIENT_ID": "example",
        "HOTMART_CLIENT_SECRET": "private",
        "HOTMART_CLIENT_TOKEN": "Basic private",
        "ESFERA_HOTMART_STAGING_TEST_ENABLED": "true",
        "RENDER_SERVICE_ID": "srv-dbe1e3ks728c738rl4k0",
    }
    result = hotmart_diagnostic(env, token_request=lambda env: "token")
    assert result["status"] == "BLOCKED"
