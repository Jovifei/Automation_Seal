#!/usr/bin/env python3
from datetime import datetime, timedelta, timezone
from download_grant_policy import *

def expect(code, fn):
    try:
        fn()
    except GrantError as exc:
        assert code in str(exc), (code, exc)
    else:
        raise AssertionError(code)

now = datetime(2030, 1, 1, tzinfo=timezone.utc)
ent = Entitlement("ent_1", "order_1", "pkg_1")
tok = "synthetic-one-time-token"
g = DownloadGrant("grant_1", "ent_1", "order_1", "pkg_1", token_hash(tok), now + timedelta(minutes=5))
validate_grant(g, tok, ent, "order_1", "pkg_1", now)
expect("TOKEN_MISMATCH", lambda: validate_grant(g, "wrong", ent, "order_1", "pkg_1", now))
expect("ORDER_MISMATCH", lambda: validate_grant(g, tok, ent, "order_2", "pkg_1", now))
expect("EXPIRED", lambda: validate_grant(g, tok, ent, "order_1", "pkg_1", now + timedelta(minutes=6)))
rev = DownloadGrant("grant_1", "ent_1", "order_1", "pkg_1", token_hash(tok), now + timedelta(minutes=5), now)
expect("REVOKED", lambda: validate_grant(rev, tok, ent, "order_1", "pkg_1", now))
rev_ent = Entitlement("ent_1", "order_1", "pkg_1", now)
expect("ENTITLEMENT_REVOKED", lambda: validate_grant(g, tok, rev_ent, "order_1", "pkg_1", now))
print("C2_DOWNLOAD_GRANT_POLICY_TESTS_PASS")
