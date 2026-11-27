# Problems 27-05 · The PC SoC

Chapter: [27-05](../chapters/27-05-pc-soc.md) · Worked solutions: [27-05 solutions](../solutions/27-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** All device parameters are assumed unless a source is cited. Average SoC power is $\sum r_iP_i$; turbo lasts $\tau\ln[(P_2 - P_0)/(P_2 - P_1)]$ under an averaged limit; bandwidth is $(w/8)R$; decode is bounded by $BW/(N_pb/8)$; prefill takes $2N_pT/(\text{TOPS}\cdot u)$; die cost uses 25-04's dies-per-wafer formula on 300 mm wafers and Poisson yield; link power is $8B\,E_{bit}$.

---

## Problems

### Problem 27-05.1 [A]

**Which engine?** Name the block best suited to each task and why in a phrase: (a) decoding a 4K video stream; (b) live captions during a call; (c) compiling code; (d) rendering a 3D game; (e) running a 70-billion-parameter model in a format the NPU runtime does not support.

### Problem 27-05.2 [A]

**Bus bandwidth.** Find the peak bandwidth of (a) a 128-bit LPDDR5X bus at 9600 MT/s and (b) a 512-bit bus at 8533 MT/s.

### Problem 27-05.3 [A]

**Residency.** A SoC spends 5% of the time active at 6.0 W, 15% in shallow idle at 1.5 W and 80% in deep idle at 0.30 W; the rest of the platform draws 2.5 W; the battery holds 60 Wh. Find the SoC's average power, the total and the battery life.

### Problem 27-05.4 [B]

**Turbo and recovery.** A package has $P_1$ = 45 W, $P_2$ = 115 W and $\tau$ = 56 s on its averaged power. (a) How long can it turbo starting from an average of 10 W? (b) After a turbo ends with the average at 45 W, the package idles at 5 W. How long until the average falls back to 10 W?

### Problem 27-05.5 [B]

**What fits?** A laptop can give 24 GB of its memory to a model. (a) What is the largest model (in billions of parameters) it can hold at 4 bits and at 8 bits? (b) Find the decode bound (weights only, dense model) for a 32-billion-parameter 4-bit model on a 136.5 GB/s bus.

### Problem 27-05.6 [B]

**Waiting for the answer.** An 8-billion-parameter, 4-bit model answers a 2000-token prompt with 500 tokens on a laptop with a 136.5 GB/s bus and an NPU sustaining 40 TOPS at 50% utilization. Find the prefill time, the decode bound in tokens/s, the decode time and the total.

### Problem 27-05.7 [B]

**NPU or GPU for a burst?** Generating an image takes $5 \times 10^{13}$ operations. The NPU runs at 40 TOPS with 50% utilization and 6 TOPS/W; the GPU at 120 TOPS with 60% utilization and 1.5 TOPS/W, plus 0.5 W to keep it awake. Find each engine's time and energy, and the ratios.

### Problem 27-05.8 [B]

**A big die.** Compare a 400 mm² monolithic die on a 3 nm-class wafer at \$18,500 with $D_0$ = 0.10 cm⁻² against two 200 mm² tiles on the same wafer type in a \$10 package with 97% assembly yield, assuming the split adds no interface area. Find both costs and their ratio.

### Problem 27-05.9 [B]

**A die-to-die budget.** A 1 TB/s die-to-die interface must draw at most 1 W. What energy per bit must it achieve?

### Problem 27-05.10 [B]

**When does memory-on-package pay?** If memory-on-package saves 2 pJ/bit of I/O energy, at what DRAM traffic does it save 1 W?

### Problem 27-05.11 [C]

**Designing for 20 hours.** A laptop with a 70 Wh battery must play video for 20 hours. Its platform draws 2.7 W (display 1.5, memory 0.3, SSD 0.1, Wi-Fi 0.2, other 0.6). (a) What average SoC power is allowed? (b) With 8% active residency at 5.0 W and the rest split between shallow idle at 1.2 W and deep idle at 0.25 W, what deep-idle residency is needed?

### Problem 27-05.12 [C]

**Does turbo matter for long tasks?** A task takes 60 s at the sustained 28 W. With the turbo of Example 27-05.2 (13.8 s at 64 W from an idle start, speed scaling as the cube root of power, then back to 28 W), how long does it take, and how much less time does it need?

### Problem 27-05.13 [B]

**Deriving the turbo duration.** The averaged power $y(t)$ obeys $\tau\,dy/dt = P - y$, and during turbo the package draws $P = P_2$.

- (a) Solve the equation by separating variables, from $y(0) = P_0$.
- (b) Set $y = P_1$ and derive $t_{turbo} = \tau\ln[(P_2 - P_0)/(P_2 - P_1)]$.
- (c) Show that for $P_0$ close to $P_1$, $t_{turbo} \approx \tau(P_1 - P_0)/(P_2 - P_1)$. Evaluate the exact and approximate durations for $P_1$ = 28 W, $P_2$ = 64 W, $\tau$ = 28 s and $P_0$ = 25 W, and the approximation's error.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Laptop SoC blocks and how they differ from a phone's | 1 |
| 2. Battery life from residency | 3, 11 |
| 3. Turbo under an averaged limit | 4, 12, 13 |
| 4. Unified memory, local models, NPU vs GPU | 2, 5, 6, 7 |
| 5. Chiplets, links and memory-on-package | 8, 9, 10 |
