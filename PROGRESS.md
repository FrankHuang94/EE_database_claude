# Progress

Build tracker for the Self-Taught BSEE. **Every session starts by reading [CLAUDE.md](CLAUDE.md) and this file, then continues from "Next step".**

## Next step

> **Phase 1 (pilot) is complete: STOPPED for learner feedback.** Both pilot chapters (`02-01`, `07-02`) are written and verified, and CI is green. Do **not** start Phase 2 until the learner has given feedback on rigor, pacing, math level, length and format. Then apply the feedback to CLAUDE.md (template/style rules) and to the two pilot chapters, and start Phase 2 with Course 00 (Orientation), then Course 01.
>
> Then get CI green and **stop and ask the learner for feedback** on rigor, pacing, math level, length and format before Phase 2.

## Phase status

| Phase | Scope | Status |
|---|---|---|
| 0 · Scaffold | Structure, CLAUDE.md, CURRICULUM.md, README, STUDY_PLAN, SETUP, env files, CI, tooling, notation | ✅ complete |
| 1 · Pilot | 02-01 and 07-02, complete with problems, solutions, labs, verification; then stop for feedback | ✅ complete — awaiting learner feedback |
| 2 · Courses | Terms 1 → 7 in prerequisite order; per-course audit; term checkpoints | ⬜ not started |
| 3 · Capstones and practitioner layer | Capstones C1–C4, practitioner playbooks and case studies, reference files, final STUDY_PLAN | ⬜ not started |
| 4 · Final QA | Full CI pass, glossary/objective/cross-link audits, final report | ⬜ not started |

## Build statistics

<!-- BEGIN STATS (tools/progress_stats.py) -->

*Auto-generated; do not edit by hand. Courses appear once any chapter is written.*

| Course | Chapters | Written | Verified | Reviewed | Words | Problems | Verified numbers | Labs | Notebooks / netlists / testbenches |
|---|---|---|---|---|---|---|---|---|---|
| 00 | 5 | 2 | 2 | 0 | 9,701 | 22 | 102 | 2 | 2 / 3 / 1 |
| 02 | 10 | 1 | 1 | 0 | 9,185 | 18 | 118 | 1 | 1 / 0 / 0 |
| 07 | 11 | 1 | 1 | 0 | 8,902 | 18 | 149 | 1 | 1 / 6 / 0 |
| **Total** | **307** | **4** | **4** | **0** | **27,788** | **58** | **369** | **4** | **4 / 9 / 1** |

Glossary terms: **79** · Flashcards: **55**

<!-- END STATS -->

## Course status

| Course | Status | Audit | Notes |
|---|---|---|---|
| 02 | 🔄 in progress (pilot) | — | 02-01 ✅ verified: 17 problems, 111 machine-checked values, lab notebook. Other chapters planned. |
| 07 | 🔄 in progress (pilot) | — | 07-02 ✅ verified: 16 problems, 128 machine-checked values, 6 ngspice netlists, lab notebook. Other chapters planned. |
| all others | ⬜ planned (stubs only) | — | |

Course status values: ⬜ planned · 🔄 in progress · ✅ complete (all chapters verified, exam + flashcards + glossary done) · 🏁 audited (independent review findings fixed).

## Open issues

| # | Issue | Raised | Owner / plan |
|---|---|---|---|
| 1 | **Companion repo URLs unknown.** "Deeper: see companion repo" callouts name the repos (semiconductor capital equipment, datacenter networking, LLM inference engineering, quantum computing) but cannot link them yet. | Phase 0 | Ask the learner for URLs; then link from CLAUDE.md and callouts. |
| 2 | **FE spec read via secondary snippets.** ncees.org was unreachable from the build environment. Question ranges for Linear Systems, Signal Processing, Electronics and Communications were confirmed only via secondary sources citing the July 2020 spec ([R-001](reference/research-log.md#r-001--ncees-fe-electrical-and-computer-specification)). | Phase 0 | Re-check against the NCEES PDF before writing the first checkpoint. |
| 3 | **FE Reference Handbook version.** 10.6 reportedly applies from July 2026; not verified on ncees.org. | Phase 0 | Verify before the first checkpoint; checkpoints cite only formula content, not page numbers. |
| 4 | **Open-source ASIC flow status.** The OpenLane/Sky130 ecosystem has reorganized; installation steps in SETUP.md §6 are deliberately deferred. | Phase 0 | Research and verify when building Course 19. |
| 5 | **Synchrophasor 20 frames/s rate** in IEC/IEEE 60255-118-1:2018 not confirmed ([R-005](reference/research-log.md#r-005--synchrophasor-standards)). | Phase 0 | Only cite rates confirmed for C37.118.1-2011 unless verified. |
| 7 | **Pilot feedback pending.** Rigor, pacing, math level, length and format of 02-01 and 07-02 to be confirmed by the learner before Phase 2. | Phase 1 | Learner |
| 8 | **Pilot chapters link forward to planned chapters** (e.g., 07-01, 02-02, 06-08) whose stubs exist but are unwritten; pilot chapters restate the needed facts in recap boxes. | Phase 1 | Re-check these cross-references when the linked chapters are written. |
| 6 | **MkDocs Material end of life.** The mkdocs-material build prints that Material for MkDocs reaches end of life on 5 May 2027 and names Zensical as its successor. | Phase 0 | Site still builds; evaluate migration in Phase 4 (content is plain Markdown, so low risk). |

## Change log

Changes relative to the original build brief's chapter plan.

| Date | Change | Reason |
|---|---|---|
| 2026-11-12 | Added **05-09 Software Engineering Practices** | FE E&C includes Software Engineering (4–6 questions); not otherwise covered. |
| 2026-11-12 | Added **17-13 Computer Networks Fundamentals** | FE E&C includes Computer Networks (4–6 questions); points to the datacenter-networking companion repo for depth. |
| 2026-11-12 | Expanded Course 22's "brief intro to motors and the power grid" into **22-11 Electric Machines and Drives** and **22-12 Power Systems Fundamentals** | FE E&C includes Power Systems (8–12 questions), the largest area not otherwise covered at exam depth. |
| 2026-11-12 | Course 07 ordering follows the brief (Laplace-domain analysis in 07-04 before sinusoidal steady state in 07-05) | Lets AC steady state be derived as the special case s = jω. Phasors are introduced first in 02-01. |
| 2026-11-12 | Course 10 split: 10-01 diodes · 10-02 MOSFET DC · 10-03 BJT DC · 10-04 small-signal models · 10-05 amplifier fundamentals | Matches the brief's example file name `10-04-small-signal-models.md`. |
| 2026-11-12 | Term 1 study order: Python chapters (05-01–05-04) before Course 01; C chapters (05-05–05-09) at term end | Every lab from 02-01 onward is a Python notebook. |

## Session log

| Date | Session summary |
|---|---|
| 2026-11-12 | Phase 1. Pilot chapters 02-01 (18 problems, 118 machine-checked values) and 07-02 (18 problems, 149 machine-checked values, 6 ngspice netlists) with labs, figures, glossary (48 terms) and flashcards (55). An independent reviewer subagent audited both chapters and found 3 critical, 8 major and ~25 minor issues, all in labels, prose and reasoning rather than computed numbers. All were fixed: an off-by-one term-count label, a wrong 'overshoot' caption, a ±% error, resistor-flyback on-state cost, an ENOB-loss calculation, a rise-time caveat, stronger ngspice coverage (i_C jumps, 72 V switch voltage), PMU standard citation, a rigor gap in the steady-state argument, notation clashes (k, s, V_Th), and added Problems 02-01.18 and 07-02.17–18 (damped exponentials, dependent sources and negative R_Th, two-position switch with u(t)). Stopped for feedback. |
| 2026-11-12 | Phase 0. Repo created; curriculum data model + generators; CLAUDE.md, CURRICULUM.md (29 courses, 307 chapters), README, STUDY_PLAN, SETUP, notation; verification toolkit (answer-key checker, ngspice/HDL/notebook runners, link and structure checkers); CI; smoke tests pass. Research log R-001–R-013. |
