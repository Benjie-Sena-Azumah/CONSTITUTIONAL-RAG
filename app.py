
import os
import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


st.set_page_config(
    page_title="Ghana Constitution Chatbot",
    page_icon="📘"
)

st.title("📘 Ghana Constitution Chatbot")
st.write(
    "Ask questions about Ghana's 1992 Constitution. "
)

# Check API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is missing. Set it in your terminal.")
    st.stop()

# Load resources and cache them to avoid reloading on every question
@st.cache_resource
def load_resources():
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    db_client = chromadb.PersistentClient(
        path="./constitution_db"
    )
    collection = db_client.get_collection(
        name="ghana_constitution"
    )

    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    return embedding_model, collection, groq_client

try:
    embedding_model, collection, groq_client = load_resources()
except Exception as error:
    st.error(f"Could not load the model or database: {error}")
    st.stop()

question = st.text_input(
    "Your question",
    placeholder="What are the powers of the President of Ghana?"
)

if st.button("Get Answer") and question.strip():
    with st.spinner("Searching the Constitution and preparing an answer..."):
        try:
            # Retrieve relevant passages
            question_embedding = embedding_model.encode(
                question
            ).tolist()

            results = collection.query(
                query_embeddings=[question_embedding],
                n_results=3
            )

            documents = results["documents"][0]

            if not documents:
                st.warning("No relevant passages were found.")
                st.stop()

            context = "\n\n".join(documents)

            # Generate the answer
            response = groq_client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Answer questions about Ghana's 1992 Constitution "
                            "using only the supplied passages. If they do not "
                            "contain enough information, say so. Do not invent "
                            "article numbers or legal provisions. This is "
                            "informational, not legal advice."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Question: {question}\n\n"
                            f"Constitution passages:\n{context}"
                        )
                    }
                ],
                temperature=0.1
            )

            answer = response.choices[0].message.content
            st.subheader("Answer")
            st.write(answer)

            with st.expander("View retrieved Constitution passages"):
                for i, document in enumerate(documents, start=1):
                    st.markdown(f"**Passage {i}**")
                    st.write(document)

        except Exception as error:
            st.error(f"Something went wrong: {error}")
