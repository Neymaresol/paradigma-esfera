import io
import json
from urllib.error import URLError

import pytest

from hotmart_auth import HotmartAuthError, credentials_configured, request_access_token


ENV = {
    "HOTMART_CLIENT_ID": "test-id",
    "HOTMART_CLIENT_SECRET": "test-secret",
    "HOTMART_CLIENT_TOKEN": "Basic test-token",
}


class Response:
    def __init__(self, data):
        self.data = data

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self, limit):
        return json.dumps(self.data).encode()


def test_missing_credentials_fail_closed():
    assert not credentials_configured({})
    with pytest.raises(HotmartAuthError, match="not configured"):
        request_access_token({})


def test_success_with_injected_transport():
    calls = []

    def fake_open(req, timeout):
        calls.append((req, timeout))
        return Response({"access_token": "access-test"})

    assert request_access_token(ENV, opener=fake_open) == "access-test"
    assert len(calls) == 1
    assert calls[0][0].get_header("Authorization") == "Basic test-token"
    assert b"grant_type=client_credentials" in calls[0][0].data


def test_errors_never_expose_credentials():
    def fake_open(req, timeout):
        raise URLError("test-secret")

    with pytest.raises(HotmartAuthError) as exc:
        request_access_token(ENV, opener=fake_open)
    assert "test-secret" not in str(exc.value)


def test_malformed_response_rejected():
    with pytest.raises(HotmartAuthError, match="missing access token"):
        request_access_token(ENV, opener=lambda req, timeout: Response({}))
