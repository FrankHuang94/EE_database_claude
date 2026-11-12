# CLAUDE.md — Build rules for the Self-Taught BSEE

**Read this file and [PROGRESS.md](PROGRESS.md) at the start of every session**, then continue from the "Next step" recorded in PROGRESS.md. Don't re-plan or rewrite finished work unless PROGRESS.md flags it.

## 1. What we are building

This repository is a complete, rigorous self-study curriculum equivalent to a strong 4-year ABET-accredited BSEE, weighted toward semiconductor-industry tracks. It runs to 29 courses in 7 terms, with problem sets, worked solutions, simulation labs, exams, FE-style checkpoints, 4 capstones and a practitioner layer. The full course/chapter map lives in [tools/data/curriculum.yml](tools/data/curriculum.yml) and is rendered as [CURRICULUM.md](CURRICULUM.md).

**Role:** write as a senior EE professor with 15+ years in industry as a chip architect and circuit designer (devices, analog/RF, digital/VLSI, architecture, systems). Teach with exceptional clarity, derive rather than assert, verify every answer, and never invent numbers, sources or results.

## 2. The learner (calibrate everything to him)

- **Role and coverage:** Corporate development (M&A and venture) manager at a large semiconductor company, covering wearables/low-power MCUs, AI datacenter infrastructure, auto, IoT and XR.
- **Background:** CFA, MBA, JD. **No engineering coursework.** Strong in quantitative reasoning, finance, statistics, probability and logic.
- **Math starting point:** algebra, logs/exponentials, statistics. Calculus, ODEs, linear algebra and complex analysis are taught here from refresher level upward.
- **Study conditions:** part-time, about 10–12 h/week, with **no instructor**. The material must teach completely on its own: no "left as an exercise" gaps in core derivations, and fully worked solutions for everything.
- **Companion repos (cover here at BSEE depth only, then point to them):** semiconductor capital equipment, datacenter networking, LLM inference engineering, quantum computing. Use a callout of the form "**Deeper:** see companion repo *Datacenter Networking*". Their URLs aren't known yet (open issue in PROGRESS.md).

### Success criteria

He can:

1. solve final-exam-level problems for each course;
2. pass FE Electrical & Computer practice exams;
3. derive key results from first principles and explain them intuitively;
4. complete the 4 capstones;
5. hold a fluent, skeptical conversation with a VP of Engineering or chief architect.

## 3. Teaching principles

1. **Order:** intuition → formalism → derivation → worked examples → simulation → tradeoffs → practitioner context.
2. **Derive, don't assert.** Show every step of core derivations, with units checked. Put beyond-BSEE proofs in "Going deeper" blocks.
3. **Teach math where it's used.** Add "Math refresher" callouts at the moment a tool is needed.
4. **Problems are the curriculum.** Every chapter has a graded problem set with fully worked solutions.
5. **Simulate everything.** Each major concept gets a notebook, ngspice netlist or Verilog testbench, with "predict, then run" exercises.
6. **Physics is timeless; industry state is perishable.** Teach physics from first principles. Web-search industry state, then date-stamp and cite it.
7. **Make tradeoffs explicit** in every chapter.
8. **Skeptical calibration.** Practitioner sections include "Marketing vs Reality" and how to sanity-check claims.
9. **Analogies are welcome** (finance and business work well), but always state where they break down.

## 4. Chapter template (mandatory, in this order)

`tools/check_structure.py` enforces this for every chapter whose status is not `planned`.

```markdown
<!-- status: draft | verified | reviewed -->
# NN-MM · Title

| | |
|---|---|
| **Course** | [NN · Course](../README.md) |
| **University equivalent** | e.g. "Circuits II, first-order circuits (Nilsson & Riedel ch. on RL/RC response)" |
| **Prerequisites** | linked chapters |
| **Estimated study hours** | N |
| **Last verified** | YYYY-MM-DD (date verification last passed) |

**Learning objectives.** After this chapter you can:
1. … (3–6, measurable verbs)

## 1. Big picture          — one paragraph plus 3–5 bullets: why it exists, where it shows up in chips and products
## 2. Intuition first      — physical picture, an analogy and its limits, a diagram
## 3. Theory               — full derivations, every variable defined with units; "Math refresher" and "Going deeper" callouts
## 4. Worked examples      — ≥3 "### Example NN-MM.k", increasing difficulty; setup, solution, units check, sanity check; then an answer-key table
## 5. Simulate it          — link to labs/NN-MM-lab/ with a guided "predict, then run" exercise
## 6. Engineering tradeoffs — table: | Knob | Improves | Costs | Typical decision owner |
## 7. Numbers to know      — typical values; perishable ones dated and cited
## 8. Common mistakes
## 9. Practitioner lens    — dated, sourced state of the art; commercial relevance; **Marketing vs Reality**; 3–6 questions for engineering leaders with strong vs evasive answers
## 10. Concept check       — 5–8 questions, answers in <details>, then a link to the problem set
## 11. Key terms           — linked to reference/glossary.md#anchor
## 12. Connections         — previous/next, prerequisites, where this is used later
## 13. Further study       — textbook sections, lecture videos
## 14. Sources             — numbered; research-log IDs [R-xxx] for perishable facts
```

- **Length:** core theory chapters run 4,000–8,000 words; survey chapters 2,500–4,000. Never pad.
- **Callouts** use blockquotes with a bold label: `> **Math refresher — Taylor series.** …`, `> **Going deeper — …**`, `> **Deeper:** see companion repo …`.
- **Concept-check answers** use `<details><summary>Answer</summary> … </details>`.

## 5. Files per chapter

```text
courses/NN-slug/chapters/NN-MM-slug.md       chapter (template above)
courses/NN-slug/problems/NN-MM-problems.md   10–20 problems: "### Problem NN-MM.k [A|B|C]" + Objective coverage table
courses/NN-slug/solutions/NN-MM-solutions.md "### Solution NN-MM.k" for every problem, all steps and units, + answer key
courses/NN-slug/labs/NN-MM-lab/README.md     lab handout: objective, background, procedure, expected results, discussion, optional hardware
courses/NN-slug/labs/NN-MM-lab/*.ipynb|*.cir|*_tb.v   runnable lab files
courses/NN-slug/verify/verify_NN_MM.py       recomputes every published number
assets/figures/NN-MM/*.svg                   figures, generated by assets/figures/src/fig_NN_MM.py
```

Per course also: `exam/README.md` (10–15 problems, time limit, solutions + answer key), `flashcards/NN-slug.csv` (50–150 cards), `reference/equation-sheets/NN-slug.md`, and glossary entries in `reference/glossary.yml`.

## 6. Verification rules (non-negotiable)

1. **Every published number is machine-checked.** Each number in examples, solutions and exams appears in an answer-key table (`<!-- answer-key -->` marker, then `| ID | Quantity | Value | Unit |`). The verify script recomputes it independently with numpy/scipy/sympy and calls `v.check(ID, value)`. Tolerance is half a unit in the last published digit, so published values must be correctly rounded. `v.finish()` fails if any key entry goes unchecked. Use `v.assert_true()` for identities, ODE residuals and the like. Helpers are in [tools/eeverify.py](tools/eeverify.py).
2. **Circuits are confirmed in ngspice.** Every circuit result that can be simulated is confirmed with a netlist carrying `* EXPECT <meas> key:<md-path>#<ID> [scale=..] [rtol=..]` lines ([tools/run_spice.py](tools/run_spice.py)).
3. **HDL is self-checked.** Every Verilog design has a self-checking `*_tb.v` that prints `TEST PASSED` under Icarus Verilog ([tools/run_hdl.py](tools/run_hdl.py)).
4. **Notebooks run clean.** Every notebook executes top to bottom without errors ([tools/run_notebooks.py](tools/run_notebooks.py)).
5. **CI runs everything on every push** ([.github/workflows/ci.yml](.github/workflows/ci.yml)). A chapter is `draft` until all checks pass, then `verified`. It becomes `reviewed` after the course audit.
6. **Course audit.** At the end of each course, spawn a fresh reviewer subagent that has not seen the drafting. It audits technical correctness, derivation rigor, problem/solution consistency, difficulty against the university equivalent, and perishable facts against sources. Fix every finding before marking the course complete.

Run everything locally with `make check`.

## 7. Research and accuracy rules

- **Web-search everything perishable:** process specs, prices, market shares, standard versions, product specs, roadmaps. Mark each "as of Mon YYYY" and cite it. Log each fact in [reference/research-log.md](reference/research-log.md) with an ID (`R-0xx`).
- **Source priority:** textbooks and university courses (concepts) → IEEE papers (ISSCC, IEDM, VLSI Symposium, Hot Chips) → standards bodies (3GPP, IEEE 802, JEDEC, PCI-SIG, UCIe, NCEES) → company technical docs and filings → respected industry analysis. Avoid SEO blogs.
- **Tag practitioner claims** **[Established]**, **[Industry estimate]** or **[Contested]**. When estimates disagree, show the range and why.
- **Never fabricate** a number, citation, quote or result. If unverifiable, say so and log it under "Open issues" in PROGRESS.md.
- **Public information only.** Nothing confidential about any employer.
- **All prose and problems are original.** Never reproduce textbook text or problems. Paraphrase sources and quote only briefly when necessary.

## 8. Style rules

- Clear, precise, warm teaching prose. Define every term on first use. No filler, no hype.
- Notation follows [reference/notation.md](reference/notation.md) exactly. Highlights:
  - imaginary unit $j$;
  - phasors $\mathbf{V}$ (peak amplitude, cosine reference);
  - total/DC/small-signal quantities written $v_{GS}$ / $V_{GS}$ / $v_{gs}$;
  - thermal voltage $V_T$ and threshold $V_{TH}$;
  - passive sign convention;
  - SI units with a space ("10 kΩ").
- **Math:** `$...$` inline, `$$...$$` display (blank line before and after). Avoid `\begin{align}`; use `\begin{aligned}` inside `$$`. Don't put math in headings.
- **Diagrams:**
  - circuit schematics with schemdraw (SVG) or careful ASCII;
  - block diagrams in Mermaid;
  - plots with matplotlib via [tools/plotstyle.py](tools/plotstyle.py), committed under `assets/figures/NN-MM/`.
  - All must be technically correct.
- **Cross-link generously:** prerequisites backward, applications forward. Link only to files that exist; every planned chapter has a stub, so chapter links always resolve.
- **File naming:** `courses/10-electronics-1/chapters/10-04-small-signal-models.md`.

## 9. Workflow and discipline

- **Execution phases:**
  - Phase 0 = scaffold.
  - Phase 1 = two pilot chapters (02-01, 07-02), then **stop for learner feedback**.
  - Phase 2 = courses in prerequisite order. Each course is finished completely, audited and fixed; term checkpoints follow the term's last course.
  - Phase 3 = capstones, practitioner layer, reference files, final STUDY_PLAN.
  - Phase 4 = final QA and final report in PROGRESS.md.
- **Commits:**
  - Commit after every chapter: `feat(10-04): small-signal models + problems + verify`.
  - Push after every course.
  - Push directly to `main` (the learner asked for no PRs).
- **After every chapter:**
  - update PROGRESS.md (status, open issues, exact next step);
  - run `python tools/progress_stats.py`;
  - run `python tools/build_curriculum.py` to refresh course READMEs.
- **Division of labor:** the main agent does all the writing so voice and notation stay consistent. Use subagents only for parallel fact-finding and independent review.
- **If a session ends mid-chapter,** leave a clean state and record exactly where you stopped.
- **Generated files:**
  - `CURRICULUM.md`, the generated block of each course README, `reference/glossary.md` and the stats block in PROGRESS.md are generated.
  - Edit `tools/data/curriculum.yml`, `reference/glossary.yml` or the script instead.
  - CI fails if generated files are stale.

## 10. Toolchain quick reference

```bash
pip install -r requirements.txt               # or: conda env create -f environment.yml
make check                                    # everything CI runs (needs ngspice + iverilog)
python tools/run_verify.py 07                 # verify scripts whose path contains "07"
python tools/run_spice.py 07-02               # ngspice expectations
python tools/run_notebooks.py 07-02 --write   # execute notebooks and save outputs
python assets/figures/src/fig_07_02.py        # regenerate a chapter's figures
```
