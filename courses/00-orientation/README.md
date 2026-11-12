<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 00 · Orientation

A map of electrical engineering and of this curriculum: the subdisciplines, the abstraction stack from physics to software, how to study without an instructor, the toolchain, and how chip companies organize their engineering teams.

| | |
|---|---|
| **Term** | 1 |
| **Study hours** | ≈ 17 |
| **University equivalents** | Freshman 'Introduction to Electrical Engineering' seminar |
| **Textbook alignment** | No required text. Optional: Hambley, *Electrical Engineering: Principles and Applications* (survey chapters) |
| **Free courses** | MIT OCW 6.002 (Circuits and Electronics), lecture 1, for the abstraction idea |
| **Prerequisites** | none |
| **FE areas** | — |

## Learning objectives

1. Name the major EE subdisciplines and place each on the abstraction stack.
2. Explain what each level of the stack (device, circuit, block, chip, package, board, system, software) optimizes and hands to the next.
3. Install and smoke-test the curriculum toolchain (Python, Jupyter, ngspice, Icarus Verilog).
4. Describe the main engineering functions in a chip company and how a product moves from spec to production.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [00-01 · The Map of Electrical Engineering](chapters/00-01-map-of-electrical-engineering.md) | 3 | ✅ verified | [problems](problems/00-01-problems.md) · [solutions](solutions/00-01-solutions.md) · [lab](labs/00-01-lab/README.md) · [verify](verify/verify_00_01.py) |
| [00-02 · The Abstraction Stack: Physics to Software](chapters/00-02-the-abstraction-stack.md) | 3.5 | ✅ verified | [problems](problems/00-02-problems.md) · [solutions](solutions/00-02-solutions.md) · [lab](labs/00-02-lab/README.md) · [verify](verify/verify_00_02.py) |
| [00-03 · How to Study This Curriculum](chapters/00-03-how-to-study-this-curriculum.md) | 2 | ✅ verified | [problems](problems/00-03-problems.md) · [solutions](solutions/00-03-solutions.md) · [lab](labs/00-03-lab/README.md) · [verify](verify/verify_00_03.py) |
| [00-04 · Toolchain Setup Walkthrough](chapters/00-04-toolchain-walkthrough.md) | 3.5 | ✅ verified | [problems](problems/00-04-problems.md) · [solutions](solutions/00-04-solutions.md) · [lab](labs/00-04-lab/README.md) · [verify](verify/verify_00_04.py) |
| [00-05 · How Chip Companies' Engineering Organizations Work](chapters/00-05-how-chip-companies-are-organized.md) | 2.5 | ✅ verified | [problems](problems/00-05-problems.md) · [solutions](solutions/00-05-solutions.md) · [lab](labs/00-05-lab/README.md) · [verify](verify/verify_00_05.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/00-orientation.csv) · [Equation sheet](../../reference/equation-sheets/00-orientation.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 00 is short (about 17 hours including the exam) and deliberately light on mathematics. Its job is to give you a mental map, a working toolchain and a study method before the heavy lifting starts in Course 01. Do it in order. 00-04 (toolchain) must be finished before any lab in later courses.

**Assessment.** The [course final exam](exam/README.md) takes 120 minutes. Aim for at least 70%. Besides calculations, it includes three short-answer diligence questions (mapping problems to subdisciplines, reading a stepping change, and restating a market claim accurately). Your hands-on use of ngspice and the verify tools is checked by the 00-04 lab, not the exam.

**Perishable content.** Chapters 00-01, 00-03 and 00-05 cite market, R&D, verification-survey and learning-science data, each dated and logged in [reference/research-log.md](../../reference/research-log.md) (R-013 to R-024). Check those entries for updates once a year.
