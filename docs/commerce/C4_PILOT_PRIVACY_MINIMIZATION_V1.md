# C4 Pilot Privacy Minimization V1

**状态：CURRENT / REQUIRED BEFORE HUMAN DECISION**  
**最后校准：2026-09-05**

## 1. Goal

Allow a small human-controlled pilot without turning the Commerce Runtime into a store of raw Xianyu customer data.

C4 is a real-user validation phase, but the existing boundary remains:

`real_customer=false`

This means the Runtime does not create persistent raw customer profiles or ingest direct buyer PII from Xianyu. A real human transaction may still be represented by a pseudonymous Pilot order controlled by Jovi.

## 2. Minimum Pilot data

Preferred fields:

- `pilot_order_id` generated internally;
- optional pseudonymous platform reference only when necessary;
- product / release / version;
- final listing candidate SHA;
- Jovi human publish confirmation;
- Jovi human payment confirmation fact;
- sanitized/local evidence reference if needed;
- Entitlement ID;
- DeliveryPackage SHA256;
- DeliveryReceipt ID;
- Jovi human delivery confirmation;
- support category/status;
- refund/dispute category/state;
- timestamps and internal audit IDs.

## 3. Platform reference: prefer random ID or keyed HMAC

Do **not** assume `SHA256(raw_username)` is strong anonymization. Public nicknames and short order references may be enumerable.

Preferred order:

1. If stable cross-order mapping is unnecessary, use only a random internal `pilot_order_id`.
2. If stable mapping is needed, use `HMAC(secret, normalized_platform_reference)`.
3. Keep the HMAC secret in local secret storage; never commit it to Git, reports, screenshots or chat.
4. Store only the HMAC output, not the original platform reference.

## 4. Do not ingest by default

- raw Xianyu Cookie / Token / Browser Profile;
- raw customer username/account identifier unless explicitly required;
- phone number;
- full shipping address;
- real name / government identity;
- full private chat transcript;
- payment credentials / bank/card data;
- unredacted screenshots with unrelated personal data;
- other customers' data visible in platform screenshots;
- external Xianyu SQLite contents.

## 5. Payment evidence

Payment remains human-confirmed by Jovi.

A C4 payment fact may contain only what is needed to bind the order:

- `pilot_order_id`;
- amount/currency snapshot when required;
- Jovi confirmation timestamp;
- sanitized/local-only transaction reference if required;
- human confirmer (`Jovi`);
- optional sanitized evidence artifact SHA.

It must never contain payment passwords, platform session secrets, bank credentials, card data, API keys or authentication tokens.

## 6. Screenshots / attachments

If a screenshot is truly needed:

1. Jovi or an authorized local process redacts unrelated personal data before Runtime ingestion;
2. retain the sanitized copy only;
3. bind SHA256;
4. record who sanitized/approved it;
5. keep raw screenshots outside public Git/evidence;
6. do not use screenshot availability as a reason to grant browser/platform automation.

## 7. Support records

Prefer structured categories rather than copying chat:

- environment;
- serial/interface;
- protocol/configuration;
- compatibility;
- documentation;
- delivery/version;
- refund/dispute;
- other/manual review.

Store a minimal issue summary only when necessary. Full buyer conversation requires a separate Human Decision and retention design.

## 8. Pilot ledger integrity

The real Pilot ledger must begin with **zero real rows**.

Synthetic/example rows must be isolated and labeled:

`EXAMPLE_ONLY / SYNTHETIC / DO_NOT_COUNT_AS_PILOT_EVIDENCE`

They must not contribute to:
- conversion;
- revenue;
- refund rate;
- support rate;
- commercial validation.

## 9. Retention

Before the first C4 order, Jovi should choose a minimal retention rule appropriate for the Pilot.

Until then:
- do not invent permanent retention promises;
- retain only what is needed for Pilot/audit/support;
- do not automatically accumulate raw attachments indefinitely;
- secrets/HMAC keys remain in local secret storage and are not evidence artifacts.

## 10. Platform boundary

All real platform actions remain human actions:

- publish;
- messaging/commitments;
- price changes;
- payment confirmation;
- final delivery/send;
- refunds/disputes.

No Cookie/Token/browser-profile access is authorized by C4.

## 11. Privacy stop conditions

Stop new Pilot processing and review immediately if:

- Runtime/Git receives raw buyer PII unexpectedly;
- Cookie/Token/Profile is found in evidence;
- unredacted chat/payment screenshots enter public artifacts;
- an HMAC/secret key is committed;
- automation starts collecting buyer fields that were not explicitly approved;
- a stored customer field cannot be justified as minimally necessary.

## 12. Future customer-data expansion

C4 PASS does **not** automatically permit `real_customer=true`.

Any future persistent customer identity/profile/CRM capability needs a new Jovi Human Decision covering:
- purpose;
- exact fields;
- source;
- retention/deletion;
- access control;
- export/subject handling if applicable;
- platform/legal basis;
- security controls.

## 13. Pilot acceptance

C4 evidence must prove both:

1. correct real-SKU order/payment-fact/Entitlement/Receipt/package workflow; and
2. data minimization / no unauthorized platform access.

A Pilot is not a PASS if it completes orders by weakening privacy or platform boundaries.
