# Solutions 25-05 · Foundries, PDKs and Specialty Processes

Problems: [25-05 problems](../problems/25-05-problems.md) · Chapter: [25-05](../chapters/25-05-foundries-pdks-specialty-processes.md)

Every number is recomputed by [verify_25_05.py](../verify/verify_25_05.py).

---

## Solutions

### Solution 25-05.1

(a) $5.9 - 5.4$ = **0.5** percentage points.

(b) $0.054 \times 55.4$ = **$3.0 B**, consistent with TrendForce's "over $3 B" given that 5.4% is itself rounded.

### Solution 25-05.2

$3 + 30 + 33 + 11$ = **77**% ✓; nodes older than 7 nm supplied **23**%.

### Solution 25-05.3

The 6 mm² minimum applies: $6 \times 913$ = **€5,478**, or **€2,739** per square millimetre actually used. Small designs share a slot or pad out their area with test structures.

### Solution 25-05.4

$2.5 \times 10^6/17{,}820$ = **140** mm².

### Solution 25-05.5

Slow: **1.67**; fast: **0.686**; spread **2.44**, against 1.67 with $\alpha$ = 1.3. A larger exponent makes delay more sensitive to the gate overdrive $V - V_{TH}$, which is exactly what the corners move; long-channel devices (α near 2) suffer more from threshold and supply spread than velocity-saturated short-channel ones.

### Solution 25-05.6

The slow corner is **1.347** times slower than typical (Example 25-05.4's 1.35, unrounded), so the path needs $2.0 \times 1.347$ = **2.69** GHz at typical.

### Solution 25-05.7

(a) $80/53.7$ = **1.49** V.

(b) $10^{80/70}$ = **13.9** times.

### Solution 25-05.8

(a) At threshold the front surface potential is pinned (strong inversion begins at a fixed surface potential). With the body fully depleted, a back-gate change $\Delta V_{BG}$ couples to the front surface through $C_{BOX}$ and $C_{Si}$ in series, injecting charge $C_{back}\Delta V_{BG}$ with $C_{back} = C_{Si}C_{BOX}/(C_{Si} + C_{BOX})$. To keep the front surface at the same potential, the front gate must supply the opposite charge, $C_{ox}\Delta V_{TH} = -C_{back}\Delta V_{BG}$, giving the coupling of §3.5.

(b) In units of $\varepsilon_0$/nm: $C_{ox}$ = **3.9**, $C_{Si}$ = **1.95**, $C_{BOX}$ = **0.156**; coupling **0.0370**, that is **37.0** mV/V.

(c) The BOX: it is the smallest capacitance. Solving for twice the coupling gives a BOX of **11.5** nm, less than half of 25 nm. The coupling is also inversely proportional to $C_{ox}$, so doubling the gate oxide's EOT would double it exactly; but that halves the front gate's control of the channel, cutting drive current and worsening short-channel behaviour, so the BOX is the knob to turn.

### Solution 25-05.9

$6/3 + 1/2.5 + 3/1.2$ = **4.90** mm²; cost ratio $1.8 \times 4.90/10$ = **0.882**, a 12% saving: more digital content makes the shrink pay.

### Solution 25-05.10

$4 \times 16{,}200$ = **€64,800**; **€1,620** per sample.

### Solution 25-05.11

$(80/20)^2$ = **16** times at a fixed critical field. Silicon's critical field falls as the drift doping falls (09-13), so the empirical scaling is closer to $V_B^{2.5}$, giving $4^{2.5}$ = **32** times. Either way, at fixed on-resistance the 80 V device needs tens of times the area, which is why high-voltage BCD dies are dominated by their power transistors and why lateral RESURF (reduced surface field) designs, which shape the drift region's field to beat the one-dimensional limit, matter commercially.

### Solution 25-05.12

$Q(3)$ = **1.35e-3**, about **1,350** dies per million slower than the slow corner, before local mismatch, which signoff covers separately with its own margins.

### Solution 25-05.13

Expected respin cost: $0.30 \times 20$ = **$6 M**. Spread over six months of earlier launch, the start pays if earlier revenue brings at least **$1.0 M** of gross profit per month, ignoring the respin's own schedule delay, which makes the bar higher.

### Solution 25-05.14

(a) The design rules and DRC deck; immature rules miss real failure modes or change after tape-out, forcing late layout fixes. (b) The LVS rule deck; errors in device recognition let a wrong connection or device size pass. (c) The device models with their corner and statistical variants; early models are fitted to few wafers, so silicon can be slower or leakier than simulated, which is why early-PDK starts carry respin risk (Problem 25-05.13). (d) The parasitic-extraction (RC) deck; mis-modelled wire resistance or coupling capacitance makes post-layout timing optimistic. (e) The parameterized cells (PCells) and their models; without a characterized inductor PCell the designer must model the device from electromagnetic simulation and accept more risk.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 25-05.1a | Samsung minus SMIC | 0.5 | points |
| 25-05.1b | SMIC revenue | 3.0 | $B |
| 25-05.2a | sum of node shares | 77 | % |
| 25-05.2b | older nodes | 23 | % |
| 25-05.3a | slot cost | 5478 | € |
| 25-05.3b | cost per used mm² | 2739 | € |
| 25-05.4a | break-even area | 140 | mm² |
| 25-05.5a | slow corner, alpha 2 | 1.67 | |
| 25-05.5b | fast corner, alpha 2 | 0.686 | |
| 25-05.5c | spread, alpha 2 | 2.44 | |
| 25-05.6a0 | slow-corner delay ratio, unrounded | 1.347 | |
| 25-05.6a | typical frequency needed | 2.69 | GHz |
| 25-05.7a | back-gate swing | 1.49 | V |
| 25-05.7b | leakage factor | 13.9 | |
| 25-05.8a | C_ox | 3.9 | |
| 25-05.8a1 | C_Si | 1.95 | |
| 25-05.8a2 | C_BOX | 0.156 | |
| 25-05.8b | coupling | 0.0370 | |
| 25-05.8b1 | coupling in mV/V | 37.0 | mV/V |
| 25-05.8c | BOX for double coupling | 11.5 | nm |
| 25-05.9a | new area | 4.90 | mm² |
| 25-05.9b | cost ratio | 0.882 | |
| 25-05.9c | saving | 12 | % |
| 25-05.10a | minimum slot, discounted | 64800 | € |
| 25-05.10b | per sample | 1620 | € |
| 25-05.11a | on-resistance ratio | 16 | |
| 25-05.11b | ratio with V_B^2.5 | 32 | |
| 25-05.12a | fraction slower than corner | 1.35e-3 | |
| 25-05.12b | per million | 1350 | |
| 25-05.13a | expected respin cost | 6 | $M |
| 25-05.13b | break-even monthly profit | 1.0 | $M |
