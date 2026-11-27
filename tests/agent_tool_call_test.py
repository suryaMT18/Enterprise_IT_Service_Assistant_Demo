
from app.agent import client, TOOLS, SYSTEM_PROMPT

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    },
    {
        "role": "user",
        "content": "Who is using asset AST-1001? Use the get_asset tool."
    }
]

response = client.chat(
    messages,
    tools=TOOLS
)

print("COMPLETE OLLAMA RESPONSE:")
print(response)

print("\nASSISTANT MESSAGE:")
print(response.get("message"))

print("\nTOOL CALLS:")
print(
    response.get("message", {}).get("tool_calls", [])
)
