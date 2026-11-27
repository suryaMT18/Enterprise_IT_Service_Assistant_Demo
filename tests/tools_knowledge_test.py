from app.tools import search_it_guide

questions = [
    "How do I troubleshoot VPN access?",
    "What is the laptop replacement policy?",
    "How much does the company reimburse for personal internet?"
]

for question in questions:
    print("\n" + "=" * 60)
    print("QUESTION:", question)

    result = search_it_guide(question)

    print("Found:", result["found"])

    if result["found"]:
        for section in result["results"]:
            print("\nTitle:", section["title"])
            print("Similarity:", section["score"])
            print("Content:", section["content"][:200])
    else:
        print("Message:", result["message"])