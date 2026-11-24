# Flashcards

One Anki deck per course, as CSV files named `NN-course-slug.csv`, with 50–150 cards per course. Cards are tagged by course and chapter (for example, `bsee::02 bsee::02-01`), so you can study one chapter or a whole course.

## Importing into Anki

1. In Anki (desktop, version 2.1.55 or later), choose **File → Import** and select the CSV.
2. The file's header lines (`#separator:comma`, `#html:true`, `#columns:Front,Back,Tags`, `#tags column:3`) configure the import automatically: comma-separated, HTML enabled, third column = tags.
3. Choose the note type **Basic** and a deck name (e.g., `BSEE::02 Complex, ODEs, Linear Algebra`).

Math is written as `\(...\)` (inline) and `\[...\]` (display), which Anki renders with MathJax.

## Decks

| Course | File | Cards |
|---|---|---|
| 00 · Orientation | [00-orientation.csv](00-orientation.csv) | 56 |
| 01 · Calculus for Engineers | [01-calculus-for-engineers.csv](01-calculus-for-engineers.csv) | 107 |
| 02 · Complex Numbers, ODEs, Linear Algebra | [02-complex-numbers-des-and-linear-algebra.csv](02-complex-numbers-des-and-linear-algebra.csv) | 140 |
| 03 · Probability, Statistics and Random Variables | [03-probability-statistics-and-random-variables.csv](03-probability-statistics-and-random-variables.csv) | 134 |
| 04 · Physics for EE | [04-physics-for-ee.csv](04-physics-for-ee.csv) | 150 |
| 05 · Programming for Engineers (05-01 to 05-09) | [05-programming-for-engineers.csv](05-programming-for-engineers.csv) | 128 |
| 06 · Circuit Analysis I | [06-circuit-analysis-1-dc.csv](06-circuit-analysis-1-dc.csv) | 122 |
| 07 · Circuit Analysis II | [07-circuit-analysis-2-transient-and-ac.csv](07-circuit-analysis-2-transient-and-ac.csv) | 134 |
| 08 · Digital Logic Design | [08-digital-logic-design.csv](08-digital-logic-design.csv) | 110 |
| 09 · Semiconductor Devices | [09-semiconductor-devices.csv](09-semiconductor-devices.csv) | 94 |
| 10 · Electronics I | [10-electronics-1.csv](10-electronics-1.csv) | 82 |
| 11 · Signals and Systems | [11-signals-and-systems.csv](11-signals-and-systems.csv) | 87 |
| 12 · Electronics II | [12-electronics-2.csv](12-electronics-2.csv) | 93 |
| 13 · Electromagnetics | [13-electromagnetics.csv](13-electromagnetics.csv) | 101 |
| 14 · Computer Organization and Architecture | [14-computer-organization-and-architecture.csv](14-computer-organization-and-architecture.csv) | 96 |
| 15 · Control Systems | [15-control-systems.csv](15-control-systems.csv) | 82 |
| 16 · Digital Signal Processing | [16-digital-signal-processing.csv](16-digital-signal-processing.csv) | 86 |
| 17 · Communication Systems | [17-communication-systems.csv](17-communication-systems.csv) | 102 |
| 18 · Embedded Systems and Microcontrollers | [18-embedded-systems-and-microcontrollers.csv](18-embedded-systems-and-microcontrollers.csv) | 95 |
| 19 · Digital VLSI Design | [19-digital-vlsi-design.csv](19-digital-vlsi-design.csv) | 82 |
| 20 · Analog and Mixed-Signal IC Design | [20-analog-and-mixed-signal-ic-design.csv](20-analog-and-mixed-signal-ic-design.csv) | 73 |
| 21 · RF and Microwave Engineering | [21-rf-and-microwave-engineering.csv](21-rf-and-microwave-engineering.csv) | 90 |
