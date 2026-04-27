import os
import re
from pathlib import Path

from openai import OpenAI


def split_into_chunks(text: str) -> list[str]:
    chunks = text.split("## ")
    cleaned_chunks = []

    for chunk in chunks:
        chunk = chunk.strip()
        if chunk:
            cleaned_chunks.append(chunk)

    return cleaned_chunks


def score_chunk(question: str, chunk: str) -> int:
    question_words = re.findall(r"\w+", question.lower())
    chunk_text = chunk.lower()

    score = 0
    for word in question_words:
        if word in chunk_text:
            score += 1

    return score


def get_top_chunks(question: str, chunks: list[str], top_k: int = 2) -> list[str]:
    scored_chunks = []

    for chunk in chunks:
        score = score_chunk(question, chunk)
        scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    top_chunks = []
    for score, chunk in scored_chunks[:top_k]:
        if score > 0:
            top_chunks.append(chunk)

    return top_chunks


notes_path = Path("ai-projects/md-qa-assistant/data/notes.md")
notes_content = notes_path.read_text(encoding="utf-8")

chunks = split_into_chunks(notes_content)

question = input("Please enter your question: ")

top_chunks = get_top_chunks(question, chunks, top_k=2)

if top_chunks:
    selected_notes = "\n\n".join(top_chunks)
else:
    selected_notes = "No relevant notes were found."

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

prompt = f"""
You are a helpful study assistant.

Answer the user's question only based on the notes below.
If the notes do not contain the answer, say that clearly.

Relevant notes:
{selected_notes}

User question:
{question}
"""

response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {
            "role": "system",
            "content": "You answer questions based on the provided notes.",
        },
        {
            "role": "user",
            "content": prompt,
        },
    ],
    temperature=0.2,
    stream=False,
)

answer = response.choices[0].message.content

print("\n--- Selected Notes ---")
print(selected_notes)

print("\n--- Answer ---")
print(answer)
