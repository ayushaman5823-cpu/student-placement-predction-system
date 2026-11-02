"""
Automated Unit Tests for Centralized Input Validation
Student Placement Prediction System â€” SRM Institute of Science and Technology
"""

import math
import unittest
import numpy as np
import pandas as pd
import sys
import os

# Add src to path
SRC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from predict import validate_student_input, StudentPlacementPredictor, REQUIRED_FEATURES, NUMERICAL_CONSTRAINTS

class TestInputValidation(unittest.TestCase):
    def setUp(self):
        self.valid_profile = {
            "Branch": "CSE",
            "College_Tier": "Tier 1",
            "10th_Percentage": 85.5,
            "12th_Percentage": 82.0,
            "Current_CGPA": 8.5,
            "Backlogs": 0,
            "Attendance_Percentage": 90.0,
            "Projects": 3,
            "Internships": 2
        }

    def test_01_valid_profile_passes(self):
        """Test that a completely valid profile passes validation."""
        is_valid, msg = validate_student_input(self.valid_profile, raise_exception=False)
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")

        # Also with raise_exception=True
        self.assertTrue(validate_student_input(self.valid_profile, raise_exception=True))

    def test_02_missing_field_raises_key_error(self):
        """Test that omission of any required field raises KeyError."""
        for field in REQUIRED_FEATURES:
            incomplete = dict(self.valid_profile)
            del incomplete[field]
            with self.assertRaises(KeyError):
                validate_student_input(incomplete, raise_exception=True)

    def test_03_extra_unauthorized_field_raises_value_error(self):
        """Test that unauthorized columns (e.g., Student_ID, Placement_Probability) are rejected."""
        unauthorized_inputs = [
            {"Student_ID": "STU1001"},
            {"Name": "Student One"},
            {"Gender": "Male"},
            {"College_Name": "SRM University"},
            {"Placement_Probability": 85.0},
            {"Random_Col": 123}
        ]
        for extra in unauthorized_inputs:
            profile_with_extra = dict(self.valid_profile, **extra)
            with self.assertRaises(ValueError):
                validate_student_input(profile_with_extra, raise_exception=True)

    def test_04_invalid_branch_rejected(self):
        """Test rejection of non-existent branches."""
        invalid = dict(self.valid_profile, Branch="Aerospace")
        with self.assertRaises(ValueError):
            validate_student_input(invalid, raise_exception=True)

    def test_05_invalid_college_tier_rejected(self):
        """Test rejection of unlisted college tiers."""
        invalid = dict(self.valid_profile, College_Tier="Tier 4")
        with self.assertRaises(ValueError):
            validate_student_input(invalid, raise_exception=True)

    def test_06_cgpa_bounds(self):
        """Test rejection of CGPA < 0 or > 10."""
        # > 10
        with self.assertRaises(ValueError):
            validate_student_input(dict(self.valid_profile, Current_CGPA=10.5), raise_exception=True)
        # < 0
        with self.assertRaises(ValueError):
            validate_student_input(dict(self.valid_profile, Current_CGPA=-0.5), raise_exception=True)
        # Boundary 0.0 and 10.0 should pass
        self.assertTrue(validate_student_input(dict(self.valid_profile, Current_CGPA=0.0)))
        self.assertTrue(validate_student_input(dict(self.valid_profile, Current_CGPA=10.0)))

    def test_07_percentage_bounds(self):
        """Test 10th, 12th, and Attendance percentage bounds (0 to 100)."""
        pct_fields = ["10th_Percentage", "12th_Percentage", "Attendance_Percentage"]
        for f in pct_fields:
            with self.assertRaises(ValueError):
                validate_student_input(dict(self.valid_profile, **{f: 100.1}), raise_exception=True)
            with self.assertRaises(ValueError):
                validate_student_input(dict(self.valid_profile, **{f: -1.0}), raise_exception=True)

    def test_08_integer_count_bounds(self):
        """Test bounds for Backlogs (0-5), Projects (0-5), and Internships (0-4)."""
        # Backlogs
        with self.assertRaises(ValueError):
            validate_student_input(dict(self.valid_profile, Backlogs=6), raise_exception=True)
        with self.assertRaises(ValueError):
            validate_student_input(dict(self.valid_profile, Backlogs=-1), raise_exception=True)

        # Projects
        with self.assertRaises(ValueError):
            validate_student_input(dict(self.valid_profile, Projects=6), raise_exception=True)
        with self.assertRaises(ValueError):
            validate_student_input(dict(self.valid_profile, Projects=-1), raise_exception=True)

        # Internships
        with self.assertRaises(ValueError):
            validate_student_input(dict(self.valid_profile, Internships=5), raise_exception=True)
        with self.assertRaises(ValueError):
            validate_student_input(dict(self.valid_profile, Internships=-1), raise_exception=True)

    def test_09_fractional_integer_values_rejected(self):
        """Test that fractional values for count fields are rejected."""
        count_fields = [("Backlogs", 1.5), ("Projects", 2.2), ("Internships", 0.5)]
        for f, val in count_fields:
            with self.assertRaises(ValueError):
                validate_student_input(dict(self.valid_profile, **{f: val}), raise_exception=True)

    def test_10_boolean_values_rejected_for_numerics(self):
        """Test that Python booleans (True/False) are explicitly rejected for numerical features."""
        for f in NUMERICAL_CONSTRAINTS:
            with self.assertRaises(TypeError):
                validate_student_input(dict(self.valid_profile, **{f: True}), raise_exception=True)
            with self.assertRaises(TypeError):
                validate_student_input(dict(self.valid_profile, **{f: False}), raise_exception=True)

    def test_11_nan_and_infinity_rejected(self):
        """Test rejection of NaN and Inf in numerical columns."""
        for f in ["10th_Percentage", "Current_CGPA", "Attendance_Percentage"]:
            with self.assertRaises(ValueError):
                validate_student_input(dict(self.valid_profile, **{f: float('nan')}), raise_exception=True)
            with self.assertRaises(ValueError):
                validate_student_input(dict(self.valid_profile, **{f: float('inf')}), raise_exception=True)
            with self.assertRaises(ValueError):
                validate_student_input(dict(self.valid_profile, **{f: float('-inf')}), raise_exception=True)

    def test_12_invalid_data_types_rejected(self):
        """Test non-numeric strings or lists passed for numerical features."""
        with self.assertRaises(TypeError):
            validate_student_input(dict(self.valid_profile, Current_CGPA="nine point two"), raise_exception=True)
        with self.assertRaises(TypeError):
            validate_student_input(dict(self.valid_profile, Backlogs=[0]), raise_exception=True)

    def test_13_dataframe_input_support(self):
        """Test validation on pandas DataFrame input."""
        df = pd.DataFrame([self.valid_profile])
        self.assertTrue(validate_student_input(df, raise_exception=True))

        # Multi-row dataframe should fail single student validation
        df_multi = pd.DataFrame([self.valid_profile, self.valid_profile])
        with self.assertRaises(ValueError):
            validate_student_input(df_multi, raise_exception=True)

if __name__ == "__main__":
    unittest.main(verbosity=2)
