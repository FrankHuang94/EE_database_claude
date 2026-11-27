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


# Acronyms whose letters come from inside words or from a symbol, so the letter-order test rejects them, but whose
# glossary term really is their expansion: equivalent series inductance (L), near-/far-end crosstalk (X),
# discontinuous reception (X), second- and third-order intercept points (IP2, IP3).
ACR_EXTRA = {"ESL", "NEXT", "FEXT", "DRX", "IP2", "IP3"}
BARE = re.compile(r"^[A-Z][A-Za-z0-9/&-]{1,9}$")


def norm(exp):
    """A comparison key for an expansion: lower case, hyphens as spaces, no parenthetical, no plural s."""
    e = re.sub(r"\s*\([^)]*\)", "", exp).lower().replace("-", " ").replace("–", " ")
    e = re.sub(r"[^a-z0-9 ]", "", e)
    e = re.sub(r"\s+", " ", e).strip()
    return e[:-1] if e.endswith("s") else e


def definition_expansion(acr, definition):
    """The expansion a bare-acronym entry's definition opens with, if its letters spell the acronym."""
    d = definition.strip()
    d = d[1:] if d.startswith("(") else d
    d = re.sub(r"^(?:The|A|An)\s+", "", d)
    head = re.split(r"[,:;.(]| \u2014 | - ", d, maxsplit=1)[0].strip()
    return head if 2 <= len(head) <= 80 and looks_like(acr, head) else None


def glossary_acronyms():
    """{acronym: {expansion key: (expansion, first chapter)}}: one entry per distinct meaning."""
    entries = yaml.safe_load((REF / "glossary.yml").read_text(encoding="utf-8"))
    found = {}

    def add(acr, exp, ch):
        exp = exp[:1].upper() + exp[1:]
        meanings = found.setdefault(acr, {})
        k = norm(exp)
        if k not in meanings or ch < meanings[k][1]:
            meanings[k] = (exp, ch)

    for e in entries:
        term, ch = str(e.get("term", "")).strip(), str(e.get("chapter", "")).strip()
        if BARE.match(term) and sum(c.isupper() for c in term) >= 2:
            exp = definition_expansion(term, str(e.get("definition", "")))
            if exp:
                add(term, exp, ch)
            continue
        for rx, swap in ((ACR_A, False), (ACR_B, True)):
            m = rx.match(term)
            if not m:
                continue
            acr, exp = m.group("acr"), m.group("exp").strip()
            if swap and not exp[:1].islower() and not re.search(r"\s", exp):
                continue
            if looks_like(acr, exp) or (not swap and acr in ACR_EXTRA):
                add(acr, exp, ch)
                break
    return found


def first_defined(acr, exp, texts):
    """The first chapter (in course order) that uses acr and also spells out its expansion, else the first use."""
    words = [re.escape(w) for w in re.split(r"[\s/-]+", re.sub(r"\s*\([^)]*\)", "", exp)) if w]
    used = re.compile(r"(?<![A-Za-z0-9])" + re.escape(acr) + r"(?![A-Za-z0-9])")
    for n in range(len(words), min(2, len(words)) - 1, -1):     # the whole expansion, then its leading words
        spelled = re.compile(r"[\s\-–/]+".join(words[:n]), re.I)
        for ch, text in texts:
            if used.search(text) and spelled.search(text):
                return ch
    for ch, text in texts:
        if used.search(text):
            return ch
    return None


def chapter_paths():
    paths = {}
    for f in (ROOT / "courses").glob("*/chapters/*.md"):
        paths[f.name[:5]] = f
    return paths


def acronyms_block(handwritten_rows):
    """Acronyms from the glossary, one row per meaning, except meanings the hand-written table already lists."""
    found = glossary_acronyms()
    paths = chapter_paths()
    hand = {(acr, norm(exp)) for acr, exp, _ in handwritten_rows}
    lines = ["## From the glossary", "",
             "Acronyms that appear in the glossary, as a term's name or as the term itself, with the chapter whose entry "
             "defines them first. An acronym with two meanings has a row for each. The table above lists the ones "
             "curated by hand.", "",
             "| Acronym | Expansion | First defined in |", "|---|---|---|"]
    for acr in sorted(found, key=lambda a: (a.lower(), a)):
        for k, (exp, ch) in sorted(found[acr].items(), key=lambda kv: kv[1][1]):
            if (acr, k) in hand or ch not in paths:
                continue
            rel = os.path.relpath(paths[ch], REF).replace(os.sep, "/")
            lines.append(f"| {acr} | {exp} | [{ch}]({rel}) |")
    return "\n".join(lines)


def hand_table(head, rows):
    """The curated table with each 'First defined in' link recomputed from the chapters."""
    paths = chapter_paths()
    texts = [(ch, paths[ch].read_text(encoding="utf-8")) for ch in sorted(paths)]
    for acr, exp, link in rows:
        ch = first_defined(acr, exp, texts)
        if ch:
            rel = os.path.relpath(paths[ch], REF).replace(os.sep, "/")
            head = head.replace(f"| {acr} | {exp} | {link} |", f"| {acr} | {exp} | [{ch}]({rel}) |")
    return head


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
                          "the chapter's as-of date and research-log ID; check the date before reusing a number. A bare number in "
                          "brackets, such as [3], cites the Sources list of the chapter the row comes from.")
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
    out[p] = (hand_table(head, hand), acronyms_block(hand))
    return out


def assemble(path, block):
    head, _ = split(path)
    if isinstance(block, tuple):
        head, block = block
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
