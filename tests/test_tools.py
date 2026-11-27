
import unittest

from app.tools import (
    get_asset,
    get_ticket,
    list_support_teams,
    prepare_incident_draft
)


class TestITTools(unittest.TestCase):

    # Asset tests

    def test_get_existing_asset(self):
        result = get_asset("AST-1001")

        self.assertTrue(result["found"])
        self.assertEqual(
            result["asset"]["asset_tag"],
            "AST-1001"
        )

    def test_get_unknown_asset(self):
        result = get_asset("AST-9999")

        self.assertFalse(result["found"])
        self.assertIn("not found", result["message"])

    # Ticket tests

    def test_get_existing_ticket(self):
        result = get_ticket("INC-2041")

        self.assertTrue(result["found"])
        self.assertEqual(
            result["ticket"]["ticket_id"],
            "INC-2041"
        )

    def test_get_unknown_ticket(self):
        result = get_ticket("INC-9999")

        self.assertFalse(result["found"])
        self.assertIn("not found", result["message"])

    # Support team test

    def test_list_support_teams(self):
        result = list_support_teams()

        self.assertIn("teams", result)
        self.assertEqual(len(result["teams"]), 4)

    # Incident draft test

    def test_prepare_incident_draft(self):
        result = prepare_incident_draft(
            asset_tag="AST-1001",
            issue_description="Laptop screen flickering",
            priority="High"
        )

        self.assertTrue(result["success"])
        self.assertEqual(
            result["draft"]["status"],
            "Draft - Pending Human Review"
        )

    
    def test_incident_draft_empty_asset_tag(self):
        result = prepare_incident_draft(
            asset_tag="",
            issue_description="Laptop screen flickering",
            priority="High"
        )

        self.assertFalse(result["success"])
        self.assertIn("asset tag", result["message"])

    def test_incident_draft_empty_issue_description(self):
        result = prepare_incident_draft(
            asset_tag="AST-1001",
            issue_description="",
            priority="High"
        )

        self.assertFalse(result["success"])
        self.assertIn("issue description", result["message"])

    def test_incident_draft_invalid_priority(self):
        result = prepare_incident_draft(
            asset_tag="AST-1001",
            issue_description="Laptop screen flickering",
            priority="Critical"
        )

        self.assertFalse(result["success"])
        self.assertIn("priority", result["message"].lower())

    def test_incident_draft_unknown_asset(self):
        result = prepare_incident_draft(
            asset_tag="AST-9999",
            issue_description="Laptop screen flickering",
            priority="High"
        )

        self.assertFalse(result["success"])
        self.assertIn("not found", result["message"])



if __name__ == "__main__":
    unittest.main()
