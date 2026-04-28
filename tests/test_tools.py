import unittest
import sys
import os

# Add the project directory to path for imports
sys.path.append(os.getcwd())

from app import get_mock_booth_info, ELECTION_DATA

class TestElectionAgentTools(unittest.TestCase):
    
    def test_scout_booth_locator(self):
        """Test if the Scout Agent can locate known constituencies."""
        result = get_mock_booth_info("West Bengal", "Bhabanipur")
        self.assertIn("St. Johns School", result)
        
        result_unknown = get_mock_booth_info("Tamil Nadu", "Random Place")
        self.assertEqual(result_unknown, "Standard Primary School Center")

    def test_national_compass_data(self):
        """Test if the National Compass has the correct state keys."""
        states = ELECTION_DATA.keys()
        self.assertIn("West Bengal", states)
        self.assertIn("Tamil Nadu", states)
        self.assertIn("Kerala", states)

    def test_election_dates(self):
        """Test if Phase 2 for WB is correctly set to April 29, 2026."""
        wb_data = ELECTION_DATA.get("West Bengal")
        self.assertEqual(wb_data["Phase 2"], "April 29, 2026")

if __name__ == '__main__':
    unittest.main()
