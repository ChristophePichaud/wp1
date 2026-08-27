"""Command-line interface for wp1 word processor."""

import argparse
import sys
from pathlib import Path

from .document import Document


def cmd_new(args: argparse.Namespace) -> None:
    doc = Document(title=args.title)
    for line in args.text or []:
        doc.add_paragraph(line)
    doc.save(args.output)
    print(f"Created '{args.output}'")


def cmd_show(args: argparse.Namespace) -> None:
    doc = Document.open(args.file)
    if args.markdown:
        print(doc.to_markdown())
    else:
        print(doc.plain_text())


def cmd_replace(args: argparse.Namespace) -> None:
    doc = Document.open(args.file)
    n = doc.replace(args.old, args.new, regex=args.regex)
    doc.save(args.file)
    print(f"Replaced {n} occurrence(s) of '{args.old}' with '{args.new}'")


def cmd_find(args: argparse.Namespace) -> None:
    doc = Document.open(args.file)
    for para_idx, start, end in doc.find(args.pattern, regex=args.regex):
        para_text = doc.paragraphs[para_idx].plain_text()
        print(f"Para {para_idx}, [{start}:{end}]: …{para_text[max(0, start-10):end+10]}…")


def cmd_export(args: argparse.Namespace) -> None:
    doc = Document.open(args.file)
    out = Path(args.output)
    if out.suffix == ".md":
        doc.export_markdown(out)
    else:
        doc.export_text(out)
    print(f"Exported to '{out}'")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wp1",
        description="wp1 – Simple Word Processor v1",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # new
    p_new = sub.add_parser("new", help="Create a new document")
    p_new.add_argument("output", help="Output .wp1 file path")
    p_new.add_argument("--title", default="Untitled", help="Document title")
    p_new.add_argument("--text", nargs="*", help="Initial paragraph(s)")
    p_new.set_defaults(func=cmd_new)

    # show
    p_show = sub.add_parser("show", help="Display a document")
    p_show.add_argument("file", help="Document file path")
    p_show.add_argument("--markdown", action="store_true", help="Render as Markdown")
    p_show.set_defaults(func=cmd_show)

    # replace
    p_rep = sub.add_parser("replace", help="Find & replace text")
    p_rep.add_argument("file", help="Document file path")
    p_rep.add_argument("old", help="Text to find")
    p_rep.add_argument("new", help="Replacement text")
    p_rep.add_argument("--regex", action="store_true", help="Treat OLD as a regex pattern")
    p_rep.set_defaults(func=cmd_replace)

    # find
    p_find = sub.add_parser("find", help="Search for text")
    p_find.add_argument("file", help="Document file path")
    p_find.add_argument("pattern", help="Text or pattern to find")
    p_find.add_argument("--regex", action="store_true", help="Treat PATTERN as a regex")
    p_find.set_defaults(func=cmd_find)

    # export
    p_exp = sub.add_parser("export", help="Export to plain text or Markdown")
    p_exp.add_argument("file", help="Document file path")
    p_exp.add_argument("output", help="Output file (.txt or .md)")
    p_exp.set_defaults(func=cmd_export)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
