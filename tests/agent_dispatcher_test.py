
from app.agent import execute_tool

print("TEST 1: Valid asset lookup")

result = execute_tool(
    "get_asset",
    {"asset_tag": "AST-1001"}
)

print(result)


print("\nTEST 2: Valid ticket lookup")

result = execute_tool(
    "get_ticket",
    {"ticket_id": "INC-2041"}
)

print(result)


print("\nTEST 3: Support teams without arguments")

result = execute_tool(
    "list_support_teams",
    {}
)

print(result)


print("\nTEST 4: Unknown tool")

result = execute_tool(
    "delete_all_files",
    {}
)

print(result)


print("\nTEST 5: Invalid argument format")

result = execute_tool(
    "get_asset",
    "AST-1001"
)

print(result)
