
from app.agent import run_agent

print("TEST 1: Greeting")

response = run_agent("Hello!")

print(response)


print("\nTEST 2: Asset lookup")

response = run_agent(
    "Who is using asset AST-1001?"
)

print(response)


print("\nTEST 3: Ticket lookup")

response = run_agent(
    "What is the status of ticket INC-2041?"
)

print(response)


print("\nTEST 4: IT guide search")

response = run_agent(
    "How can I troubleshoot VPN issues?"
)

print(response)
