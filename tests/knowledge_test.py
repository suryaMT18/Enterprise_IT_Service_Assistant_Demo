# from app.knowledge import load_guide_sections

# sections = load_guide_sections()

# print("Total Sections:",len(sections))

# for section in sections:
#     print("\nTitle:", section["title"])
#     print("Content preview:", section["content"][:100])


from app.knowledge import load_guide_sections, generate_embeddings

sections = load_guide_sections()

sections = generate_embeddings(sections)

print("Total sections:", len(sections))

for section in sections:
    print("\nTitle:", section["title"])
    print("Embedding length:", len(section["embedding"]))
    print("First five values:", section["embedding"][:5])