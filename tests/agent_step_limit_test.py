from app.agent import run_agent

question = (
    "Check ticket INC-2041, find the escalation process, "
    "and explain the relevant support team responsibilities."
)

print("AGENT STEP LIMIT TEST")
print("Question:", question)

response = run_agent(question)

print("\nFINAL RESPONSE:")
print(response)