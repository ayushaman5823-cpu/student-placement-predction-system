"""
Automated Unit Tests for SQLite Prediction History Store
Student Placement Prediction System — SRM Institute of Science and Technology
"""

import os
import sys
import unittest
import tempfile
import sqlite3

SRC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from history_store import (
    init_db, save_prediction, get_history, get_prediction_by_id,
    clear_history, get_db_connection, DEFAULT_MODEL_VERSION
)

class TestHistoryStore(unittest.TestCase):
    def setUp(self):
        # Create a fresh temporary file for isolated database tests
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()

        self.sample_features = {
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

    def tearDown(self):
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except Exception:
                pass

    def test_01_init_db(self):
        """Verify database initialization creates table cleanly."""
        init_db(self.db_path)
        history = get_history(db_path=self.db_path)
        self.assertEqual(history, [])

    def test_02_save_and_retrieve_single_prediction(self):
        """Verify saving and retrieving a single prediction with confidence score and model version."""
        rec_id = save_prediction(
            student_features=self.sample_features,
            predicted_status="Placed",
            probability_placed=98.50,
            probability_not_placed=1.50,
            confidence_score=98.50,
            model_version=DEFAULT_MODEL_VERSION,
            db_path=self.db_path
        )
        self.assertIsInstance(rec_id, int)
        self.assertGreater(rec_id, 0)

        # Retrieve by ID
        rec = get_prediction_by_id(rec_id, db_path=self.db_path)
        self.assertIsNotNone(rec)
        self.assertEqual(rec['id'], rec_id)
        self.assertEqual(rec['predicted_status'], "Placed")
        self.assertEqual(rec['probability_placed'], 98.50)
        self.assertEqual(rec['probability_not_placed'], 1.50)
        self.assertEqual(rec['confidence_score'], 98.50)
        self.assertEqual(rec['model_version'], DEFAULT_MODEL_VERSION)
        self.assertEqual(rec['student_features'], self.sample_features)
        self.assertTrue('created_at' in rec)

    def test_03_reverse_chronological_ordering(self):
        """Verify get_history returns records newest first."""
        id1 = save_prediction(
            student_features=dict(self.sample_features, Branch="ECE"),
            predicted_status="Placed",
            probability_placed=85.0,
            probability_not_placed=15.0,
            db_path=self.db_path
        )
        id2 = save_prediction(
            student_features=dict(self.sample_features, Branch="Civil"),
            predicted_status="Not Placed",
            probability_placed=20.0,
            probability_not_placed=80.0,
            db_path=self.db_path
        )
        id3 = save_prediction(
            student_features=dict(self.sample_features, Branch="IT"),
            predicted_status="Placed",
            probability_placed=90.0,
            probability_not_placed=10.0,
            db_path=self.db_path
        )

        history = get_history(limit=10, db_path=self.db_path)
        self.assertEqual(len(history), 3)
        self.assertEqual([h['id'] for h in history], [id3, id2, id1])
        self.assertEqual(history[0]['branch'], "IT")
        self.assertEqual(history[1]['branch'], "Civil")
        self.assertEqual(history[2]['branch'], "ECE")

    def test_04_get_nonexistent_id_returns_none(self):
        """Verify querying non-existent record returns None."""
        init_db(self.db_path)
        rec = get_prediction_by_id(999999, db_path=self.db_path)
        self.assertIsNone(rec)

    def test_05_clear_history(self):
        """Verify clear_history empties the table."""
        save_prediction(self.sample_features, "Placed", 95.0, 5.0, db_path=self.db_path)
        self.assertEqual(len(get_history(db_path=self.db_path)), 1)
        clear_history(db_path=self.db_path)
        self.assertEqual(len(get_history(db_path=self.db_path)), 0)

    def test_06_connection_persistence_multi_connection(self):
        """Verify persistence across distinct database connections using temporary file."""
        # Connection 1: initialize and insert
        conn1 = get_db_connection(self.db_path)
        init_db(self.db_path)
        rec_id = save_prediction(
            student_features=self.sample_features,
            predicted_status="Placed",
            probability_placed=92.0,
            probability_not_placed=8.0,
            db_path=self.db_path
        )
        conn1.close()

        # Connection 2: open new connection to same database file and verify record
        conn2 = get_db_connection(self.db_path)
        cursor = conn2.execute("SELECT * FROM prediction_history WHERE id = ?", (rec_id,))
        row = cursor.fetchone()
        conn2.close()

        self.assertIsNotNone(row)
        self.assertEqual(row['predicted_status'], "Placed")
        self.assertEqual(row['probability_placed'], 92.0)
        self.assertEqual(row['probability_not_placed'], 8.0)
        self.assertEqual(row['confidence_score'], 92.0)
        self.assertEqual(row['model_version'], DEFAULT_MODEL_VERSION)

    # --- Negative Validation Tests (Issue 3) ---

    def test_07_reject_non_dict_features(self):
        """Verify non-dict features raise TypeError."""
        with self.assertRaises(TypeError):
            save_prediction(["CSE", "Tier 1"], "Placed", 90.0, 10.0, db_path=self.db_path)

    def test_08_reject_missing_feature(self):
        """Verify missing feature raises ValueError."""
        incomplete = dict(self.sample_features)
        del incomplete["Branch"]
        with self.assertRaises(ValueError) as ctx:
            save_prediction(incomplete, "Placed", 90.0, 10.0, db_path=self.db_path)
        self.assertIn("Missing required feature", str(ctx.exception))

    def test_09_reject_extra_feature(self):
        """Verify unauthorized extra feature raises ValueError."""
        extra = dict(self.sample_features, Student_ID="12345")
        with self.assertRaises(ValueError) as ctx:
            save_prediction(extra, "Placed", 90.0, 10.0, db_path=self.db_path)
        self.assertIn("Unexpected extra feature", str(ctx.exception))

    def test_10_reject_invalid_branch(self):
        """Verify invalid branch category raises ValueError."""
        invalid = dict(self.sample_features, Branch="Aeronautical")
        with self.assertRaises(ValueError) as ctx:
            save_prediction(invalid, "Placed", 90.0, 10.0, db_path=self.db_path)
        self.assertIn("Invalid Branch", str(ctx.exception))

    def test_11_reject_invalid_college_tier(self):
        """Verify invalid tier category raises ValueError."""
        invalid = dict(self.sample_features, College_Tier="Tier 4")
        with self.assertRaises(ValueError) as ctx:
            save_prediction(invalid, "Placed", 90.0, 10.0, db_path=self.db_path)
        self.assertIn("Invalid College_Tier", str(ctx.exception))

    def test_12_reject_cgpa_out_of_bounds(self):
        """Verify CGPA above 10.0 or below 0.0 raises ValueError."""
        with self.assertRaises(ValueError):
            save_prediction(dict(self.sample_features, Current_CGPA=10.5), "Placed", 90.0, 10.0, db_path=self.db_path)
        with self.assertRaises(ValueError):
            save_prediction(dict(self.sample_features, Current_CGPA=-1.0), "Placed", 90.0, 10.0, db_path=self.db_path)

    def test_13_reject_negative_backlogs(self):
        """Verify negative backlogs raise ValueError."""
        with self.assertRaises(ValueError):
            save_prediction(dict(self.sample_features, Backlogs=-1), "Placed", 90.0, 10.0, db_path=self.db_path)

    def test_14_reject_fractional_counts(self):
        """Verify fractional project/backlog counts raise ValueError."""
        with self.assertRaises(ValueError):
            save_prediction(dict(self.sample_features, Projects=2.5), "Placed", 90.0, 10.0, db_path=self.db_path)
        with self.assertRaises(ValueError):
            save_prediction(dict(self.sample_features, Backlogs=1.2), "Placed", 90.0, 10.0, db_path=self.db_path)

    def test_15_reject_boolean_features(self):
        """Verify boolean values in numeric features raise TypeError."""
        with self.assertRaises(TypeError):
            save_prediction(dict(self.sample_features, Backlogs=True), "Placed", 90.0, 10.0, db_path=self.db_path)

    def test_16_reject_nan_and_infinity_features(self):
        """Verify NaN and Inf features raise ValueError."""
        with self.assertRaises(ValueError):
            save_prediction(dict(self.sample_features, Current_CGPA=float('nan')), "Placed", 90.0, 10.0, db_path=self.db_path)
        with self.assertRaises(ValueError):
            save_prediction(dict(self.sample_features, Attendance_Percentage=float('inf')), "Placed", 90.0, 10.0, db_path=self.db_path)

    def test_17_reject_invalid_predicted_status(self):
        """Verify invalid predicted_status raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            save_prediction(self.sample_features, "Maybe", 90.0, 10.0, db_path=self.db_path)
        self.assertIn("predicted_status", str(ctx.exception))

    def test_18_reject_negative_probability(self):
        """Verify negative probability raises ValueError."""
        with self.assertRaises(ValueError):
            save_prediction(self.sample_features, "Placed", -5.0, 105.0, db_path=self.db_path)

    def test_19_reject_probability_above_100(self):
        """Verify probability exceeding 100.0 raises ValueError."""
        with self.assertRaises(ValueError):
            save_prediction(self.sample_features, "Placed", 105.0, -5.0, db_path=self.db_path)

    def test_20_reject_probabilities_not_summing_to_100(self):
        """Verify probabilities that do not sum to 100.0% raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            save_prediction(self.sample_features, "Placed", 80.0, 10.0, db_path=self.db_path)
        self.assertIn("sum to 100.0%", str(ctx.exception))

    def test_21_reject_contradictory_confidence_score(self):
        """Verify passed confidence score contradicting max probability raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            save_prediction(
                self.sample_features, "Placed", 90.0, 10.0,
                confidence_score=50.0, db_path=self.db_path
            )
        self.assertIn("contradicts maximum class probability", str(ctx.exception))

    def test_22_reject_missing_model_identifier(self):
        """Verify missing or empty model version raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            save_prediction(
                self.sample_features, "Placed", 90.0, 10.0,
                model_version="", db_path=self.db_path
            )
        self.assertIn("Model version/identifier", str(ctx.exception))

    def test_23_failed_insertion_does_not_create_partial_record(self):
        """Verify failed validation leaves zero records in database."""
        init_db(self.db_path)
        try:
            save_prediction(
                dict(self.sample_features, Current_CGPA=99.9),
                "Placed", 90.0, 10.0, db_path=self.db_path
            )
        except ValueError:
            pass
        self.assertEqual(len(get_history(db_path=self.db_path)), 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
