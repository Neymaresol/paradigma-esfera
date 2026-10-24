"""Fail-closed authentication helper for ESFERA development integration.

Not wired to endpoints yet: integrating requires an explicit code review.
Use a trusted identity provider and validated signed tokens before enabling.
"""
from dataclasses import dataclass
from enum import Enum


class Role(str, Enum):
    VIEWER = "viewer"
    OPERATOR = "operator"
    ADMIN = "admin"


@dataclass(frozen=True)
class Identity:
    subject: str
    role: Role
    authenticated: bool = False


class AccessDenied(PermissionError):
    pass


def require_role(identity: Identity | None, allowed: set[Role]) -> Identity:
    if identity is None or not identity.authenticated or not identity.subject:
        raise AccessDenied("Authentication required")
    if identity.role not in allowed:
        raise AccessDenied("Insufficient role")
    return identity


def external_actions_allowed(*, provider_verified: bool = False, owner_approved: bool = False) -> bool:
    # Deliberate P0 guard: no external actions in the development demo.
    return False
