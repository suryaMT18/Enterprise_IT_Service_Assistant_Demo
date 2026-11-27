from app.agent import run_agent

question = (
    "Prepare an incident report draft for asset AST-1001. "
    "The laptop screen is flickering and displaying horizontal lines. "
    "Set the priority to High."
)

print("INCIDENT DRAFT TEST")
print("Question:", question)

response = run_agent(question)

print("\nFINAL RESPONSE:")
print(response)