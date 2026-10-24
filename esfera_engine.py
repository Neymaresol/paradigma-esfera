"""PARADIGMA: fail-closed cellular expansion and marketing planning.
No posting, payment, provisioning, or external side effects.
"""
from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class Gate:
    verified_sales: int = 0
    verified_margin_brl: float = 0
    fulfilled_orders: int = 0
    unresolved_incidents: int = 0
    approved_budget_brl: float = 0
    platform_authorized: bool = False
    owner_approved: bool = False
    health_ok: bool = False


def expansion_decision(gate: Gate, proposed_children: int = 10) -> dict:
    failures = []
    if not 1 <= proposed_children <= 10: failures.append('CHILD_LIMIT')
    if gate.verified_sales < 3: failures.append('INSUFFICIENT_VERIFIED_SALES')
    if gate.fulfilled_orders < 3: failures.append('UNVERIFIED_FULFILLMENT')
    if gate.verified_margin_brl <= 0: failures.append('NON_POSITIVE_MARGIN')
    if gate.unresolved_incidents: failures.append('UNRESOLVED_INCIDENTS')
    if gate.approved_budget_brl <= 0: failures.append('NO_APPROVED_BUDGET')
    if not gate.platform_authorized: failures.append('CHANNEL_NOT_AUTHORIZED')
    if not gate.owner_approved: failures.append('OWNER_APPROVAL_REQUIRED')
    if not gate.health_ok: failures.append('HEALTH_CHECK_FAILED')
    return {'decision': 'ELIGIBLE_FOR_STAGING_REVIEW' if not failures else 'BLOCKED',
            'failures': failures, 'requested_children': proposed_children,
            'production_changes': False}


def campaign_plan(product: dict, channel: Literal['facebook','instagram','tiktok','search']='facebook') -> dict:
    if not product.get('id') or not product.get('name'):
        raise ValueError('Product must have id and name')
    name = product['name']
    return {'product_id': product['id'], 'channel': channel, 'status': 'DRAFT_REVIEW_REQUIRED',
            'text': f'Quer aprender mais sobre {name}? Estamos preparando uma solução digital acessível. Acompanhe as novidades da PARADIGMA ESFERA. Em breve.',
            'publication_authorized': False, 'campaign_budget_brl': 0,
            'landing_page_ready': False, 'claims_verified': False}
