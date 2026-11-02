"""
Unit and Integration Tests for FastAPI Placement Prediction Service
Student Placement Prediction System — SRM Institute of Science and Technology
"""

import os
import sys
import unittest
from fastapi.testclient import TestClient

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_DIR = os.path.join(PROJECT_ROOT, "api")
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

for p in (PROJECT_ROOT, API_DIR, SRC_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

from app import app
from predict import DEFAULT_MODEL_VERSION

class TestFastAPIService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_health_check(self):
        """Verify /api/health returns healthy and expected model hash."""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["model_artifact_sha256"], DEFAULT_MODEL_VERSION)
        self.assertEqual(data["features_count"], 9)

    def test_02_model_info_metrics(self):
        """Verify /api/model/info returns authoritative holdout metrics."""
        response = self.client.get("/api/model/info")
        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        metrics = data["holdout_test_metrics"]
        self.assertAlmostEqual(metrics["accuracy"], 0.8310, places=4)
        self.assertAlmostEqual(metrics["precision"], 0.8276, places=4)
        self.assertAlmostEqual(metrics["recall"], 0.9019, places=4)
        self.assertAlmostEqual(metrics["f1_score"], 0.8632, places=4)
        self.assertAlmostEqual(metrics["roc_auc"], 0.9036, places=4)
        self.assertAlmostEqual(metrics["brier_score"], 0.1158, places=4)
        self.assertEqual(len(data["valid_branches"]), 10)
        self.assertEqual(len(data["valid_tiers"]), 3)

    def test_03_sample_profiles(self):
        """Verify /api/sample-profiles returns the 5 verified profiles."""
        response = self.client.get("/api/sample-profiles")
        self.assertEqual(response.status_code, 200)
        profiles = response.json()["data"]
        self.assertEqual(len(profiles), 5)
        # Profile 4 should be High Backlog
        p4 = next(p for p in profiles if p["id"] == "profile_4")
        self.assertEqual(p4["expected_status"], "Not Placed")
        self.assertAlmostEqual(p4["expected_prob_placed"], 43.42, places=2)

    def test_04_predict_valid_student(self):
        """Verify POST /api/predict returns placement prediction and persists to history."""
        payload = {
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
        response = self.client.post("/api/predict", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertEqual(data["predicted_status"], "Placed")
        self.assertEqual(data["probability_placed"], 97.05)
        self.assertEqual(data["probability_not_placed"], 2.95)
        self.assertEqual(data["confidence_score"], 97.05)
        self.assertIsNotNone(data["history_id"])

    def test_05_predict_invalid_cgpa_rejected(self):
        """Verify POST /api/predict rejects out-of-range CGPA with 422."""
        payload = {
            "Branch": "CSE",
            "College_Tier": "Tier 1",
            "10th_Percentage": 92.0,
            "12th_Percentage": 90.0,
            "Current_CGPA": 11.5,  # Exceeds max 10.0
            "Backlogs": 0,
            "Attendance_Percentage": 92.0,
            "Projects": 4,
            "Internships": 2
        }
        response = self.client.post("/api/predict", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_06_predict_invalid_branch_rejected(self):
        """Verify POST /api/predict rejects invalid branch with 422."""
        payload = {
            "Branch": "Aerospace",  # Invalid
            "College_Tier": "Tier 1",
            "10th_Percentage": 92.0,
            "12th_Percentage": 90.0,
            "Current_CGPA": 8.5,
            "Backlogs": 0,
            "Attendance_Percentage": 85.0,
            "Projects": 2,
            "Internships": 1
        }
        response = self.client.post("/api/predict", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_07_get_history(self):
        """Verify GET /api/history returns logged predictions."""
        response = self.client.get("/api/history?limit=10")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("data", data)
        self.assertIsInstance(data["data"], list)

if __name__ == "__main__":
    unittest.main(verbosity=2)

