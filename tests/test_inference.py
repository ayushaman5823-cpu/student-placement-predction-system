"""
Unit and Integration Tests for Student Placement Prediction System.
Can be executed with pytest or standard python runner:
    pytest tests/
    python tests/test_inference.py
"""

import os
import sys
import json
import hashlib
import unittest
import pandas as pd

# Add project root and src to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from predict import StudentPlacementPredictor, REQUIRED_FEATURES, DEFAULT_MODEL_VERSION

EXPECTED_MODEL_SHA256 = "7330783a64173b5dadb941cc4c1342b9d89733dd63c951e151705e52a2acca17"

class TestPlacementPredictionSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model_path = os.path.join(PROJECT_ROOT, "models", "best_model.pkl")
        cls.fixtures_json = os.path.join(PROJECT_ROOT, "tests", "fixtures", "sample_students.json")
        cls.fixtures_csv = os.path.join(PROJECT_ROOT, "tests", "fixtures", "sample_students.csv")
        cls.predictor = StudentPlacementPredictor(model_path=cls.model_path)

    def test_01_model_artifact_integrity(self):
        """Verify model file exists and SHA256 matches frozen production hash."""
        self.assertTrue(os.path.exists(self.model_path), f"Model not found at {self.model_path}")
        with open(self.model_path, "rb") as f:
            computed_hash = hashlib.sha256(f.read()).hexdigest().lower()
        self.assertEqual(
            computed_hash,
            EXPECTED_MODEL_SHA256.lower(),
            f"Model SHA256 mismatch! Got: {computed_hash}, Expected: {EXPECTED_MODEL_SHA256}"
        )

    def test_02_feature_contract(self):
        """Verify that REQUIRED_FEATURES contains exactly the 9 authorized features."""
        expected_9 = [
            'Branch', 'College_Tier', '10th_Percentage', '12th_Percentage',
            'Current_CGPA', 'Backlogs', 'Attendance_Percentage', 'Projects', 'Internships'
        ]
        self.assertEqual(REQUIRED_FEATURES, expected_9)

    def test_03_single_student_prediction_contract(self):
        """Test single student prediction output types, range, and probability sum."""
        sample_student = {
            "Branch": "CSE",
            "College_Tier": "Tier 1",
            "10th_Percentage": 92.0,
            "12th_Percentage": 90.0,
            "Current_CGPA": 9.20,
            "Backlogs": 0,
            "Attendance_Percentage": 92.0,
            "Projects": 4,
            "Internships": 2
        }
        res = self.predictor.predict_student(sample_student)

        self.assertIn("predicted_status", res)
        self.assertIn("probability_placed", res)
        self.assertIn("probability_not_placed", res)
        self.assertIn("confidence_score", res)
        self.assertIn("model_version", res)

        self.assertIn(res["predicted_status"], ["Placed", "Not Placed"])
        self.assertTrue(0.0 <= res["probability_placed"] <= 100.0)
        self.assertTrue(0.0 <= res["probability_not_placed"] <= 100.0)
        prob_sum = res["probability_placed"] + res["probability_not_placed"]
        self.assertAlmostEqual(prob_sum, 100.0, places=1)
        self.assertEqual(res["confidence_score"], max(res["probability_placed"], res["probability_not_placed"]))
        self.assertEqual(res["model_version"], EXPECTED_MODEL_SHA256)

    def test_04_batch_fixtures_json(self):
        """Run all 5 diverse fixtures from JSON and assert validity."""
        self.assertTrue(os.path.exists(self.fixtures_json))
        with open(self.fixtures_json, "r", encoding="utf-8-sig") as f:
            profiles = json.load(f)

        self.assertEqual(len(profiles), 5)
        for p in profiles:
            feats = p["features"]
            res = self.predictor.predict_student(feats)
            self.assertIn(res["predicted_status"], ["Placed", "Not Placed"])
            self.assertAlmostEqual(res["probability_placed"] + res["probability_not_placed"], 100.0, places=1)

    def test_05_batch_dataframe_fixtures_csv(self):
        """Run batch inference from CSV fixture."""
        self.assertTrue(os.path.exists(self.fixtures_csv))
        df = pd.read_csv(self.fixtures_csv)
        self.assertEqual(len(df), 5)
        df_res = self.predictor.predict_batch(df)

        self.assertIn("predicted_Placement_Status", df_res.columns)
        self.assertIn("probability_Placed", df_res.columns)
        self.assertIn("probability_Not_Placed", df_res.columns)
        self.assertTrue(all(status in ["Placed", "Not Placed"] for status in df_res["predicted_Placement_Status"]))

    def test_06_missing_required_feature_raises_error(self):
        """Assert KeyError when input is missing a required feature."""
        incomplete_input = {
            "Branch": "CSE",
            "College_Tier": "Tier 1",
            "10th_Percentage": 92.0,
            "12th_Percentage": 90.0,
            # Missing Current_CGPA
            "Backlogs": 0,
            "Attendance_Percentage": 92.0,
            "Projects": 4,
            "Internships": 2
        }
        with self.assertRaises(KeyError):
            self.predictor.predict_student(incomplete_input)

    # --- Issue 2: High-Backlog Reconciliation Test ---

    def test_07_high_backlog_sample_reconciliation(self):
        """
        Verify exact prediction on High Backlog profile:
        IT, Tier 2, 10th: 74%, 12th: 72%, CGPA: 7.20, Backlogs: 5, Attendance: 80%, Projects: 2, Internships: 1.
        Authoritative frozen model yields 43.42% Placed, 56.58% Not Placed (Status: Not Placed).
        """
        high_backlog_profile = {
            "Branch": "IT",
            "College_Tier": "Tier 2",
            "10th_Percentage": 74.0,
            "12th_Percentage": 72.0,
            "Current_CGPA": 7.20,
            "Backlogs": 5,
            "Attendance_Percentage": 80.0,
            "Projects": 2,
            "Internships": 1
        }
        res = self.predictor.predict_student(high_backlog_profile)
        self.assertEqual(res["predicted_status"], "Not Placed")
        self.assertEqual(res["probability_placed"], 43.42)
        self.assertEqual(res["probability_not_placed"], 56.58)
        self.assertEqual(res["confidence_score"], 56.58)

    def test_08_model_version_identifier_consistency(self):
        """Verify model_version matches immutable artifact SHA256 exactly."""
        self.assertEqual(self.predictor.model_version, EXPECTED_MODEL_SHA256)
        self.assertEqual(DEFAULT_MODEL_VERSION, EXPECTED_MODEL_SHA256)

if __name__ == "__main__":
    unittest.main(verbosity=2)
