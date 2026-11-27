import re
from pathlib import Path
import math
from app.ollama_client import OllamaClient

BASE_DIR = Path(__file__).resolve().parent.parent
GUIDE_PATH = BASE_DIR/"data"/"it_operations_guide.md"
client = OllamaClient()

MIN_SIMILARITY = 0.15
_knowledge_sections = None


def load_guide_sections():
    if not GUIDE_PATH.exists():
        raise FileNotFoundError(f"Knowledge guide not found: {GUIDE_PATH}")
    content = GUIDE_PATH.read_text(encoding="utf-8")

    sections = []
    current_title = None
    current_content = []

    for line in content.splitlines():
        if line.startswith("## "):
            if current_title is not None:
                sections.append({
                    "title": current_title,
                    "content": "\n".join(current_content).strip()
                })
            current_title = line[3: ].strip()
            current_content = []
        elif current_title is not None:
            current_content.append(line)
    if current_title is not None:
        sections.append({
            "title": current_title,
            "content": "\n".join(current_content).strip()
        })
    return sections

def generate_embeddings(sections):
    for section in sections:
        section["embedding"] = client.embed(
            section["title"] + "\n" + section["content"]
        )
    return sections

def cosine_similarity(vector_a,vector_b):
    if len(vector_a) != len(vector_b):
        raise ValueError("Embedding dimensions must match.")

    dot_product = sum(
        a*b for a,b in zip(vector_a,vector_b)
    )

    magnitude_a = math.sqrt(sum(a*a for a in vector_a))
    magnitude_b = math.sqrt(sum(b*b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product/(magnitude_a*magnitude_b)


def search_guide(question, top_k=3):
    global _knowledge_sections

    if not isinstance(question,str) or not question.strip():
        raise ValueError("A valid question is required.")

    if not isinstance(top_k,int) or top_k < 1:
        raise ValueError("top_k must be a positive integer.")

    if _knowledge_sections is None:
        sections = load_guide_sections()
        _knowledge_sections = generate_embeddings(sections)

    question_embedding = client.embed(question.strip())

    scored_sections = []

    for section in _knowledge_sections:
        score = cosine_similarity(
            question_embedding,
            section["embedding"]
        )
        scored_sections.append({
            "score": score,
            "title": section["title"],
            "content": section["content"]
        })

    scored_sections.sort(
        key=lambda item:item["score"],
        reverse=True
    )

    results=[
        {
            "score": round(section["score"],4),
            "title": section["title"],
            "content": section["content"]
        }

        for section in scored_sections[:top_k]
        if section["score"]>=MIN_SIMILARITY
    ]

    return results