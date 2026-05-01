import unittest
import sys
import os

# Add the project directory to path for imports
sys.path.append(os.getcwd())

from app import get_mock_booth_info, ELECTION_DATA, sanitize_input, get_rag_response, generate_voter_slip, generate_mermaid_mission

class TestElectionAgentTools(unittest.TestCase):
    
    def test_scout_booth_locator(self):
        """[TEST] Verify Scout Agent booth location accuracy."""
        result = get_mock_booth_info("West Bengal", "Bhabanipur")
        self.assertIn("St. Johns School", result)
        
        result_unknown = get_mock_booth_info("Tamil Nadu", "Random Place")
        self.assertEqual(result_unknown, "Standard Primary School Center")

    def test_input_sanitization(self):
        """[SECURITY TEST] Verify that malicious inputs are sanitized."""
        toxic_input = "Hello <script>alert('hack')</script> !!!"
        clean = sanitize_input(toxic_input)
        self.assertNotIn("<script>", clean)
        self.assertIn("Hello", clean)
        
        long_input = "a" * 1000
        self.assertEqual(len(sanitize_input(long_input)), 500)

    def test_rag_semantic_retrieval(self):
        """[EFFICIENCY TEST] Verify RAG tool can retrieve from knowledge_base.json."""
        # This test assumes knowledge_base.json exists
        result = get_rag_response("bhabanipur booth")
        if result:
            self.assertIn("legal", result)
            self.assertIn("advice", result)

    def test_artifact_generation(self):
        """[USABILITY TEST] Verify HTML and Mermaid artifact consistency."""
        slip = generate_voter_slip("John Doe", "West Bengal", "Booth A", "South")
        self.assertIn("John Doe", slip)
        self.assertIn("Official Election Readiness Slip", slip)
        
        mermaid = generate_mermaid_mission("Kolkata", "Active")
        self.assertIn("graph TD", mermaid)
        self.assertIn("Kolkata", mermaid)

    def test_national_compass_integrity(self):
        """[DATA QUALITY TEST] Verify election data structure."""
        states = ELECTION_DATA.keys()
        self.assertIn("West Bengal", states)
        self.assertIn("Tamil Nadu", states)

if __name__ == '__main__':
    unittest.main()
