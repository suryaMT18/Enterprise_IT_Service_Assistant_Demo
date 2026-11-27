from app.ollama_client import OllamaClient

c=OllamaClient()

text="How do I troubleshoot VPN access?"
result=c.embed(text)

print("Input text:", text)
print("Embedding:", result)
print("Embedding length:",len(result))
print("First five values:", result[:5])