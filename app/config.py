import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL","http://localhost:11434").rstrip("/")
CHAT_MODEL = os.getenv("CHAT_MODEL","qwen2.5:3b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
MAX_AGENT_STEPS = int(os.getenv("MAX_AGENT_STEPS", "4"))