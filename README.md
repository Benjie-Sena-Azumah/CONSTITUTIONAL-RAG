Retrieval-Augmented Generation (RAG) project that answers questions about Ghana's 1992 Constitution. It retrieves relevant passages from a local text database and sends those passages, along with the user's question, to a language model to generate a grounded answer.

The project uses **Sentence Transformers** to create embeddings, ChromaDB to store and search constitutional passages, Groq to generate answers, and Streamlit to provide a web interface.

How It Works
1. *Extract text:* Read the Constitution PDF and save its text to constitution.txt.
2. *Split into chunks:* Divide the extracted text into overlapping text sections. The current settings use 1,000 characters per chunk with a 200-character overlap.
3. *Create embeddings and store chunks:* Convert chunks into numerical vectors with all-MiniLM-L6-v2 and store the chunks and vectors in ChromaDB.
4. *Retrieve relevant passages:* Convert a user's question into an embedding and search the database for the three most relevant chunks.
5. *Generate an answer:* Send the question and retrieved passages to a Groq-hosted language model, with instructions to answer from the supplied passages.
6. *Display the result:* Streamlit shows the answer and provides an expandable section to inspect the retrieved passages


Technology Stack

- *Python* — application language
- *PyMuPDF (pymupdf)* — extracts text from the Constitution PDF
- *Sentence Transformers* — creates text embeddings using all-MiniLM-L6-v2
- *ChromaDB* — persistent vector database and similarity search
- *Groq*— provides the chat-completion API
- *Streamlit* — web-based user interface
- *python-dotenv* — loads the API key from a .env file

Important Implementation Details

- **Embedding model:** all-MiniLM-L6-v2
- **Chunk size:** 1,000 characters
- **Chunk overlap:** 200 characters
- **Retrieved passages:** up to 3
- **Vector database:** ChromaDB, persisted in ./constitution_db
- **Generation provider:** Groq API
- **Chat model in the Streamlit code:** openai/gpt-oss-20b



Try running Streamlit through Python:

`python -m streamlit run app.py`

