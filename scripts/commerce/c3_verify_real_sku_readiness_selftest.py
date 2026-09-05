#!/usr/bin/env python3
import hashlib, json, subprocess, tempfile, sys
from pathlib import Path

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def write_json(p, obj):
    p.write_text(json.dumps(obj, indent=2, sort_keys=True)+"\n", encoding="utf-8")
def sidecar(p):
    Path(str(p)+".sha256").write_text(f"{sha(p)}  {p.name}\n", encoding="utf-8")
def git(root,*args):
    r=subprocess.run(["git","-C",str(root),*args],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if r.returncode: raise RuntimeError(r.stderr)
    return r.stdout.strip()
def run_verify(script, product, ev, expected=0, needle=None):
    r=subprocess.run([sys.executable,str(script),"--product-root",str(product),"--evidence-dir",str(ev)],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if r.returncode!=expected:
        raise AssertionError(f"expected {expected} got {r.returncode}\nOUT={r.stdout}\nERR={r.stderr}")
    text=r.stdout+r.stderr
    if needle and needle not in text:
        raise AssertionError(f"missing {needle}\n{text}")
    return text

if len(sys.argv) != 2:
    raise SystemExit("usage: c3_verify_real_sku_readiness_selftest.py <verifier.py>")

with tempfile.TemporaryDirectory() as td:
    root=Path(td)
    product=root/"product"; ev=root/"evidence"; product.mkdir(); ev.mkdir()
    (product/"version.txt").write_text("1.0.0\n",encoding="utf-8")
    (product/"test.log").write_text("PASS\n",encoding="utf-8")
    (product/"support.md").write_text("Windows 11 smoke tested\n",encoding="utf-8")
    (product/"LICENSES.csv").write_text("name,version,license\nx,1,MIT\n",encoding="utf-8")
    git(product,"init")
    git(product,"config","user.email","test@example.invalid"); git(product,"config","user.name","C3 Selftest")
    git(product,"add","version.txt","test.log","support.md","LICENSES.csv"); git(product,"commit","-m","baseline")
    (product/"dist").mkdir(); artifact=product/"dist"/"tool.zip"; artifact.write_bytes(b"FAKE-MODBUS-RELEASE\n")
    head=git(product,"rev-parse","HEAD")
    art={"role":"portable_zip","relative_path":"dist/tool.zip","sha256":sha(artifact),"size_bytes":artifact.stat().st_size,"media_type":"application/zip","authenticode_status":"NOT_APPLICABLE"}
    q={"schema_version":1,"product_id":"E01","source_repository_path":str(product),"source_git_head":head,"tracked_worktree_clean":True,"source_index_clean":True,"qualified_untracked_release_artifacts":[art],"product_source_readonly":True,"product_repository_modified_by_commerce":False,"version":"1.0.0","version_evidence":{"relative_path":"version.txt","sha256":sha(product/"version.txt")},"deliverables":[art],"tests":[{"name":"smoke","result":"PASS","evidence_path":"test.log","evidence_sha256":sha(product/"test.log")}],"supported_platforms":[{"platform":"Windows 11","status":"VERIFIED","evidence_path":"support.md","evidence_sha256":sha(product/"support.md")}],"license_inventory_status":"VERIFIED","third_party_notices_status":"NOT_REQUIRED_WITH_EVIDENCE","known_limitations":[],"support_boundary":"Synthetic selftest","authenticode_status":"NOT_VERIFIED","smart_screen_status":"NOT_A_GUARANTEE","qualification_verdict":"C3_PRODUCT_SOURCE_QUALIFIED"}
    p={"schema_version":1,"product_id":"E01","name":"Modbus RTU Diagnostic Toolkit","version":"1.0.0","owner":"Jovi","rights_status":"original_plus_licensed_dependencies","prohibited_content_confirmed_absent":True,"source_git_head":head,"supported_platforms":[{"name":"Windows 11","status":"VERIFIED","evidence_ref":"C3-CLAIM-001"}],"deliverables":[{k:art[k] for k in ("role","relative_path","sha256","size_bytes")}],"acceptance_criteria":[{"criterion":"smoke","status":"PASS","evidence_ref":"test.log"}],"third_party_dependencies":[],"support_boundary":"Synthetic selftest","known_limitations":[],"product_source_readonly":True,"candidate_only":True}
    claims={"schema_version":1,"product_id":"E01","product_version":"1.0.0","claims":[{"claim_id":"C3-CLAIM-001","claim_text":"Windows 11 smoke tested","claim_type":"compatibility","status":"VERIFIED","evidence_type":"file","evidence_path":"support.md","evidence_sha256":sha(product/"support.md")}],"omitted_unverified_claims":[],"verdict":"C3_LISTING_CLAIMS_EVIDENCE_BOUND"}
    write_json(ev/"C3_MODBUS_SOURCE_QUALIFICATION.json",q)
    write_json(ev/"C3_PRODUCT_MANIFEST.json",p)
    write_json(ev/"C3_LISTING_CLAIM_EVIDENCE.json",claims)
    write_json(ev/"C3_LISTING_CANDIDATE.json",{"candidate_only":True,"platform_action_allowed":False})
    write_json(ev/"C3_XIANYU_DRAFT_BUNDLE.json",{"candidate_only":True,"platform_action_allowed":False})
    for name in ("C3_DIGITAL_RELEASE.json","C3_DELIVERY_PACKAGE_MANIFEST.json","C3_SYNTHETIC_ORDER_RESULT.json","C3_NEGATIVE_TEST_RESULTS.json","C3_REPLAY_RECOVERY_RESULT.json","C3_ADMIN_E2E_RESULT.json","C3_SOURCE_MANIFEST.json","C3_ROLLBACK_PLAN.json"):
        write_json(ev/name,{"selftest":True})
    (ev/"C3_INDEPENDENT_AUDIT_PROMPT.md").write_text("# selftest\n",encoding="utf-8")
    package_sha="a"*64
    rc={"schema_version":1,"rc_id":"c3_rc_selftest","product_id":"E01","product_version":"1.0.0","source_git_head":head,"source_qualification_sha256":sha(ev/"C3_MODBUS_SOURCE_QUALIFICATION.json"),"product_manifest_sha256":sha(ev/"C3_PRODUCT_MANIFEST.json"),"listing_claim_evidence_sha256":sha(ev/"C3_LISTING_CLAIM_EVIDENCE.json"),"digital_release_id":"release_selftest","source_artifacts":[{k:art[k] for k in ("relative_path","sha256","size_bytes")}],"delivery_package_sha256":package_sha,"listing_candidate_sha256":sha(ev/"C3_LISTING_CANDIDATE.json"),"xianyu_draft_bundle_sha256":sha(ev/"C3_XIANYU_DRAFT_BUNDLE.json"),"synthetic_order_id":"order_selftest","synthetic_payment_evidence_sha256":"b"*64,"entitlement_count":1,"delivery_receipt_count":1,"download_grant_verified":True,"downloaded_package_sha256":package_sha,"replay_unique_result":True,"recovery_unique_result":True,"real_action_flags":{"production_integration_allowed":False,"real_payment":False,"real_customer":False,"xianyu":False,"auto_delivery":False,"n8n_production":False},"candidate_only":True,"final_state":"READY_FOR_HUMAN_DELIVERY"}
    write_json(ev/"C3_RELEASE_CANDIDATE.json",rc)
    for name in ["C3_MODBUS_SOURCE_QUALIFICATION.json","C3_PRODUCT_MANIFEST.json","C3_LISTING_CLAIM_EVIDENCE.json","C3_DIGITAL_RELEASE.json","C3_DELIVERY_PACKAGE_MANIFEST.json","C3_LISTING_CANDIDATE.json","C3_XIANYU_DRAFT_BUNDLE.json","C3_SYNTHETIC_ORDER_RESULT.json","C3_NEGATIVE_TEST_RESULTS.json","C3_REPLAY_RECOVERY_RESULT.json","C3_ADMIN_E2E_RESULT.json","C3_RELEASE_CANDIDATE.json","C3_SOURCE_MANIFEST.json","C3_ROLLBACK_PLAN.json","C3_INDEPENDENT_AUDIT_PROMPT.md"]:
        sidecar(ev/name)
    run_verify(Path(sys.argv[1]),product,ev,0,"C3_REAL_SKU_READINESS_PASS")
    (product/"support.md").write_text("tampered\n",encoding="utf-8")
    run_verify(Path(sys.argv[1]),product,ev,2,"C3_PRODUCT_SOURCE_DIRTY")
    git(product,"checkout","--","support.md")
    rc=json.loads((ev/"C3_RELEASE_CANDIDATE.json").read_text())
    rc["real_action_flags"]["real_payment"]=True
    write_json(ev/"C3_RELEASE_CANDIDATE.json",rc); sidecar(ev/"C3_RELEASE_CANDIDATE.json")
    run_verify(Path(sys.argv[1]),product,ev,2,"RC_REAL_ACTION_FLAG_NOT_FALSE real_payment")
print("C3_VERIFIER_SELFTEST_PASS")
