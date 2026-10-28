

with open("constitution.txt", "r", encoding="utf-8") as file:
    text = file.read()


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

chunks = []
start = 0

while start < len(text):
    end = start + CHUNK_SIZE
    chunk = text[start:end]

    if chunk.strip():
        chunks.append(chunk)


    start += CHUNK_SIZE - CHUNK_OVERLAP


with open("chunks.txt", "w", encoding="utf-8") as file:
    for i, chunk in enumerate(chunks, start=1):
        file.write(f"\n{'=' * 20} CHUNK {i} {'=' * 20}\n")
        file.write(chunk)
        file.write("\n")

print(f"Total characters: {len(text)}")
print(f"Total chunks created: {len(chunks)}")
print(f"Chunk size: {CHUNK_SIZE} characters")
print(f"Chunk overlap: {CHUNK_OVERLAP} characters")
print("Saved chunks to chunks.txt")
