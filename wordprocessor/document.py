"""Core document model for the word processor."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, List, Optional


@dataclass
class TextFormat:
    """Character-level formatting attributes."""

    bold: bool = False
    italic: bool = False
    underline: bool = False
    font_size: int = 12  # points
    font_name: str = "Arial"

    def to_dict(self) -> dict:
        return {
            "bold": self.bold,
            "italic": self.italic,
            "underline": self.underline,
            "font_size": self.font_size,
            "font_name": self.font_name,
        }

    @staticmethod
    def from_dict(data: dict) -> "TextFormat":
        return TextFormat(
            bold=data.get("bold", False),
            italic=data.get("italic", False),
            underline=data.get("underline", False),
            font_size=data.get("font_size", 12),
            font_name=data.get("font_name", "Arial"),
        )


@dataclass
class TextRun:
    """A contiguous run of text sharing the same formatting."""

    text: str
    fmt: TextFormat = field(default_factory=TextFormat)

    def to_dict(self) -> dict:
        return {"text": self.text, "fmt": self.fmt.to_dict()}

    @staticmethod
    def from_dict(data: dict) -> "TextRun":
        return TextRun(
            text=data["text"],
            fmt=TextFormat.from_dict(data.get("fmt", {})),
        )

    def to_markdown(self) -> str:
        """Render this run to Markdown markup."""
        t = self.text
        if self.fmt.bold:
            t = f"**{t}**"
        if self.fmt.italic:
            t = f"*{t}*"
        if self.fmt.underline:
            t = f"__{t}__"
        return t

    def plain_text(self) -> str:
        return self.text


@dataclass
class Paragraph:
    """A paragraph composed of one or more text runs."""

    runs: List[TextRun] = field(default_factory=list)

    # -- factory helpers --------------------------------------------------

    @staticmethod
    def from_text(text: str, fmt: Optional[TextFormat] = None) -> "Paragraph":
        """Create a paragraph from a plain string."""
        return Paragraph(runs=[TextRun(text=text, fmt=fmt or TextFormat())])

    # -- serialisation ----------------------------------------------------

    def to_dict(self) -> dict:
        return {"runs": [r.to_dict() for r in self.runs]}

    @staticmethod
    def from_dict(data: dict) -> "Paragraph":
        return Paragraph(runs=[TextRun.from_dict(r) for r in data.get("runs", [])])

    # -- rendering --------------------------------------------------------

    def plain_text(self) -> str:
        return "".join(r.plain_text() for r in self.runs)

    def to_markdown(self) -> str:
        return "".join(r.to_markdown() for r in self.runs)

    # -- editing ----------------------------------------------------------

    def insert_text(self, offset: int, text: str, fmt: Optional[TextFormat] = None) -> None:
        """Insert *text* at character *offset* within this paragraph.

        Existing runs' formatting is preserved for the unmodified portions of
        text.  The newly inserted characters use *fmt* (defaults to a fresh
        :class:`TextFormat`).
        """
        plain = self.plain_text()
        if offset < 0 or offset > len(plain):
            raise IndexError(f"Offset {offset} out of range for paragraph of length {len(plain)}")
        new_fmt = fmt or TextFormat()
        new_runs: List[TextRun] = []
        pos = 0
        inserted = False
        for run in self.runs:
            run_end = pos + len(run.text)
            if not inserted and pos <= offset <= run_end:
                before = run.text[: offset - pos]
                after = run.text[offset - pos :]
                if before:
                    new_runs.append(TextRun(text=before, fmt=run.fmt))
                new_runs.append(TextRun(text=text, fmt=new_fmt))
                if after:
                    new_runs.append(TextRun(text=after, fmt=run.fmt))
                inserted = True
            else:
                new_runs.append(TextRun(text=run.text, fmt=run.fmt))
            pos = run_end
        if not inserted:
            new_runs.append(TextRun(text=text, fmt=new_fmt))
        self.runs = new_runs

    def delete_text(self, start: int, end: int) -> None:
        """Delete characters from *start* (inclusive) to *end* (exclusive).

        Existing runs' formatting is preserved for all characters outside the
        deleted range.
        """
        plain = self.plain_text()
        length = len(plain)
        if start < 0 or end > length or start > end:
            raise IndexError(f"Range [{start}, {end}) invalid for paragraph of length {length}")
        new_runs: List[TextRun] = []
        pos = 0
        for run in self.runs:
            run_end = pos + len(run.text)
            keep_before = run.text[: max(0, start - pos)]
            keep_after = run.text[max(0, end - pos) :]
            surviving = keep_before + keep_after
            if surviving:
                new_runs.append(TextRun(text=surviving, fmt=run.fmt))
            pos = run_end
        self.runs = new_runs or [TextRun(text="", fmt=self.runs[0].fmt if self.runs else TextFormat())]


class Document:
    """A simple word-processing document."""

    def __init__(self, title: str = "Untitled") -> None:
        self.title: str = title
        self.paragraphs: List[Paragraph] = []

    # -- paragraph operations --------------------------------------------

    def add_paragraph(self, text: str = "", fmt: Optional[TextFormat] = None) -> Paragraph:
        """Append a new paragraph and return it."""
        para = Paragraph.from_text(text, fmt)
        self.paragraphs.append(para)
        return para

    def insert_paragraph(self, index: int, text: str = "", fmt: Optional[TextFormat] = None) -> Paragraph:
        """Insert a paragraph at *index*."""
        para = Paragraph.from_text(text, fmt)
        self.paragraphs.insert(index, para)
        return para

    def delete_paragraph(self, index: int) -> None:
        """Remove the paragraph at *index*."""
        if index < 0 or index >= len(self.paragraphs):
            raise IndexError(f"Paragraph index {index} out of range")
        del self.paragraphs[index]

    # -- search & replace ------------------------------------------------

    def find(self, pattern: str, regex: bool = False, case_sensitive: bool = False) -> Iterator[tuple[int, int, int]]:
        """Yield *(para_index, start, end)* for every match of *pattern*.

        When *regex* is False the pattern is treated as a literal string.
        By default the search is case-insensitive; pass ``case_sensitive=True``
        to perform a case-sensitive match.
        """
        flags = 0 if case_sensitive else re.IGNORECASE
        rx = re.compile(pattern if regex else re.escape(pattern), flags)
        for i, para in enumerate(self.paragraphs):
            text = para.plain_text()
            for m in rx.finditer(text):
                yield (i, m.start(), m.end())

    def replace(self, old: str, new: str, regex: bool = False, case_sensitive: bool = False) -> int:
        """Replace all occurrences of *old* with *new*.

        By default the match is case-insensitive; pass ``case_sensitive=True``
        for a case-sensitive replacement.  Returns the total number of
        replacements made.
        """
        count = 0
        flags = 0 if case_sensitive else re.IGNORECASE
        rx = re.compile(old if regex else re.escape(old), flags)
        for para in self.paragraphs:
            plain = para.plain_text()
            replaced, n = rx.subn(new, plain)
            if n:
                fmt = para.runs[0].fmt if para.runs else TextFormat()
                para.runs = [TextRun(text=replaced, fmt=fmt)]
                count += n
        return count

    # -- plain-text rendering --------------------------------------------

    def plain_text(self) -> str:
        """Return the full document as plain text."""
        return "\n".join(p.plain_text() for p in self.paragraphs)

    def to_markdown(self) -> str:
        """Render the document as Markdown."""
        lines = [f"# {self.title}", ""]
        lines += [p.to_markdown() for p in self.paragraphs]
        return "\n".join(lines)

    # -- serialisation ---------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "paragraphs": [p.to_dict() for p in self.paragraphs],
        }

    @staticmethod
    def from_dict(data: dict) -> "Document":
        doc = Document(title=data.get("title", "Untitled"))
        doc.paragraphs = [Paragraph.from_dict(p) for p in data.get("paragraphs", [])]
        return doc

    # -- file I/O --------------------------------------------------------

    def save(self, path: str | Path) -> None:
        """Save the document to a JSON file."""
        Path(path).write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def open(path: str | Path) -> "Document":
        """Load a document from a JSON file."""
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return Document.from_dict(data)

    def export_text(self, path: str | Path) -> None:
        """Export document as plain text."""
        Path(path).write_text(self.plain_text(), encoding="utf-8")

    def export_markdown(self, path: str | Path) -> None:
        """Export document as Markdown."""
        Path(path).write_text(self.to_markdown(), encoding="utf-8")

    @staticmethod
    def import_text(path: str | Path, title: str = "") -> "Document":
        """Create a document from a plain-text file."""
        text = Path(path).read_text(encoding="utf-8")
        title = title or Path(path).stem
        doc = Document(title=title)
        for line in text.splitlines():
            doc.add_paragraph(line)
        return doc

    def __repr__(self) -> str:  # pragma: no cover
        return f"Document(title={self.title!r}, paragraphs={len(self.paragraphs)})"
