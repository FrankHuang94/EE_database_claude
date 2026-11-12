# Lab 00-03 · Tools for Learning Like an Engineer

**Chapter:** [00-03](../../chapters/00-03-how-to-study-this-curriculum.md) · **Notebook:** [00-03-study-tools.ipynb](00-03-study-tools.ipynb) · **Time:** about 30 minutes

## Objective

1. Use SymPy's units module to check the dimensions of any formula automatically.
2. Compare cramming with spaced review in a simple forgetting model, and see why spacing wins.
3. Create your personal error-log file.

## Background

Chapter sections 3.4 (dimensional analysis), 3.6 (spacing) and 3.7 (error log).

**The toy forgetting model used here.** Recall decays as $R = e^{-t/S}$. A review done when recall has fallen to $R$ multiplies the stability $S$ by $1 + 3(1 - R)$. So reviewing something you still remember perfectly adds almost nothing, while a harder, successful retrieval adds a lot. This is a deliberately simple illustration of the spacing effect, not a model of any particular software.

## Procedure

1. Run all notebook cells.
2. **Part 1:** add two formulas of your own to the units checker, including one deliberately wrong one, and confirm the checker catches it.
3. **Part 2:** before running, predict recall at day 60 for each schedule: six reviews crammed into the first two days, or six reviews at days 1, 3, 7, 14, 30 and 50.
4. **Part 3:** run the cell that writes `my-error-log.md` (to your home folder by default). Keep it for the rest of the curriculum.

## Expected results

| Schedule (6 reviews each) | Recall at day 60 | Final stability |
|---|---|---|
| Crammed: days 0.25, 0.5, 0.75, 1, 1.5, 2 | 0.0158% (essentially forgotten) | 6.63 days |
| Spaced: days 1, 3, 7, 14, 30, 50 | 92.3% | 124 days |

The same six reviews, spent differently, give opposite outcomes. Crammed reviews happen while recall is still high, so each one adds little stability.

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 00-03.1 | recall at day 60, crammed | 0.0158 | % |
| Lab 00-03.2 | recall at day 60, spaced | 92.3 | % |
| Lab 00-03.3 | final stability, crammed | 6.63 | days |
| Lab 00-03.4 | final stability, spaced | 124 | days |

## Discussion questions

1. In the model, why does a review at high recall add little? What real-world experience does that match?
2. The model ignores *failed* reviews. How would forgetting a card and relearning it change the schedule?
3. Which of your past study habits does this lab argue against?

## Optional hardware version

None. Instead, install Anki and import [flashcards/02-complex-numbers-des-and-linear-algebra.csv](../../../../flashcards/02-complex-numbers-des-and-linear-algebra.csv) following [flashcards/README.md](../../../../flashcards/README.md).
