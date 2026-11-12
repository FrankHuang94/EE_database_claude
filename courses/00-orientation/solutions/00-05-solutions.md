# Solutions 00-05 · How Chip Companies' Engineering Organizations Work

Problems: [00-05 problems](../problems/00-05-problems.md) · Chapter: [00-05](../chapters/00-05-how-chip-companies-are-organized.md)

All numbers are in the answer key and recomputed by [verify_00_05.py](../verify/verify_00_05.py).

---

## Solutions

### Solution 00-05.1

(a) Design for test (DFT). (b) Product / test engineering. (c) Physical design. (d) Design verification. (e) Firmware / software. (f) Quality and reliability.

### Solution 00-05.2

Architecture freeze → RTL freeze → tapeout → first silicon → qualification complete → production release. Formal **gates** are normally architecture freeze, RTL freeze, tapeout (readiness review) and production release. First silicon and qualification are milestones whose results feed the next gate.

### Solution 00-05.3

(a) $60 \times 1.5 = 90.0$ days, about 13 weeks.
(b) $60 \times 0.8 = 48.0$ days.
(c) $12 \times 1.2 = 14.4$ days of processing, plus mask making, packaging and test.

### Solution 00-05.4

(a) $0.99^{20} = 0.818$, i.e. **81.8%**.
(b) $p = 0.90^{1/100} = 0.99895$. Each block must be about 99.9% bug-free.

### Solution 00-05.5

Lost revenue $= 300 \times \frac{4}{12} = \$100$ M, so lost gross profit $= 100 \times 0.55 = \$55.0$ M. The loss would be much smaller if the sales were **deferred** rather than lost. For example, if the customer waits for the product because there is no alternative, the revenue arrives later, and the cost is mainly the time value of money and any price erosion.

### Solution 00-05.6

Labor $= 0.6 \times 400 = \$240$ M, which is $240/0.35 = 686$ engineer-years. Over 3 years, that is an average of $686/3 = 229$ engineers.

A 60-engineer startup might:

- license most IP (CPU cores, interfaces, memory controllers) instead of designing it;
- use a design-services partner for physical design or verification;
- have a smaller software scope (customers write the software);
- target a less advanced node or a smaller die;
- or be underestimating the work, which is the diligence question to probe.

### Solution 00-05.7

NVIDIA: $31\,000/42\,000 = 73.8\%$. ADI: $13\,000/24\,500 = 53.1\%$.

A fabless company outsources manufacturing to foundries, so its workforce is concentrated in design and software. A company with its own fabs (ADI runs some) employs many manufacturing, process and operations staff, lowering the engineering share. The two ratios also count differently ("R&D" versus "engineering roles"), so compare them with care.

### Solution 00-05.8

Respin probability went from $1 - 0.30 = 0.70$ to $1 - 0.14 = 0.86$, a factor of $0.86/0.70 = 1.23$.

**Cautions:**

- These are self-reported survey results with possible selection bias.
- Definitions of "success" may differ.
- The mix of projects shifts over time: more of them are larger and on advanced nodes.
- The 2026 study changed its recruitment method again.

### Solution 00-05.9

(a) $20 + 10 + 14 = 44$ weeks.
(b) The phase means are $(16 + 20 + 32)/3 = 22.67$, $(8 + 10 + 16)/3 = 11.33$ and $(12 + 14 + 20)/3 = 15.33$, so the expected total is **49.3** weeks.
(c) Numerically, $P(T \le 44) = 0.095$ (**9.5%**), and the 80th percentile is **53.0** weeks.
(d) Commit to about 53 weeks, the 80% point. For the CEO: "The 44-week plan assumes every phase goes as hoped, which happens less than one time in ten. A 53-week commitment gives us a 4-in-5 chance of keeping our word to customers, and we will report early if we're tracking better."

### Solution 00-05.10

(a) $0.29 \times 725 = \$210$ M.
(b) If estimates are 50–66% above reality, then real cost $= 725/1.50$ to $725/1.66$, i.e. **\$437 M to \$483 M**.
(c) A derivative design:

- reuses verified IP, verification environments and software stacks;
- skips the from-scratch architecture work and much of the IP qualification;
- benefits from a team already proficient on the node and its PDK.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 00-05.3a | cycle time at 1.5 days/layer | 90.0 | days |
| 00-05.3b | cycle time at 0.8 days/layer | 48.0 | days |
| 00-05.3c | metal-only fix processing | 14.4 | days |
| 00-05.4a | P(success), 20 blocks at 99% | 81.8 | % |
| 00-05.4b | required per-block p, 100 blocks for 90% | 0.99895 | — |
| 00-05.5 | lost gross profit | 55.0 | US$ M |
| 00-05.6a | engineer-years | 686 | — |
| 00-05.6b | average team size | 229 | engineers |
| 00-05.7a | NVIDIA R&D share | 73.8 | % |
| 00-05.7b | ADI engineering share | 53.1 | % |
| 00-05.8 | respin-probability increase factor | 1.23 | — |
| 00-05.9a | sum of most-likely values | 44 | weeks |
| 00-05.9b | expected duration | 49.3 | weeks |
| 00-05.9c | P(finish within 44 weeks) | 9.5 | % |
| 00-05.9d | 80th-percentile duration | 53.0 | weeks |
| 00-05.10a | remaining 29 % of estimate | 210 | US$ M |
| 00-05.10b | implied real cost, low end | 437 | US$ M |
| 00-05.10c | implied real cost, high end | 483 | US$ M |
