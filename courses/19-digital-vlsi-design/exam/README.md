# Course 19 · Final Exam (Digital VLSI Design)

**Time limit:** 240 minutes.
**Allowed:** a scientific calculator and the [Course 19 equation sheet](../../../reference/equation-sheets/19-digital-vlsi-design.md) printed without its chapter links. No notes, no Python and no simulator.

**Instructions.**

- Answer all 14 questions and show every step.
- Question 1 [A] is worth 8 points (2 per part), each [B] 8 (2 per part), and Questions 13 and 14 [C] 12 each (4 per part in Question 13, 3 per part in Question 14): 120 points in total. 84 or more (70%) is a strong pass.
- Give numerical answers to 3–4 significant figures, with units.
- Question 13 asks for derivations; Question 14 is a diligence question, partly graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These follow the chapters, with the threshold written $V_{TH}$ and the thermal voltage $V_T = kT/q$ (25.85 mV at 300 K).

- Transistors follow the square law (SPICE level 1) with $\lambda = 0$ unless a question gives λ; $k = \mu C_{ox}W/L$, with thresholds $V_{TN}$ and $\lvert V_{TP}\rvert$.
- A lumped RC delay is $t_p = \ln 2\,RC \approx 0.69\,RC$; a distributed wire's 50% delay is $0.38\,RC$; an "Elmore constant" is the unscaled sum $\sum R_jC_k$.
- Logical effort uses $\mu_n/\mu_p = 2$, $p_{inv} = 1$ and $\tau = 0.69\,RC_{inv}$, with capacitances in units of a unit inverter's input capacitance.
- The activity factor α counts 0→1 transitions per node per cycle, so $P = \alpha CV_{DD}^2f$, and clocks have α = 1.
- Skew is $\delta = L_2 - L_1$ (capture minus launch latency); negative slack fails, and hold slack is arrival minus required.
- Alpha-power delay is $t_p \propto V_{DD}/(V_{DD} - V_{TH})^{\alpha}$, with the exponent given in each question.
- $Q(z)$ is the standard normal upper tail; failure counts in large arrays are Poisson.

---

**1 [A] · The inverter's static behavior.** (19-01)
A process has $V_{DD}$ = 1.0 V, $V_{TN}$ = 0.30 V, $\lvert V_{TP}\rvert$ = 0.35 V and $\mu_n/\mu_p$ = 2.4, with equal channel lengths.
(a) Find the switching threshold $V_M$ of an inverter with equal NMOS and PMOS widths.
(b) What $W_p/W_n$ puts $V_M$ at 0.50 V?
(c) For a symmetric inverter ($k_n = k_p$, $V_{TN} = \lvert V_{TP}\rvert$ = 0.30 V, $V_{DD}$ = 1.0 V), find $V_{IL}$, $V_{IH}$ and the noise margins.
(d) The symmetric inverter of (c) has λ = 0.08 V⁻¹ for both devices. Find its small-signal gain at $V_M$ (exact symmetric form and the $2/(\lambda V_{ov})$ approximation), and the approximate input range over which the output swings. If each threshold has an independent random spread of σ = 20 mV, what is $\sigma_{V_M}$?

**2 [B] · Delay of an inverter.** (19-02)
(a) An inverter has $W_n$ = 0.5 µm and $W_p$ = 1.0 µm, with gate capacitance 1.1 fF/µm and drain capacitance 0.9 fF/µm (Miller effect included). It drives three copies of itself and 3 fF of wire. Find its input capacitance, $C_{int}$, $C_{ext}$, $C_L$ and γ.
(b) An NMOS with $k_n$ = 250 µA/V² and $V_{TN}$ = 0.30 V discharges 12 fF from $V_{DD}$ = 1.0 V after an ideal input step. Find $t_{pHL}$ from the exact square-law integration.
(c) Estimate the same delay with the approximation $R_{eq} \approx 3V_{DD}/(4I_{sat})$ and $t_p = \ln 2\,R_{eq}C_L$. Give $I_{sat}$, $R_{eq}$ and $t_p$.
(d) A 41-stage ring oscillator in the same process runs at 320 MHz. What stage delay does it imply, and why is a ring's stage delay longer than the step-input delay of a stage with the same load?

**3 [B] · Logic families.** (19-03)
(a) Using a unit inverter with NMOS width 1 and PMOS width 2, size a NAND4 and a NOR4 for unit drive and give each one's input capacitance relative to the inverter.
(b) A NAND3 has unit resistance $R$ = 8 kΩ, diffusion capacitance $c$ = 0.6 fF per unit width and drives $C_{ext}$ = 15 fF. With all internal nodes initially charged, find the Elmore constant of its pull-down and the 50% delay estimate.
(c) A pseudo-NMOS gate has $k_n$ = 300 µA/V² and $k_p$ = 60 µA/V², with $V_{DD}$ = 1.0 V and $V_{TN} = \lvert V_{TP}\rvert$ = 0.30 V. Find the PMOS load current, $V_{OL}$ and the static power while the output is low.
(d) A dynamic gate has $C_L$ = 12 fF, $V_{DD}$ = 1.0 V and $V_{TN}$ = 0.30 V (no body effect). After precharge, an input opens a path to an uncharged internal node of capacitance $C_a$ without discharging the output. Find the output voltage for $C_a$ = 4 fF and for $C_a$ = 6 fF, and the boundary ratio $C_a/C_L$ between the two behaviors.

**4 [B] · Sizing a path.** (19-04)
A path has four stages: a NOR2 whose input capacitance is 6 units, an inverter that drives three identical NAND3 gates (one of them on the path), the NAND3, and an inverter that drives a load of 180 units.
(a) Find $G$, $B$, $H$, $F$ and the parasitic delay $P$.
(b) Find the optimal stage effort and the minimum delay in units of τ.
(c) Size the gates backward from the load (input capacitance of each stage), and check the first stage.
(d) Is four the best number of stages? Compare with five (add an inverter) using ρ = 3.59. With τ = 12 ps, what is the delay in picoseconds?

**5 [B] · Wires and repeaters.** (19-05)
A 2 mm wire has $r$ = 8 Ω/µm and $c$ = 0.2 fF/µm.
(a) Find $R_w$, $C_w$, and the 50% delays of the distributed line and of a lumped RC with the same totals.
(b) A 2 kΩ driver drives the wire into a 20 fF load. Estimate the delay, and the share of it due to the wire's resistance.
(c) Repeaters have unit resistance $R_0$ = 10 kΩ and input capacitance $C_0$ = 0.2 fF. Find the optimal number and size of repeaters, the minimum delay (use the exact coefficient $2\sqrt{0.69 \times 0.38} + 1.38$), and the speed-up over (b).
(d) A floating victim wire has 40 fF to ground and 30 fF to each of two neighbors. One neighbor switches by 1.0 V while the other stays quiet. Find the noise on the victim. Then find the victim's effective capacitance for delay when both neighbors switch with it, when both are quiet, and when both switch against it.

**6 [B] · Power.** (19-06)
(a) A block switches 400 pF of capacitance with α = 0.12 at 1.5 GHz and 0.75 V. Find its dynamic power. Its clock network adds 150 pF at α = 1: find the clock power, and the clock power if gating stops the clock 40% of the time.
(b) A process has slope factor $n$ = 1.35 at 300 K. Find the subthreshold slope, and the factor by which leakage rises when the threshold drops by 60 mV.
(c) A block runs at 0.9 V with $V_{TH}$ = 0.30 V and an alpha-power exponent of 1.3. What supply halves its frequency, and what are the new power and energy per operation relative to the original?
(d) Power-gating a block saves 3 mW of leakage. Waking it recharges an 800 pF virtual rail to 0.75 V (charge drawn from the supply) and costs 0.05 nJ in control. What is the break-even idle time?

**7 [B] · Sequential timing.** (19-07)
(a) A flip-flop path has $t_{pcq}$ = 45 ps, $t_{setup}$ = 25 ps and logic $t_{pd}$ = 380 ps; the capture clock arrives 20 ps after the launch clock, and cycle-to-cycle jitter is 12 ps. Find the minimum period and the maximum frequency.
(b) The same pair has $t_{ccq}$ = 25 ps, shortest logic $t_{cd}$ = 10 ps and $t_{hold}$ = 20 ps. Find the hold slack and the fix.
(c) Logic totalling 1800 ps is to be pipelined with 70 ps of sequencing overhead per stage to reach at least 2.5 GHz. How many stages are needed? Give the resulting frequency, latency and overhead share.
(d) A synchronizer flip-flop has τ = 18 ps and $T_0$ = 15 ps, with a 1.5 GHz clock and asynchronous data at 80 MHz. With 600 ps allowed for resolution, find the MTBF. How much does a second flip-flop (one extra full cycle of resolution) multiply it by?

**8 [B] · SRAM.** (19-08)
(a) A 6T cell at $V_{DD}$ = 0.9 V has $V_{TN} = \lvert V_{TP}\rvert$ = 0.30 V, $k_A$ = 100 µA/V² and cell ratio 1.8. Find the read disturbance $\Delta V$ of the '0' node, and its margin to $V_{TN}$.
(b) A bitline has 512 cells at 0.07 fF each plus 12 fF of wiring, and the cell current is 18 µA. How long does a 90 mV swing take? A sense amplifier with τ = 12 ps then regenerates it to the full 0.9 V: how long does that take?
(c) A 256 Mib array (2²⁸ cells) is designed for a 6σ cell margin. Find the cell failure probability, the expected number of failing cells and the array yield without repair, and the yield if one failure can be repaired. What margin would give 99% yield without repair?
(d) A 64 Mib macro uses a 0.0175 µm² bitcell with 72% array efficiency. Find the bitcell area, the macro area and the density in Mb/mm².

**9 [B] · Layout and cells.** (19-09)
Use the chapter's illustrative rules: poly width 2λ, poly spacing 3λ, contact 2λ, contact-to-gate 2λ, active enclosure of contact 1λ.
(a) Give the contacted and uncontacted gate pitches. A NAND4 pull-down is a strip of four series transistors with contacts at its two ends. How long is the strip if the internal nodes are left uncontacted, and how long if every internal node were contacted? Give both in λ and in µm for λ = 0.09 µm.
(b) For the OAI211 gate $Y = \overline{(A + B)CD}$, find every input ordering that is an Euler path in both the pull-down and the pull-up networks, so that each diffusion strip is unbroken.
(c) A block has 350 kGates of logic at a routed density of 120 kGates/mm² and 20 000 flip-flops of 20.02 µm² each, placed at 70% utilization. Estimate the block area.
(d) A gate of 0.3 µm × 1.0 µm connects to a 0.2 µm wide metal-1 line. With an antenna ratio limit of 400 (metal area over gate area), how long can the line be before a jumper or diode is needed?

**10 [B] · Static timing.** (19-10)
(a) A small timing graph has inputs $a$ (arrival 0) and $b$ (arrival 0.10 ns). Gate G1 takes $a$ and $b$ with delay 0.20 ns; G2 takes $b$ with delay 0.35 ns; G3 takes G1 and G2 with delay 0.15 ns and drives an output required at 0.70 ns. Find the arrival times, required times and slacks of every node, and the critical path.
(b) A register-to-register path has $T_c$ = 1.20 ns, $L_1$ = 0.35 ns, $L_2$ = 0.28 ns, $t_{pcq}$ = 0.12 ns, $t_{pd}$ = 0.62 ns, $t_{setup}$ = 0.06 ns and $U$ = 0.05 ns. Find the setup slack, and the shortest period and highest frequency the path allows.
(c) For hold, $t_{ccq}$ = 0.09 ns, $t_{cd}$ = 0.04 ns, $t_{hold}$ = 0.03 ns and the hold uncertainty is 0.02 ns. Find the hold slack. A clock-tree change raises $L_2$ to 0.60 ns: recompute both slacks, say how much delay must be added, and where it may be added without hurting setup.
(d) A path has 12 stages with independent-gate sigma 8 ps and correlation 0.2 between stages. Find the path sigma and a 3σ margin, and compare with the margin if the stages were independent.

**11 [B] · Floorplan, place and route.** (19-11)
(a) A block has 1.20 mm² of standard cells. Find the core area and the side of a square core at 70% utilization.
(b) A 400 µm power strap is 1.6 µm wide on a layer of 0.047 Ω/□ and carries 3 mA spread uniformly along its length. Find its resistance and the worst IR drop when fed from both ends and from one end. What is the largest feed spacing that keeps the drop below 10 mV at the same current per length?
(c) Two clock subtrees have delays $t_1$ = 50 ps and $t_2$ = 55 ps and loads $C_1$ = 20 fF and $C_2$ = 30 fF. A 300 µm wire with $r$ = 0.5 Ω/µm and $c$ = 0.2 fF/µm joins them. Find the zero-skew tapping point, measured from subtree 1, and the Elmore delay from the tap to the sinks.
(d) A net has pins at (0, 0), (40, 10), (10, 50) and (30, 30) µm. Find its HPWL, its rectilinear minimum spanning tree length and its rectilinear Steiner tree length (Steiner points on the Hanan grid), and check Hwang's bound.

**12 [B] · Test and verification.** (19-12, 19-13)
(a) A product yields 85% and its test reaches 98% stuck-at coverage. Find the defect level in DPPM, and the coverage needed for 200 DPPM.
(b) A design has 200 000 scan flip-flops in 100 balanced chains and 3000 patterns, shifted at 50 MHz. Find the clock cycles, the test time, and the uncompressed test data volume (≈ 2FP bits) in megabytes.
(c) A coverpoint has three bins hit with probabilities 0.6, 0.3 and 0.1 per random transaction. Find the expected number of transactions to fill it, and compare with $1/p_{\min}$.
(d) A 3-bit counter starts at 0 and adds 3 (modulo 8) every cycle. The property is "$x \ne 5$". Is it violated? If so, at what BMC depth is the violation found, and what is the diameter of the reachable state graph?

**13 [C] · Three derivations.** (19-01, 19-05, 19-04)
(a) Derive the switching threshold of a square-law CMOS inverter, $V_M = (V_{TN}\sqrt r + V_{DD} - \lvert V_{TP}\rvert)/(1 + \sqrt r)$ with $r = k_n/k_p$, stating your assumptions. Show that it is $V_{DD}/2$ for a symmetric inverter, derive $\partial V_M/\partial V_{TN}$, and evaluate it for the process of Question 1 with equal widths.
(b) For a wire of total resistance $R_w$ and capacitance $C_w$ split by $k$ repeaters of size $h$ (unit resistance $R_0$, unit input capacitance $C_0$), derive $k_{opt}$ and $h_{opt}$ from $T(k, h) = 0.69R_0C_w/h + 0.69kR_0C_0 + 0.38R_wC_w/k + 0.69R_whC_0$. Show that at the optimum each segment's wire delay equals the repeater's intrinsic delay $0.69R_0C_0$, and evaluate that delay for Question 5's repeaters.
(c) Prove that for a path of $N$ stages with fixed path effort $F$, delay is minimized when every stage bears effort $F^{1/N}$. Then let $N$ vary, adding inverters with parasitic delay $p_{inv}$, and derive the condition $\rho(\ln\rho - 1) = p_{inv}$ for the best stage effort. Find ρ for $p_{inv}$ = 1.5.

**14 [C] · Diligence: an AI inference accelerator.** (19-05 to 19-13)
A start-up seeks an investment for an inference accelerator on a 3 nm process. Its deck claims:

1. "The 600 mm² die draws 450 W at 1.2 GHz and 0.75 V; our switched capacitance is 1.6 µF at an activity of 0.25."
2. "We can reach 2.0 GHz in a turbo mode by raising the supply to 0.85 V." (Use $V_{TH}$ = 0.30 V and an alpha-power exponent of 1.3.)
3. "With 97% stuck-at coverage we will ship at 50 DPPM; we expect 55% yield."
4. "512 MB of on-die SRAM at a 0.021 µm² bitcell; the design is fully verified, so first-pass silicon is guaranteed."

(a) Check claim 1: compute the dynamic power, the remainder it implies, and the power density. Is the claim internally consistent, and what would you ask?
(b) Check claim 2: what frequency does 0.85 V support, and by what factor does dynamic power rise? What would the turbo mode really deliver?
(c) Check claim 3: find the defect level the stated coverage and yield imply, and the coverage that 50 DPPM would need. What would you ask about the test strategy?
(d) Check claim 4: compute the raw bitcell area of the SRAM and its share of the die at 70% array efficiency. Then assess the verification claim against the industry's reported first-silicon success rates (19-13 §9), and list three questions you would put to the VP of Engineering.
