# wp1 – Simple Word Processor v1

A lightweight, pure-Python word processing library and CLI tool.

## Features

- **Document model**: `Document`, `Paragraph`, and `TextRun` with character-level `TextFormat` (bold, italic, underline, font size, font name)
- **Editing**: insert / delete text within paragraphs; add, insert, or remove paragraphs
- **Search & replace**: literal or regex, case-insensitive
- **Import / Export**: save/load in a JSON-based `.wp1` format; export as plain text or Markdown; import plain-text files
- **CLI**: `wp1` command-line tool for common operations

## Installation

```bash
pip install -e .
```

## Quick start (Python API)

```python
from wordprocessor import Document, TextFormat

doc = Document(title="My First Document")
doc.add_paragraph("Hello, World!")
doc.add_paragraph("This is bold text.", TextFormat(bold=True))

doc.save("hello.wp1")

# Reload
doc2 = Document.open("hello.wp1")
print(doc2.plain_text())
```

## CLI usage

```bash
# Create a new document
wp1 new hello.wp1 --title "My Doc" --text "Hello, World!" "Second paragraph"

# Display a document
wp1 show hello.wp1
wp1 show hello.wp1 --markdown

# Find & replace
wp1 replace hello.wp1 "World" "Python"

# Search
wp1 find hello.wp1 "python"

# Export
wp1 export hello.wp1 output.md
wp1 export hello.wp1 output.txt
```

## Running tests

```bash
pip install pytest
pytest tests/ -v
```
