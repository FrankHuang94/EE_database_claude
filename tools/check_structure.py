#!/usr/bin/env python3
"""Check that every written chapter (status other than "planned") follows the mandatory template,
and that its problem set, solutions, lab and verify script exist and are consistent.

Also validates the flashcard CSV files. Exits 1 on any error.
"""
from __future__ import annotations

import csv
import io
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
STATUS_RE = re.compile(r"<!--\s*status:\s*([a-z-]+)\s*-->")
SECTIONS = [
    "Big picture", "Intuition first", "Theory", "Worked examples", "Simulate it",
    "Engineering tradeoffs", "Numbers to know", "Common mistakes", "Practitioner lens",
    "Concept check", "Key terms", "Connections", "Further study", "Sources",
]
META_KEYS = ["Course", "University equivalent", "Prerequisites", "Estimated study hours", "Last verified"]


def h2s(text: str) -> list[str]:
    out, fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
        if not fence and line.startswith("## "):
            out.append(re.sub(r"^\d+\.\s*", "", line[3:].strip()))
    return out


def section(text: str, name: str) -> str:
    m = re.search(rf"^## (?:\d+\.\s*)?{re.escape(name)}.*?$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def check_chapter(c: dict, ch: dict, errs: list[str]) -> None:
    cdir = ROOT / f"courses/{c['id']}-{c['slug']}"
    path = cdir / "chapters" / f"{ch['id']}-{ch['slug']}.md"
    text = path.read_text(encoding="utf-8")
    m = STATUS_RE.search(text[:300])
    status = m.group(1) if m else "planned"
    if status == "planned":
        return
    tag = ch["id"]

    def err(msg):
        errs.append(f"{tag}: {msg}")

    # 1. metadata + objectives
    for k in META_KEYS:
        if f"**{k}**" not in text.split("## ", 1)[0]:
            err(f"metadata missing '{k}'")
    obj = re.search(r"\*\*Learning objectives\.\*\*(.*?)(?=\n## )", text, re.S)
    n_obj = len(re.findall(r"^\d+\.\s", obj.group(1), re.M)) if obj else 0
    if not 3 <= n_obj <= 6:
        err(f"needs 3–6 numbered learning objectives (found {n_obj})")
    # 2-12. sections in order
    found = h2s(text)
    pos = -1
    for s in SECTIONS:
        idx = next((i for i, h in enumerate(found) if h.startswith(s)), None)
        if idx is None:
            err(f"missing section '## {s}'")
        elif idx < pos:
            err(f"section '{s}' out of order")
        else:
            pos = idx
    ex = section(text, "Worked examples")
    n_ex = len(re.findall(r"^### Example", ex, re.M))
    if n_ex < 3:
        err(f"needs ≥3 worked examples (found {n_ex})")
    if "<!-- answer-key -->" not in text:
        err("no answer-key table for worked examples")
    tr = section(text, "Engineering tradeoffs")
    if not re.search(r"\|\s*Knob\s*\|\s*Improves\s*\|\s*Costs\s*\|", tr, re.I):
        err("tradeoffs table must have columns Knob | Improves | Costs | Typical decision owner")
    if "Marketing vs Reality" not in section(text, "Practitioner lens"):
        err("practitioner lens lacks a 'Marketing vs Reality' block")
    cc = section(text, "Concept check")
    n_cc = cc.count("<details>")
    if not 5 <= n_cc <= 8:
        err(f"concept check needs 5–8 <details> answers (found {n_cc})")
    if "glossary.md#" not in section(text, "Key terms"):
        err("key terms must link to the glossary")
    if "Simulate it" in found and "labs/" not in section(text, "Simulate it"):
        err("'Simulate it' must link to a lab in labs/")

    # problems / solutions / verify / lab
    pf = cdir / "problems" / f"{tag}-problems.md"
    sf = cdir / "solutions" / f"{tag}-solutions.md"
    vf = cdir / "verify" / f"verify_{tag.replace('-', '_')}.py"
    lab = cdir / "labs" / f"{tag}-lab" / "README.md"
    for p in (pf, sf, vf, lab):
        if not p.exists():
            err(f"missing {p.relative_to(ROOT)}")
    if pf.exists():
        ptext = pf.read_text(encoding="utf-8")
        probs = re.findall(rf"^### Problem {re.escape(tag)}\.(\d+)\s+\[([ABC])\]", ptext, re.M)
        if not 10 <= len(probs) <= 20:
            err(f"problem set needs 10–20 problems (found {len(probs)})")
        tiers = {t for _, t in probs}
        if not {"A", "B", "C"} <= tiers:
            err(f"problem set should include tiers A, B and C (found {sorted(tiers)})")
        if "Objective coverage" not in ptext:
            err("problem set lacks an 'Objective coverage' table")
        if sf.exists():
            stext = sf.read_text(encoding="utf-8")
            sols = set(re.findall(rf"^### Solution {re.escape(tag)}\.(\d+)", stext, re.M))
            missing = [n for n, _ in probs if n not in sols]
            if missing:
                err(f"no worked solution for problem(s) {', '.join(missing)}")
            if "<!-- answer-key -->" not in stext:
                err("solutions file has no answer-key table")


def check_flashcards(errs: list[str]) -> None:
    for f in sorted((ROOT / "flashcards").glob("*.csv")):
        rows = [ln for ln in f.read_text(encoding="utf-8").splitlines() if ln and not ln.startswith("#")]
        for i, row in enumerate(csv.reader(io.StringIO("\n".join(rows))), 1):
            if len(row) != 3 or not all(x.strip() for x in row):
                errs.append(f"{f.name}: card {i} must have non-empty Front, Back, Tags")


def main() -> int:
    cur = yaml.safe_load((ROOT / "tools" / "data" / "curriculum.yml").read_text(encoding="utf-8"))
    errs: list[str] = []
    n = 0
    for c in cur["courses"]:
        for ch in c["chapters"]:
            n += 1
            check_chapter(c, ch, errs)
    check_flashcards(errs)
    for e in errs:
        print("ERROR", e)
    print(f"structure: {n} chapters scanned, {len(errs)} problem(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
