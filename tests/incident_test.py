from app.tools import prepare_incident_draft

print("VALID INCIDENT")

result = prepare_incident_draft(
    "AST-1002",
    "Laptop screen is flickering",
    "High"
)
print(result)

print("\nINVALID ASSET")

print(
    prepare_incident_draft(
        "AST-9999",
        "Laptop screen is flickering",
        "High"
    )
)

print("\nINVALID PRIORITY")

print(
    prepare_incident_draft(
        "AST-1002",
        "Laptop screen is flickering",
        "Urgent"
    )
)

print("\nEMPTY DESCRIPTION")

print(
    prepare_incident_draft(
        "AST-1002",
        "",
        "High"
    )
)