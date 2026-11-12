#!/usr/bin/env python3
"""Check every relative link (and #anchor) in the repository's Markdown files.

External (http/https/mailto) links are skipped here; they are checked by the
scheduled lychee job in CI. Anchors are validated against GitHub-style heading
slugs and explicit `<a id="...">` / `id="..."` anchors in the target file.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "site", "docs", "node_modules", ".venv", "venv", ".ipynb_checkpoints"}
LINK_RE = re.compile(r"!?\[(?:[^\[\]]|\[[^\]]*\])*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
HTML_LINK_RE = re.compile(r"""(?:href|src)=["']([^"']+)["']""")
ID_RE = re.compile(r"""\bid=["']([^"']+)["']""")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def md_files():
    for p in ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        yield p


def strip_code(text: str) -> str:
    """Blank out fenced code blocks and inline code so links inside them are ignored."""
    out, fence = [], None
    for line in text.splitlines():
        s = line.lstrip()
        if fence:
            if s.startswith(fence):
                fence = None
            out.append("")
            continue
        if s.startswith("```") or s.startswith("~~~"):
            fence = s[:3]
            out.append("")
            continue
        out.append(re.sub(r"`[^`]*`", "", line))
    return "\n".join(out)


def gh_slug(text: str) -> str:
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links -> text
    text = re.sub(r"<[^>]+>", "", text)                       # html tags
    text = text.replace("`", "").replace("*", "")
    text = text.strip().lower()
    out = []
    for ch in text:
        if ch.isalnum() or ch in "-_ ":
            out.append(ch)
        elif unicodedata.category(ch).startswith("M"):
            out.append(ch)
    return "".join(out).replace(" ", "-")


_anchor_cache: dict[Path, set[str]] = {}


def anchors_of(path: Path) -> set[str]:
    if path in _anchor_cache:
        return _anchor_cache[path]
    text = path.read_text(encoding="utf-8")
    anchors = set(ID_RE.findall(text))
    counts: dict[str, int] = {}
    for line in strip_code(text).splitlines():
        m = HEADING_RE.match(line)
        if m:
            base = gh_slug(m.group(2))
            n = counts.get(base, 0)
            anchors.add(base if n == 0 else f"{base}-{n}")
            counts[base] = n + 1
    _anchor_cache[path] = anchors
    return anchors


def main() -> int:
    errors = 0
    checked = 0
    for md in sorted(md_files()):
        text = strip_code(md.read_text(encoding="utf-8"))
        targets = LINK_RE.findall(text) + HTML_LINK_RE.findall(text)
        for t in targets:
            if re.match(r"^[a-z][a-z0-9+.-]*:", t) or t.startswith("//"):
                continue  # external or mailto
            checked += 1
            path_part, _, frag = t.partition("#")
            path_part = unquote(path_part)
            target = md if path_part == "" else (md.parent / path_part).resolve()
            if path_part and not target.exists():
                print(f"{md.relative_to(ROOT)}: broken link -> {t}")
                errors += 1
                continue
            if frag and target.is_file() and target.suffix == ".md":
                if unquote(frag) not in anchors_of(target):
                    print(f"{md.relative_to(ROOT)}: missing anchor -> {t}")
                    errors += 1
    print(f"links: {checked} relative links checked, {errors} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
