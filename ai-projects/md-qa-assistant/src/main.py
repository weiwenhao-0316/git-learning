from pathlib import Path

notes_path = Path("ai-projects/md-qa-assistant/data/notes.md")

notes_content = notes_path.read_text(encoding="utf-8")

question = input("Please enter your question: ")

print("\n--- Your Question ---")
print(question)

print("\n--- Notes Content ---")
print(notes_content)
