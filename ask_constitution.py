
import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq

# Check that the API key is available
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY is missing. Set it in your terminal first."
    )

# Connect to Groq
client = Groq(api_key=api_key)

# Load the embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to the Constitution database
db_client = chromadb.PersistentClient(path="./constitution_db")
collection = db_client.get_collection(name="ghana_constitution")

# Ask a question
question = input("Ask a question about Ghana's Constitution: ")

# Retrieve relevant passages
question_embedding = embedding_model.encode(question).tolist()

results = collection.query(
    query_embeddings=[question_embedding],
    n_results=3
)

documents = results["documents"][0]

if not documents:
    print("No relevant passages were found.")
    raise SystemExit

context = "\n\n".join(documents)

# Ask the language model to answer using the retrieved context
response = client.chat.completions.create(
    model="openai/gpt-oss-safeguard-20b",
    messages=[
        {
            "role": "system",
            "content": (
                "You answer questions about Ghana's 1992 Constitution. "
                "Use only the supplied constitutional passages. "
                "If the passages do not contain enough information, "
                "say so clearly. Do not invent article numbers or legal "
                "provisions. Make clear that your answer is informational, "
                "not legal advice."
            )
        },
        {
            "role": "user",
            "content": (
                f"Question: {question}\n\n"
                f"Retrieved constitutional passages:\n{context}"
            )
        }
    ],
    temperature=0.1
)

print("\nAnswer:\n")
print(response.choices[0].message.content)

print("\nRetrieved passages for verification:\n")
for i, document in enumerate(documents, start=1):
    print(f"\n--- Passage {i} ---")
    print(document)
