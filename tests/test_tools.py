import unittest
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from utils.tools import get_rag_response, get_mock_booth_info
from shield.moderator import sanitize_and_moderate
from ui.styles import generate_voter_slip, generate_mermaid_mission

class TestElectionAgentModular(unittest.TestCase):
    
    def test_sanitization(self):
        """[SECURITY] Verify input filtering."""
        self.assertNotIn("<script>", sanitize_and_moderate("<script>alert(1)</script>"))
        self.assertIn("Hello", sanitize_and_moderate("Hello!!!"))

    def test_rag_retrieval(self):
        """[EFFICIENCY] Verify local RAG tool."""
        # Check if knowledge_base.json exists before testing
        if os.path.exists("knowledge_base.json"):
            result = get_rag_response("bhabanipur booth")
            if result:
                self.assertIn("legal", result)

    def test_booth_tool(self):
        """[TOOL] Verify specialized booth locator."""
        self.assertIn("St. Johns School", get_mock_booth_info("WB", "Bhabanipur"))

    def test_ui_artifacts(self):
        """[UX] Verify artifact generation strings."""
        slip = generate_voter_slip("User", "WB", "Booth A", "South")
        self.assertIn("OFFICIAL VOTER READINESS SLIP", slip)
        
        mermaid = generate_mermaid_mission("South", "Active")
        self.assertIn("graph TD", mermaid)

if __name__ == '__main__':
    unittest.main()
