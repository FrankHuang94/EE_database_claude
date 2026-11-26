# Lab 28-09 · Translating Area, Power and Time into Money

**Objective.** Use small models to see how die cost rises with area, how a margin target becomes an area budget, how a customer's power bill depends on electricity price, and which engineering knobs move gross margin most for small and large dies.

**Chapter:** [28-09 · The Business ↔ Engineering Translation Table](../../chapters/28-09-business-engineering-translation.md)

## Background

The lab uses the chapter's conversions with its assumed parameters:

- §3.2: dies per wafer, Poisson yield, cost per good die and the elasticity $d\ln C/d\ln A$.
- §3.3: the area budget from a margin target.
- §3.4: lifetime energy cost $P \cdot \text{PUE} \cdot h \cdot p_e$.
- §3.6: a ±10% tornado of gross margin.

Wafer prices are reported estimates [R-575].

## Files

- `translate.py`: the conversions.
- `28-09-translate-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Cost against area** (notebook). *Predict* the elasticity of die cost to area at 600 mm² (0.1 defects per cm², with the edge term). Then plot cost per good die and elasticity against area from 20 to 800 mm².

**Part 2 · Area budgets** (notebook). *Predict* the maximum die area for Example 28-09.2's product ($60 price, $8 package and test, 60% margin) on a $30,000 N2 wafer. Then plot the budget against the margin target for N3 and N2 prices.

**Part 3 · Electricity price** (notebook). *Predict* the lifetime energy cost of a 1,000 W device (PUE 1.3, 4 years) at $0.15 per kWh. Then plot energy cost against power for $0.05, $0.10 and $0.15 per kWh.

**Part 4 · A big-die tornado** (notebook). For a 600 mm² die selling at $900 with $80 of package and test on an $18,500 wafer, *predict* the base margin and how much a 10% rise in defect density costs. Then draw its tornado next to Example 28-09.6's.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 28-09.a | elasticity at 600 mm² | 1.75 | — |
| Lab 28-09.b | area budget on N2 | 34.4 | mm² |
| Lab 28-09.c | energy cost at $0.15 | 6837 | $ |
| Lab 28-09.d | base margin, 600 mm² die | 49.5 | % |
| Lab 28-09.d1 | defect density +10% | −2.57 | points |
| Lab 28-09.d2 | die area +10% | −7.48 | points |

## Discussion

1. At 600 mm² the elasticity is **1.75**: each 1% of area costs 1.75% of die cost, against about 1.15 at 100 mm². Large dies are where chiplets and area discipline earn their keep.
2. On N2 the same product can afford only **34.4** mm² of silicon. Moving a cost-sensitive product to the leading edge is a margin decision before it is a performance one.
3. At $0.15 per kWh the device's energy costs **6837** $ over four years, nearly twice the cost at $0.08. Where a customer's datacenter sits changes the value of a watt.
4. The large die starts at **49.5**% margin; a 10% rise in defect density costs **2.57** points, about seven times as much as for the 100 mm² die, and a 10% rise in area **7.48** points, nearly twice as much. Yield claims deserve more scrutiny for big dies.

## Optional hardware

None. As an exercise, take a public product announcement with a stated die size and node, estimate its die cost with the reported wafer price, and compare the implied margin with the company's reported gross margin.
