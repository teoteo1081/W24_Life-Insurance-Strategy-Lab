"""
Tests for Automated Repository Quality Gates (scripts/validate_repo.py).

Verifies both:
1. Current repository passes all validation gates.
2. Seeded negative fixtures (duplicate Rule_ID, broken Rule_ID ref, invalid rights enum,
   local Windows path leak, secret pattern leak) are accurately caught!
"""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.validate_repo import (
    run_all_validations,
    validate_business_rules,
    validate_public_hygiene,
    validate_source_registry,
)


class TestQualityGates(unittest.TestCase):
    def test_current_repo_passes_all_gates(self) -> None:
        ok, errors = run_all_validations(REPO_ROOT)
        self.assertTrue(ok, f"Current repo failed quality gates: {errors}")

    def test_validator_catches_seeded_rule_defects(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rules_dir = root / "knowledge/business-rules"
            rules_dir.mkdir(parents=True)
            (rules_dir / "business-rules-catalog.csv").write_text(
                "Rule_ID,Scheme_ID,Source_ID_And_Page,Stacking_Rule,Source_Verification,Implementation_Status,Calculation_Verification\n"
                "AIA-CV-001,AIA,SRC-001 p.1,Ref AIA-CV-999,SOURCE_VERIFIED,IMPLEMENTED,TESTED_PASS\n"
                "AIA-CV-001,AIA,,None,INVALID_ENUM,IMPLEMENTED,TESTED_PASS\n",
                encoding="utf-8",
            )
            errs = validate_business_rules(root)
            joined = "\n".join(errs)
            self.assertIn("duplicate Rule_ID", joined)
            self.assertIn("broken Rule_ID reference -> AIA-CV-999", joined)
            self.assertIn("empty Source_ID_And_Page", joined)
            self.assertIn("invalid Source_Verification", joined)

    def test_validator_catches_seeded_invalid_rights_enum(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src_dir = root / "knowledge/sources"
            src_dir.mkdir(parents=True)
            (src_dir / "source-registry.csv").write_text(
                "Source_ID,Original_Filename,Local_Relative_Path,SHA256_Hash,Company,Document_Type,Revision_Class,Confidentiality,Redistribution_Rights_Status,Verification_Status\n"
                "SRC-X,file.pdf,docs/x.md,N/A,Co,Policy,Main,Internal,BAD_RIGHTS,VERIFIED_FACT\n",
                encoding="utf-8",
            )
            errs = validate_source_registry(root)
            self.assertTrue(any("invalid Redistribution_Rights_Status" in e for e in errs))

    def test_validator_catches_seeded_hygiene_leaks(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            bad_doc = root / "bad.md"
            bad_doc.write_text("Link: file:///C:/Users/Test/doc.md\nToken: ghp_1234567890abcdefghij123456\n", encoding="utf-8")
            errs = validate_public_hygiene(root, text_files=[bad_doc])
            joined = "\n".join(errs)
            self.assertIn("abs_local_path", joined)
            self.assertIn("secret_pattern", joined)


if __name__ == "__main__":
    unittest.main(verbosity=2)
