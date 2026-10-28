
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


with open("constitution.txt", "r", encoding="utf-8") as file:
    text = file.read()

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

chunks = []
start = 0

while start < len(text):
    chunk = text[start:start + CHUNK_SIZE]

    if chunk.strip():
        chunks.append(chunk)

    start += CHUNK_SIZE - CHUNK_OVERLAP

# Convert each chunk into a numerical embedding
embeddings = model.encode(chunks)

print("Total chunks:", len(chunks))
print("Number of embeddings:", len(embeddings))
print("Embedding dimensions:", embeddings.shape[1])
print("First embedding (first 10 numbers):", embeddings[0][:10])
