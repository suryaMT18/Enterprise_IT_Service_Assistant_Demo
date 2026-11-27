from app.knowledge import search_guide


ASSETS = {
    "AST-1001":{
        "asset_tag": "AST-1001",
        "device": "Dell Latitude 5440",
        "assigned_employee": "Nisha Rao",
        "department": "Finance",
        "status": "In service"
    },
    "AST-1002": {
        "asset_tag": "AST-1002",
        "device": "HP EliteBook 840",
        "assigned_employee": "Arjun Mehta",
        "department": "Engineering",
        "status": "In service"
    },
    "AST-1003": {
        "asset_tag": "AST-1003",
        "device": "Lenovo ThinkPad T14",
        "assigned_employee": "Maya Sen",
        "department": "Operations",
        "status": "Under repair"
    },
    "AST-1004": {
        "asset_tag": "AST-1004",
        "device": "Dell Precision 3581",
        "assigned_employee": "Kabir Das",
        "department": "Engineering",
        "status": "In service"
    }
}


TICKETS = {
    "INC-2041": {
        "ticket_id": "INC-2041",
        "category": "Laptop display",
        "priority": "High",
        "status": "In progress",
        "assigned_team": "Endpoint Support"
    },
    "INC-2042": {
        "ticket_id": "INC-2042",
        "category": "VPN access",
        "priority": "Medium",
        "status": "Waiting for user",
        "assigned_team": "Network Support"
    },
    "INC-2043": {
        "ticket_id": "INC-2043",
        "category": "Printer issue",
        "priority": "Low",
        "status": "Resolved",
        "assigned_team": "Workplace Technology"
    },
    "INC-2044": {
        "ticket_id": "INC-2044",
        "category": "Email access",
        "priority": "High",
        "status": "Open",
        "assigned_team": "Identity Support"
    }
}


SUPPORT_TEAMS = [
    {
        "team_name": "Endpoint Support",
        "responsibility": "Laptop, desktop, hardware and device-related issues"
    },
    {
        "team_name": "Network Support",
        "responsibility": "VPN, Wi-Fi, network connectivity and internet issues"
    },
    {
        "team_name": "Identity Support",
        "responsibility": "Email access, account access, passwords and authentication"
    },
    {
        "team_name": "Workplace Technology",
        "responsibility": "Printers, office technology and workplace equipment"
    }
]

def get_asset(asset_tag):
    if not isinstance(asset_tag,str) or not asset_tag.strip():
        return{
            "found": False,
            "message": "A valid asset tag is required."
        }
    asset_tag = asset_tag.strip().upper()
    asset = ASSETS.get(asset_tag)

    if asset is None:
        return{
            "found": False,
            "message":f"Asset {asset_tag} was not found."
        }
    return{
        "found": True,
        "asset": asset.copy()
    }

def get_ticket(ticket_id):
    if not isinstance(ticket_id,str) or not ticket_id.strip():
        return{
            "found": False,
            "message": "A valid ticket ID is required."
        }
    ticket_id = ticket_id.strip().upper()

    ticket = TICKETS.get(ticket_id)

    if ticket is None:
        return{
            "found": False,
            "message": f"Ticket {ticket_id} was not found."
        }
    return{
        "found": True,
        "ticket": ticket.copy()
    }

def list_support_teams():
    return{
        "teams": [team.copy() for team in SUPPORT_TEAMS]
    }

def prepare_incident_draft(asset_tag, issue_description, priority):
    if not isinstance(asset_tag,str) or not asset_tag.strip():
        return{
            "success":False,
            "message": "A valid asset tag is required."
        }
    if not isinstance(issue_description,str) or not issue_description.strip():
        return{
            "success": False,
            "message": "An issue description is required."
        }
    if not isinstance(priority,str):
        return{
            "success": False,
            "message": "A valid priority is required."
        }
    priority = priority.strip().capitalize()

    if priority not in ["Low", "Medium", "High"]:
        return{
            "success": False,
            "message": "Priority must be Low, Medium, or High."
        }

    asset_tag = asset_tag.strip().upper()
    asset=ASSETS.get(asset_tag)
    if asset is None:
        return{
            "success":False,
            "message": f"Asset {asset_tag} was not found."
        }
    draft = {
        "asset_tag": asset_tag,
        "device": asset["device"],
        "assigned_employee": asset["assigned_employee"],
        "department": asset["department"],
        "issue_description": issue_description.strip(),
        "priority": priority,
        "status": "Draft - Pending Human Review"
    }
    return{
        "success": True,
        "message": "Incident draft prepared successfully. Human review is required before submission.",
        "draft": draft
    }


def search_it_guide(question):
    try:
        results = search_guide(question)

    except ValueError as error:
        return{
            "found": False,
            "message": str(error)
        }
    if not results:
        return{
            "found": False,
            "message": "No relevant information was found in the IT operations guide."
        }
    return{
        "found": True,
        "results": results
    }