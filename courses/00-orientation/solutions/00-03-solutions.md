# Solutions 00-03 · How to Study This Curriculum

Problems: [00-03 problems](../problems/00-03-problems.md) · Chapter: [00-03](../chapters/00-03-how-to-study-this-curriculum.md)

All numbers are in the answer key and recomputed by [verify_00_03.py](../verify/verify_00_03.py).

---

## Solutions

### Solution 00-03.1

**High utility:** practice testing and distributed practice. **Low utility** (any three): summarization, highlighting/underlining, the keyword mnemonic, imagery for text, and rereading. Most learners rely heavily on rereading and highlighting, the two that feel most productive.

### Solution 00-03.2

- **Volt:** V = W/A = (kg·m²·s⁻³)/A = **kg·m²·s⁻³·A⁻¹**.
- **Ohm:** Ω = V/A = **kg·m²·s⁻³·A⁻²**.
- **Farad:** F = C/V = (A·s)/(kg·m²·s⁻³·A⁻¹) = **kg⁻¹·m⁻²·s⁴·A²**.
- **Henry:** H = V·s/A = (kg·m²·s⁻³·A⁻¹)(s)/A = **kg·m²·s⁻²·A⁻²**.

Check: Ω·F = (kg·m²·s⁻³·A⁻²)(kg⁻¹·m⁻²·s⁴·A²) = s ✓.

### Solution 00-03.3

(a) H/Ω = (Ω·s)/Ω = s ✓, a time.
(b) H·A² = (V·s/A)·A² = V·A·s = W·s = J ✓, an energy.
(c) 1/(Ω·F) = 1/s ✓, a frequency (the 2π is dimensionless).
(d) $\sqrt{\text{H/F}} = \sqrt{\Omega\cdot\text{s}/(\text{s}/\Omega)} = \Omega$, an impedance, not a speed ✗.
(e) A/Ω = A²/V, not W ✗. The correct forms are $P = I^2R$ or $P = V^2/R$.

### Solution 00-03.4

1. **Understand.** A single loop with 12 V, 0.5 Ω and 5.5 Ω in series.
2. **Plan.** KVL, then $P = I^2R$.
3. **Execute.**
   - $I = 12/(0.5 + 5.5) = 2.000$ A.
   - $V_L = IR_L = 11.00$ V.
   - $P_L = I^2R_L = 4 \times 5.5 = 22.00$ W.
   - Battery power is $12 \times 2 = 24$ W, so efficiency $= 22/24 = 91.7\%$.
4. **Check.**
   - *Units:* V/Ω = A, A·Ω = V, A²·Ω = W ✓.
   - *Limit:* with $R_{int} \to 0$, $I \to 12/5.5 = 2.18$ A and the efficiency tends to 100%. Our results are slightly lower ✓.
   - *Magnitude:* 22 W from a 12 V battery is ordinary, about a car brake or turn-signal bulb (21 W is a common rating) ✓.

### Solution 00-03.5

(a) $P = 5\times10^{10} \times 0.01 \times 2\times10^9 \times 3\times10^{-16} = 300$ W.
(b) $300/(5\times10^{10}) = 6\times10^{-9}$ W $= 6$ nW per transistor.
(c) 300 W is in the range of large datacenter processors, so the estimate is plausible. Activity factor is the least certain input: it can vary by 10× between workloads and between logic and memory arrays. Leakage power is also ignored here, and it can be a significant share at advanced nodes ([19-06](../../19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md)).

### Solution 00-03.6

(a) Ease 2.0: intervals 1, 2, 4, …, 256 days. Cumulative after $n$ reviews is $2^n - 1$. After 8 reviews it is 255 days (< 365); after 9 it is 511 days. **9 reviews.**
(b) Ease 3.0: intervals 1, 3, 9, 27, 81, 243, 729 days. Cumulative after 6 reviews is 364 days (just short); after 7 it is 1093. **7 reviews.**

A higher ease means fewer reviews but longer gaps, so each review is a harder retrieval and more items are forgotten (and must be relearned) between reviews. Spaced-repetition software adjusts ease per card based on how hard you find it.

### Solution 00-03.7

At 11 h/week: $116/11 = 10.5$ weeks. At 8 h/week: $116/8 = 14.5$ weeks. Protect the **problem sets** (retrieval practice) first. If time is short, shorten the reading by skimming theory you can already reproduce, rather than skipping problems.

### Solution 00-03.8

Absolute difference: $61 - 40 = 21$ percentage points. Relative improvement: $21/40 = 52.5\%$. A marketer would quote "52.5% better retention" because the relative figure sounds bigger. An analyst reports both, and asks about the baseline and the time horizon (here, one week).

### Solution 00-03.9

(a) $CV$ has units (C/V)·V = C, a charge, not an energy. The correct form is $E = \tfrac{1}{2}CV^2$, with units C·V = J.
(b) $R/L$ has units Ω/(Ω·s) = 1/s, a rate, not a time. The correct form is $\tau = L/R$.
(c) $VR$ has units V·Ω = V²/A, not A. The correct form is $I = V/R$.

### Solution 00-03.10

(a) $e^{-7/5} = e^{-1.4} = 0.247$, so **24.7%**.
(b) $0.9 = e^{-t/5}$ gives $t = 5\ln(1/0.9) = 0.527$ days, about 13 hours.
(c) $S = 12.5$ days, so $t = 12.5 \times 0.1054 = 1.32$ days after the review.
(d) The interval to reach a fixed recall target is proportional to $S$. Each successful review multiplies $S$, so each interval is longer than the last. Spacing gets more efficient the better you know something.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 00-03.4a | current | 2.000 | A |
| 00-03.4b | load voltage | 11.00 | V |
| 00-03.4c | load power | 22.00 | W |
| 00-03.4d | efficiency | 91.7 | % |
| 00-03.4e | current with ideal battery | 2.18 | A |
| 00-03.5a | dynamic power estimate | 300 | W |
| 00-03.5b | power per transistor | 6 | nW |
| 00-03.6a | reviews to cover a year, ease 2.0 | 9 | — |
| 00-03.6b | reviews to cover a year, ease 3.0 | 7 | — |
| 00-03.7a | weeks at 11 h/week | 10.5 | weeks |
| 00-03.7b | weeks at 8 h/week | 14.5 | weeks |
| 00-03.8a | absolute difference | 21 | points |
| 00-03.8b | relative improvement | 52.5 | % |
| 00-03.10a | recall after 7 days | 24.7 | % |
| 00-03.10b | first review time | 0.527 | days |
| 00-03.10c | next interval | 1.32 | days |
