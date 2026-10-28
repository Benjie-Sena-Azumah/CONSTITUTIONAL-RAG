
import pymupdf


pdf = pymupdf.open("constitution.pdf")


all_text = ""

for page_number, page in enumerate(pdf, start=1):
    page_text = page.get_text()
    all_text += f"\n\n--- Page {page_number} ---\n\n"
    all_text += page_text


with open("constitution.txt", "w", encoding="utf-8") as file:
    file.write(all_text)

print(f"Text extracted from {len(pdf)} pages.")
print(f"Total characters extracted: {len(all_text)}")
print("Saved the text to constitution.txt")
