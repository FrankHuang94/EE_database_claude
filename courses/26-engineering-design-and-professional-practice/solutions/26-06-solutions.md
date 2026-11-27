# Solutions 26-06 · Engineering Team Structures and Sizing

Problems: [26-06 problems](../problems/26-06-problems.md) · Chapter: [26-06](../chapters/26-06-team-structures-and-sizing.md). Every number is recomputed by [verify_26_06.py](../verify/verify_26_06.py).

---

## Solutions

### Solution 26-06.1

(a) $\binom{8}{2}$ = **28**, $\binom{25}{2}$ = **300**, $\binom{200}{2}$ = **19900**.

(b) $8 \times 300 + \binom{8}{2} = 2400 + 28$ = **2428**, about **8.2** times fewer.

### Solution 26-06.2

(a) **Program** (a single team): one product, and every engineer needs to see the whole chip.

(b) **Matrix with platform teams**: shared CPU, interconnect and flow teams serve the six programs, which keeps them compatible and avoids six copies of the same work.

(c) **Functional** (or a platform verification team): a single verification organization can impose one methodology and move people between programs.

(d) **Program**: a stable flagship line benefits from a dedicated, long-lived team with clear ownership.

### Solution 26-06.3

(a) $n^* = (1 + 25)/2$ = **13**; $O(13) = 13(1 - 0.04 \times 12)$ = **6.76** FTE.

(b) $1 + 1/0.04$ = **26** people.

(c) $20(1 - 0.04 \times 19)$ = **4.8** FTE, less than the 13-person team's output.

### Solution 26-06.4

(a) $1 - 0.03 \times 5$ = **0.85**.

(b) $6 \times 0.85$ = **5.1** FTE.

(c) $1 - 0.015 \times 11$ = **0.835**.

(d) $12 \times 5.1 \times 0.835$ = **51.1** FTE, **0.608** per head: nearly the same output as the 90-person hierarchy with six fewer people, partly because smaller teams coordinate less internally (0.85 against 0.79 per member) and partly because each interface is assumed cheaper ($c_x$ = 0.015 against 0.02). With $c_x$ = 0.02 the factor would be $1 - 0.02 \times 11$ = 0.78, giving **47.7** FTE, **0.568** per head, below Example 26-06.2's **0.576**.

### Solution 26-06.5

(a) $e_0 = 1 - 0.02 \times 7 = 0.86$, so $60/(8 \times 0.86)$ = **8.72** months.

(b) $e = 1 - 0.02 \times 11$ = **0.78**. During the ramp, $(8 - 2) \times 0.78$ = **4.68** FTE for 2 months, **9.36** person-months; then $12 \times 0.78$ = **9.36** FTE. Time $2 + (60 - 9.36)/9.36$ = **7.41** months: adding helps.

(c) Setting the two finishing times equal gives **26.0** person-months, about **3.77** months of work at the current rate. With less left, the four new engineers delay the finish.

### Solution 26-06.6

Span 7: **215**, **31**, **5**, **1**: four layers, **252** managers ($N/6$ = **250**). Span 10: **150**, **15**, **2**, **1**: four layers, **168** managers ($N/9$ = **167**). The wider span cuts a third of the managers but not a layer here, because 1,500 sits just above $10^3$.

### Solution 26-06.7

(a) $C_e/C_c$ = **0.8**. A base of 20 is exceeded in 6 of 8 quarters (**0.75**), below 0.8, so the base is **20**.

(b) $20 \times 8 \times 80{,}000 + 160 \times 100{,}000$ = **\$28.8 M**, with **160** engineer-quarters contracted.

(c) $30 \times 8 \times 80{,}000 + 100 \times 100{,}000 = 19.2 + 10.0$ = **\$29.2 M** (**100** engineer-quarters contracted).

(d) $60 \times 8 \times 80{,}000$ = **\$38.4 M**.

(e) $320 \times 100{,}000$ = **\$32.0 M**.

### Solution 26-06.8

(a) In-house $18 \times 150{,}000$ = **\$2.70 M**; outsourced $14 \times 200{,}000$ = **\$2.80 M**: in-house is slightly cheaper.

(b) Break-even utilization $150/200$ = **0.75**, that is **13.5** work-months of 18. Below that, outsource; the decision also depends on whether the DFT team would be needed for the next program (a reason to keep it) and on the oversight effort outsourcing needs.

### Solution 26-06.9

(a) At the cache-coherent interconnect, which two teams own, so its specification and verification fall between them (Conway's law); and at the memory controller's physical design, where the time-zone split slows the timing and floorplan iterations with the front-end team.

(b) Organizational: give the interconnect a single owning team, with the other team as a reviewed customer; co-locate or overlap working hours for the memory controller's front-end and physical-design engineers. Architectural: define the interconnect's protocol and interfaces as a written specification with its own verification environment (26-01), so the two sides meet at a clean interface; harden the memory controller as a self-contained block with fixed boundary constraints.

### Solution 26-06.10

$0.75 \times 725 \times 10^6/350{,}000$ = **1554** engineer-years, an average of **518** engineers over 3 years (more at the peak).

### Solution 26-06.11

(a) The staffing profile is a triangle of base 30 months, so $\frac{1}{2} \times 30 \times P = 600$ and $P$ = **40** engineers.

(b) $40/18$ = **2.22** engineers a month, every month for a year and a half.

(c) Hiring and ramping 40 verification engineers in 18 months is hard in a competitive market, and after month 18 the load falls, leaving idle employees: the profile is exactly where contractors and services firms cover the peak (§3.6).

### Solution 26-06.12

Advantages: shared methodology and expertise across programs; people can move to where the load is. Disadvantages: two reporting lines, with conflicting priorities; slower decisions when the functional and program managers disagree. Practices: a clear rule on who decides what (the program manager sets priorities and dates, the functional manager methods and staffing), and an escalation path with a named arbiter.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 26-06.1a | channels, 8 | 28 | |
| 26-06.1a1 | channels, 25 | 300 | |
| 26-06.1a2 | channels, 200 | 19900 | |
| 26-06.1b | channels, hierarchy | 2428 | |
| 26-06.1b1 | ratio | 8.2 | |
| 26-06.3a | best size | 13 | |
| 26-06.3a1 | output | 6.76 | FTE |
| 26-06.3b | zero-output size | 26 | |
| 26-06.3c | output of 20 | 4.8 | FTE |
| 26-06.4a | member efficiency | 0.85 | |
| 26-06.4b | team output | 5.1 | FTE |
| 26-06.4c | cross-team factor | 0.835 | |
| 26-06.4d | total output | 51.1 | FTE |
| 26-06.4d1 | per head | 0.608 | |
| 26-06.4d2 | member efficiency, Example 26-06.2 | 0.79 | |
| 26-06.4d3 | cross-team factor at 0.02 | 0.78 | |
| 26-06.4d4 | total at 0.02 | 47.7 | FTE |
| 26-06.4d5 | per head at 0.02 | 0.568 | |
| 26-06.4d6 | per head, Example 26-06.2 | 0.576 | |
| 26-06.5a | time without | 8.72 | months |
| 26-06.5b | efficiency with hires | 0.78 | |
| 26-06.5b1 | output during ramp | 4.68 | FTE |
| 26-06.5b2 | work during ramp | 9.36 | person-months |
| 26-06.5b3 | output after ramp | 9.36 | FTE |
| 26-06.5b4 | time with | 7.41 | months |
| 26-06.5c | break-even work | 26.0 | person-months |
| 26-06.5c1 | break-even time | 3.77 | months |
| 26-06.6a | span 7, level 1 | 215 | |
| 26-06.6a1 | span 7, level 2 | 31 | |
| 26-06.6a2 | span 7, level 3 | 5 | |
| 26-06.6a3 | span 7, total | 252 | |
| 26-06.6a4 | span 7, approximation | 250 | |
| 26-06.6b | span 10, level 1 | 150 | |
| 26-06.6b1 | span 10, level 2 | 15 | |
| 26-06.6b2 | span 10, level 3 | 2 | |
| 26-06.6b3 | span 10, total | 168 | |
| 26-06.6b4 | span 10, approximation | 167 | |
| 26-06.7a | critical ratio | 0.8 | |
| 26-06.7a1 | share above 20 | 0.75 | |
| 26-06.7a2 | base | 20 | |
| 26-06.7b | cost with base | 28.8 | $M |
| 26-06.7b1 | contracted | 160 | engineer-quarters |
| 26-06.7c0 | employee cost, base 30 | 19.2 | $M |
| 26-06.7c1 | contractor cost, base 30 | 10.0 | $M |
| 26-06.7c2 | contracted, base 30 | 100 | engineer-quarters |
| 26-06.7c | cost, base 30 | 29.2 | $M |
| 26-06.7d | all employees | 38.4 | $M |
| 26-06.7e | all contractors | 32.0 | $M |
| 26-06.8a | in-house | 2.70 | $M |
| 26-06.8a1 | outsourced | 2.80 | $M |
| 26-06.8b | break-even utilization | 0.75 | |
| 26-06.8b1 | break-even work-months | 13.5 | months |
| 26-06.10 | engineer-years | 1554 | |
| 26-06.10a | average headcount | 518 | |
| 26-06.11a | peak headcount | 40 | |
| 26-06.11b | hiring rate | 2.22 | per month |
