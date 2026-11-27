from app.agent import run_agent

question = "How much money does the company reimburse employees for personal internet expenses?"

print("KNOWLEDGE NO-ANSWER TEST")
print("Question:", question)

response = run_agent(question)

print("\nFINAL RESPONSE:")
print(response)