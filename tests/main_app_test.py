# from fastapi.testclient import TestClient

# from app.main import app


# client = TestClient(app)

# response = client.post(
#     "/chat",
#     json={
#         "message": "Who is using asset AST-1001?"
#     }
# )

# print("STATUS CODE:", response.status_code)
# print("RESPONSE:", response.json())



from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

response = client.post(
    "/api/chat",
    json={
        "message": (
            "Check ticket INC-2041 and explain "
            "how the escalation process works."
        )
    }
)

print("STATUS CODE:", response.status_code)

data = response.json()

print("\nFINAL ANSWER:")
print(data["answer"])

print("\nTOOLS RETURNED BY API:")

for item in data["trace"]:
    print(item["tool"])

print("\nTOTAL TOOLS:", len(data["trace"]))
