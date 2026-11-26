# Lab 26-06 · How Big, How Organized, Who Pays

**Objective.** Explore how coordination cost limits a flat team, how splitting a group into teams changes its output, when adding engineers helps, and how the price of contractors sets the right base of employees.

**Chapter:** [26-06 · Engineering Team Structures and Sizing](../../chapters/26-06-team-structures-and-sizing.md)

## Background

§3.2 derived the flat-team output $O(n) = n[1 - c(n - 1)]$, its maximum at $n^* = (1 + 1/c)/2$ and the hierarchical output $km[1 - c(m - 1)][1 - c_x(k - 1)]$. §3.3 gave the finishing time with added staff who need ramp-up and mentoring. §3.6 derived the newsvendor rule: staff employees up to the load exceeded in more than $C_e/C_c$ of periods.

## Files

- `team.py`: channel counts (flat and hierarchical), flat and hierarchical output, the best flat size, finishing times with added staff, management layers, staffing cost with a contractor pool, the newsvendor base, and engineer-years from a design cost.
- `26-06-team-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · The flat-team limit** (notebook). *Predict* the size at which a flat team with $c$ = 0.03 produces nothing. Then plot $O(n)$ from 1 to 40 people.

**Part 2 · Splitting 96 engineers** (notebook). *Predict* the number of teams (each with its own lead) that maximizes the output of 96 engineers with $c$ = 0.03 and $c_x$ = 0.02. Then compute the output for every even split.

**Part 3 · When hiring stops helping** (notebook). *Predict* the remaining work below which Example 26-06.3's five new engineers lengthen the project. Then plot both finishing times against the remaining work.

**Part 4 · Expensive contractors** (notebook). *Predict* the newsvendor base for Example 26-06.5's load if contractors cost 2.5 times as much as employees. Then compute the cost of every base from 0 to 40.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 26-06.a | zero-output flat size | 34.3 | |
| Lab 26-06.b | best number of teams | 12 | |
| Lab 26-06.b1 | output at the best split | 59.2 | FTE |
| Lab 26-06.c | break-even remaining work | 51.1 | person-months |
| Lab 26-06.c1 | break-even in months of current work | 6.2 | months |
| Lab 26-06.d | base with expensive contractors | 25 | |
| Lab 26-06.d1 | cost at that base | 20.625 | $M |
| Lab 26-06.d2 | critical ratio | 0.40 | |

## Discussion

1. A flat team with a 3% coordination cost per colleague stops producing at 34.3 people; long before that, at 17, it has passed its best. Teams need structure well before they are large.
2. Twelve teams of eight give 59.2 FTE from 96 engineers. Fewer, larger teams lose output to internal coordination; more, smaller teams lose it to interfaces between teams. The best split balances the two, and in practice it is set by the architecture's natural blocks.
3. With 51.1 person-months or more left, the five hires shorten the project; with less, they lengthen it. The break-even is **6.2** months of the existing team's work, about twice the three-month ramp.
4. At 2.5 times the price, contractors are worth using only above a load exceeded in less than **0.40** of quarters, so the base rises from 10 to 25 engineers and the total cost to $20.625 M.

## Optional hardware

None needed. If you manage a team, count the recurring meetings and the people in each for a week, and estimate your own team's $c$.
