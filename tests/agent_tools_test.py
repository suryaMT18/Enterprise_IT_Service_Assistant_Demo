
from app.agent import TOOLS

print("Total tools:", len(TOOLS))

for tool in TOOLS:
    function = tool["function"]

    print("\nTool name:", function["name"])
    print("Description:", function["description"])

    parameters = function["parameters"]
    properties = parameters["properties"]

    print("Arguments:", list(properties.keys()))
    print("Required:", parameters.get("required", []))


    
