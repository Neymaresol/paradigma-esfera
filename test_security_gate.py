import pytest
from security_gate import Identity, Role, AccessDenied, require_role, external_actions_allowed


@pytest.mark.parametrize("identity", [None, Identity("admin", Role.ADMIN, False), Identity("", Role.ADMIN, True)])
def test_unauthenticated_denied(identity):
    with pytest.raises(AccessDenied):
        require_role(identity, {Role.ADMIN})


def test_viewer_cannot_admin():
    with pytest.raises(AccessDenied):
        require_role(Identity("user", Role.VIEWER, True), {Role.ADMIN})


def test_authenticated_admin():
    identity = Identity("admin", Role.ADMIN, True)
    assert require_role(identity, {Role.ADMIN}) == identity


def test_external_actions_fail_closed():
    assert external_actions_allowed(provider_verified=True, owner_approved=True) is False
