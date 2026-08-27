"""Tests for the wp1 word processor."""

import json
import tempfile
from pathlib import Path

import pytest

from wordprocessor.document import Document, Paragraph, TextFormat, TextRun


# ---------------------------------------------------------------------------
# TextFormat
# ---------------------------------------------------------------------------

def test_textformat_defaults():
    fmt = TextFormat()
    assert fmt.bold is False
    assert fmt.italic is False
    assert fmt.underline is False
    assert fmt.font_size == 12
    assert fmt.font_name == "Arial"


def test_textformat_roundtrip():
    fmt = TextFormat(bold=True, italic=True, font_size=16, font_name="Times")
    assert TextFormat.from_dict(fmt.to_dict()) == fmt


# ---------------------------------------------------------------------------
# TextRun
# ---------------------------------------------------------------------------

def test_textrun_plain_text():
    run = TextRun(text="Hello")
    assert run.plain_text() == "Hello"


def test_textrun_markdown_bold():
    run = TextRun(text="Hello", fmt=TextFormat(bold=True))
    assert run.to_markdown() == "**Hello**"


def test_textrun_markdown_italic():
    run = TextRun(text="World", fmt=TextFormat(italic=True))
    assert run.to_markdown() == "*World*"


def test_textrun_markdown_underline():
    run = TextRun(text="Under", fmt=TextFormat(underline=True))
    assert run.to_markdown() == "__Under__"


def test_textrun_roundtrip():
    run = TextRun(text="abc", fmt=TextFormat(bold=True, font_size=18))
    assert TextRun.from_dict(run.to_dict()) == run


# ---------------------------------------------------------------------------
# Paragraph
# ---------------------------------------------------------------------------

def test_paragraph_from_text():
    para = Paragraph.from_text("Hello World")
    assert para.plain_text() == "Hello World"


def test_paragraph_insert_text():
    para = Paragraph.from_text("Hello World")
    para.insert_text(5, " Beautiful")
    assert para.plain_text() == "Hello Beautiful World"


def test_paragraph_insert_at_start():
    para = Paragraph.from_text("World")
    para.insert_text(0, "Hello ")
    assert para.plain_text() == "Hello World"


def test_paragraph_insert_at_end():
    para = Paragraph.from_text("Hello")
    para.insert_text(5, " World")
    assert para.plain_text() == "Hello World"


def test_paragraph_insert_invalid_offset():
    para = Paragraph.from_text("Hi")
    with pytest.raises(IndexError):
        para.insert_text(10, "!")


def test_paragraph_delete_text():
    para = Paragraph.from_text("Hello World")
    para.delete_text(5, 11)
    assert para.plain_text() == "Hello"


def test_paragraph_delete_invalid_range():
    para = Paragraph.from_text("Hi")
    with pytest.raises(IndexError):
        para.delete_text(5, 10)


def test_paragraph_roundtrip():
    para = Paragraph.from_text("test", TextFormat(bold=True))
    assert Paragraph.from_dict(para.to_dict()).plain_text() == "test"


# ---------------------------------------------------------------------------
# Document
# ---------------------------------------------------------------------------

def test_document_add_paragraph():
    doc = Document("My Doc")
    p = doc.add_paragraph("Hello")
    assert len(doc.paragraphs) == 1
    assert p.plain_text() == "Hello"


def test_document_insert_paragraph():
    doc = Document()
    doc.add_paragraph("First")
    doc.add_paragraph("Third")
    doc.insert_paragraph(1, "Second")
    assert doc.paragraphs[1].plain_text() == "Second"


def test_document_delete_paragraph():
    doc = Document()
    doc.add_paragraph("Keep")
    doc.add_paragraph("Delete me")
    doc.delete_paragraph(1)
    assert len(doc.paragraphs) == 1
    assert doc.paragraphs[0].plain_text() == "Keep"


def test_document_delete_paragraph_invalid():
    doc = Document()
    with pytest.raises(IndexError):
        doc.delete_paragraph(0)


def test_document_plain_text():
    doc = Document()
    doc.add_paragraph("Line 1")
    doc.add_paragraph("Line 2")
    assert doc.plain_text() == "Line 1\nLine 2"


def test_document_to_markdown():
    doc = Document(title="Test")
    doc.add_paragraph("Hello")
    md = doc.to_markdown()
    assert "# Test" in md
    assert "Hello" in md


def test_document_find():
    doc = Document()
    doc.add_paragraph("The quick brown fox")
    doc.add_paragraph("jumps over the lazy dog")
    results = list(doc.find("the"))
    assert len(results) == 2  # case-insensitive


def test_document_find_regex():
    doc = Document()
    doc.add_paragraph("foo123bar")
    results = list(doc.find(r"\d+", regex=True))
    assert results == [(0, 3, 6)]


def test_document_replace():
    doc = Document()
    doc.add_paragraph("Hello World")
    n = doc.replace("World", "Python")
    assert n == 1
    assert doc.paragraphs[0].plain_text() == "Hello Python"


def test_document_replace_multiple():
    doc = Document()
    doc.add_paragraph("foo foo foo")
    n = doc.replace("foo", "bar")
    assert n == 3
    assert doc.paragraphs[0].plain_text() == "bar bar bar"


def test_document_save_and_open(tmp_path):
    path = tmp_path / "test.wp1"
    doc = Document(title="Saved Doc")
    doc.add_paragraph("Paragraph one")
    doc.add_paragraph("Paragraph two")
    doc.save(path)

    loaded = Document.open(path)
    assert loaded.title == "Saved Doc"
    assert len(loaded.paragraphs) == 2
    assert loaded.paragraphs[0].plain_text() == "Paragraph one"


def test_document_export_text(tmp_path):
    doc = Document()
    doc.add_paragraph("Hello")
    doc.add_paragraph("World")
    out = tmp_path / "out.txt"
    doc.export_text(out)
    assert out.read_text() == "Hello\nWorld"


def test_document_export_markdown(tmp_path):
    doc = Document(title="MD Test")
    doc.add_paragraph("Hello")
    out = tmp_path / "out.md"
    doc.export_markdown(out)
    content = out.read_text()
    assert "# MD Test" in content
    assert "Hello" in content


def test_document_import_text(tmp_path):
    src = tmp_path / "source.txt"
    src.write_text("Line 1\nLine 2\nLine 3")
    doc = Document.import_text(src, title="Imported")
    assert doc.title == "Imported"
    assert len(doc.paragraphs) == 3
    assert doc.paragraphs[2].plain_text() == "Line 3"


def test_document_roundtrip_json(tmp_path):
    path = tmp_path / "roundtrip.wp1"
    doc = Document(title="RT")
    fmt = TextFormat(bold=True, font_size=14)
    doc.add_paragraph("Bold text", fmt)
    doc.save(path)
    loaded = Document.open(path)
    assert loaded.paragraphs[0].runs[0].fmt.bold is True
    assert loaded.paragraphs[0].runs[0].fmt.font_size == 14
