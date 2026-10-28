
from sentence_transformers import SentenceTransformer
import chromadb


model = SentenceTransformer("all-MiniLM-L6-v2")


client = chromadb.PersistentClient(path="./constitution_db")

collection = client.get_collection(
    name="ghana_constitution"
)

# Ask a question
question = "What are the powers of the President of Ghana?"

# Convert the question into an embedding
question_embedding = model.encode(question).tolist()

# Find the 3 most relevant chunks
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=3
)


print("\nQuestion:", question)
print("\nRelevant passages:\n")

for i, document in enumerate(results["documents"][0], start=1):
    print(f"\n--- Passage {i} ---")
    print(document)
