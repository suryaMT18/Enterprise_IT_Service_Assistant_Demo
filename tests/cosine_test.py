from app.knowledge import cosine_similarity

vector_a = [1, 2, 3]
vector_b = [1, 2, 3]
vector_c = [3, 2, 1]

print("Same vectors:", cosine_similarity(vector_a, vector_b))
print("Different vectors:", cosine_similarity(vector_a, vector_c))