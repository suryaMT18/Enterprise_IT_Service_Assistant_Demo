
from app.agent import run_agent

question = (
    "Check ticket INC-2041 and explain "
    "how the escalation process works."
)

print("MULTI-STEP AGENT TEST")
print("Question:", question)

response = run_agent(question)

print("\nFINAL RESPONSE:")
print(response)
