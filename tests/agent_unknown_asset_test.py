from app.agent import run_agent

question = "Who is using asset AST-9999?"

print("UNKNOWN ASSET TEST")
print("Question:", question)

response = run_agent(question)

print("\nFINAL RESPONSE:")
print(response)