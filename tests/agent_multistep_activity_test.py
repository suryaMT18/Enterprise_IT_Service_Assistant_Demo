
from app.agent import run_agent

question = (
    "Check ticket INC-2041 and explain "
    "how the escalation process works."
)

result = run_agent(
    question,
    include_activity=True
)

print("\nFINAL ANSWER:")
print(result["answer"])

print("\nNUMBER OF TOOLS EXECUTED:")
print(len(result["trace"]))

print("\nTOOL EXECUTION TRACE:")

for step in result["trace"]:
    print("Tool:", step["tool"])
    print("Arguments:", step["arguments"])
    print("Result:", step["result"])
    print("-" * 50)
