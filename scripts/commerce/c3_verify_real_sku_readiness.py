#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_BOUNDARY_FLAGS = (
    "production_integration_allowed","real_payment","real_customer","xianyu","auto_delivery","n8n_production",
)
REQUIRED_EVIDENCE = (
    "C3_MODBUS_SOURCE_QUALIFICATION.json","C3_PRODUCT_MANIFEST.json","C3_LISTING_CLAIM_EVIDENCE.json",
    "C3_DIGITAL_RELEASE.json","C3_DELIVERY_PACKAGE_MANIFEST.json","C3_LISTING_CANDIDATE.json",
    "C3_XIANYU_DRAFT_BUNDLE.json","C3_SYNTHETIC_ORDER_RESULT.json","C3_NEGATIVE_TEST_RESULTS.json",
    "C3_REPLAY_RECOVERY_RESULT.json","C3_ADMIN_E2E_RESULT.json","C3_RELEASE_CANDIDATE.json",
    "C3_SOURCE_MANIFEST.json","C3_ROLLBACK_PLAN.json","C3_INDEPENDENT_AUDIT_PROMPT.md",
)
class VerificationError(RuntimeError): pass
def fail(message: str) -> None: raise VerificationError(message)
def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()
def load_json(path: Path) -> dict[str,Any]:
    try: data=json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc: fail(f"JSON_INVALID {path}: {exc}")
    if not isinstance(data,dict): fail(f"JSON_ROOT_NOT_OBJECT {path}")
    return data
def run_git(root:Path,*args:str,check:bool=True)->subprocess.CompletedProcess[str]:
    p=subprocess.run(["git","-C",str(root),*args],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
    if check and p.returncode!=0: fail(f"GIT_COMMAND_FAILED git {' '.join(args)}: {p.stderr.strip()}")
    return p
def normalize_rel_path(raw:str)->str:
    if not isinstance(raw,str) or not raw: fail("EMPTY_RELATIVE_PATH")
    if "\\" in raw: fail(f"BACKSLASH_PATH_FORBIDDEN {raw}")
    p=PurePosixPath(raw); wp=PureWindowsPath(raw)
    if p.is_absolute() or wp.is_absolute() or wp.drive or raw.startswith("//"): fail(f"ABSOLUTE_OR_DRIVE_PATH_FORBIDDEN {raw}")
    if any(part in ("",".","..") for part in p.parts): fail(f"UNSAFE_PATH_COMPONENT {raw}")
    return p.as_posix()
def resolve_inside(root:Path,rel:str)->Path:
    rel=normalize_rel_path(rel); base=root.resolve(strict=True); candidate=(base/rel).resolve(strict=True)
    try: candidate.relative_to(base)
    except ValueError: fail(f"PATH_ESCAPE {rel}")
    return candidate
def verify_file_binding(root:Path,item:dict[str,Any],path_key:str="relative_path")->None:
    rel=normalize_rel_path(item.get(path_key,"")); path=resolve_inside(root,rel)
    expected_sha=item.get("sha256")
    if not isinstance(expected_sha,str) or not SHA256_RE.fullmatch(expected_sha): fail(f"INVALID_SHA256_BINDING {rel}")
    actual=sha256_file(path)
    if actual!=expected_sha: fail(f"SHA256_MISMATCH {rel} expected={expected_sha} actual={actual}")
    if "size_bytes" in item:
        expected_size=item["size_bytes"]; actual_size=path.stat().st_size
        if not isinstance(expected_size,int) or expected_size<0: fail(f"INVALID_SIZE_BINDING {rel}")
        if actual_size!=expected_size: fail(f"SIZE_MISMATCH {rel} expected={expected_size} actual={actual_size}")
def resolve_evidence(product_root:Path,evidence_dir:Path,rel:str)->Path:
    rel=normalize_rel_path(rel); candidates=[]
    for root in (product_root,evidence_dir):
        p=root/rel
        if p.exists(): candidates.append(resolve_inside(root,rel))
    if not candidates: fail(f"EVIDENCE_PATH_NOT_FOUND {rel}")
    unique={str(p.resolve()) for p in candidates}
    if len(unique)!=1: fail(f"EVIDENCE_PATH_AMBIGUOUS {rel}")
    return candidates[0]
def verify_evidence_ref(product_root:Path,evidence_dir:Path,item:dict[str,Any])->None:
    rel=item.get("evidence_path") or item.get("relative_path"); expected=item.get("evidence_sha256") or item.get("sha256")
    if not isinstance(rel,str) or not isinstance(expected,str) or not SHA256_RE.fullmatch(expected): fail("EVIDENCE_BINDING_INVALID")
    actual=sha256_file(resolve_evidence(product_root,evidence_dir,rel))
    if actual!=expected: fail(f"EVIDENCE_SHA_MISMATCH {rel} expected={expected} actual={actual}")
def verify_sidecar(path:Path)->None:
    sidecar=Path(str(path)+".sha256")
    if not sidecar.exists(): fail(f"SIDECAR_MISSING {sidecar.name}")
    text=sidecar.read_text(encoding="utf-8-sig").strip(); token=text.split()[0] if text else ""
    if token!=sha256_file(path): fail(f"SIDECAR_MISMATCH {path.name}")
def verify_required_evidence(evidence_dir:Path)->None:
    for name in REQUIRED_EVIDENCE:
        p=evidence_dir/name
        if not p.is_file(): fail(f"REQUIRED_EVIDENCE_MISSING {name}")
        verify_sidecar(p)
def verify_git_state(product_root:Path,q:dict[str,Any])->None:
    expected=q.get("source_git_head"); actual=run_git(product_root,"rev-parse","HEAD").stdout.strip()
    if actual!=expected: fail(f"PRODUCT_HEAD_MISMATCH expected={expected} actual={actual}")
    if run_git(product_root,"diff","--quiet",check=False).returncode!=0: fail("C3_PRODUCT_SOURCE_DIRTY")
    if run_git(product_root,"diff","--cached","--quiet",check=False).returncode!=0: fail("C3_PRODUCT_INDEX_DIRTY")
    actual_untracked={normalize_rel_path(x.strip()) for x in run_git(product_root,"ls-files","--others","--exclude-standard").stdout.splitlines() if x.strip()}
    declared_items=q.get("qualified_untracked_release_artifacts",[])
    if not isinstance(declared_items,list): fail("QUALIFIED_UNTRACKED_ARTIFACTS_NOT_ARRAY")
    declared={normalize_rel_path(i.get("relative_path","")) for i in declared_items if isinstance(i,dict)}
    if actual_untracked!=declared: fail(f"C3_UNTRACKED_SET_MISMATCH actual={sorted(actual_untracked)} declared={sorted(declared)}")
    for i in declared_items:
        if not isinstance(i,dict): fail("QUALIFIED_UNTRACKED_ARTIFACT_NOT_OBJECT")
        verify_file_binding(product_root,i)
def verify_qualification(product_root:Path,evidence_dir:Path,q:dict[str,Any])->None:
    if q.get("schema_version")!=1 or q.get("product_id")!="E01": fail("QUALIFICATION_IDENTITY_INVALID")
    if q.get("product_source_readonly") is not True: fail("PRODUCT_SOURCE_READONLY_NOT_TRUE")
    if q.get("product_repository_modified_by_commerce") is not False: fail("PRODUCT_REPOSITORY_MODIFIED_BY_COMMERCE")
    if q.get("tracked_worktree_clean") is not True: fail("TRACKED_WORKTREE_NOT_CLEAN")
    if q.get("source_index_clean") is not True: fail("INDEX_NOT_CLEAN")
    if q.get("license_inventory_status")!="VERIFIED": fail("C3_LICENSE_INVENTORY_NOT_VERIFIED")
    if q.get("third_party_notices_status") not in ("VERIFIED","NOT_REQUIRED_WITH_EVIDENCE"): fail("C3_THIRD_PARTY_NOTICE_NOT_VERIFIED")
    if q.get("qualification_verdict")!="C3_PRODUCT_SOURCE_QUALIFIED": fail("QUALIFICATION_VERDICT_INVALID")
    ve=q.get("version_evidence")
    if not isinstance(ve,dict): fail("C3_VERSION_EVIDENCE_MISSING")
    verify_evidence_ref(product_root,evidence_dir,ve)
    ds=q.get("deliverables")
    if not isinstance(ds,list) or not ds: fail("C3_DELIVERABLES_EMPTY")
    for i in ds:
        if not isinstance(i,dict): fail("DELIVERABLE_NOT_OBJECT")
        verify_file_binding(product_root,i)
    for i in q.get("tests",[]):
        if not isinstance(i,dict) or i.get("result")!="PASS": fail("PRODUCT_TEST_NOT_PASS")
        verify_evidence_ref(product_root,evidence_dir,i)
    for i in q.get("supported_platforms",[]):
        if not isinstance(i,dict) or i.get("status")!="VERIFIED": fail("C3_UNSUPPORTED_PLATFORM_CLAIM")
        verify_evidence_ref(product_root,evidence_dir,i)
def canonical_deliverable_map(items:list[dict[str,Any]])->dict[str,tuple[str,int]]:
    out={}
    for i in items:
        rel=normalize_rel_path(i.get("relative_path","")); sha=i.get("sha256"); size=i.get("size_bytes")
        if not isinstance(sha,str) or not SHA256_RE.fullmatch(sha) or not isinstance(size,int): fail(f"INVALID_DELIVERABLE_BINDING {rel}")
        out[rel]=(sha,size)
    return out
def verify_product_manifest(q:dict[str,Any],p:dict[str,Any])->None:
    if p.get("schema_version")!=1 or p.get("product_id")!="E01": fail("PRODUCT_MANIFEST_IDENTITY_INVALID")
    if p.get("name")!="Modbus RTU Diagnostic Toolkit": fail("PRODUCT_NAME_MISMATCH")
    if p.get("source_git_head")!=q.get("source_git_head"): fail("PRODUCT_MANIFEST_HEAD_MISMATCH")
    if p.get("version")!=q.get("version"): fail("PRODUCT_MANIFEST_VERSION_MISMATCH")
    if p.get("product_source_readonly") is not True or p.get("candidate_only") is not True: fail("PRODUCT_MANIFEST_BOUNDARY_INVALID")
    if p.get("prohibited_content_confirmed_absent") is not True: fail("PROHIBITED_CONTENT_FLAG_NOT_TRUE")
    if canonical_deliverable_map(q.get("deliverables",[]))!=canonical_deliverable_map(p.get("deliverables",[])): fail("PRODUCT_MANIFEST_DELIVERABLE_DRIFT")
def verify_claims(product_root:Path,evidence_dir:Path,p:dict[str,Any],claims:dict[str,Any])->None:
    if claims.get("schema_version")!=1 or claims.get("product_id")!="E01": fail("CLAIM_EVIDENCE_IDENTITY_INVALID")
    if claims.get("product_version")!=p.get("version"): fail("CLAIM_EVIDENCE_VERSION_MISMATCH")
    if claims.get("verdict")!="C3_LISTING_CLAIMS_EVIDENCE_BOUND": fail("CLAIM_EVIDENCE_VERDICT_INVALID")
    rows=claims.get("claims")
    if not isinstance(rows,list) or not rows: fail("CLAIMS_EMPTY")
    seen=set()
    for row in rows:
        if not isinstance(row,dict): fail("CLAIM_NOT_OBJECT")
        cid=row.get("claim_id")
        if not isinstance(cid,str) or cid in seen: fail(f"CLAIM_ID_INVALID_OR_DUPLICATE {cid}")
        seen.add(cid)
        if row.get("status")!="VERIFIED": fail(f"C3_UNVERIFIED_LISTING_CLAIM {cid}")
        verify_evidence_ref(product_root,evidence_dir,row)
def verify_candidate_flags(evidence_dir:Path)->None:
    for name in ("C3_LISTING_CANDIDATE.json","C3_XIANYU_DRAFT_BUNDLE.json"):
        d=load_json(evidence_dir/name)
        if d.get("candidate_only") is not True: fail(f"CANDIDATE_ONLY_NOT_TRUE {name}")
        if d.get("platform_action_allowed") is not False: fail(f"PLATFORM_ACTION_NOT_FALSE {name}")
def verify_rc(evidence_dir:Path,q:dict[str,Any],p:dict[str,Any],claims:dict[str,Any],rc:dict[str,Any])->None:
    if rc.get("schema_version")!=1 or rc.get("product_id")!="E01": fail("RC_IDENTITY_INVALID")
    if rc.get("product_version")!=p.get("version"): fail("RC_VERSION_MISMATCH")
    if rc.get("source_git_head")!=q.get("source_git_head"): fail("RC_HEAD_MISMATCH")
    for field,fn in (("source_qualification_sha256","C3_MODBUS_SOURCE_QUALIFICATION.json"),("product_manifest_sha256","C3_PRODUCT_MANIFEST.json"),("listing_claim_evidence_sha256","C3_LISTING_CLAIM_EVIDENCE.json"),("listing_candidate_sha256","C3_LISTING_CANDIDATE.json"),("xianyu_draft_bundle_sha256","C3_XIANYU_DRAFT_BUNDLE.json")):
        if rc.get(field)!=sha256_file(evidence_dir/fn): fail(f"RC_BINDING_MISMATCH {field}")
    if rc.get("entitlement_count")!=1 or rc.get("delivery_receipt_count")!=1: fail("RC_EXACTLY_ONCE_COUNTS_INVALID")
    if rc.get("download_grant_verified") is not True: fail("RC_DOWNLOAD_GRANT_NOT_VERIFIED")
    if rc.get("downloaded_package_sha256")!=rc.get("delivery_package_sha256"): fail("RC_DOWNLOADED_PACKAGE_SHA_MISMATCH")
    if rc.get("replay_unique_result") is not True or rc.get("recovery_unique_result") is not True: fail("RC_REPLAY_RECOVERY_NOT_UNIQUE")
    flags=rc.get("real_action_flags")
    if not isinstance(flags,dict): fail("RC_REAL_ACTION_FLAGS_MISSING")
    for k in REQUIRED_BOUNDARY_FLAGS:
        if flags.get(k) is not False: fail(f"RC_REAL_ACTION_FLAG_NOT_FALSE {k}")
    if rc.get("candidate_only") is not True: fail("RC_CANDIDATE_ONLY_NOT_TRUE")
    if rc.get("final_state")!="READY_FOR_HUMAN_DELIVERY": fail("RC_FINAL_STATE_INVALID")
    rc_sources=rc.get("source_artifacts",[])
    if not isinstance(rc_sources,list) or not rc_sources: fail("RC_SOURCE_ARTIFACTS_EMPTY")
    if canonical_deliverable_map(q.get("deliverables",[]))!=canonical_deliverable_map(rc_sources): fail("RC_SOURCE_ARTIFACT_BINDING_DRIFT")
def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--product-root",required=True,type=Path)
    ap.add_argument("--evidence-dir",required=True,type=Path)
    args=ap.parse_args()
    product_root=args.product_root.resolve(); evidence_dir=args.evidence_dir.resolve()
    if not product_root.is_dir(): fail(f"PRODUCT_ROOT_NOT_FOUND {product_root}")
    if not evidence_dir.is_dir(): fail(f"EVIDENCE_DIR_NOT_FOUND {evidence_dir}")
    verify_required_evidence(evidence_dir)
    q=load_json(evidence_dir/"C3_MODBUS_SOURCE_QUALIFICATION.json")
    p=load_json(evidence_dir/"C3_PRODUCT_MANIFEST.json")
    claims=load_json(evidence_dir/"C3_LISTING_CLAIM_EVIDENCE.json")
    rc=load_json(evidence_dir/"C3_RELEASE_CANDIDATE.json")
    verify_git_state(product_root,q)
    verify_qualification(product_root,evidence_dir,q)
    verify_product_manifest(q,p)
    verify_claims(product_root,evidence_dir,p,claims)
    verify_candidate_flags(evidence_dir)
    verify_rc(evidence_dir,q,p,claims,rc)
    print(f"C3_PRODUCT_HEAD_OK {q['source_git_head']}")
    print(f"C3_PRODUCT_VERSION_OK {q['version']}")
    print(f"C3_DELIVERABLES_OK {len(q['deliverables'])}")
    print(f"C3_LISTING_CLAIMS_OK {len(claims['claims'])}")
    print("C3_REAL_ACTION_FLAGS_OK")
    print("C3_REAL_SKU_READINESS_PASS")
    return 0
if __name__=="__main__":
    try: raise SystemExit(main())
    except VerificationError as exc:
        print(f"C3_REAL_SKU_READINESS_FAIL: {exc}",file=sys.stderr)
        raise SystemExit(2)
