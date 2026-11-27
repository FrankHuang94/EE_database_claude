#!/usr/bin/env python3
"""Generate the consolidated reference pages from the chapters and the glossary.

  reference/numbers-to-know.md   every chapter's "Numbers to know" section (section 7), by course
  reference/reading-list.md      every chapter's "Further study" section (section 13), by course
  reference/acronyms.md          the hand-written rows plus every acronym in reference/glossary.yml

Only the text between the GENERATED markers is rewritten; the hand-written text above it is kept. Relative links
are rewritten so they resolve from reference/, and headings inside a copied section are demoted below the
chapter's heading.

Usage:
    python tools/build_reference.py          # write the files
    python tools/build_reference.py --check  # exit 1 if any generated block is stale (CI)
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "reference"
BEGIN = "<!-- BEGIN GENERATED (tools/build_reference.py): edit the chapters or glossary.yml, not this block -->"
END = "<!-- END GENERATED -->"
STATUS_RE = re.compile(r"<!--\s*status:\s*([a-z-]+)\s*-->")
TITLE_RE = re.compile(r"^# (\d\d-\d\d) · (.+)$", re.M)
LINK_RE = re.compile(r"(!?\[[^\]]*\])\(([^)\s]+)\)")


def section(text, number):
    m = re.search(rf"^## {number}\. [^\n]*\n(.*?)(?=^## {number + 1}\. )", text, re.M | re.S)
    return m.group(1).strip("\n") if m else ""


def rewrite(md, chapter: Path, out_dir: Path):
    def fix(m):
        label, target = m.group(1), m.group(2)
        if re.match(r"^[a-z]+:", target):
            return m.group(0)
        path, _, anchor = target.partition("#")
        src = chapter if path == "" else (chapter.parent / path).resolve()
        rel = os.path.relpath(src, out_dir).replace(os.sep, "/")
        return f"{label}({rel}{'#' + anchor if anchor else ''})"
    md = LINK_RE.sub(fix, md)
    return re.sub(r"^(#{3,5}) ", lambda m: "#" * (len(m.group(1)) + 1) + " ", md, flags=re.M)


def chapters():
    out = []
    for f in sorted((ROOT / "courses").glob("*/chapters/*.md")):
        text = f.read_text(encoding="utf-8")
        st, t = STATUS_RE.search(text), TITLE_RE.search(text)
        if st and st.group(1) != "planned" and t:
            out.append((t.group(1), t.group(2).strip(), f, text))
    return out


def course_titles():
    titles = {}
    for d in sorted((ROOT / "courses").iterdir()):
        r = d / "README.md"
        if r.exists():
            m = re.search(r"^# (.+)$", r.read_text(encoding="utf-8"), re.M)
            titles[d.name[:2]] = (d, m.group(1).strip() if m else d.name)
    return titles


def collected(number, intro):
    titles, body, last = course_titles(), [], None
    for key, title, f, text in chapters():
        sec = section(text, number)
        if not sec:
            continue
        cid = key[:2]
        if cid != last:
            cdir, ctitle = titles[cid]
            body += [f"## [{ctitle}]({os.path.relpath(cdir / 'README.md', REF).replace(os.sep, '/')})", ""]
            last = cid
        body += [f"### [{key} · {title}]({os.path.relpath(f, REF).replace(os.sep, '/')})", "", rewrite(sec, f, REF), ""]
    return "\n".join([intro, ""] + body).rstrip("\n")


# ---------------------------------------------------------------- acronyms
ACR_A = re.compile(r"^(?P<exp>.+?) \((?P<acr>[A-Za-z0-9/&+.-]{2,12})\)$")
ACR_B = re.compile(r"^(?P<acr>[A-Z][A-Za-z0-9/&+-]{1,11}) \((?P<exp>[^)]{4,})\)$")


def looks_like(acr, exp):
    """True if acr is plausibly an abbreviation of exp: at least two capitals, same first letter, letters in order."""
    if sum(c.isupper() for c in acr) < 2 or " " in acr:
        return False
    letters = [c.lower() for c in acr if c.isalpha()]
    words = exp.lower()
    if not letters or not words or letters[0] != words[0]:
        return False
    i = 0
    for ch in words:
        if i < len(letters) and ch == letters[i]:
            i += 1
    return i == len(letters)


def glossary_acronyms():
    entries = yaml.safe_load((REF / "glossary.yml").read_text(encoding="utf-8"))
    found = {}
    for e in entries:
        term, ch = str(e.get("term", "")).strip(), str(e.get("chapter", "")).strip()
        for rx, swap in ((ACR_A, False), (ACR_B, True)):
            m = rx.match(term)
            if not m:
                continue
            acr, exp = m.group("acr"), m.group("exp").strip()
            if swap and not exp[:1].islower() and not re.search(r"\s", exp):
                continue
            if looks_like(acr, exp):
                exp = exp[:1].upper() + exp[1:]
                if acr not in found or ch < found[acr][1]:
                    found[acr] = (exp, ch)
                break
    return found


def chapter_paths():
    paths = {}
    for f in (ROOT / "courses").glob("*/chapters/*.md"):
        paths[f.name[:5]] = f
    return paths


def acronyms_block(handwritten_rows):
    """Acronyms from the glossary that the hand-written table above the block does not already list."""
    found = glossary_acronyms()
    paths = chapter_paths()
    hand = {acr for acr, _, _ in handwritten_rows}
    lines = ["## From the glossary", "",
             "Acronyms that appear in the glossary's term names, with the chapter whose entry defines them first. "
             "The table above lists the ones curated by hand.", "",
             "| Acronym | Expansion | First defined in |", "|---|---|---|"]
    for acr in sorted(found, key=lambda a: (a.lower(), a)):
        exp, ch = found[acr]
        if acr in hand or ch not in paths:
            continue
        rel = os.path.relpath(paths[ch], REF).replace(os.sep, "/")
        lines.append(f"| {acr} | {exp} | [{ch}]({rel}) |")
    return "\n".join(lines)


def split(path):
    text = path.read_text(encoding="utf-8")
    if BEGIN in text:
        head, rest = text.split(BEGIN, 1)
        return head.rstrip("\n"), rest.split(END, 1)[1] if END in rest else ""
    return text.rstrip("\n"), ""


def render():
    out = {}
    p = REF / "numbers-to-know.md"
    head, _ = split(p)
    out[p] = collected(7, "## By chapter\n\nEach chapter's own *Numbers to know* table, in course order. Perishable values carry "
                          "the chapter's as-of date and research-log ID; check the date before reusing a number.")
    p = REF / "reading-list.md"
    out[p] = collected(13, "## By chapter\n\nEach chapter's *Further study* list: textbook sections, free courses, lecture "
                           "videos and landmark papers, in course order.")
    p = REF / "acronyms.md"
    head, tail = split(p)
    hand = []
    hand_text = head
    for m in re.finditer(r"^\| ([^|]+?) \| ([^|]+?) \| (\[[^\]]+\]\([^)]+\)) \|$", hand_text, re.M):
        if m.group(1) not in ("Acronym",):
            hand.append((m.group(1).strip(), m.group(2).strip(), m.group(3).strip()))
    out[p] = acronyms_block(hand)
    return out


def assemble(path, block):
    head, _ = split(path)
    return f"{head}\n\n{BEGIN}\n\n{block}\n\n{END}\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    stale = []
    for path, block in render().items():
        new = assemble(path, block)
        old = path.read_text(encoding="utf-8")
        if new != old:
            stale.append(path)
            if not args.check:
                path.write_text(new, encoding="utf-8")
    if args.check and stale:
        print("build_reference: stale: " + ", ".join(str(p.relative_to(ROOT)) for p in stale))
        return 1
    print(f"build_reference: {'checked' if args.check else 'wrote'} 3 files"
          + ("" if args.check else f" ({len(stale)} changed)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
