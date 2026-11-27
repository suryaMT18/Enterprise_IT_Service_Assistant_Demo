import requests

from app.config import OLLAMA_BASE_URL, CHAT_MODEL, EMBED_MODEL

class OllamaError(RuntimeError):
    pass

class OllamaClient:
    def chat(self,messages, tools = None):
        url = f"{OLLAMA_BASE_URL}/api/chat"

        payload={
            "model": CHAT_MODEL,
            "messages":messages,
            "stream": False
        }

        if tools is not None:
            payload["tools"] = tools

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=180
            )
            if not response.ok:
                raise OllamaError(
                    f"Ollama returned status {response.status_code}: {response.text}"
                )
            result = response.json()

            if "message" not in result:
                raise OllamaError("Ollama returned an invalid chat response")
            return result

        except requests.RequestException as error:
            raise OllamaError(f"Ollama chat request failed: {error}") from error


    def embed(self,text):
        if not text.strip():
            raise ValueError("Text to embed cannot be empty")
        url = f"{OLLAMA_BASE_URL}/api/embed"
        payload={
            "model": EMBED_MODEL,
            "input": text
        }
        try:
            response = requests.post(
                url,
                json=payload,
                timeout=60
            )

            if not response.ok:
                raise OllamaError(
                    f"Ollama returned status {response.status_code}: {response.text}"
                )

            result = response.json()

            embeddings = result.get("embeddings")
            if not embeddings or not embeddings[0]:
                raise OllamaError("Ollama returned an empty embedding.")
            return embeddings[0]
        except requests.RequestException as error:
            raise OllamaError(f"Ollama embedding request failed: {error}") from error