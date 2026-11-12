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
| 01 · Calculus for Engineers | [01-calculus-for-engineers.csv](01-calculus-for-engineers.csv) | 101 |
| 02 · Complex Numbers, ODEs, Linear Algebra (02-01 so far) | [02-complex-numbers-des-and-linear-algebra.csv](02-complex-numbers-des-and-linear-algebra.csv) | 29 |
| 07 · Circuit Analysis II (07-02 so far) | [07-circuit-analysis-2-transient-and-ac.csv](07-circuit-analysis-2-transient-and-ac.csv) | 26 |
