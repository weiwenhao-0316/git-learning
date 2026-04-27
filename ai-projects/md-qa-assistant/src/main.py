import os
from pathlib import Path

from openai import OpenAI

notes_path = Path("ai-projects/md-qa-assistant/data/notes.md")
notes_content = notes_path.read_text(encoding="utf-8")

question = input("Please enter your question: ")

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

prompt = f"""
You are a helpful study assistant.

Answer the user's question only based on the notes below.
If the notes do not contain the answer, say that clearly.

Notes:
{notes_content}

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

print("\n--- Answer ---")
print(answer)
