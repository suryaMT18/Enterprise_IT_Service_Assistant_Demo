
from app.agent import ALLOWED_TOOLS

print("Total allowed tools:", len(ALLOWED_TOOLS))

for tool_name, function in ALLOWED_TOOLS.items():
    print(tool_name, "->", function.__name__)

print("\nChecking an approved tool:")
print("get_asset" in ALLOWED_TOOLS)

print("\nChecking an unknown tool:")
print("delete_all_files" in ALLOWED_TOOLS)
