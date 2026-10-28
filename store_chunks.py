
from sentence_transformers import SentenceTransformer
import chromadb


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


embeddings = model.encode(chunks).tolist()


client = chromadb.PersistentClient(path="./constitution_db")


collection = client.get_or_create_collection(
    name="ghana_constitution"
)

# Store each chunk and its embedding
# IDs are stable so rerunning the script updates existing chunks.
collection.upsert(
    ids=[f"chunk_{i}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings,
    metadatas=[{"chunk_number": i} for i in range(len(chunks))]
)

print("Total chunks stored:", collection.count())
print("Database saved in: constitution_db")
