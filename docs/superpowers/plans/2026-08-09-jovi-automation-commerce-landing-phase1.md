# JOVI-AUTOMATION-COMMERCE-LANDING-PHASE1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Code tasks additionally require `test-driven-development` and `verification-before-completion`. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move Jovi Automation from a pre-decision governance candidate to a local, auditable Commerce Engine that passes one complete synthetic X2 flow without performing any real platform action.

**Architecture:** Keep Commerce Core independent from sales channels. Store product contracts as strict JSON, orders and append-only audit events in local SQLite, and generated listings/delivery packages in `workspace/review-queue/`; the Xianyu adapter renders drafts only. The governance unlock is a short prerequisite chain, while all product implementation begins only after Decision V3, Manifest-only APPLY, Post-Apply PASS, Gate A.P verification, and the `S1/CLOSED -> C/APPLY` transition.

**Tech Stack:** Python 3.11+ standard library, SQLite, JSON Schema Draft 2020-12 exchange contracts, PowerShell 5.1 human-only gates, SHA-256, `unittest`, local filesystem only.

---

## 1. Current verified state

### 1.1 Completed

- Jovi reported the independent G3 verdict `PASS_READY_FOR_JOVI_DECISION` in the current task.
- RERUN1 human-only evidence is `PASS_ZERO_DRIFT`.
- `FINAL_CONTROL_TARGET_SET_V2.json` was independently reported as 13/13 SHA and byte-length matches.
- V4 review package was independently reported as 18/18 matches.
- Hook policy remains `DO_NOT_TRUST` with `hook_runtime_dependency=false`, `hook_restore_allowed=false`, and `hook_trust_allowed=false`.
- The candidate Commerce architecture, ten strict schemas, fixtures, and candidate manifest exist only under `workspace/review-queue/commerce-v1/`.
- Governance regression evidence exists for Security Semantics 20/20, S2A2 25/25, S1 34/34, S2A1 43/43, and Hook 10/10.

### 1.2 Current candidate hashes

| Artifact | SHA-256 |
|---|---|
| `workspace/review-queue/commerce-v1/governance-v2/JOVI_S1_RESTART_DECISION_V3_CANDIDATE.json` | `c5cc3d0f6c3a60287b79becf401bc66ff8b626af4d10f9dd57926c0cc81b71ff` |
| `workspace/review-queue/commerce-v1/governance-v2/CONTROLLED_BASELINE_V2_CANDIDATE.json` | `3a85bf26729d874f28f6874f7ed76781fba4fdde265e61a22701f6719898e190` |
| `workspace/review-queue/commerce-v1/governance-v2/FINAL_CONTROL_TARGET_SET_V2.json` | `1ee1dcd0e41fc9d822ae6839a60d96c284d8d184ce3141e81547ffc00c67ad5a` |
| `workspace/review-queue/commerce-v1/governance-v2/FRAMEWORK_MANIFEST_V2_CANDIDATE.sha256` | `00550de6fabff131298168d33e3ace04440cd4b5bbe1bcc021c4b31cfa2b8e8e` |
| `workspace/review-queue/commerce-v1/governance-v2/PRE_APPLY_AUDIT_INPUT_V4/REVIEW_PACKAGE_MANIFEST.json` | `6acd9e1998eb60bc6d69d7a3fd9d06837bd2d79fc991fc028a77c2a968dcaa79` |

These values are a plan-time snapshot. Every consumer must recompute them immediately before use and stop on any drift.

### 1.3 Not completed

- The independent PASS exists in the task conversation, but no auditor-owned PASS report and sidecar were found in the workspace. This is a missing receipt, not a request for another audit.
- Formal `JOVI_S1_RESTART_DECISION_V3.json` and sidecar do not exist.
- `FRAMEWORK_MANIFEST.sha256` has not been replaced by the V2 candidate.
- Post-Apply Audit has not run.
- `GATE_A_PLAN.json` and `GATE_A.P.approval.json` do not exist.
- Control plane remains `S1/CLOSED/1` with `HOOK_UNTRUSTED` and `FORMAL_MANIFEST_MISMATCH`.
- No valid Git HEAD or remote exists.
- `docs/commerce/`, `schemas/commerce/`, `jovi_commerce/`, `tests/commerce/`, and `data/commerce/` do not exist.
- No order ledger, entitlement, delivery package, draft adapter, support service, or X2 synthetic flow exists.

## 2. Final target and progress

### Phase 1 exit

```text
X2_COMMERCE_FLOW_PASS
REAL_COMMERCE_PILOT_NOT_STARTED
REMOTE_REPOSITORY_NOT_CONFIGURED
HUMAN_ONLY_ENTRYPOINTS_CANDIDATE_NOT_INSTALLED
```

### Ultimate product goal

Create a local, auditable system that supports:

```text
Product asset
-> deterministic listing draft
-> order
-> Jovi human payment confirmation
-> entitlement
-> tamper-evident delivery package
-> Jovi human delivery
-> support record
-> aggregate commercial metrics
```

Real publishing, chat, payment collection, file sending, price changes, refunds, and verification remain human actions. Phase 1 proves the synthetic local flow; a separate future pilot must prove a real original SKU and real paid delivery.

### Progress interpretation

| View | Current estimate | Meaning |
|---|---:|---|
| Governance preparation | about 90% | G3 pre-apply review passed; Decision, APPLY, Post-Apply, Gate and C/APPLY remain |
| Commerce Landing Phase 1 to X2 | about 20% | candidate contracts exist, but no formal runtime or X2 implementation exists |
| Full commercial objective | about 30-35% | research, boundaries and governance are mature; real commerce software and pilot evidence are absent |

These are planning estimates, not acceptance-test pass rates.

## 3. Locked file structure

### Governance and phase evidence

```text
workspace/review-queue/commerce-v1/
├── JOVI_DECISION_V3_REVIEW_PACKAGE.md
├── governance/                         # exact canonical mirror consumed by current readiness/Gate code
│   ├── CONTROLLED_BASELINE_V2_CANDIDATE.json
│   ├── CONTROLLED_BASELINE_V2_CANDIDATE.sha256
│   └── PRE_APPLY_AUDIT_INPUT_V4/
├── governance-v2/
│   ├── G3_PREAPPLY_AUDIT_PASS_RERUN1.md
│   ├── G3_PREAPPLY_AUDIT_PASS_RERUN1.md.sha256.sidecar
│   └── post-apply/
│       ├── MANIFEST_ONLY_APPLY_REPORT.json
│       ├── MANIFEST_ONLY_APPLY_REPORT.json.sha256.sidecar
│       ├── POST_APPLY_AUDIT_V1.md
│       └── POST_APPLY_AUDIT_V1.md.sha256.sidecar
└── human-only-candidates/
    ├── Confirm-CommercePayment.ps1
    └── Confirm-CommerceDelivery.ps1
```

The two G3 PASS files must be authored or exported by the independent reviewer. Luna must not fabricate them from the conversation.

The current readiness validator and Gate generator consume `workspace/review-queue/commerce-v1/governance/`, while the reviewed package is frozen in `governance-v2/`. Task 0 creates `governance/` as a byte-identical, fail-if-present mirror of the reviewed baseline and V4 package; it does not regenerate or reinterpret evidence.

### Formal Commerce paths after Gate

```text
docs/commerce/
├── AUTOMATED_COMMERCE_ARCHITECTURE.md
├── PRODUCT_LIFECYCLE_V1.md
├── ORDER_FLOW_V1.md
├── DELIVERY_FLOW_V1.md
└── SALES_ADAPTER_DESIGN_V1.md
schemas/commerce/
├── PRODUCT_ASSET_SCHEMA_V1.json
├── PRODUCT_VERSION_SCHEMA_V1.json
├── PRICING_PLAN_SCHEMA_V1.json
├── DELIVERY_POLICY_SCHEMA_V1.json
├── ORDER_SCHEMA_V1.json
├── PAYMENT_VERIFICATION_SCHEMA_V1.json
├── ENTITLEMENT_SCHEMA_V1.json
├── DELIVERY_SCHEMA_V1.json
├── SUPPORT_CASE_SCHEMA_V1.json
└── LISTING_BUNDLE_SCHEMA_V1.json
jovi_commerce/
├── __init__.py
├── __main__.py
├── models.py
├── validation.py
├── catalog.py
├── listing.py
├── store.py
├── orders.py
├── payment.py
├── entitlement.py
├── delivery.py
├── support.py
├── metrics.py
└── adapters/
    ├── __init__.py
    └── xianyu.py
tests/commerce/
├── test_models_and_validation.py
├── test_catalog.py
├── test_listing.py
├── test_order_ledger.py
├── test_payment_entitlement_delivery.py
├── test_xianyu_adapter.py
├── test_support_metrics.py
└── test_x2_workflow.py
data/commerce/
products/
```

Each module owns one responsibility. Do not create a second `commerce/`, `generated_products/`, `sales_adapter/`, `orders/`, `delivery/`, or `customer/` root.

### Public model contract

```python
@dataclass(frozen=True)
class ProductAsset:
    product_id: str
    name: str
    summary: str
    owner: str
    rights_status: str


@dataclass(frozen=True)
class ProductVersion:
    version: str
    status: str
    change_summary: str
    compatibility: tuple[str, ...]


@dataclass(frozen=True)
class PricingPlan:
    currency: str
    amount_minor: int
    status: str


@dataclass(frozen=True)
class DeliveryPolicy:
    mode: str
    files: tuple[str, ...]
    license_type: str
    support_days: int


@dataclass(frozen=True)
class ProductPackage:
    product: ProductAsset
    version: ProductVersion
    pricing: PricingPlan
    delivery: DeliveryPolicy
    faq_markdown: str
    changelog_markdown: str
    tree_sha256: str


@dataclass(frozen=True)
class OrderRecord:
    order_id: str
    product_id: str
    version: str
    amount_minor: int
    currency: str
    customer_ref: str
    status: str
    last_event_sha256: str


@dataclass(frozen=True)
class PaymentVerification:
    order_id: str
    amount_minor: int
    currency: str
    confirmed_by: str
    confirmed_at: str
    evidence_sha256: str | None


@dataclass(frozen=True)
class Entitlement:
    entitlement_id: str
    order_id: str
    product_id: str
    version: str
    license_type: str
    terms_sha256: str


@dataclass(frozen=True)
class DeliveryReceipt:
    order_id: str
    entitlement_id: str
    package_sha256: str
    manifest_sha256: str
    status: str


@dataclass(frozen=True)
class SupportCase:
    case_id: str
    order_id: str
    category: str
    severity: str
    summary: str
    resolution_status: str


@dataclass(frozen=True)
class ListingBundle:
    product_id: str
    version: str
    rights_status: str
    content_hashes: dict[str, str]
    actions: dict[str, bool]
```

Public services remain:

```python
CatalogService.load(product_dir: Path) -> ProductPackage
ListingService.generate(product: ProductPackage, output_dir: Path, run_id: str) -> ListingBundle
OrderService.create(product_id: str, version: str, amount_minor: int, idempotency_key: str) -> OrderRecord
OrderService.transition(order_id: str, target_state: str, actor: str, idempotency_key: str) -> OrderRecord
PaymentService.apply_human_verification(receipt: PaymentVerification, idempotency_key: str) -> OrderRecord
EntitlementService.issue(order_id: str, idempotency_key: str) -> Entitlement
DeliveryService.prepare(order_id: str, product_dir: Path, output_dir: Path, idempotency_key: str) -> DeliveryReceipt
SupportService.open(order_id: str, category: str, summary: str, idempotency_key: str) -> SupportCase
XianyuDraftAdapter.render(listing: dict, output_dir: Path) -> dict
```

Order transitions are fixed:

```text
DRAFT -> AWAITING_PAYMENT -> PAYMENT_VERIFIED -> PACKAGE_READY
-> READY_FOR_HUMAN_DELIVERY -> DELIVERED_CONFIRMED -> CLOSED

DRAFT/AWAITING_PAYMENT -> CANCELLED
DELIVERED_CONFIRMED -> REFUND_REQUESTED -> REFUNDED_CONFIRMED
```

All other transitions fail closed.

## 4. Permanent boundaries

- Do not run `scripts/human-only/**` or `scripts/xianyu/human-only/**`.
- Do not read or modify `E:\project\xianyu-auto-reply`.
- Do not read cookies, messages, platform databases, tokens, payment records, browser profiles, or customer PII.
- Do not store contact details or platform identifiers. Use random `customer_ref` only.
- Store money as integer `amount_minor`; currency is `CNY`.
- Hook remains `DO_NOT_TRUST` and is never a Commerce runtime dependency.
- Do not change `MANIFEST.sha256`.
- Before Gate A.P and C/APPLY, do not create formal Commerce paths or new product content.
- Do not configure a Git remote, push, merge, tag, publish, or claim a live sale.
- The audit budget for this plan is one already-completed Pre-Apply review plus one required Post-Apply review. Do not add adjacent audit work unless a named gate fails.

## 5. Task-by-task execution

### Task 0: Persist the passed G3 receipt and create the Decision review package

**Files:**

- Receive from independent reviewer: `workspace/review-queue/commerce-v1/governance-v2/G3_PREAPPLY_AUDIT_PASS_RERUN1.md`
- Receive from independent reviewer: `workspace/review-queue/commerce-v1/governance-v2/G3_PREAPPLY_AUDIT_PASS_RERUN1.md.sha256.sidecar`
- Create: `workspace/review-queue/commerce-v1/JOVI_DECISION_V3_REVIEW_PACKAGE.md`
- Create exact mirror: `workspace/review-queue/commerce-v1/governance/`
- Modify: `tasks/todo.md`
- Modify: `STATUS.md`
- Modify: `CHANGELOG.md`
- Modify: Obsidian `02-当前进度.md`, `03-任务台账.md`, and `06-自动售卖Commerce主线.md`

- [ ] **Step 1: Require the auditor-owned PASS receipt**

Expected report content must include the exact verdict, reviewed target-set SHA, V4 package SHA, reviewer identity/lineage separation statement, UTC, read-only statement, and prohibited-action statement. If the report or sidecar is missing, stop at `G3_PASS_REPORTED_RECEIPT_NOT_BOUND`.

- [ ] **Step 2: Verify the receipt sidecar**

Run:

```powershell
$report = 'workspace/review-queue/commerce-v1/governance-v2/G3_PREAPPLY_AUDIT_PASS_RERUN1.md'
$sidecar = "$report.sha256.sidecar"
$actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $report).Hash.ToLowerInvariant()
$expected = (Get-Content -Raw -Encoding utf8 -LiteralPath $sidecar).Trim().Split()[0].ToLowerInvariant()
if ($actual -ne $expected) { throw "G3 audit sidecar mismatch: expected=$expected actual=$actual" }
```

Expected: no output and exit code 0.

- [ ] **Step 3: Recompute all Decision inputs**

Run:

```powershell
$inputs = @(
  'workspace/review-queue/commerce-v1/governance-v2/JOVI_S1_RESTART_DECISION_V3_CANDIDATE.json',
  'workspace/review-queue/commerce-v1/governance-v2/CONTROLLED_BASELINE_V2_CANDIDATE.json',
  'workspace/review-queue/commerce-v1/governance-v2/FINAL_CONTROL_TARGET_SET_V2.json',
  'workspace/review-queue/commerce-v1/governance-v2/FRAMEWORK_MANIFEST_V2_CANDIDATE.sha256',
  'workspace/review-queue/commerce-v1/governance-v2/PRE_APPLY_AUDIT_INPUT_V4/REVIEW_PACKAGE_MANIFEST.json',
  'workspace/review-queue/commerce-v1/governance-v2/G3_PREAPPLY_AUDIT_PASS_RERUN1.md'
)
$inputs | ForEach-Object {
  $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $_).Hash.ToLowerInvariant()
  "$_ $hash"
}
```

Expected: six existing files and six lowercase SHA-256 values.

- [ ] **Step 4: Write the Jovi review package**

The Markdown must contain: reason for Decision V3, the six current hashes, `manifest_apply_scope=[FRAMEWORK_MANIFEST.sha256]`, Hook DNT policy, rollback file, forbidden actions, and the exact fields Jovi must set. It must say `CANDIDATE_ONLY` and must not create a Decision or Approval.

- [ ] **Step 5: Materialize the byte-identical canonical governance mirror**

Run only when `workspace/review-queue/commerce-v1/governance/` does not exist:

```powershell
$source = (Resolve-Path 'workspace/review-queue/commerce-v1/governance-v2').Path
$target = 'workspace/review-queue/commerce-v1/governance'
if (Test-Path -LiteralPath $target) { throw 'canonical governance mirror already exists; refusing overwrite' }
New-Item -ItemType Directory -Path $target | Out-Null
Copy-Item -LiteralPath "$source\CONTROLLED_BASELINE_V2_CANDIDATE.json" -Destination $target
Copy-Item -LiteralPath "$source\CONTROLLED_BASELINE_V2_CANDIDATE.sha256" -Destination $target
Copy-Item -LiteralPath "$source\PRE_APPLY_AUDIT_INPUT_V4" -Destination $target -Recurse
```

Recompute every mirrored file by relative path. Expected: identical file set for the copied subset and 100% SHA/byte-length equality. On any mismatch, leave the failed mirror as evidence, mark it stale, and stop; do not overwrite or delete it in place.

- [ ] **Step 6: Verify no authority object changed**

Run:

```powershell
Get-ChildItem workspace/decisions -File | Select-Object -ExpandProperty Name
Get-ChildItem workspace/approvals -File | Select-Object -ExpandProperty Name
Get-ChildItem reports/gates -File -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name
```

Expected: Decision V1 body/sidecar only, approvals `README.md` only, no Gate files.

No Git commit is possible before Task 4.

### Task 1: Jovi issues Decision V3; Luna performs read-only validation

**Files:**

- Jovi creates: `workspace/decisions/JOVI_S1_RESTART_DECISION_V3.json`
- Jovi creates: `workspace/decisions/JOVI_S1_RESTART_DECISION_V3.json.sha256.sidecar`
- Luna creates only after validation: `workspace/review-queue/commerce-v1/governance-v2/DECISION_V3_VALIDATION_REPORT.json`

- [ ] **Step 1: Jovi creates the Decision body and sidecar**

The body must contain these exact authority fields:

```json
{
  "issued_from_human": true,
  "hook_status": "DO_NOT_TRUST",
  "hook_runtime_dependency": false,
  "hook_restore_allowed": false,
  "hook_trust_allowed": false,
  "manifest_apply_scope": ["FRAMEWORK_MANIFEST.sha256"],
  "track_p_allowed": false,
  "track_i_allowed": false,
  "real_platform_actions_allowed": false
}
```

The actual Decision also binds the six hashes from Task 0. Luna must not create or repair these two files.

- [ ] **Step 2: Verify body and sidecar**

Run:

```powershell
$decision = 'workspace/decisions/JOVI_S1_RESTART_DECISION_V3.json'
$sidecar = "$decision.sha256.sidecar"
$actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $decision).Hash.ToLowerInvariant()
$expected = (Get-Content -Raw -Encoding utf8 -LiteralPath $sidecar).Trim().Split()[0].ToLowerInvariant()
if ($actual -ne $expected) { throw 'Decision V3 sidecar mismatch' }
python -B scripts/validate_commerce_gate_readiness.py --root .
```

Expected: sidecar match. Gate readiness may still report the expected pre-APPLY blockers, but it must recognize a valid human Decision and no hidden Hook/Track/platform permission.

- [ ] **Step 3: Stop on any hidden authority expansion**

Any `true` Track/platform flag, missing Hook policy field, expanded Manifest scope, target hash drift, or sidecar mismatch yields `DECISION_V3_INVALID` and stops Task 2.

### Task 2: Apply the Framework Manifest candidate and obtain the single Post-Apply audit

**Files:**

- Modify exactly: `FRAMEWORK_MANIFEST.sha256`
- Create: `workspace/review-queue/commerce-v1/governance-v2/post-apply/FRAMEWORK_MANIFEST_PRE_APPLY_BACKUP.sha256`
- Create: `workspace/review-queue/commerce-v1/governance-v2/post-apply/MANIFEST_ONLY_APPLY_REPORT.json`
- Create: `workspace/review-queue/commerce-v1/governance-v2/post-apply/MANIFEST_ONLY_APPLY_REPORT.json.sha256.sidecar`
- Independent reviewer creates: `POST_APPLY_AUDIT_V1.md` and sidecar
- Independent reviewer creates machine receipt: `reports/remediation/COMMERCE_V1_POST_APPLY_AUDIT.json` and sidecar

- [ ] **Step 1: Capture the protected before state**

Hash `.codex/hooks.json`, `MANIFEST.sha256`, Decision V3, approvals, control state, and both human-only trees into the APPLY report input. Do not run the human-only scripts.

- [ ] **Step 2: Verify Decision scope and candidate hash again**

Expected candidate file hash: the current recomputed hash must equal the value bound by Decision V3. The Decision scope must be exactly `FRAMEWORK_MANIFEST.sha256`.

- [ ] **Step 3: Apply exact candidate bytes**

Use `apply_patch` to replace the contents of `FRAMEWORK_MANIFEST.sha256` with the exact current contents of `workspace/review-queue/commerce-v1/governance-v2/FRAMEWORK_MANIFEST_V2_CANDIDATE.sha256`. Do not edit any other protected object.

- [ ] **Step 4: Verify the new Framework Manifest**

Run:

```powershell
python -B scripts/validate-package.py
python -B scripts/run-security-semantics.py
python -B tests/test_s2a2_enforcement.py
python -B tests/test_s1_integrity.py
python -B tests/test_s2a1_control_plane.py
python -B tests/hooks/test_pre_tool_guard.py
```

Expected: Framework Manifest entries all match and all governance regressions pass. `MANIFEST.sha256` may remain a historical shipment mismatch and must be byte-identical to its before snapshot.

- [ ] **Step 5: Produce APPLY report and sidecar**

The report records pre/post hashes, the sole modified protected file, rollback backup, Decision SHA, audit SHA, candidate SHA, and test results.

- [ ] **Step 6: Independent Post-Apply audit**

The fresh independent reviewer performs one bounded read-only audit. Allowed verdicts: `PASS` or `FAIL`. The machine receipt must include `{"verdict":"PASS","independent":true}` plus Decision, Framework Manifest, APPLY report, pre-audit, and target-set SHA bindings; its sidecar must match. A FAIL stops the plan and allows only the exact reported remediation; a PASS advances to Task 3. This is the only new audit scheduled in this plan.

### Task 3: Close S1, obtain Gate A.P, and transition to C/APPLY

**Files:**

- Modify through existing guarded transition tools: `config/control-plane-state.json`, `PROJECT_STATE.json`, `STATUS.md`, `CODEX_START_PROMPT.txt`
- Create: `workspace/review-queue/commerce-v1/governance-v2/post-apply/S1_CLOSEOUT_RECEIPT.json`
- Create once: `reports/gates/GATE_A_PLAN.json`
- Create once by Jovi human-only action: `workspace/approvals/GATE_A.P.approval.json`

- [ ] **Step 1: Apply S1 closeout**

Use the existing closeout/transition helpers to increment state revision, preserve the previous-state hash, clear `FORMAL_MANIFEST_MISMATCH`, and record `HOOK_UNTRUSTED` as an accepted DNT limitation rather than TRUST.

- [ ] **Step 2: Run Gate readiness**

Run:

```powershell
python -B scripts/validate_commerce_gate_readiness.py --root .
```

Expected: `PASS` with no Gate A.P receipt yet, Track I false, platform actions false, Decision V3 valid, Framework Manifest matching, and both independent audit receipts bound.

- [ ] **Step 3: Generate Gate Plan once**

Run:

```powershell
python -B scripts/generate_gate_a_plan.py --root .
```

Expected: `reports/gates/GATE_A_PLAN.json` and its SHA sidecar are created once for `COMMERCE_V1_X2`; Track I is `NOT_AUTHORIZED` and all real platform actions are false.

- [ ] **Step 4: Jovi runs the human-only Gate command**

Only Jovi runs:

```powershell
powershell -File .\scripts\human-only\Approve-Gate.ps1 `
  -Gate GATE_A `
  -Track P `
  -PlanPath .\reports\gates\GATE_A_PLAN.json `
  -ExpectedSha256 <exact-current-plan-sha256> `
  -Approver Jovi
```

Luna must not substitute the hash, run the script, or create the receipt.

- [ ] **Step 5: Verify Gate receipt**

Run:

```powershell
python -B scripts/verify-gate-approval.py --root . --gate GATE_A --track P
```

Expected: PASS with exact Plan SHA binding.

- [ ] **Step 6: Transition control plane**

Run the existing bound transition to change only:

```text
S1/CLOSED -> C/APPLY
```

Expected: Commerce local development/test actions allowed; Track I, release, human-only, Approval, Manifest, and Xianyu real actions remain denied.

### Task 4: Establish the local Git baseline

**Files:**

- Create: `.gitignore`
- Create: `reports/baseline/GIT_BASELINE_FILES_V1.txt`
- Create: `reports/baseline/GIT_BASELINE_REVIEW_V1.md`
- Initialize: `.git/`

- [ ] **Step 1: Prove Gate and C/APPLY**

Run Gate verification and read `config/control-plane-state.json`. Expected: valid GATE_A.P and `C/APPLY`.

- [ ] **Step 2: Build an explicit baseline file list**

Exclude `.git`, runtime databases, caches, logs, backups, build output, secrets, approvals, review queues, and external projects. Run the existing secret scanner and stop on new high-risk findings.

- [ ] **Step 3: Initialize local Git**

Run:

```powershell
git init -b main
git remote -v
```

Expected: repository initialized and no remote output.

- [ ] **Step 4: Stage only the explicit list**

Run:

```powershell
Get-Content reports/baseline/GIT_BASELINE_FILES_V1.txt | ForEach-Object { git add -- $_ }
git diff --cached --check
```

Expected: no whitespace errors and no excluded file staged.

- [ ] **Step 5: Commit**

```powershell
git commit -m "chore: establish audited jovi automation baseline"
git status --short
git remote -v
```

Expected: one baseline commit, clean worktree, no remote.

### Task 5: Freeze formal Commerce contracts and package skeleton

**Files:**

- Create the formal `docs/commerce/`, `schemas/commerce/`, `jovi_commerce/`, `tests/commerce/`, and `data/commerce/` paths from Section 3.
- Test: `tests/commerce/test_models_and_validation.py`

- [ ] **Step 1: Copy reviewed contracts byte-for-byte**

Copy the ten candidate schemas from `workspace/review-queue/commerce-v1/schemas/` and the architecture candidate into formal paths. Recompute source and destination SHA; each pair must match.

- [ ] **Step 2: Write the failing model/validator test**

```python
import unittest

from jovi_commerce.models import PricingPlan
from jovi_commerce.validation import validate_pricing_plan


class PricingPlanTests(unittest.TestCase):
    def test_rejects_float_amount(self):
        with self.assertRaises(ValueError):
            validate_pricing_plan({"currency": "CNY", "amount_minor": 99.0, "status": "ACTIVE"})

    def test_accepts_integer_minor_units(self):
        plan = validate_pricing_plan({"currency": "CNY", "amount_minor": 9900, "status": "ACTIVE"})
        self.assertEqual(plan, PricingPlan(currency="CNY", amount_minor=9900, status="ACTIVE"))
```

- [ ] **Step 3: Run the focused test and observe failure**

Run:

```powershell
python -B -m unittest tests.commerce.test_models_and_validation -v
```

Expected: FAIL because `jovi_commerce.models` does not exist.

- [ ] **Step 4: Implement the minimal type and validator**

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class PricingPlan:
    currency: str
    amount_minor: int
    status: str
```

```python
from .models import PricingPlan


def validate_pricing_plan(value: dict) -> PricingPlan:
    if set(value) != {"currency", "amount_minor", "status"}:
        raise ValueError("pricing fields must match the V1 contract")
    if value["currency"] != "CNY":
        raise ValueError("currency must be CNY")
    if type(value["amount_minor"]) is not int or value["amount_minor"] <= 0:
        raise ValueError("amount_minor must be a positive integer")
    return PricingPlan(**value)
```

- [ ] **Step 5: Run focused and full tests**

Expected: focused PASS; governance suite remains PASS.

- [ ] **Step 6: Commit**

```powershell
git add docs/commerce schemas/commerce jovi_commerce tests/commerce tasks/todo.md STATUS.md CHANGELOG.md
git commit -m "docs: freeze commerce v1 contracts"
```

### Task 6: Implement product catalog validation

**Files:**

- Create: `jovi_commerce/catalog.py`
- Test: `tests/commerce/test_catalog.py`
- Create fixtures under: `tests/fixtures/commerce/valid_product/` and `tests/fixtures/commerce/blocked_product/`

- [ ] **Step 1: Write failing catalog tests**

```python
import unittest
from pathlib import Path

from jovi_commerce.catalog import CatalogService


class CatalogServiceTests(unittest.TestCase):
    def test_loads_fixed_seven_file_product(self):
        package = CatalogService().load(Path("tests/fixtures/commerce/valid_product"))
        self.assertEqual(package.product.product_id, "synthetic-guide-v1")
        self.assertEqual(package.pricing.amount_minor, 9900)

    def test_blocks_pending_rights(self):
        with self.assertRaisesRegex(ValueError, "rights status"):
            CatalogService().load(Path("tests/fixtures/commerce/blocked_product"))
```

Add separate tests for missing file, unknown file, invalid SemVer, float price, absolute path, `..`, and symlink.

- [ ] **Step 2: Run and observe failure**

Expected: import or attribute failure.

- [ ] **Step 3: Implement the fixed file allowlist and path guard**

```python
REQUIRED_FILES = {
    "product.json",
    "version.json",
    "pricing.json",
    "delivery.json",
    "faq.md",
    "changelog.md",
    "assets",
}


def _assert_safe_child(root: Path, child: Path) -> None:
    if child.is_symlink():
        raise ValueError("symlinks are not allowed")
    resolved_root = root.resolve()
    resolved_child = child.resolve()
    if resolved_root not in resolved_child.parents and resolved_child != resolved_root:
        raise ValueError("path escapes product root")
```

`CatalogService.load()` reads only the allowed files, validates rights as `ORIGINAL` or `VERIFIED_LICENSE`, builds canonical JSON using sorted keys and compact separators, and emits a SHA-256 product-tree manifest.

- [ ] **Step 4: Run focused, full Commerce, and governance tests**

- [ ] **Step 5: Commit**

```powershell
git add jovi_commerce/catalog.py tests/commerce/test_catalog.py tests/fixtures/commerce tasks/todo.md STATUS.md CHANGELOG.md
git commit -m "feat: add commerce product asset catalog"
```

### Task 7: Implement deterministic listing generation

**Files:**

- Create: `jovi_commerce/listing.py`
- Test: `tests/commerce/test_listing.py`
- Output only under: `workspace/review-queue/commerce/<product>/<version>/<run_id>/`

- [ ] **Step 1: Write failing deterministic-output tests**

```python
import tempfile
import unittest
from pathlib import Path

from jovi_commerce.catalog import CatalogService
from jovi_commerce.listing import ListingService


class ListingServiceTests(unittest.TestCase):
    def test_same_product_produces_same_content_hashes(self):
        product = CatalogService().load(Path("tests/fixtures/commerce/valid_product"))
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            one = ListingService().generate(product, Path(first), run_id="run-a")
            two = ListingService().generate(product, Path(second), run_id="run-b")
            self.assertEqual(one.content_hashes, two.content_hashes)
            self.assertFalse(one.actions["publish"])
```

Add tests for Markdown escaping, title length, missing FAQ, blocked rights, and network-call absence.

- [ ] **Step 2: Run and observe failure**

- [ ] **Step 3: Implement deterministic templates**

```python
def _escape_markdown(value: str) -> str:
    for token in ("\\", "*", "_", "`", "[", "]", "<", ">"):
        value = value.replace(token, f"\\{token}")
    return value


ACTION_DEFAULTS = {
    "publish": False,
    "send_message": False,
    "deliver": False,
    "change_price": False,
    "refund": False,
}
```

Generate `title.md`, `description.md`, `faq.md`, `delivery.md`, `changelog.md`, `images_prompt.md`, `listing.json`, and `manifest.sha256.json`. Every user-facing file includes `人工审核后使用`.

- [ ] **Step 4: Verify focused/full tests and manifest hashes**

- [ ] **Step 5: Commit**

```powershell
git add jovi_commerce/listing.py tests/commerce/test_listing.py tasks/todo.md STATUS.md CHANGELOG.md
git commit -m "feat: add deterministic product listing generator"
```

### Task 8: Implement the audited SQLite order ledger

**Files:**

- Create: `jovi_commerce/store.py`
- Create: `jovi_commerce/orders.py`
- Test: `tests/commerce/test_order_ledger.py`

- [ ] **Step 1: Write failing state-machine and hash-chain tests**

```python
import tempfile
import unittest
from pathlib import Path

from jovi_commerce.orders import OrderService
from jovi_commerce.store import CommerceStore


class OrderLedgerTests(unittest.TestCase):
    def test_rejects_payment_skip(self):
        with tempfile.TemporaryDirectory() as temp:
            service = OrderService(CommerceStore(Path(temp) / "commerce.db"))
            order = service.create("synthetic-guide-v1", "1.0.0", 9900, "create-1")
            with self.assertRaisesRegex(ValueError, "illegal transition"):
                service.transition(order.order_id, "PAYMENT_VERIFIED", "synthetic-agent", "skip-1")

    def test_idempotent_transition_creates_one_event(self):
        with tempfile.TemporaryDirectory() as temp:
            service = OrderService(CommerceStore(Path(temp) / "commerce.db"))
            order = service.create("synthetic-guide-v1", "1.0.0", 9900, "create-1")
            one = service.transition(order.order_id, "AWAITING_PAYMENT", "synthetic-agent", "await-1")
            two = service.transition(order.order_id, "AWAITING_PAYMENT", "synthetic-agent", "await-1")
            self.assertEqual(one.last_event_sha256, two.last_event_sha256)
```

Add tests for foreign keys, `user_version=1`, concurrent duplicate keys, chain tampering, unknown state, refund side path, and database corruption.

- [ ] **Step 2: Run and observe failure**

- [ ] **Step 3: Implement schema and transactions**

```python
SCHEMA_V1 = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS orders (
  order_id TEXT PRIMARY KEY,
  product_id TEXT NOT NULL,
  version TEXT NOT NULL,
  amount_minor INTEGER NOT NULL CHECK(amount_minor > 0),
  currency TEXT NOT NULL CHECK(currency = 'CNY'),
  customer_ref TEXT NOT NULL,
  status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS order_events (
  event_id TEXT PRIMARY KEY,
  order_id TEXT NOT NULL REFERENCES orders(order_id),
  idempotency_key TEXT NOT NULL,
  previous_event_sha256 TEXT,
  event_sha256 TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  UNIQUE(order_id, idempotency_key)
);
"""
```

Initialize all seven required tables, set `PRAGMA user_version=1`, `busy_timeout`, and use `BEGIN IMMEDIATE`. Event SHA is computed from canonical event JSON including `previous_event_sha256`.

- [ ] **Step 4: Run concurrency, tamper, focused, full, and governance tests**

- [ ] **Step 5: Commit**

```powershell
git add jovi_commerce/store.py jovi_commerce/orders.py tests/commerce/test_order_ledger.py tasks/todo.md STATUS.md CHANGELOG.md
git commit -m "feat: add audited commerce order ledger"
```

### Task 9: Implement synthetic payment, entitlement, and delivery preparation

**Files:**

- Create: `jovi_commerce/payment.py`
- Create: `jovi_commerce/entitlement.py`
- Create: `jovi_commerce/delivery.py`
- Test: `tests/commerce/test_payment_entitlement_delivery.py`
- Create candidates only: `workspace/review-queue/commerce-v1/human-only-candidates/*.ps1`

- [ ] **Step 1: Write failing payment and delivery tests**

```python
def test_unpaid_order_cannot_issue_entitlement(self):
    with self.assertRaisesRegex(ValueError, "PAYMENT_VERIFIED"):
        self.entitlements.issue(self.order.order_id, "issue-1")


def test_delivery_package_is_idempotent_and_tamper_evident(self):
    first = self.delivery.prepare(self.paid_order.order_id, self.product_dir, self.output, "pack-1")
    second = self.delivery.prepare(self.paid_order.order_id, self.product_dir, self.output, "pack-1")
    self.assertEqual(first.package_sha256, second.package_sha256)
    self.output.joinpath("payload.zip").write_bytes(b"tampered")
    with self.assertRaisesRegex(ValueError, "package hash mismatch"):
        self.delivery.verify(first)
```

Add tests for amount mismatch, duplicate payment, invalid evidence SHA, path escape, unlisted delivery file, repeated entitlement, and real-delivery confirmation denial.

- [ ] **Step 2: Run and observe failure**

- [ ] **Step 3: Implement synthetic receipt validation**

```python
def validate_evidence_sha256(value: str | None) -> None:
    if value is None:
        return
    if len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
        raise ValueError("evidence_sha256 must be lowercase SHA-256")
```

Payment transition is only `AWAITING_PAYMENT -> PAYMENT_VERIFIED`; entitlement ID is `ent_<uuid>` and binds order, product, version, license type, and terms SHA.

- [ ] **Step 4: Implement deterministic ZIP membership and receipt hashing**

Only files explicitly listed in `delivery.json` enter the ZIP. Normalize archive paths, reject symlinks, set deterministic ZIP timestamps, generate package manifest and receipt, and stop at `READY_FOR_HUMAN_DELIVERY`.

- [ ] **Step 5: Create but do not install or run human-only script candidates**

Each candidate requires exact interactive phrases:

```text
CONFIRM PAYMENT <order_id> <amount_minor> CNY
CONFIRM DELIVERY <order_id> <package_sha256>
```

- [ ] **Step 6: Verify focused/full tests and commit**

```powershell
git add jovi_commerce/payment.py jovi_commerce/entitlement.py jovi_commerce/delivery.py tests/commerce/test_payment_entitlement_delivery.py tasks/todo.md STATUS.md CHANGELOG.md
git commit -m "feat: add payment entitlement and delivery preparation"
```

Do not stage the uninstalled human-only candidates in this commit unless the Gate Plan explicitly lists them.

### Task 10: Implement the manual-only Xianyu draft adapter

**Files:**

- Create: `jovi_commerce/adapters/__init__.py`
- Create: `jovi_commerce/adapters/xianyu.py`
- Test: `tests/commerce/test_xianyu_adapter.py`

- [ ] **Step 1: Write failing action-boundary tests**

```python
class XianyuAdapterTests(unittest.TestCase):
    def test_all_real_actions_are_false(self):
        bundle = self.adapter.render(self.listing, self.output)
        self.assertEqual(
            bundle["actions"],
            {
                "publish": False,
                "send_message": False,
                "deliver": False,
                "change_price": False,
                "refund": False,
            },
        )
        self.assertEqual(bundle["approval"], "PENDING")
```

Add tests for blocked rights, non-empty delivery directory, external path, and compatibility with the existing in-repository Xianyu bundle validator.

- [ ] **Step 2: Run and observe failure**

- [ ] **Step 3: Implement pure mapping**

```python
class XianyuDraftAdapter:
    def render(self, listing: dict, output_dir: Path) -> dict:
        if listing["rights_status"] not in {"ORIGINAL", "VERIFIED_LICENSE"}:
            raise ValueError("rights status blocks draft generation")
        bundle = {
            "approval": "PENDING",
            "actions": ACTION_DEFAULTS.copy(),
            "listing": listing,
            "fixed_replies": [],
        }
        return bundle
```

The adapter must not import network, browser, database, or external Xianyu modules.

- [ ] **Step 4: Run the existing in-repository bundle validator and full regressions**

- [ ] **Step 5: Commit**

```powershell
git add jovi_commerce/adapters tests/commerce/test_xianyu_adapter.py tasks/todo.md STATUS.md CHANGELOG.md
git commit -m "feat: add manual-only xianyu draft adapter"
```

### Task 11: Implement support records, metrics, and CLI

**Files:**

- Create: `jovi_commerce/support.py`
- Create: `jovi_commerce/metrics.py`
- Create: `jovi_commerce/__main__.py`
- Test: `tests/commerce/test_support_metrics.py`

- [ ] **Step 1: Write failing privacy and missing-metric tests**

```python
def test_support_rejects_pii_like_fields(self):
    with self.assertRaisesRegex(ValueError, "PII"):
        self.support.open(self.order_id, "INSTALL", "phone=13800000000", "case-1")


def test_missing_metrics_are_not_recorded(self):
    result = self.metrics.weekly({"views": 12, "sales": 1})
    self.assertEqual(result["refunds"], "NOT_RECORDED")
    self.assertEqual(result["repurchases"], "NOT_RECORDED")
```

- [ ] **Step 2: Run and observe failure**

- [ ] **Step 3: Implement bounded support and aggregate metrics**

Use allowlisted categories/severities and reject phone/email/platform-ID patterns. Metrics accept only non-negative integers or absent values; absence becomes `NOT_RECORDED`.

- [ ] **Step 4: Implement CLI routing**

The CLI exposes exactly:

```text
python -m jovi_commerce validate-product
python -m jovi_commerce generate-listing
python -m jovi_commerce order create
python -m jovi_commerce order show
python -m jovi_commerce delivery prepare
python -m jovi_commerce support open
python -m jovi_commerce adapter xianyu
```

No CLI command confirms real payment, real delivery, or platform action.

- [ ] **Step 5: Verify tests and commit**

```powershell
git add jovi_commerce/support.py jovi_commerce/metrics.py jovi_commerce/__main__.py tests/commerce/test_support_metrics.py tasks/todo.md STATUS.md CHANGELOG.md
git commit -m "feat: add support metrics and commerce cli"
```

### Task 12: Qualify the synthetic X2 workflow

**Files:**

- Create: `tests/commerce/test_x2_workflow.py`
- Create: `reports/commerce/X2_COMMERCE_FLOW_REPORT.json`
- Create: `reports/commerce/X2_COMMERCE_FLOW_REPORT.json.sha256.sidecar`
- Modify: project ledgers and Obsidian notes

- [ ] **Step 1: Write the failing end-to-end test**

```python
def test_one_synthetic_order_reaches_ready_for_human_delivery(self):
    product = catalog.load(self.product_dir)
    listing = listings.generate(product, self.review_dir, run_id="x2-run-1")
    order = orders.create(product.product_id, product.version, 9900, "x2-create")
    orders.transition(order.order_id, "AWAITING_PAYMENT", "synthetic-agent", "x2-await")
    payment.apply_human_verification(self.synthetic_payment(order), "x2-payment")
    entitlement = entitlements.issue(order.order_id, "x2-entitlement")
    receipt = delivery.prepare(order.order_id, self.product_dir, self.delivery_dir, "x2-package")
    adapter = xianyu.render(listing.to_dict(), self.adapter_dir)
    self.assertEqual(receipt.status, "READY_FOR_HUMAN_DELIVERY")
    self.assertTrue(entitlement.entitlement_id.startswith("ent_"))
    self.assertTrue(all(value is False for value in adapter["actions"].values()))
```

Add X2 tests proving exactly one payment, entitlement, and delivery receipt; idempotent replay; unpaid denial; rights-blocked denial; illegal transition denial; hash-chain tamper denial; ZIP tamper denial; zero PII; and zero external Xianyu access.

- [ ] **Step 2: Run and observe failure**

- [ ] **Step 3: Add the minimal orchestration required by the test**

Orchestration calls existing services only. It contains no direct SQL, network, browser, human-only, or platform action.

- [ ] **Step 4: Run the full acceptance matrix**

```powershell
python -B -m unittest discover -s tests/commerce -v
python -B scripts/run-security-semantics.py
python -B tests/test_s2a2_enforcement.py
python -B tests/test_s1_integrity.py
python -B tests/test_s2a1_control_plane.py
python -B tests/hooks/test_pre_tool_guard.py
git diff --check
git status --short
git remote -v
```

Expected: all tests PASS, diff check clean, no remote, five Xianyu actions false, no new secret/PII finding, and no real platform access.

- [ ] **Step 5: Write the X2 report and synchronize knowledge**

The report binds test commands/results, current commit SHA, database schema version, order/event/receipt hashes, package SHA, adapter actions, secret/PII scan, and external-repository non-access statement.

- [ ] **Step 6: Commit**

```powershell
git add tests/commerce/test_x2_workflow.py reports/commerce tasks/todo.md STATUS.md CHANGELOG.md
git commit -m "test: qualify synthetic commerce workflow"
```

Expected final state:

```text
X2_COMMERCE_FLOW_PASS
REAL_COMMERCE_PILOT_NOT_STARTED
REMOTE_REPOSITORY_NOT_CONFIGURED
HUMAN_ONLY_ENTRYPOINTS_CANDIDATE_NOT_INSTALLED
```

## 6. Every-task verification and reporting

At the end of each task, update `tasks/todo.md`, `STATUS.md`, `CHANGELOG.md`, and the four Obsidian project notes. After Git exists, make one small commit per task. Every report uses:

```text
当前阶段：
本轮目标：
完成：
未完成：
代码变化：
新增文件：
测试：
证据：
商业价值：
风险：
下一步：
提交：
```

Stop immediately on Decision/sidecar drift, Framework candidate drift, Post-Apply FAIL, Gate mismatch, Hook TRUST, `MANIFEST.sha256` change, unowned worktree changes, PII/secrets, external Xianyu access, real platform action, or missing Jovi human action.

## 7. Self-review checklist

- [ ] Every requirement maps to one numbered task.
- [ ] No formal Commerce path is created before Gate A.P and C/APPLY.
- [ ] The plan does not introduce `customer.contact`, platform IDs, or raw customer history.
- [ ] Money uses `amount_minor` and `CNY` only.
- [ ] There is exactly one required new audit: Post-Apply.
- [ ] All code tasks use a failing test before implementation.
- [ ] Every public service is exercised by unit or X2 acceptance tests.
- [ ] Xianyu actions remain false in code, schema, tests, and evidence.
- [ ] Phase 1 ends at synthetic X2, not a live pilot or release.
