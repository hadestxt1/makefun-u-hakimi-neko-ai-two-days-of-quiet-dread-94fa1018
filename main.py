#!/usr/bin/env python3
"""Two Days of Quiet Dread — one approving code-review comment.

The program writes a single hand-written line to /output/entry.txt:
an approval of a pull request carrying quiet existential dread.
It is deterministic by construction: no clock, no randomness, no
network, no model calls, no input files. Running it twice produces
the same bytes every time.
"""

from __future__ import annotations

import os
import sys

# The comment itself. Written by hand, kept as one literal so the
# output is exactly this line and nothing else.
COMMENT = (
    "LGTM. The tests pass for reasons no one on this team can explain "
    "anymore, and I have made my peace with that."
)

MAX_CHARS = 140


def build_comment() -> str:
    """Return the one-line comment the entry submits."""
    return COMMENT


def gate_ok(text: str) -> bool:
    """Mirror the competition gate: 1-140 chars, single line, not blank."""
    if not text or text.strip() == "":
        return False
    if text != text.strip():
        return False
    if len(text) > MAX_CHARS:
        return False
    if "\n" in text or "\r" in text:
        return False
    return True


def resolve_output_path() -> str:
    """Where the text goes: /output/entry.txt, unless overridden."""
    override = os.environ.get("MAKEFUN_OUTPUT_PATH")
    if override:
        return override
    return os.path.join(os.sep + "output", "entry.txt")


def write_entry(path: str, text: str) -> None:
    """Write the comment as UTF-8 text with a trailing newline."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")


def main() -> int:
    text = build_comment()
    if not gate_ok(text):
        print(f"comment fails the gate ({len(text)} chars)", file=sys.stderr)
        return 1
    write_entry(resolve_output_path(), text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
