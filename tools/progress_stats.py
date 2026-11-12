#!/usr/bin/env python3
"""Compute build statistics and write them into the generated block of PROGRESS.md.

Counts per course: chapter status, words in written chapters, problems,
answer-key entries (machine-verified numbers), labs, notebooks, netlists and
testbenches; plus glossary terms and flashcards.

Usage:
    python tools/progress_stats.py          # rewrite the stats block
    python tools/progress_stats.py --check  # exit 1 if the block is stale
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BEGIN = "<!-- BEGIN STATS (tools/progress_stats.py) -->"
END = "<!-- END STATS -->"
STATUS_RE = re.compile(r"<!--\s*status:\s*([a-z-]+)\s*-->")


def words(md: str) -> int:
    md = re.sub(r"```.*?```", " ", md, flags=re.S)
    md = re.sub(r"<!--.*?-->", " ", md, flags=re.S)
    md = re.sub(r"\$\$.*?\$\$", " ", md, flags=re.S)
    return len(re.findall(r"[A-Za-z0-9][\w'’-]*", md))


def key_rows(md: str) -> int:
    n, on = 0, False
    for line in md.splitlines():
        if line.strip() == "<!-- answer-key -->":
            on = True
            continue
        if on:
            if line.strip().startswith("|"):
                if not set(line.replace("|", "").strip()) <= set("-: ") and not re.match(r"^\|\s*ID\s*\|", line):
                    n += 1
            elif n and line.strip() == "":
                on = False
    return n


def build() -> str:
    cur = yaml.safe_load((ROOT / "tools" / "data" / "curriculum.yml").read_text(encoding="utf-8"))
    rows = []
    tot = dict(ch=0, written=0, verified=0, reviewed=0, words=0, probs=0, keys=0, labs=0, nb=0, cir=0, tb=0)
    for c in cur["courses"]:
        d = ROOT / f"courses/{c['id']}-{c['slug']}"
        st = {"planned": 0, "draft": 0, "verified": 0, "reviewed": 0}
        w = probs = keys = 0
        for ch in c["chapters"]:
            p = d / "chapters" / f"{ch['id']}-{ch['slug']}.md"
            text = p.read_text(encoding="utf-8") if p.exists() else ""
            m = STATUS_RE.search(text[:300])
            s = m.group(1) if m else "planned"
            st[s] = st.get(s, 0) + 1
            if s != "planned":
                w += words(text)
                keys += key_rows(text)
        for pf in (d / "problems").glob("*.md") if (d / "problems").exists() else []:
            probs += len(re.findall(r"^### Problem ", pf.read_text(encoding="utf-8"), re.M))
        for sf in [*(d / "solutions").glob("*.md"), *(d / "exam").glob("*.md")]:
            keys += key_rows(sf.read_text(encoding="utf-8"))
        labs = len(list((d / "labs").glob("*/README.md")))
        nb = len(list(d.glob("labs/**/*.ipynb")))
        cir = len(list(d.glob("labs/**/*.cir")))
        tb = len(list(d.glob("labs/**/*_tb.*v")))
        written = len(c["chapters"]) - st["planned"]
        if written:
            rows.append(f"| {c['id']} | {len(c['chapters'])} | {written} | {st['verified'] + st['reviewed']} | "
                        f"{st['reviewed']} | {w:,} | {probs} | {keys} | {labs} | {nb} / {cir} / {tb} |")
        tot["ch"] += len(c["chapters"])
        tot["written"] += written
        tot["verified"] += st["verified"] + st["reviewed"]
        tot["reviewed"] += st["reviewed"]
        tot["words"] += w
        tot["probs"] += probs
        tot["keys"] += keys
        tot["labs"] += labs
        tot["nb"] += nb
        tot["cir"] += cir
        tot["tb"] += tb
    gl = yaml.safe_load((ROOT / "reference" / "glossary.yml").read_text(encoding="utf-8")) or []
    cards = 0
    for f in (ROOT / "flashcards").glob("*.csv"):
        cards += sum(1 for ln in f.read_text(encoding="utf-8").splitlines() if ln and not ln.startswith("#"))
    out = [BEGIN, "",
           "*Auto-generated; do not edit by hand. Courses appear once any chapter is written.*", "",
           "| Course | Chapters | Written | Verified | Reviewed | Words | Problems | Verified numbers | Labs | Notebooks / netlists / testbenches |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    out += rows or ["| — | | | | | | | | | |"]
    out += [f"| **Total** | **{tot['ch']}** | **{tot['written']}** | **{tot['verified']}** | **{tot['reviewed']}** | "
            f"**{tot['words']:,}** | **{tot['probs']}** | **{tot['keys']}** | **{tot['labs']}** | "
            f"**{tot['nb']} / {tot['cir']} / {tot['tb']}** |", "",
            f"Glossary terms: **{len(gl)}** · Flashcards: **{cards}**", "", END]
    return "\n".join(out)


def main() -> int:
    prog = ROOT / "PROGRESS.md"
    text = prog.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        sys.exit("PROGRESS.md lacks the stats markers")
    pre, rest = text.split(BEGIN, 1)
    _, post = rest.split(END, 1)
    new = pre + build() + post
    if "--check" in sys.argv:
        if new != text:
            print("PROGRESS.md stats are stale; run `python tools/progress_stats.py`")
            return 1
        print("progress stats: up to date")
        return 0
    prog.write_text(new, encoding="utf-8")
    print("progress stats: updated PROGRESS.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
