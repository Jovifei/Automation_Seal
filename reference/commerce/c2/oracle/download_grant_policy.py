#!/usr/bin/env python3
"""Pure reference policy for C2 DownloadGrant separation."""
from __future__ import annotations
import hashlib, hmac
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

class GrantError(ValueError):
    pass

def token_hash(token: str) -> str:
    if not token:
        raise GrantError("EMPTY_GRANT_TOKEN")
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

@dataclass(frozen=True)
class Entitlement:
    entitlement_id: str
    order_id: str
    package_id: str
    revoked_at: Optional[datetime] = None

@dataclass(frozen=True)
class DownloadGrant:
    grant_id: str
    entitlement_id: str
    order_id: str
    package_id: str
    token_hash: str
    expires_at: datetime
    revoked_at: Optional[datetime] = None
    synthetic_only: bool = True

def assert_can_issue(entitlement: Entitlement, package_id: str) -> None:
    if entitlement.revoked_at is not None:
        raise GrantError("ENTITLEMENT_REVOKED")
    if entitlement.package_id != package_id:
        raise GrantError("ENTITLEMENT_PACKAGE_MISMATCH")

def validate_grant(grant: DownloadGrant, token: str, entitlement: Entitlement,
                   order_id: str, package_id: str, now: datetime) -> None:
    if not grant.synthetic_only:
        raise GrantError("SYNTHETIC_GRANT_REQUIRED")
    if grant.revoked_at is not None:
        raise GrantError("DOWNLOAD_GRANT_REVOKED")
    if entitlement.revoked_at is not None:
        raise GrantError("ENTITLEMENT_REVOKED")
    if now.tzinfo is None:
        raise GrantError("AWARE_DATETIME_REQUIRED")
    if now >= grant.expires_at:
        raise GrantError("DOWNLOAD_GRANT_EXPIRED")
    if grant.entitlement_id != entitlement.entitlement_id:
        raise GrantError("DOWNLOAD_GRANT_ENTITLEMENT_MISMATCH")
    if grant.order_id != order_id or entitlement.order_id != order_id:
        raise GrantError("DOWNLOAD_GRANT_ORDER_MISMATCH")
    if grant.package_id != package_id or entitlement.package_id != package_id:
        raise GrantError("DOWNLOAD_GRANT_PACKAGE_MISMATCH")
    actual = token_hash(token)
    if not hmac.compare_digest(actual, grant.token_hash):
        raise GrantError("DOWNLOAD_GRANT_TOKEN_MISMATCH")
