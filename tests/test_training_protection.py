"""
Automated Unit Tests for Training Script Output Guards & Path Traversal Protection
Student Placement Prediction System — SRM Institute of Science and Technology
"""

import os
import sys
import hashlib
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import train_pipeline
from train_pipeline import get_model_save_path, MODELS_DIR

EXPECTED_PRODUCTION_HASH = "7330783a64173b5dadb941cc4c1342b9d89733dd63c951e151705e52a2acca17"

class TestTrainingOutputProtection(unittest.TestCase):
    def setUp(self):
        self.prod_path = os.path.realpath(os.path.join(MODELS_DIR, "best_model.pkl"))

    def test_01_default_output_targets_candidate_directory(self):
        """Verify that default training output targets models/candidates/."""
        save_path = get_model_save_path("test_candidate.pkl")
        expected_dir = os.path.realpath(os.path.join(MODELS_DIR, "candidates"))
        self.assertTrue(save_path.startswith(expected_dir))
        self.assertTrue(os.path.exists(expected_dir))
        self.assertEqual(os.path.basename(save_path), "test_candidate.pkl")

    def test_02_production_model_overwrite_blocked_by_default(self):
        """Verify that attempting to target best_model.pkl raises PermissionError without override."""
        if "ALLOW_OVERWRITE_PRODUCTION_MODEL" in os.environ:
            del os.environ["ALLOW_OVERWRITE_PRODUCTION_MODEL"]

        with self.assertRaises(PermissionError) as ctx:
            get_model_save_path("best_model.pkl", allow_production_overwrite=False)
        self.assertIn("BLOCKED", str(ctx.exception))

    def test_03_explicit_flag_allows_production_target(self):
        """Verify that explicit override allow_production_overwrite=True permits targeting best_model.pkl."""
        save_path = get_model_save_path("best_model.pkl", allow_production_overwrite=True)
        self.assertEqual(save_path, self.prod_path)

    def test_04_env_var_allows_production_target(self):
        """Verify that environment variable ALLOW_OVERWRITE_PRODUCTION_MODEL=1 permits targeting best_model.pkl."""
        os.environ["ALLOW_OVERWRITE_PRODUCTION_MODEL"] = "1"
        try:
            save_path = get_model_save_path("best_model.pkl")
            self.assertEqual(save_path, self.prod_path)
        finally:
            del os.environ["ALLOW_OVERWRITE_PRODUCTION_MODEL"]

    def test_05_production_model_artifact_remains_unmodified(self):
        """Verify that production artifact SHA-256 remains exactly unchanged."""
        self.assertTrue(os.path.exists(self.prod_path), f"Production model missing at {self.prod_path}")
        with open(self.prod_path, "rb") as f:
            current_hash = hashlib.sha256(f.read()).hexdigest().lower()
        self.assertEqual(
            current_hash,
            EXPECTED_PRODUCTION_HASH,
            f"Production model altered! Current: {current_hash}, Expected: {EXPECTED_PRODUCTION_HASH}"
        )

    # --- Path Traversal Hardening Tests (Issue 6) ---

    def test_06_reject_relative_traversal_parent_dir(self):
        """Verify path traversal with ../best_model.pkl is blocked."""
        with self.assertRaises(PermissionError) as ctx:
            get_model_save_path("../best_model.pkl", allow_production_overwrite=False)
        self.assertIn("BLOCKED", str(ctx.exception))

    def test_07_reject_relative_traversal_double_parent(self):
        """Verify path traversal with ../../models/best_model.pkl is blocked."""
        with self.assertRaises(PermissionError) as ctx:
            get_model_save_path("../../models/best_model.pkl", allow_production_overwrite=False)
        self.assertIn("BLOCKED", str(ctx.exception))

    def test_08_reject_absolute_path_to_production_model(self):
        """Verify absolute path to models/best_model.pkl is blocked."""
        with self.assertRaises(PermissionError) as ctx:
            get_model_save_path(self.prod_path, allow_production_overwrite=False)
        self.assertIn("BLOCKED", str(ctx.exception))

    def test_09_reject_traversal_to_external_directory(self):
        """Verify arbitrary path traversal outside candidates directory is blocked."""
        with self.assertRaises(PermissionError) as ctx:
            get_model_save_path("../external_exploit/model.pkl", allow_production_overwrite=False)
        self.assertIn("Path traversal detected", str(ctx.exception))

    # --- Undefined Variable Resolution Test (Issue 5) ---

    def test_10_best_model_path_variable_defined(self):
        """Verify best_model_path variable is properly defined in train_pipeline."""
        self.assertTrue(hasattr(train_pipeline, "best_model_path"))
        resolved = os.path.realpath(train_pipeline.best_model_path)
        self.assertEqual(resolved, self.prod_path)

if __name__ == "__main__":
    unittest.main(verbosity=2)
