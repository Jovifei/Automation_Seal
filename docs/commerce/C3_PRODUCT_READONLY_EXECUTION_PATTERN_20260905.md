# C3 Product Read-Only Execution Pattern

## Why this exists

Running tests or packaging commands directly inside the real product repository can create `__pycache__`, `.pytest_cache`, logs, build directories, or other untracked files. Deleting those files afterward would still mean Commerce wrote into the product source and would invalidate the C3 zero-write guarantee.

Therefore C3 separates **source qualification** from **test execution**.

## Source repository operations allowed

Against:

`E:\project\jovi-modbus-diagnostic-toolkit-v1`

C3 may only perform read-only operations such as:

- `git rev-parse HEAD`
- `git diff --quiet`
- `git diff --cached --quiet`
- `git ls-files`
- `git ls-files --others --exclude-standard`
- read files
- compute hashes/sizes
- inspect PE/installer metadata without modifying the file

No test, build, formatter, package manager, installer compiler, or application launch should run with the real product repository as its working directory if it may create files.

## Test sandbox

For tests requiring source execution:

1. Record source HEAD and source-state snapshot first.
2. Create a temporary local clone/export outside the product root. Preferred pattern:
   - `git clone --no-local --no-hardlinks <product-root> <temp-test-root>`; or
   - a read-only `git archive HEAD` export if repository structure permits.
3. Verify the sandbox HEAD equals the qualified product HEAD.
4. Run canonical tests in the sandbox.
5. Write test logs into the C3 Commerce evidence directory, not the product repository.
6. Hash test logs and bind them into `C3_MODBUS_SOURCE_QUALIFICATION.json`.
7. Delete the temporary sandbox only after evidence is frozen.

If dependencies are not already available, dependency installation belongs in the sandbox/isolated environment. It must not modify the product source repository.

## Existing release artifacts

If an installer/portable ZIP is an untracked generated artifact in the product repository:

1. list it explicitly in `qualified_untracked_release_artifacts`;
2. record SHA256 and size before C3 work;
3. copy it to a C3 staging/private asset location only after hash verification;
4. never overwrite/rebuild it from Commerce;
5. at the end recompute the original product-root artifact SHA/size and prove it is unchanged.

## Application/installer smoke

If launching the existing application/installer creates files in the product directory, perform the smoke test on a copied artifact outside the product root.

Capture:

- artifact source SHA;
- copied artifact SHA before launch;
- smoke command/action;
- result;
- evidence/log/screenshot SHA;
- copied artifact SHA after launch when relevant.

The smoke environment may write to normal Windows user/temp locations, but C3 must not infer compatibility claims beyond the environment actually tested.

## Zero-write finish proof

Before C3 starts and immediately before evidence freeze, capture:

- HEAD;
- tracked diff status;
- index status;
- exact untracked file set;
- exact SHA/size of qualified untracked release artifacts.

The two states must match exactly and `product_repo_write_attempts=0`.

Required verdict:

`PASS_ZERO_WRITE`

If the product repository changes for any reason, C3 stops. Do not clean/reset the product repo to conceal the change; investigate and restart C3 from a fresh qualification baseline.
