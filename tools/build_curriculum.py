#!/usr/bin/env python3
"""Generate CURRICULUM.md, course READMEs and chapter stubs from tools/data/curriculum.yml.

Usage:
    python tools/build_curriculum.py          # write files
    python tools/build_curriculum.py --check  # exit 1 if any generated file is stale (CI)

Rules:
  * CURRICULUM.md is fully generated.
  * Course READMEs: only the text between GEN_BEGIN and GEN_END is rewritten;
    anything outside the markers is preserved (hand-written course notes).
  * Chapter files are created as "planned" stubs only if they do not exist.
    Existing chapter files are never modified.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "tools" / "data"
GEN_BEGIN = "<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->"
GEN_END = "<!-- END GENERATED -->"
STATUS_RE = re.compile(r"<!--\s*status:\s*([a-z-]+)\s*-->")
STATUS_LABEL = {
    "planned": "⬜ planned",
    "draft": "✏️ draft",
    "verified": "✅ verified",
    "reviewed": "🏁 reviewed",
}


# --------------------------------------------------------------------------- data
def load():
    cur = yaml.safe_load((DATA / "curriculum.yml").read_text(encoding="utf-8"))
    fe = yaml.safe_load((DATA / "fe_spec.yml").read_text(encoding="utf-8"))
    validate(cur, fe)
    return cur, fe


def validate(cur, fe):
    errors = []
    ids = [c["id"] for c in cur["courses"]]
    if len(ids) != len(set(ids)):
        errors.append("duplicate course ids")
    order = {cid: i for i, cid in enumerate(ids)}
    seen_ch = set()
    for c in cur["courses"]:
        for p in c.get("prerequisites", []):
            if p not in order:
                errors.append(f"{c['id']}: unknown prerequisite {p}")
            elif order[p] >= order[c["id"]]:
                errors.append(f"{c['id']}: prerequisite {p} is not earlier in the sequence")
        for area in c.get("fe", []):
            if area not in fe["areas"]:
                errors.append(f"{c['id']}: unknown FE area {area}")
        for ch in c["chapters"]:
            if not ch["id"].startswith(c["id"] + "-"):
                errors.append(f"chapter {ch['id']} does not belong to course {c['id']}")
            if ch["id"] in seen_ch:
                errors.append(f"duplicate chapter id {ch['id']}")
            seen_ch.add(ch["id"])
            if not re.fullmatch(r"[a-z0-9-]+", ch["slug"]):
                errors.append(f"bad slug {ch['slug']}")
    if errors:
        sys.exit("curriculum.yml validation failed:\n  " + "\n  ".join(errors))


# --------------------------------------------------------------------------- paths
def course_dir(c) -> str:
    return f"courses/{c['id']}-{c['slug']}"


def chapter_path(c, ch) -> str:
    return f"{course_dir(c)}/chapters/{ch['id']}-{ch['slug']}.md"


def chapter_status(c, ch) -> str:
    p = ROOT / chapter_path(c, ch)
    if not p.exists():
        return "planned"
    m = STATUS_RE.search(p.read_text(encoding="utf-8")[:500])
    return m.group(1) if m else "planned"


def course_hours(c) -> float:
    return sum(ch["hours"] for ch in c["chapters"]) + c.get("review_hours", 0)


def fmt_h(x: float) -> str:
    return f"{x:g}"


# --------------------------------------------------------------------------- graph
def transitive_reduction(courses):
    """Return {course_id: [direct prereqs not implied by other prereqs]}."""
    prereq = {c["id"]: set(c.get("prerequisites", [])) for c in courses}

    def ancestors(cid, memo={}):
        if cid in memo:
            return memo[cid]
        acc = set()
        for p in prereq[cid]:
            acc |= {p} | ancestors(p)
        memo[cid] = acc
        return acc

    reduced = {}
    for cid, ps in prereq.items():
        keep = []
        for p in sorted(ps):
            implied = any(p in ancestors(q) for q in ps if q != p)
            if not implied:
                keep.append(p)
        reduced[cid] = keep
    return reduced


def mermaid_graph(cur) -> str:
    courses = cur["courses"]
    reduced = transitive_reduction(courses)
    lines = ["```mermaid", "flowchart TD"]
    for t in cur["terms"]:
        lines.append(f'  subgraph T{t["id"]}["Term {t["id"]} — {t["title"]}"]')
        for c in courses:
            if c["term"] == t["id"]:
                label = f'{c["id"]} {c["title"]}'.replace('"', "'")
                lines.append(f'    C{c["id"]}["{label}"]')
        lines.append("  end")
    for c in courses:
        for p in reduced[c["id"]]:
            lines.append(f"  C{p} --> C{c['id']}")
    lines.append("```")
    return "\n".join(lines)


# --------------------------------------------------------------------------- CURRICULUM.md
def build_curriculum_md(cur, fe) -> str:
    courses = cur["courses"]
    n_ch = sum(len(c["chapters"]) for c in courses)
    total_course_h = sum(course_hours(c) for c in courses)
    cap_h = sum(k["hours"] for k in cur["capstones"])
    chk_h = cur["checkpoint_hours"] * len(cur["terms"])
    grand = total_course_h + cap_h + chk_h
    by_id = {c["id"]: c for c in courses}
    out = []
    w = out.append
    w("# Curriculum")
    w("")
    w(GEN_BEGIN)
    w("")
    w("The complete map of the Self-Taught BSEE: every course and chapter, with university equivalents, "
      "textbook alignment, prerequisites, learning objectives and estimated study hours. "
      "For the week-by-week schedule see [STUDY_PLAN.md](STUDY_PLAN.md). For build status see "
      "[PROGRESS.md](PROGRESS.md).")
    w("")
    w(f"**At a glance:** {len(courses)} courses · {n_ch} chapters · 7 terms · 4 capstones · "
      f"≈ {fmt_h(round(grand, -1))} study hours in total (courses {fmt_h(total_course_h)} h, "
      f"capstones {fmt_h(cap_h)} h, term checkpoints {fmt_h(chk_h)} h).")
    w("")
    w("> **About the hour estimates.** Hours cover reading, working the examples, the full problem set and the "
      "lab for each chapter, for a strong learner meeting the material for the first time. At 10–12 hours per "
      "week, the full curriculum is a multi-year undertaking; see [STUDY_PLAN.md](STUDY_PLAN.md) for the "
      "calendar and the shorter practitioner fast track.")
    w("")
    w("## Course map")
    w("")
    w("| Course | Term | Chapters | Hours | Typical university equivalent |")
    w("|---|---|---|---|---|")
    for c in courses:
        w(f"| [{c['id']} · {c['title']}](#course-{c['id']}) | {c['term']} | {len(c['chapters'])} | "
          f"{fmt_h(course_hours(c))} | {c['equivalents'][0]} |")
    w("")
    w("## Prerequisite graph")
    w("")
    w("Arrows point from a prerequisite to the course that needs it. Implied edges are omitted (if A → B → C, "
      "the edge A → C is not drawn).")
    w("")
    w(mermaid_graph(cur))
    w("")
    w("## FE Electrical & Computer coverage")
    w("")
    w(f"The NCEES FE Electrical and Computer exam (spec effective {fe['spec_effective']}, "
      f"{fe['total_questions']} questions, checked {fe['as_of']}; see "
      "[reference/research-log.md](reference/research-log.md#r-001--ncees-fe-electrical-and-computer-specification)) "
      "has 17 knowledge areas. Each maps onto the courses below, and each term checkpoint in "
      "[checkpoints/](checkpoints/README.md) samples the areas covered so far.")
    w("")
    w("| FE knowledge area | Exam questions | Primary courses |")
    w("|---|---|---|")
    for key, area in fe["areas"].items():
        cs = [c for c in courses if key in c.get("fe", [])]
        links = ", ".join(f"[{c['id']}](#course-{c['id']})" for c in cs) or "—"
        w(f"| {area['name']} | {area['questions']} | {links} |")
    w("")
    for t in cur["terms"]:
        tcs = [c for c in courses if c["term"] == t["id"]]
        th = sum(course_hours(c) for c in tcs)
        w(f"## Term {t['id']} — {t['title']}")
        w("")
        w(f"{t['summary']} *Term total: ≈ {fmt_h(th)} hours + checkpoint ({cur['checkpoint_hours']} h).*")
        w("")
        for c in tcs:
            w(f'<a id="course-{c["id"]}"></a>')
            w("")
            w(f"### {c['id']} · {c['title']}")
            w("")
            w(c["overview"])
            w("")
            w(f"- **Course page:** [{course_dir(c)}/]({course_dir(c)}/README.md)")
            w(f"- **University equivalents:** {'; '.join(c['equivalents'])}")
            w(f"- **Textbook alignment:** {'; '.join(c['textbooks'])}")
            if c.get("free_courses"):
                w(f"- **Free courses:** {'; '.join(c['free_courses'])}")
            pre = ", ".join(f"[{p} · {by_id[p]['title']}](#course-{p})" for p in c.get("prerequisites", [])) or "none"
            w(f"- **Prerequisites:** {pre}")
            fe_names = ", ".join(fe["areas"][a]["name"] for a in c.get("fe", [])) or "—"
            w(f"- **FE areas served:** {fe_names}")
            if c.get("companion"):
                w(f"- **Deeper:** see companion repo(s): {c['companion']}")
            w(f"- **Study hours:** ≈ {fmt_h(course_hours(c))} "
              f"({fmt_h(sum(ch['hours'] for ch in c['chapters']))} chapter hours + {fmt_h(c.get('review_hours', 0))} review/exam)")
            w("")
            w("**Learning objectives.** By the end of the course you can:")
            w("")
            for i, o in enumerate(c["objectives"], 1):
                w(f"{i}. {o}")
            w("")
            w("| Chapter | Hours | Key topics |")
            w("|---|---|---|")
            for ch in c["chapters"]:
                w(f"| [{ch['id']} · {ch['title']}]({chapter_path(c, ch)}) | {fmt_h(ch['hours'])} | {ch['topics']} |")
            w("")
    w("## Capstones and checkpoints")
    w("")
    w("| Item | Hours | Prerequisites |")
    w("|---|---|---|")
    for k in cur["capstones"]:
        pre = ", ".join(f"[{p}](#course-{p})" for p in k["prerequisites"])
        w(f"| Capstone {k['id']}: {k['title']} | {k['hours']} | {pre} |")
    for t in cur["terms"]:
        w(f"| Term {t['id']} checkpoint (FE-style, 40–60 questions) | {cur['checkpoint_hours']} | Term {t['id']} courses |")
    w("")
    w("## Changes to the original plan")
    w("")
    w("Chapter splits that differ from the original build brief are logged in "
      "[PROGRESS.md](PROGRESS.md#change-log).")
    w("")
    w(GEN_END)
    w("")
    return "\n".join(out)


# --------------------------------------------------------------------------- course README
def materials_cell(c, ch) -> str:
    d = ROOT / course_dir(c)
    parts = []
    if (d / "problems" / f"{ch['id']}-problems.md").exists():
        parts.append(f"[problems](problems/{ch['id']}-problems.md)")
    if (d / "solutions" / f"{ch['id']}-solutions.md").exists():
        parts.append(f"[solutions](solutions/{ch['id']}-solutions.md)")
    lab = d / "labs" / f"{ch['id']}-lab" / "README.md"
    if lab.exists():
        parts.append(f"[lab](labs/{ch['id']}-lab/README.md)")
    v = d / "verify" / f"verify_{ch['id'].replace('-', '_')}.py"
    if v.exists():
        parts.append(f"[verify](verify/{v.name})")
    return " · ".join(parts) if parts else "—"


def build_course_block(c, cur, fe) -> str:
    by_id = {x["id"]: x for x in cur["courses"]}
    out = []
    w = out.append
    w(GEN_BEGIN)
    w("")
    w(f"# {c['id']} · {c['title']}")
    w("")
    w(c["overview"])
    w("")
    w("| | |")
    w("|---|---|")
    w(f"| **Term** | {c['term']} |")
    w(f"| **Study hours** | ≈ {fmt_h(course_hours(c))} |")
    w(f"| **University equivalents** | {'; '.join(c['equivalents'])} |")
    w(f"| **Textbook alignment** | {'; '.join(c['textbooks'])} |")
    if c.get("free_courses"):
        w(f"| **Free courses** | {'; '.join(c['free_courses'])} |")
    pre = ", ".join(f"[{p} · {by_id[p]['title']}](../{p}-{by_id[p]['slug']}/README.md)"
                    for p in c.get("prerequisites", [])) or "none"
    w(f"| **Prerequisites** | {pre} |")
    fe_names = ", ".join(fe["areas"][a]["name"] for a in c.get("fe", [])) or "—"
    w(f"| **FE areas** | {fe_names} |")
    if c.get("companion"):
        w(f"| **Deeper** | Companion repo(s): {c['companion']} |")
    w("")
    w("## Learning objectives")
    w("")
    for i, o in enumerate(c["objectives"], 1):
        w(f"{i}. {o}")
    w("")
    w("## Chapter map")
    w("")
    w("| Chapter | Hours | Status | Materials |")
    w("|---|---|---|---|")
    for ch in c["chapters"]:
        st = STATUS_LABEL.get(chapter_status(c, ch), chapter_status(c, ch))
        w(f"| [{ch['id']} · {ch['title']}](chapters/{ch['id']}-{ch['slug']}.md) | {fmt_h(ch['hours'])} | {st} | "
          f"{materials_cell(c, ch)} |")
    w("")
    d = ROOT / course_dir(c)
    extras = []
    if (d / "exam" / "README.md").exists():
        extras.append("[Course final exam](exam/README.md)")
    fc = ROOT / "flashcards" / f"{c['id']}-{c['slug']}.csv"
    if fc.exists():
        extras.append(f"[Flashcards (Anki CSV)](../../flashcards/{fc.name})")
    eq = ROOT / "reference" / "equation-sheets" / f"{c['id']}-{c['slug']}.md"
    if eq.exists():
        extras.append(f"[Equation sheet](../../reference/equation-sheets/{eq.name})")
    if extras:
        w("**Course resources:** " + " · ".join(extras))
        w("")
    w("Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)")
    w("")
    w(GEN_END)
    return "\n".join(out)


def merge_block(existing: str | None, block: str) -> str:
    if existing and GEN_BEGIN in existing and GEN_END in existing:
        pre, rest = existing.split(GEN_BEGIN, 1)
        _, post = rest.split(GEN_END, 1)
        return pre + block + post
    tail = "\n\n## Course notes\n\n*(Hand-written notes for this course go below the generated block.)*\n"
    return block + tail


# --------------------------------------------------------------------------- README block
def build_readme_block(cur) -> str:
    courses = cur["courses"]
    out = [GEN_BEGIN, "", "### Course map", "",
           "| Term | Course | Chapters | Hours | Written |", "|---|---|---|---|---|"]
    for c in courses:
        written = sum(1 for ch in c["chapters"] if chapter_status(c, ch) != "planned")
        out.append(f"| {c['term']} | [{c['id']} · {c['title']}]({course_dir(c)}/README.md) | {len(c['chapters'])} | "
                   f"{fmt_h(course_hours(c))} | {written}/{len(c['chapters'])} |")
    out += ["", "### Prerequisite graph", "",
            "Arrows point from a prerequisite to the course that depends on it (implied edges omitted).", "",
            mermaid_graph(cur), "", GEN_END]
    return "\n".join(out)


# --------------------------------------------------------------------------- STUDY_PLAN block
def _expand(item: str, by_id: dict):
    """Expand a sequence item into (course, [chapters], include_review)."""
    if ".." in item:
        a, b = item.split("..")
        c = by_id[a[:2]]
        ids = [ch["id"] for ch in c["chapters"]]
        chs = c["chapters"][ids.index(a): ids.index(b) + 1]
        last = chs[-1]["id"] == c["chapters"][-1]["id"]
        return c, chs, last
    c = by_id[item]
    return c, c["chapters"], True


def build_study_block(cur) -> str:
    by_id = {c["id"]: c for c in cur["courses"]}
    caps = {k["id"]: k for k in cur["capstones"]}
    wk = cur["weekly_hours"]
    per_year = cur["study_weeks_per_year"]
    out = [GEN_BEGIN, ""]
    cum = 0.0

    def weeks(h0, h1):
        a = int(h0 // wk) + 1
        b = max(a, int(-(-h1 // wk)))
        return f"{a}" if a == b else f"{a}–{b}"

    out += ["## Term-by-term schedule", "",
            f"Computed at **{wk} hours per week**, in the recommended order. \"Week\" is the program week, counted "
            "from the day you start. Each course row includes its review and final exam. Expand a term to see "
            "chapter-level weeks.", ""]
    for t in cur["terms"]:
        seq = t.get("sequence") or ([*cur["term7_sequence"]] if t["id"] == 7 else
                                    [c["id"] for c in cur["courses"] if c["term"] == t["id"]])
        rows, detail = [], []
        t0 = cum
        for item in seq:
            if item in caps:
                k = caps[item]
                rows.append(f"| {weeks(cum, cum + k['hours'])} | Capstone {k['id']}: {k['title']} | {k['hours']} |")
                detail.append(f"| {weeks(cum, cum + k['hours'])} | Capstone {k['id']} | {k['hours']} |")
                cum += k["hours"]
                continue
            c, chs, review = _expand(item, by_id)
            start = cum
            for ch in chs:
                detail.append(f"| {weeks(cum, cum + ch['hours'])} | {ch['id']} {ch['title']} | {fmt_h(ch['hours'])} |")
                cum += ch["hours"]
            if review and c.get("review_hours"):
                detail.append(f"| {weeks(cum, cum + c['review_hours'])} | {c['id']} review + final exam | "
                              f"{fmt_h(c['review_hours'])} |")
                cum += c["review_hours"]
            span = "" if len(chs) == len(c["chapters"]) else f" (chapters {chs[0]['id']}–{chs[-1]['id']})"
            rows.append(f"| {weeks(start, cum)} | [{c['id']} · {c['title']}]({course_dir(c)}/README.md){span} | "
                        f"{fmt_h(cum - start)} |")
        ck = cur["checkpoint_hours"]
        rows.append(f"| {weeks(cum, cum + ck)} | **Term {t['id']} checkpoint** (FE-style exam + error log review) | {ck} |")
        detail.append(f"| {weeks(cum, cum + ck)} | Term {t['id']} checkpoint | {ck} |")
        cum += ck
        n_weeks = (cum - t0) / wk
        out += [f"### Term {t['id']} — {t['title']}", "",
                f"≈ {fmt_h(round(cum - t0))} hours · ≈ {round(n_weeks)} weeks · ends around program week "
                f"{int(-(-cum // wk))} (≈ {cum / wk / per_year:.1f} years in, at {per_year} study weeks/year)", "",
                "| Weeks | Course | Hours |", "|---|---|---|", *rows, "",
                "<details><summary>Chapter-level weeks</summary>", "",
                "| Weeks | Item | Hours |", "|---|---|---|", *detail, "", "</details>", ""]
    total_weeks = cum / wk
    out += ["### Totals", "",
            f"- **Total:** ≈ {fmt_h(round(cum, -1))} hours ≈ {round(total_weeks)} study weeks.",
            f"- **Calendar time:** at {per_year} study weeks per year (6 weeks of breaks), "
            f"≈ **{total_weeks / per_year:.1f} years** at {wk} h/week.",
            f"- **Faster pace:** at 15 h/week it is ≈ {cum / 15 / per_year:.1f} years.", ""]

    # fast track
    ft = cur["paths"]["fast_track"]
    chap_index = {ch["id"]: (c, ch) for c in cur["courses"] for ch in c["chapters"]}
    out += ["## Practitioner fast track", "",
            "The minimum path to fluent, skeptical conversations with engineering leaders. In fast-track mode you "
            "read each chapter, work its examples, do the concept check and the **[A]** problems, and skip the "
            f"[B]/[C] sets. That is estimated at {int(ft['factor'] * 100)}% of the full chapter hours. "
            "Courses " + ", ".join(ft["full_courses"]) + " are done in full.", "",
            "| Course | Chapters | Fast-track hours |", "|---|---|---|"]
    ft_total = 0.0
    groups: dict[str, list] = {}
    for cid in ft["chapters"]:
        c, ch = chap_index[cid]
        groups.setdefault(c["id"], []).append(ch)
    for cid, chs in groups.items():
        c = by_id[cid]
        h = sum(ch["hours"] for ch in chs) * ft["factor"]
        ft_total += h
        links = ", ".join(f"[{ch['id']}]({chapter_path(c, ch)})" for ch in chs)
        out.append(f"| {cid} · {c['title']} | {links} | {h:.0f} |")
    for cid in ft["full_courses"]:
        c = by_id[cid]
        h = course_hours(c)
        ft_total += h
        out.append(f"| {cid} · {c['title']} | all (full depth) | {fmt_h(h)} |")
    out += [f"| **Total** | | **≈ {fmt_h(round(ft_total, -1))}** |", "",
            f"At {wk} h/week that is ≈ {ft_total / wk:.0f} weeks (≈ {ft_total / wk / per_year:.1f} years). "
            "Chapters skipped on the fast track can be back-filled later without re-doing anything.", ""]

    # FE prep
    fp = cur["paths"]["fe_prep"]
    fe_h = sum(course_hours(c) for c in cur["courses"] if c["term"] in fp["terms"])
    fe_h += sum(chap_index[x][1]["hours"] for x in fp["chapters"])
    fe_h += cur["checkpoint_hours"] * len(fp["checkpoints"])
    out += ["## FE preparation path", "",
            "All courses in Terms " + ", ".join(map(str, fp["terms"])) + ", plus the chapters "
            + ", ".join(f"[{x}]({chapter_path(*chap_index[x])})" for x in fp["chapters"])
            + " (power systems, materials, economics and ethics), plus checkpoints "
            + ", ".join(map(str, fp["checkpoints"])) + ". "
            f"Total ≈ **{fmt_h(round(fe_h, -1))} hours**, then a full-length practice exam under exam conditions.", "",
            GEN_END]
    return "\n".join(out)


# --------------------------------------------------------------------------- stubs
def chapter_stub(c, ch) -> str:
    return f"""<!-- status: planned -->
# {ch['id']} · {ch['title']}

> **Status: planned.** This chapter has not been written yet. The build order and the current next step are in [PROGRESS.md](../../../PROGRESS.md).

**Course:** [{c['id']} · {c['title']}](../README.md) · **Estimated study hours:** {fmt_h(ch['hours'])}

**Planned topics:** {ch['topics']}.
"""


# --------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="fail if generated files are stale")
    args = ap.parse_args()
    cur, fe = load()

    targets: dict[Path, str] = {}
    targets[ROOT / "CURRICULUM.md"] = build_curriculum_md(cur, fe)
    for c in cur["courses"]:
        readme = ROOT / course_dir(c) / "README.md"
        existing = readme.read_text(encoding="utf-8") if readme.exists() else None
        targets[readme] = merge_block(existing, build_course_block(c, cur, fe))
        for ch in c["chapters"]:
            p = ROOT / chapter_path(c, ch)
            if not p.exists():
                targets[p] = chapter_stub(c, ch)

    readme = ROOT / "README.md"
    if readme.exists():
        targets[readme] = merge_block(readme.read_text(encoding="utf-8"), build_readme_block(cur))
    plan = ROOT / "STUDY_PLAN.md"
    if plan.exists():
        targets[plan] = merge_block(plan.read_text(encoding="utf-8"), build_study_block(cur))

    stale = []
    for path, text in targets.items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != text:
            stale.append(path)
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
    rel = [str(p.relative_to(ROOT)) for p in stale]
    if args.check:
        if rel:
            print("Generated files are stale; run `python tools/build_curriculum.py`:\n  " + "\n  ".join(rel))
            return 1
        print("curriculum: generated files up to date")
        return 0
    print(f"curriculum: wrote {len(rel)} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
