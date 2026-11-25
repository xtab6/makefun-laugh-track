#!/usr/bin/env python3
"""Laugh Track: The Crypto Trading Joke Contest — program/v1 entry.

Writes one original one-line joke about crypto trading life to
$MAKEFUN_OUTPUT_DIR/entry.txt (UTF-8, 1-200 chars, single line).

The joke: a trader over-annotates the chart with trend lines until the chart
itself fights back. Setup (drawing lines) + turn (harassment complaint),
punchline on the last word.
"""

import os
import sys

JOKE = "I drew so many lines on the chart it filed for harassment."


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get(
        "OUTPUT_DIR"
    ) or "/output"
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    # Clean only the contents of the output folder, never the folder itself:
    # the grader mounts it and removing it fails with EPERM.
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)

    text = JOKE
    encoded = text.encode("utf-8")
    if not 1 <= len(text) <= 200:
        print(f"entry must be 1-200 characters, got {len(text)}", file=sys.stderr)
        return 1
    if text.strip() == "" or "\n" in text or "\r" in text:
        print("entry must be a single non-blank line", file=sys.stderr)
        return 1

    target = os.path.join(out_dir, "entry.txt")
    with open(target, "wb") as f:
        f.write(encoded)
    # Read-back verification: the file on disk must decode to exactly the joke.
    with open(target, "rb") as f:
        raw = f.read()
    if raw != encoded or raw.decode("utf-8") != text:
        print("read-back mismatch", file=sys.stderr)
        return 1
    if not os.path.isdir(out_dir):
        print("output folder missing after write", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
