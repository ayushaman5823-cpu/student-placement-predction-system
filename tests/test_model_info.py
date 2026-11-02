"""
Unit tests for Terminal Model Information Display and Authoritative Metrics
Student Placement Prediction System — SRM Institute of Science and Technology
"""

import io
import os
import sys
import unittest
from unittest.mock import patch

SRC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from menu import get_authoritative_metrics, show_model_info

class TestModelInfo(unittest.TestCase):
    def test_authoritative_metrics_values(self):
        """Verify baseline metrics match authoritative holdout evaluation exactly."""
        metrics = get_authoritative_metrics()
        self.assertAlmostEqual(metrics['accuracy'], 0.8310, places=4)
        self.assertAlmostEqual(metrics['precision'], 0.8276, places=4)
        self.assertAlmostEqual(metrics['recall'], 0.9019, places=4)
        self.assertAlmostEqual(metrics['f1_score'], 0.8632, places=4)
        self.assertAlmostEqual(metrics['roc_auc'], 0.9036, places=4)
        self.assertAlmostEqual(metrics['brier_score'], 0.1158, places=4)

    @patch('builtins.input', return_value='')
    def test_show_model_info_output(self, mock_input):
        """Verify show_model_info displays correct metrics and NOT 94.12%."""
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            show_model_info()
        output = captured_output.getvalue()

        self.assertIn("83.10%", output)
        self.assertIn("82.76%", output)
        self.assertIn("90.19%", output)
        self.assertIn("86.32%", output)
        self.assertIn("90.36%", output)
        self.assertIn("0.1158", output)
        self.assertNotIn("94.12%", output)
        self.assertNotIn("95.01%", output)
        self.assertNotIn("95.17%", output)

if __name__ == "__main__":
    unittest.main(verbosity=2)

