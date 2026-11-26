"""
W24 Single-Command Verification Entrypoint (Section 09 & 16).

Usage:
    python scripts/run_checks.py

Runs in order and fails with non-zero exit code on ANY error or if 0 tests run:
1. Repository data, reference, lookup, schema & public hygiene gates (`scripts/validate_repo.py`).
2. Standard unittest discovery across `tests/` (`python -m unittest discover -s tests -v`),
   enforcing tests_run > 0.
3. Example scenario execution (`model/compensation/compensation_engine.py`).
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    print("=== [1/3] AUTOMATED REPOSITORY QUALITY GATES ===")
    from scripts.validate_repo import run_all_validations

    ok, errors = run_all_validations(REPO_ROOT)
    if not ok:
        print(f"QUALITY GATES FAILED ({len(errors)} errors):")
        for e in errors:
            print("  -", e)
        return 1
    print("  [PASS] Source registry, rules (0 broken refs), lookups, inventories, schema & public hygiene.")

    print("\n=== [2/3] STANDARD UNITTEST DISCOVERY (tests/) ===")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(REPO_ROOT / "tests"), pattern="test_*.py", top_level_dir=str(REPO_ROOT))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.testsRun == 0:
        print("ERROR: 0 tests discovered! Refusing to report PASS.")
        return 2
    if not result.wasSuccessful():
        print(f"UNITTEST FAILED: run={result.testsRun}, failures={len(result.failures)}, errors={len(result.errors)}")
        return 1
    print(f"  [PASS] Discovered and passed {result.testsRun} test cases (0 failures, 0 errors).")

    print("\n=== [3/3] EXAMPLE SCENARIO EXECUTION ===")
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "model/compensation/compensation_engine.py")],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        print("EXAMPLE EXECUTION FAILED:")
        print(proc.stdout)
        print(proc.stderr)
        return proc.returncode
    print(proc.stdout.strip())
    print("\n=== W24 ALL CHECKS PASSED (SELF_VERIFIED) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
