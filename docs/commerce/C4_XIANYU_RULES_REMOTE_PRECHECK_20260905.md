# C4 Xianyu Rules Remote Precheck — 2026-09-05

**Status:** `REMOTE_PRECHECK_ONLY / HUMAN_IN_APP_CONFIRMATION_REQUIRED / NOT_C4_AUTHORIZATION`

## Purpose

This note records a conservative remote precheck of current Xianyu/Goofish official materials before the first C4 Human Pilot. It does **not** prove that the exact Modbus RTU software SKU is currently eligible for listing under Jovi's personal seller account, and it does not replace the actual in-app rules/category/fulfillment UI shown to Jovi at publish time.

## Official materials checked

### 1. Xianyu Community Privacy Policy

Official page:
`https://terms.goofish.com/legal-agreement/terms/suit_bu1_taobao/suit_bu1_taobao202103021554_43790.html`

Observed policy dates:
- updated: `2026-06-29`
- effective: `2026-07-17`

The policy describes order/payment/delivery-related personal information processing. C4 should therefore keep the existing minimization rule: do not copy buyer plaintext profile/chat/payment evidence/Cookie/Token into Runtime or Git. Store only the minimum pseudonymous audit fields approved by the C4 policy.

### 2. Xianyu Open Platform — server integration documentation

Official page:
`https://open.goofish.com/doc/development/dev/server.html`

The official developer documentation currently exposes separate transaction capabilities including:
- virtual delivery / no-logistics scenario (`alibaba.idle.isv.goosefish.virtual.delivery`);
- physical logistics delivery;
- refund query;
- partial refund;
- after-send refund/close;
- return/refund handling.

The documentation also includes a `virtual_item_order` concept and refund/dispute states. This is sufficient to reject blanket copy such as “digital goods are never refundable”. Refund/dispute handling must remain human-controlled and follow the actual current platform/order rules.

### 3. Xianyu Open Platform — quick start

Official page:
`https://open.goofish.com/doc/quick-start.html`

The documentation lists `orderVirtualDelivery` as a no-logistics virtual-delivery capability and separately lists refund APIs. This confirms that a no-logistics virtual-delivery concept exists in the platform's developer ecosystem.

**Important limitation:** this does not prove that Jovi's ordinary personal-seller listing UI will expose the same option for this exact software SKU. Do not hard-code “click 无需物流发货” into the Pilot SOP until Jovi verifies the actual order UI/category behavior on the account used for the Pilot.

## What this precheck does NOT establish

Remote public documentation checked here does not, by itself, establish all of the following for the exact C4 SKU:

- that `Modbus RTU Diagnostic Toolkit` is allowed in the specific category available to Jovi;
- the exact category/subcategory Jovi must choose;
- whether the personal-seller UI shows virtual/no-logistics fulfillment for this listing;
- current seller fees/deposits or category-specific requirements;
- all current virtual/digital-goods refund/dispute requirements;
- whether special software/license/source-code wording triggers an additional rule;
- whether a particular cloud-drive delivery method is permitted or recommended.

Therefore those points remain a Human Pre-Publish check.

## Mandatory Human Pre-Publish check in the actual Xianyu UI

Before signing `C4_HUMAN_PILOT_DECISION`, Jovi should manually open the current Xianyu app/site and record a sanitized checklist result for the actual account and listing flow:

1. Is the exact software/digital-service SKU/category publishable?
2. What category/subcategory is selected?
3. Does the publish flow show any special digital/virtual-goods notice, deposit, fee, qualification or prohibited-content rule?
4. What fulfillment options appear on a real draft/order for that category?
5. What refund/dispute wording is shown for that category/order type?
6. Is the planned price and inventory format accepted?
7. Is the planned delivery transport acceptable under the current flow?
8. Does any copy imply unsupported compatibility, guaranteed results, permanent updates, or an absolute no-refund policy? If yes, remove it.

Record only sanitized observations. Do not commit buyer identifiers, cookies, tokens, payment credentials, full account screenshots or private chats to Git.

Suggested local evidence artifact:

`governance/c4/C4_XIANYU_HUMAN_RULE_CHECK_20260905.md`

with verdict:

`C4_XIANYU_HUMAN_RULE_CHECK_PASS`

or a blocking reason.

## C4 rules derived from this precheck

- Keep all actual publish/message/payment confirmation/delivery/refund actions human-controlled.
- Do not state “digital goods are non-refundable” as an absolute rule.
- Do not state “click 无需物流发货” as a guaranteed personal-seller workflow until verified in the real UI.
- Do not move payment off-platform to avoid platform processes/fees.
- Keep customer-data minimization and pseudonymous Runtime records.
- Re-check current in-app rules at the moment of real Pilot authorization because platform behavior/rules can change.

## Gate effect

This remote precheck is informative only. It does not change any commercial permission flag and does not make the C4 Decision Candidate signable by itself.
