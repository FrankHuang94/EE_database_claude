#!/usr/bin/env python3
"""Lint: a currency '$' on a line with inline math must be escaped as '\\$'.

Inline math is paired with the same rule the site's renderer (pymdownx.arithmatex) uses: a '$' not preceded by
a backslash, then non-space content, then a '$' not preceded by whitespace. On a line that has at least one such
pair, any other unescaped '$' is a currency sign that a renderer with a looser pairing rule (GitHub's, for
example) can pair with a math delimiter. Lines inside fenced code and lines with display math ('$$') are skipped.

Usage:
    python tools/check_currency.py           # report offending lines; exit 1 if any (CI)
    python tools/check_currency.py --fix     # escape them in place
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {"site", "docs", "node_modules", ".venv", ".git"}
RE_INLINE = re.compile(r"(?<!\\)(\$)(?!\s)((?:\\.|[^\\$])+?)(?<!\s)(\$)")


def mask_code(line):
    """Blank out inline code spans (`...`) so a '$' inside them is not read as currency or math."""
    return re.sub(r"(`+)(.+?)\1", lambda m: m.group(1) + " " * len(m.group(2)) + m.group(1), line)


def offending(line):
    """Indices of unescaped '$' that are not inline-math delimiters, on a line that has inline math."""
    line = mask_code(line)
    if "$" not in line or "$$" in line:
        return []
    delims, pos = set(), 0
    while (m := RE_INLINE.search(line, pos)):
        delims.update((m.start(1), m.start(3)))
        pos = m.end()
    if not delims:
        return []
    return [i for i, c in enumerate(line) if c == "$" and (i == 0 or line[i - 1] != "\\") and i not in delims]


def md_files():
    for p in sorted(ROOT.rglob("*.md")):
        if not any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            yield p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true")
    args = ap.parse_args()
    problems = 0
    for f in md_files():
        lines = f.read_text(encoding="utf-8").split("\n")
        in_code, changed = False, False
        for n, line in enumerate(lines):
            if line.lstrip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            bad = offending(line)
            if not bad:
                continue
            problems += 1
            if args.fix:
                for i in reversed(bad):
                    line = line[:i] + "\\" + line[i:]
                lines[n], changed = line, True
            else:
                print(f"{f.relative_to(ROOT)}:{n + 1}: unescaped currency '$' on a line with inline math")
        if changed:
            f.write_text("\n".join(lines), encoding="utf-8")
    verb = "fixed" if args.fix else "found"
    print(f"currency: {problems} line(s) {verb}")
    return 1 if problems and not args.fix else 0


if __name__ == "__main__":
    sys.exit(main())
