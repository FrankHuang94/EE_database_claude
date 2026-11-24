# Problems 20-01 · Analog Design Fundamentals in Nanometer CMOS

Chapter: [20-01](../chapters/20-01-analog-design-fundamentals-gm-id.md) · Worked solutions: [20-01 solutions](../solutions/20-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Unless stated, use the chapter's illustrative T130 NMOS at 300 K: μ = 350 cm²/V·s, $C_{ox}$ = 8.6 fF/µm², $n$ = 1.3, $V_{TH}$ = 0.45 V, $v_{sat}$ = 8 × 10⁶ cm/s, $V_A'$ = 8 V/µm, $V_T$ = 25.85 mV, and $I_{spec,\square}$ = 0.523 µA. "Long channel" means $\lambda_c$ = 0; otherwise include velocity saturation through $\lambda_c = \mu V_T/(v_{sat}L)$. $C_{gg} = \tfrac23WLC_{ox}$. Mobility varies as $T^{-3/2}$ where temperature changes. Problems marked *(lab)* can be checked with `labs/20-01-lab/gmid.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 20-01.1 [A]

**Which region?** An NMOS with $W/L$ = 5 µm/1 µm is biased in saturation at 0.2 µA, 4 µA and 200 µA. Find its specific current, and for each current the inversion coefficient, the region and the long-channel $g_m/I_D$.

### Problem 20-01.2 [A]

**The two limits.** (a) Show that $g_m/I_D = 2/[nV_T(1 + \sqrt{1 + 4IC})]$ tends to $1/(nV_T)$ in weak inversion and to $2/V_{ov}$ in strong inversion. (b) Evaluate the weak-inversion limit at −40 °C and at 125 °C.

### Problem 20-01.3 [A]

**Width without current.** The transistor of Example 20-01.1 ($W/L$ = 10 µm/0.5 µm, 20 µA) is redrawn with twice the width at the same current. (a) What happens to its inversion coefficient and its $g_m/I_D$? Give both numbers. (b) Why is "make it wider" a way to raise $g_m$ at fixed power, and what does it cost? (c) Why can a single lookup table, computed for one width, size transistors of every width at that length?

### Problem 20-01.4 [B]

**Overdrive and inversion.** (a) Compute the long-channel overdrive $V_{GS} - V_{TH}$ at $IC$ = 0.01, 0.1, 1, 10 and 100. (b) At what inversion coefficient is the overdrive exactly zero? (c) What does a negative overdrive mean physically, and why is it a poor design variable?

### Problem 20-01.5 [B] *(lab)*

**Sizing for a transconductance.** A transistor must deliver $g_m$ = 1 mS at $g_m/I_D$ = 20 S/A with $L$ = 0.5 µm. Find $I_D$, the inversion coefficient, the current density, $W$, $f_T$, the intrinsic gain and $C_{gg}$.

### Problem 20-01.6 [B]

**Gain at two operating points.** A stage needs an intrinsic gain of 100. (a) Find the length needed at $g_m/I_D$ = 20 S/A and at 12 S/A. (b) Find $f_T$ in each case. (c) Which choice is faster, and why is the answer not obvious?

### Problem 20-01.7 [B]

**The velocity-saturated limit.** (a) Show that the chapter's model gives $I_D \to WC_{ox}v_{sat}V_{ov}$ in deep strong inversion. (b) Find $\lambda_c$ and the limiting $f_T = 3v_{sat}/(4\pi L)$ for $L$ = 0.15 µm and 60 nm. (c) Why does the limit scale as $1/L$ rather than $1/L^2$?

### Problem 20-01.8 [B]

**Checking the strong-inversion $f_T$.** A long-channel transistor with $L$ = 1 µm has an overdrive of 0.2 V. (a) Find its normalized charge $q$ and its $f_T$ from the chapter's model. (b) Compare with 09-09's $3\mu V_{ov}/(4\pi nL^2)$, and explain the difference.

### Problem 20-01.9 [B]

**A corner in weak inversion.** The transistor of Example 20-01.1 carries 0.5 µA. (a) Find its inversion coefficient and gate voltage. (b) With that gate voltage held fixed, find the current if $V_{TH}$ rises or falls by 30 mV, from the model and from the weak-inversion approximation $e^{-\Delta V_{TH}/(nV_T)}$. (c) What happens to $g_m$ instead if the current is held fixed?

### Problem 20-01.10 [B]

**Temperature in weak inversion.** The same transistor carries a constant 1 µA. Find $g_m$ at −40 °C, 27 °C and 125 °C, both from the weak-inversion limit $I_D/(nV_T)$ and from the model. Why are the model's values lower?

### Problem 20-01.11 [C] *(lab)*

**The sweet spot at an intermediate length.** For $L$ = 0.3 µm, find the inversion coefficient, $g_m/I_D$ and $f_T$ at which $(g_m/I_D)\,f_T$ peaks, and the peak value. Compare with the 0.15 µm result of Example 20-01.4 and explain the shift.

### Problem 20-01.12 [C]

**Transconductance with velocity saturation.** (a) Starting from $IC = (q^2 + q)/(1 + \lambda_cq)$ and $V_P/V_T = 2q + \ln q$, derive the chapter's expression for $g_m/I_D$. (b) Show that it reduces to $1/[nV_T(1 + q)]$ for $\lambda_c = 0$ and tends to $1/(2nV_Tq)$ for large $q$. (c) Evaluate it at $IC$ = 10 for $L$ = 0.15 µm and compare with the long-channel value.

### Problem 20-01.13 [C]

**Power-optimal sizing under a speed constraint.** An input transistor at $L$ = 0.15 µm must provide $g_m$ = 2 mS with $f_T$ of at least 10 GHz. (a) Find the highest $g_m/I_D$ that meets the $f_T$ requirement, and the resulting current and width. (b) Compare with a design at the sweet spot, $g_m/I_D$ = 8 S/A. (c) Which would you choose for a battery-powered product, and what would make you change your mind?

### Problem 20-01.14 [B]

**Efficiency costs area.** A transistor at $L$ = 0.5 µm must provide 500 µS. (a) Find its current, width and gate area at $g_m/I_D$ = 25 S/A and at 10 S/A. (b) Threshold mismatch between two such transistors scales as $1/\sqrt{WL}$ (Pelgrom's law, 20-11). By what factor does the weak-inversion design's mismatch improve?

### Problem 20-01.15 [A]

**Reading a design review.** A team reports that its ADC driver's input pair runs at $g_m/I_D$ = 22 S/A at minimum length (0.15 µm in T130). (a) Find the inversion coefficient, $f_T$ and intrinsic gain at that point. (b) Write two questions you would ask the team, and say what answer would reassure you.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Derive the model, the inversion coefficient and $g_m/I_D$ | 1, 2, 4, 12 |
| 2. Compute $g_m/I_D$, current density, $f_T$ and intrinsic gain | 3, 5, 7, 8, 15 |
| 3. Size a transistor with the $g_m/I_D$ method | 5, 6, 13, 14 |
| 4. The $(g_m/I_D) f_T$ sweet spot and choosing a region | 11, 13, 15 |
| 5. Current bias, corners and temperature | 9, 10 |
