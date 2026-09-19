import unittest
from pydantic import ValidationError
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from assignment_2.agent import ReviewVerdict

class TestSchemas(unittest.TestCase):
    def test_review_verdict_valid(self):
        verdict = ReviewVerdict(is_approved=True, reason="Looks good")
        self.assertTrue(verdict.is_approved)

if __name__ == '__main__':
    unittest.main()
