from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

response = client.get("/")

print("STATUS CODE:", response.status_code)
print("CONTENT TYPE:", response.headers.get("content-type"))
print("HTML RECEIVED:", "html" in response.text.lower())