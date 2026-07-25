"""
Unit tests for Brain Loader Validation Engine.
"""

import unittest
from brain.loader.validator import ValidationEngine

class TestValidationEngine(unittest.TestCase):
    def setUp(self):
        self.validator = ValidationEngine()

    def test_validate_all(self):
        errors = self.validator.validate_all()
        # Verify zero blocking errors on active repository
        error_msgs = [str(e) for e in errors if e.severity == "ERROR"]
        self.assertEqual(len(error_msgs), 0, f"Validation errors found: {error_msgs}")

if __name__ == "__main__":
    unittest.main()
