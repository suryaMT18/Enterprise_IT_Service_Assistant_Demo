from app.tools import search_it_guide

question = "How does the ticket escalation process work?"

print("ESCALATION KNOWLEDGE TEST")
print("Question:", question)

result = search_it_guide(question)

print("\nKNOWLEDGE TOOL RESULT:")
print(result)