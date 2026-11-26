# Solutions 25-07 · Packaging II: 2.5D, 3D, Hybrid Bonding and Chiplets

Problems: [25-07 problems](../problems/25-07-problems.md) · Chapter: [25-07](../chapters/25-07-advanced-packaging-and-chiplets.md)

Every number is recomputed by [verify_25_07.py](../verify/verify_25_07.py).

---

## Solutions

### Solution 25-07.1

(a) $14 \times 858$ = **12012** mm²; $14 \times 830$ = **11620** mm².

(b) $(12{,}012 - 11{,}620)/11{,}620$ = **3.4**%.

(c) $6{,}864/8$ = **858** mm² and $7{,}722/9$ = **858** mm²: both use the full field, while the 2025 figure of 7,885 mm² for 9.5 reticles uses 830 mm² (Example 25-07.1). A roadmap that switches basis can look like growth or shrinkage of a few percent that is only arithmetic.

### Solution 25-07.2

(a) $(55/45)^2$ = **1.49**. (b) $(45/35)^2$ = **1.65**. (c) $(45/36)^2$ = **1.5625**. The 65% gain matches **35 µm**; at 36 µm it would be **56**%.

### Solution 25-07.3

(a) $2/0.004$ = **500** wires per mm.

(b) $2048/500$ = **4.10** mm.

(c) 2 mm must carry 1,024 wires per mm, so $L = 1024 \times 0.004$ = **4.1**: round up to **5** layers. Coarser RDL can match a silicon interposer's shoreline only by adding layers, each with its own yield and cost.

### Solution 25-07.4

(a) The exact count gives **33** interposers. (b) The formula gives $\pi \times 300^2/(4 \times 1600) - \pi \times 300/\sqrt{3200}$ = **27.5**, again an underestimate for large rectangles. (c) $120{,}000 \times 33 \times 0.95$ = **3.76e6** packages per month.

### Solution 25-07.5

(a) $1.275 \times 10^6/12$ = **1.06e5** wafers per month.

(b) $2.73/1.275 - 1$ = **114**% for 2027 and $3.48/2.73 - 1$ = **27.5**% for 2028.

(c) $250/160 - 1$ = **56**%. This is industry capacity including OSATs, so it cannot be compared directly with TSMC-only figures.

(d) A CAGR of 80% over five years compounds to $1.8^5$ = **18.9** times or more; doubling for three years gives $2^3$ = **8** times. The two statements cover different windows and are consistent with growth slowing at the end of the window, or with a lower base in 2022.

(e) $12{,}000\ \text{m}^2 = 1.2 \times 10^{10}$ mm². Over $3 \times 10^6$ packages that is **4.0e3** mm² each; over $2 \times 10^6$, **6.0e3** mm². That is a square **63** to **77** mm on a side, a plausible size for a large accelerator substrate before panel-edge losses, so the press estimate is at least self-consistent.

### Solution 25-07.6

(a) The error along $x$ is $\theta\lvert y\rvert$ and along $y$ is $\theta\lvert x\rvert$, largest at the half-width $\lvert x\rvert$ or $\lvert y\rvert$ = **5** mm: every pad on the outermost rows and columns, corners included, has error $5\theta$ on one axis or both.

(b) $\theta = (p/4)/5\ \text{mm} = 1.5 \times 10^{-3}\ \text{mm}/5\ \text{mm}$ = **300** µrad.

(c) $300 \times 10^{-6} \times 180/\pi$ = **0.0172**°.

(d) The corner pads are $\sqrt{5^2 + 5^2}$ = **7.07** mm out, so $\theta = 1.5 \times 10^{-3}/7.07$ = **212** µrad. Either way, die rotation must be held to about a hundredth of a degree, and on a 10 mm die it alone uses the whole overlay budget, so translation and rotation must share it.

### Solution 25-07.7

(a) $3 \times 10^{-9}/(16.5 \times 10^{-6} \times 0.5 \times 10^{-6})$ = **364** K: too hot for many stacks, so a thin pad needs a smaller recess.

(b) $\delta = 16.5 \times 10^{-6} \times 1.0 \times 10^{-6} \times 225$ m = **3.71** nm.

### Solution 25-07.8

(a) Assume the test never rejects a good die and catches a fraction $c$ of bad ones. By the law of total probability, $P(\text{pass}) = Y + (1 - Y)(1 - c)$. By Bayes' rule,

$$
e = P(\text{bad} \mid \text{pass}) = \frac{P(\text{pass} \mid \text{bad})P(\text{bad})}{P(\text{pass})} = \frac{(1 - c)(1 - Y)}{Y + (1 - Y)(1 - c)}.
$$

As $c \to 1$ the second term of the denominator vanishes, leaving $e \approx (1 - Y)(1 - c)/Y$.

(b) $0.5 \times 0.01/(0.5 + 0.005)$ = **0.990**%; the approximation gives $0.5 \times 0.01/0.5$ = **1.00**%.

(c) $0.05 \times 0.01/(0.95 + 0.0005)$ = **0.0526**%. At the same coverage, the low-yield die escapes about **19** times as often: early in a node's life, when yields are low, imperfect test lets many more bad dies into packages, so test coverage matters most exactly when yields are worst.

### Solution 25-07.9

(a) $Y_{pkg} = 0.998^{14}(1 - 0.00249)^2(0.995)^{12}$ = **0.911** (unrounded **0.91104**, used below).

(b) $5400/0.91104$ = **$5.93e3**.

(c) $5400(1/0.91104 - 1)$ = **$527**. Four more stacks add four attaches and four chances of an escape, and each failure scraps a more expensive kit: scrap rises from $283 to $527.

### Solution 25-07.10

Solve $C_M(A) = C_C(A)$ for $A$ numerically:

(a) **562** mm². (b) **359** mm²: a worse defect density favours chiplets at smaller sizes. (c) **882** mm²: above the 858 mm² reticle, so at a mature defect density the monolithic die is cheaper wherever it can be made at all, and chiplets pay only when the reticle forces them.

### Solution 25-07.11

(a) $Y_M = (1 + 0.8/2)^{-2}$ = **0.510**; $Y_C = (1 + 0.22/2)^{-2}$ = **0.812** (unrounded **0.8116**).

(b) $C_M = [(240 + 3)/0.510 + 50]/0.99$ = **$532** (unrounded **$531.6**); $C_C = [4(66 + 3)/0.8116 + 110]/0.99^4$ = **$469** (unrounded **$468.5**).

(c) $468.5/531.6$ = **0.881**: a **12**% saving instead of **21**%.

(d) The break-even rises to **0.067** cm⁻². Clustering helps the large die more than the small ones, so it narrows the chiplet advantage.

### Solution 25-07.12

(a) $(900 - 160)/20$ = **37.0** µm per layer.

(b) $37.0 - 10$ = **27.0** µm with microbumps; with hybrid bonding the whole 37.0 µm is silicon. A taller limit lets 20-high stacks keep microbumps with dies about as thin as 16-high stacks use under 775 µm (23-05), which is why each relaxation postpones hybrid bonding in HBM [R-594].

### Solution 25-07.13

(a) $4{,}719/(6 \times 54)$ = **14.6**.

(b) $1208/6$ = **201** bridge sets per wafer, against **9** silicon interposers of 55 mm × 86 mm (about the same area, exact count), if a silicon interposer that large could be made at all; CoWoS-S stops near 3.3 reticles.

### Solution 25-07.14

(a) $z = 3.48$ for 99.9%, so $\sigma = (4.5/4)/3.48$ = **0.323** µm, or 3σ = **0.970** µm.

(b) With $\sigma = 0.5/3$ µm, each pad must tolerate $3.48\sigma = 3.48 \times 0.5/3$ = **0.580** µm. On a 1 µm pitch that exceeds half the pitch (0.5 µm): pads would have to be wider than the space between them allows, so no pad design reaches 99.9% with this tool. Sub-micrometre die-to-wafer bonding needs better placement, which is why the finest pitches are wafer-to-wafer.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 25-07.1a | 14×, 858 basis | 12012 | mm² |
| 25-07.1a1 | 14×, 830 basis | 11620 | mm² |
| 25-07.1b | difference | 3.4 | % |
| 25-07.1c | basis of 8× figure | 858 | mm² |
| 25-07.1c1 | basis of 9× figure | 858 | mm² |
| 25-07.2a | gain 55 → 45 µm | 1.49 | |
| 25-07.2b | gain 45 → 35 µm | 1.65 | |
| 25-07.2c | gain 45 → 36 µm | 1.5625 | |
| 25-07.2c1 | gain at 36 µm as a percentage | 56 | % |
| 25-07.2d | pitch matching 65% | 35 | µm |
| 25-07.3a | wires per mm | 500 | /mm |
| 25-07.3b | edge for 2,048 wires | 4.10 | mm |
| 25-07.3c0 | layers needed, unrounded | 4.1 | |
| 25-07.3c | layers for 2 mm | 5 | |
| 25-07.4a | interposers per wafer, exact | 33 | |
| 25-07.4b | formula estimate | 27.5 | |
| 25-07.4c | packages per month | 3.76e6 | |
| 25-07.5a | Goldman 2026 monthly average | 1.06e5 | wafers |
| 25-07.5b | 2027 growth | 114 | % |
| 25-07.5b1 | 2028 growth | 27.5 | % |
| 25-07.5c | UBS industry growth | 56 | % |
| 25-07.5d | five years at 80% | 18.9 | |
| 25-07.5d1 | three doublings | 8 | |
| 25-07.5e | substrate per package, 3 million | 4.0e3 | mm² |
| 25-07.5e1 | substrate per package, 2 million | 6.0e3 | mm² |
| 25-07.5e2 | side, 3 million | 63 | mm |
| 25-07.5e3 | side, 2 million | 77 | mm |
| 25-07.6a | largest lever arm per axis | 5 | mm |
| 25-07.6b | rotation budget, per axis | 300 | µrad |
| 25-07.6c | rotation budget, per axis | 0.0172 | ° |
| 25-07.6d | corner distance | 7.07 | mm |
| 25-07.6d1 | rotation budget, radial | 212 | µrad |
| 25-07.7a | rise, 3 nm on 0.5 µm | 364 | K |
| 25-07.7b | largest recess | 3.71 | nm |
| 25-07.8b | escape, Y 0.5 | 0.990 | % |
| 25-07.8b1 | approximation | 1.00 | % |
| 25-07.8c | escape, Y 0.95 | 0.0526 | % |
| 25-07.8c1 | ratio of escape rates | 19 | |
| 25-07.9a | package yield, 12 stacks | 0.911 | |
| 25-07.9a0 | package yield, unrounded | 0.91104 | |
| 25-07.9b | cost per good package | 5.93e3 | $ |
| 25-07.9c | scrap overhead | 527 | $ |
| 25-07.10a | break-even area, 0.1 | 562 | mm² |
| 25-07.10b | break-even area, 0.2 | 359 | mm² |
| 25-07.10c | break-even area, 0.05 | 882 | mm² |
| 25-07.11a | monolithic yield, clustered | 0.510 | |
| 25-07.11a1 | chiplet yield, clustered | 0.812 | |
| 25-07.11a2 | chiplet yield, unrounded | 0.8116 | |
| 25-07.11b | monolithic cost | 532 | $ |
| 25-07.11b1 | chiplet cost | 469 | $ |
| 25-07.11b0 | monolithic cost, unrounded | 531.6 | $ |
| 25-07.11b2 | chiplet cost, unrounded | 468.5 | $ |
| 25-07.11c | ratio | 0.881 | |
| 25-07.11c1 | saving, clustered | 12 | % |
| 25-07.11c2 | saving, Poisson | 21 | % |
| 25-07.11d | break-even D0 | 0.067 | cm⁻² |
| 25-07.12a | layer pitch | 37.0 | µm |
| 25-07.12b | core-die thickness | 27.0 | µm |
| 25-07.13a | silicon ratio | 14.6 | |
| 25-07.13b | bridge sets per wafer | 201 | |
| 25-07.13c | 55 × 86 mm interposers per wafer | 9 | |
| 25-07.14a | sigma at 4.5 µm | 0.323 | µm |
| 25-07.14a1 | 3 sigma | 0.970 | µm |
| 25-07.14b | required tolerance | 0.580 | µm |
