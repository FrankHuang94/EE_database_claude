<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 05 · Programming for Engineers

Python for engineering computation and C for hardware-adjacent programming, plus the data structures, algorithms and software-engineering practices that embedded systems, verification and the FE exam assume.

| | |
|---|---|
| **Term** | 1 |
| **Study hours** | ≈ 80 |
| **University equivalents** | Intro to Programming (Python) + Programming in C for Engineers; MIT 6.0001 (Python); CS50 (C portions) |
| **Textbook alignment** | Downey, *Think Python* (free); Kernighan & Ritchie, *The C Programming Language*; VanderPlas, *Python Data Science Handbook* (free, NumPy/Matplotlib chapters) |
| **Free courses** | MIT OCW 6.0001 Introduction to Computer Science and Programming in Python; Harvard CS50 (C weeks) |
| **Prerequisites** | [00 · Orientation](../00-orientation/README.md) |
| **FE areas** | Software Engineering, Computer Systems |

## Learning objectives

1. Write, test and debug Python programs that solve engineering problems with NumPy, SciPy, SymPy and Matplotlib.
2. Write C programs that use pointers, arrays, structs and dynamic memory correctly.
3. Manipulate bits, masks and fixed-width integers the way firmware manipulates hardware registers.
4. Choose appropriate data structures (arrays, ring buffers, linked lists, hash tables, trees) and reason about algorithmic complexity.
5. Apply basic software-engineering practice: version control, testing, requirements and design methods.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [05-01 · Python Fundamentals for Engineers](chapters/05-01-python-fundamentals.md) | 8 | 🏁 reviewed | [problems](problems/05-01-problems.md) · [solutions](solutions/05-01-solutions.md) · [lab](labs/05-01-lab/README.md) · [verify](verify/verify_05_01.py) |
| [05-02 · NumPy, Vectorization and Numerical Computing](chapters/05-02-numpy-and-vectorization.md) | 8 | 🏁 reviewed | [problems](problems/05-02-problems.md) · [solutions](solutions/05-02-solutions.md) · [lab](labs/05-02-lab/README.md) · [verify](verify/verify_05_02.py) |
| [05-03 · SciPy, SymPy and Matplotlib](chapters/05-03-scipy-sympy-matplotlib.md) | 8 | 🏁 reviewed | [problems](problems/05-03-problems.md) · [solutions](solutions/05-03-solutions.md) · [lab](labs/05-03-lab/README.md) · [verify](verify/verify_05_03.py) |
| [05-04 · Jupyter, Testing and Reproducible Workflows](chapters/05-04-reproducible-workflows.md) | 6 | 🏁 reviewed | [problems](problems/05-04-problems.md) · [solutions](solutions/05-04-solutions.md) · [lab](labs/05-04-lab/README.md) · [verify](verify/verify_05_04.py) |
| [05-05 · C Fundamentals](chapters/05-05-c-fundamentals.md) | 10 | 🏁 reviewed | [problems](problems/05-05-problems.md) · [solutions](solutions/05-05-solutions.md) · [lab](labs/05-05-lab/README.md) · [verify](verify/verify_05_05.py) |
| [05-06 · C Pointers, Arrays and Memory](chapters/05-06-c-pointers-and-memory.md) | 10 | 🏁 reviewed | [problems](problems/05-06-problems.md) · [solutions](solutions/05-06-solutions.md) · [lab](labs/05-06-lab/README.md) · [verify](verify/verify_05_06.py) |
| [05-07 · Bit Manipulation and Fixed-Width Integers](chapters/05-07-bit-manipulation.md) | 8 | 🏁 reviewed | [problems](problems/05-07-problems.md) · [solutions](solutions/05-07-solutions.md) · [lab](labs/05-07-lab/README.md) · [verify](verify/verify_05_07.py) |
| [05-08 · Data Structures and Algorithms You Will Need](chapters/05-08-data-structures-and-algorithms.md) | 12 | 🏁 reviewed | [problems](problems/05-08-problems.md) · [solutions](solutions/05-08-solutions.md) · [lab](labs/05-08-lab/README.md) · [verify](verify/verify_05_08.py) |
| [05-09 · Software Engineering Practices](chapters/05-09-software-engineering-practices.md) | 6 | 🏁 reviewed | [problems](problems/05-09-problems.md) · [solutions](solutions/05-09-solutions.md) · [lab](labs/05-09-lab/README.md) · [verify](verify/verify_05_09.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/05-programming-for-engineers.csv) · [Equation sheet](../../reference/equation-sheets/05-programming-for-engineers.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 05 takes about 80 hours and is split across Term 1: the four Python chapters (05-01 to 05-04) come right after Course 00, because every later lab is a Python notebook, and the five C and computer-science chapters (05-05 to 05-09) come at the end of the term. Python is taught as an engineer's calculator and laboratory: types and floats (05-01), NumPy arrays (05-02), SciPy's solvers, fits and integrators, SymPy and plotting (05-03), then the habits that make results trustworthy: notebooks used safely, git, pytest and reproducibility (05-04). C is taught as the language of the hardware: the build process and C's arithmetic rules (05-05), pointers and memory (05-06), bits, registers, byte order and fixed point (05-07). The course closes with the data structures and algorithms, and the software-engineering practices, that the FE exam's Software Engineering area tests (05-08, 05-09). Every code block in the chapters and solutions is executed by the verify scripts, except a few short fragments marked as such because they cannot stand alone (a struct declaration, a register macro), and every complete C block is compiled with warnings as errors and run under AddressSanitizer and UndefinedBehaviorSanitizer; run the code yourself, then change it and predict what happens.

**What to master cold.** Aliasing versus copying, floor division and floating-point equality (05-01); broadcasting, dtypes and wrap-around (05-02); checking a solver's answer by substituting it back, and reading residuals (05-03); tolerances chosen from the problem's scale, and seeds (05-04); C's truncating division, promotion, signed/unsigned conversion and undefined behavior (05-05); pointer arithmetic, string sizes, struct padding and object lifetimes (05-06); masks and shifts, `volatile`, byte order and Q15 arithmetic (05-07); Big-O, binary search, $n\log n$ sorting, ring buffers, hash-table load factors and heaps (05-08); testable requirements, boundary values, coverage, MC/DC and defect filters (05-09). The [reference sheet](../../reference/equation-sheets/05-programming-for-engineers.md) collects them.

**Assessment.** The [course final exam](exam/README.md) has 15 questions, takes 180 minutes, and allows a calculator and the reference sheet but no computer: you trace code and write C by hand. Aim for at least 70%. Question 15 is a short-answer diligence question about a firmware team's claims. The [flashcards](../../flashcards/05-programming-for-engineers.csv) (128 cards) are for spaced review.

**Why this course matters for diligence.** Software is now a large part of what a chip company sells: SDKs, drivers, firmware and safety documentation decide design wins, and a target's code quality decides integration cost. This course gives you the vocabulary and the skeptical checks: whether a number can be regenerated (05-04), how a team manages C's undefined behavior and memory safety (05-05, 05-06), whether data formats and register maps are specified precisely (05-07), whether performance claims hold as problems grow (05-08), and whether a process can show evidence rather than assurances (05-09). The chapters' Marketing vs Reality sections practice those questions.

**Perishable content.** The programming concepts are stable. The dated facts are logged as [R-087](../../reference/research-log.md#r-087--python-releases-floating-point-and-developer-usage) to [R-097](../../reference/research-log.md#r-097--safety-standard-coverage-requirements-and-the-defect-cost-curve) in the research log, together with [R-001](../../reference/research-log.md#r-001--ncees-fe-electrical-and-computer-specification) (the FE exam's Software Engineering topics) and [R-057](../../reference/research-log.md#r-057--patriot-missile-timing-error) (the Patriot clock). The ones most likely to move are Python, NumPy and pytest releases ([R-087](../../reference/research-log.md#r-087--python-releases-floating-point-and-developer-usage), [R-089](../../reference/research-log.md#r-089--python-testing-tools-pytest-release-and-usage)), Git's SHA-256 transition ([R-090](../../reference/research-log.md#r-090--git-usage-and-hash-functions)), C standard and compiler support ([R-092](../../reference/research-log.md#r-092--c-language-standards-coding-standards-and-embedded-usage)) and memory-safety adoption data ([R-094](../../reference/research-log.md#r-094--memory-safety-vulnerability-data-and-policy), [R-095](../../reference/research-log.md#r-095--rust-adoption-in-android-and-the-linux-kernel)). Check those entries once a year.
