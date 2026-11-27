
from app.knowledge import search_guide

questions = [
    "My VPN is not connecting. What should I do?",
    "When can I request a replacement laptop?",
    "What should I do if my company laptop is stolen?",
    "Can I install software without IT approval?",
    "How much does the company reimburse for personal internet?"
]

for question in questions:
    print("\n" + "=" * 60)
    print("QUESTION:", question)

    results = search_guide(question)

    if not results:
        print("No relevant information found in the guide.")
        continue

    for result in results:
        print("\nTitle:", result["title"])
        print("Similarity:", result["score"])
        print("Content preview:", result["content"][:250])
