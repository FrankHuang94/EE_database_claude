# Course 22 · Final Exam (Power Electronics and Energy Conversion)

**Time limit:** 330 minutes, best taken in two sittings of about 165 minutes: Questions 1–7, then Questions 8–14.
**Allowed:** a scientific calculator and the [Course 22 equation sheet](../../../reference/equation-sheets/22-power-electronics-and-energy-conversion.md) printed without its chapter links. No notes, no Python and no simulator.

**Instructions.**

- Answer all 14 questions and show every step.
- Questions 1–12 [B] are worth 8 points each (2 per part), and Questions 13 and 14 [C] 12 each (3 per part): 120 points in total. 84 or more (70%) is a strong pass.
- Give numerical answers to 3–4 significant figures, with units.
- Question 13 asks for derivations: results quoted from the equation sheet earn no credit unless derived. Question 14 is a diligence question, partly graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These follow the chapters.

- Converters are in steady state, with ideal switches and lossless components unless a loss is given, and in continuous conduction unless a question says otherwise. A ripple written Δ is peak-to-peak; $D' = 1 - D$.
- Copper's resistivity is 17.24 nΩ·m at 20 °C and 22.66 nΩ·m at 100 °C; $\mu_0 = 4\pi \times 10^{-7}$ H/m; $F$ = 96 485 C/mol; carbon's molar mass is 12.011 g/mol.
- Three-phase voltages are line-to-line RMS unless written "per phase". Per-unit quantities are on the bases stated in the question.

---

**1 [B] · Efficiency, loss and hold-up.** (22-01)
(a) A 48 V to 12 V converter delivers 1.2 kW at 96.5% efficiency. Find its input power and loss. By how many watts, and by what percentage, does the loss fall if the efficiency rises to 97.5%?
(b) A 3.6 V cell feeds a 1.2 V, 15 mA rail. Compare an LDO with a 25 µA quiescent current against a buck converter of 90% efficiency: find the LDO's efficiency, each regulator's battery current and their ratio.
(c) A converter's loss is $P_0 + aI + RI^2$ with $P_0$ = 0.3 W, $a$ = 0.02 V and $R$ = 12 mΩ, at a 1.8 V output. Find the current of peak efficiency and that efficiency, and the efficiency at 20 A. A second identical phase (its own $P_0$, each phase carrying half the current through its own $R$) is added: find the efficiency at 20 A and the current above which two phases beat one.
(d) A 54 V rack bus must ride through a 20 ms outage at 3 kW while falling no lower than 40 V. Find the hold-up capacitance and the fraction of its stored energy that it uses.

**2 [B] · A point-of-load buck.** (22-02)
A synchronous buck converts 5 V to 1.0 V at 6 A, switching at 2 MHz with $L$ = 220 nH and $C$ = 47 µF.
(a) Find $D$, the inductor ripple $\Delta i_L$, the ripple ratio $r = \Delta i_L/I$, the peak inductor current and the capacitive output ripple. What ripple would a 2 mΩ ESR alone add?
(b) Find the RMS currents of the inductor, the high-side switch, the low-side switch and the input capacitor.
(c) With $R_{HS}$ = 12 mΩ, $R_{LS}$ = 5 mΩ and $R_L$ = 3 mΩ, find $R_{eq}$, the conduction loss and the efficiency at the ideal duty cycle. What duty cycle actually holds 1.0 V at 6 A?
(d) Find the critical load current. If the converter runs in discontinuous conduction at 0.4 A (both switches off once the inductor current reaches zero), find $K$, the duty cycle $D_1$, the freewheeling interval $D_2$ and the peak inductor current.

**3 [B] · Boost and buck-boost.** (22-03)
(a) A boost converts 3.0 V to 12 V at 0.5 A, switching at 1 MHz with $L$ = 4.7 µH and $C$ = 22 µF. Find $D$, the inductor current, its ripple and the output ripple.
(b) The inductor's winding resistance is $R_L$ = 50 mΩ; treat the switch and diode as ideal. At the duty cycle of part (a), find the efficiency and the output voltage. What duty cycle restores 12 V, and what is the efficiency there? Find the largest gain this converter can reach and the duty cycle at which it does.
(c) An inverting buck-boost makes −12 V at 0.3 A from 5 V. Find $D$, the inductor current, the voltage the switch must block and the average input current.
(d) The boost of part (a) runs at 20 mA. Find $K$ and $K_{crit}$, show that it is in discontinuous conduction, and find the duty cycle that gives 12 V.

**4 [B] · Isolated converters.** (22-04)
(a) A flyback with turns ratio $n = N_1/N_2$ = 3 makes 12 V from a 36–72 V input. Find $D$ at 36, 48 and 72 V and the switch's off-state voltage at 72 V, ignoring leakage.
(b) Its leakage inductance is 1.2 µH, the peak primary current 2.5 A, the switching frequency 150 kHz, and an RCD clamp holds $V_c$ = 60 V above the input. Find the clamp interval $t_c$, the energy per cycle the clamp absorbs, the clamp loss and the peak drain voltage at 72 V. How does the clamp energy compare with the energy stored in the leakage inductance?
(c) A forward converter with a reset winding of $N_3 = 0.8N_1$ makes 3.3 V from 36–72 V. Choose $n = N_1/N_2$ so that $D$ = 0.495 at 36 V. Find $D$ at 72 V, the maximum duty cycle the reset allows and the switch's off-state voltage at 72 V.
(d) The forward converter switches at 300 kHz with $N_1$ = 15 turns on a core of $A_e$ = 50 mm². Find the flux swing in normal operation, and show that it does not depend on the input voltage. What swing does the core see if a transient drives $D$ to its maximum at 72 V, and how many times the normal swing is that? With $L_m$ = 250 µH, find the magnetizing-current ripple in normal operation.

**5 [B] · A gapped inductor.** (22-05)
A ferrite core has $A_e$ = 80 mm², $\ell_e$ = 60 mm and $\mu_r$ = 2500. It carries 30 turns and has a 0.8 mm gap.
(a) Find the core and gap reluctances, the inductance and the effective permeability.
(b) Find the saturation current for $B_{max}$ = 0.32 T, the energy stored at that current and the fraction of it stored in the gap.
(c) The ferrite's Steinmetz parameters are $k$ = 3.0, α = 1.4 and β = 2.5 ($P_v$ in W/m³ with $f$ in Hz and $B$ in T), for which the iGSE coefficient is $k_i$ = 0.1873. Find the core-loss density and the core loss ($V_e = A_e\ell_e$) for a 100 kHz sinusoid of 0.1 T peak. Then find the loss density for a triangular flux of the same peak and frequency at $D$ = 0.5 and at $D$ = 0.1, and each one's ratio to the sinusoidal loss.
(d) Find copper's skin depth at 200 kHz and 100 °C. A three-layer foil winding uses 0.12 mm foil: find Δ and the AC-resistance factor from the low-Δ approximation of Dowell's formula.

**6 [B] · Switching loss and wide bandgap.** (22-06)
A 380 V half-bridge leg (as in a totem-pole PFC stage or an inverter) hard-switches 12 A at 80 kHz. Each switch has a hot on-resistance of 40 mΩ and carries 8 A RMS.
(a) The current rise and voltage fall at turn-on take 24 ns in total, and the voltage rise and current fall at turn-off 16 ns. Find the overlap loss and the conduction loss of one switch.
(b) Each switch has $Q_{oss}$ = 70 nC and $E_{oss}$ = 9 µJ at 380 V. Find the energy and power a hard turn-on dissipates through output charge, and what an $E_{oss}$-only estimate would give. If the complementary device is a SiC MOSFET whose body diode has $Q_{rr}$ = 90 nC, find the reverse-recovery energy and loss. What is that loss for a GaN HEMT?
(c) Treat the device size as free, with conduction loss $I_{rms}^2R$ and output-charge loss $Q_{oss}Vf_s$, and $R \cdot Q_{oss}$ fixed at the values above. Find the optimal on-resistance and the minimum loss, the minimum at 160 kHz, and the loss if a 20 mΩ device is used at 80 kHz.
(d) A GaN buck converts 48 V to 12 V at 5 A and 400 kHz in triangular-current mode. Each switch has $Q_{oss}$ = 8 nC and the dead time is 8 ns. Find the negative current needed for ZVS at the high-side turn-on, the inductor ripple that provides it, the inductance, the peak and the RMS inductor current, and the factor by which the conduction loss exceeds that of a ripple-free 5 A.

**7 [B] · Closing the loop.** (22-07)
A voltage-mode buck converts 12 V to 1.2 V at 10 A ($R$ = 0.12 Ω) with $L$ = 0.5 µH and $C$ = 470 µF (negligible ESR), switching at 500 kHz with $V_M$ = 1 V and $H$ = 1.
(a) Find $f_0$, $Q = R\sqrt{C/L}$, the DC control-to-output gain in dB, and $\lvert G_{vd}\rvert$ and its phase at 40 kHz.
(b) Design a type-III compensator by the k-factor method for a 40 kHz crossover and a 55° phase margin: find the boost $B$, $k$, the zero and pole frequencies and $f_I = \omega_I/2\pi$.
(c) A peak-current-mode buck converts 12 V to 7.5 V with $L$ = 3.3 µH. Find the inductor slopes $m_1$ and $m_2$ and the perturbation ratio α without compensation. What is the smallest compensating slope $m_a$ that makes it stable? With $m_a = m_2/2$, find α and the size of a perturbation after five cycles, as a fraction of its initial value.
(d) For the converter of parts (a) and (b), estimate the output deviation for a 5 A load step. A digital controller adds 1 µs of delay: find the phase it costs at crossover and the phase margin left. What is the highest crossover frequency at which the delay costs no more than 10°?

**8 [B] · PMIC budgets.** (22-08)
(a) A 3.8 V battery feeds a 0.8 V, 100 mA rail through a 90%-efficient buck to 1.0 V and then an LDO. Find the chain's efficiency and the battery current. A buck straight to 0.8 V would be 87% efficient: find its battery current and how much more current the cascade draws.
(b) A buck converts 3.8 V to 1.0 V. Its losses are $12\ \text{mW} + 0.15I^2$ in forced PWM, and $V_{in}I_q + 0.06I + 0.5I^2$ in PFM with $I_q$ = 0.5 µA (W, A and Ω). Find the crossover current, and each mode's efficiency at 0.5 mA and at 200 mA.
(c) A tracker runs from a 150 mAh, 3.8 V cell. Each day its loads draw 20 µW for 23.5 h (through a regulator at 80%), 6 mW for 25 min (90%) and 45 mW for 5 min (88%), and the PMIC's own quiescent current is 1.5 µA from the battery. Find each term of the daily energy, the total, the average battery power and the battery life.
(d) A processor rail ramps from 0.65 V to 0.95 V in 15 µs with 47 µF on the rail: find the extra current. Adaptive voltage scaling then lowers 0.95 V to 0.88 V: find the dynamic-power saving. A power-gated domain has 5 nF, runs at 0.88 V, needs 0.3 µJ to save and restore state and leaks 2 mW: find its break-even time.

**9 [B] · A lithium-ion cell.** (22-09)
(a) Find graphite's theoretical capacity, taking one lithium per six carbon atoms (LiC₆). A cell is rated 4.2 Ah at 3.6 V nominal: find its energy and the C-rate of a 6 A load.
(b) The cell's model has $V_{OC}$ = 3.8 V, $R_0$ = 40 mΩ and one RC pair with $R_1$ = 25 mΩ and τ₁ = 50 s. Find the terminal voltage at 0⁺, 50 s and 200 s of a 3 A discharge pulse, and the largest current for a 3.0 V cutoff at the start of a pulse and in steady state (ignoring the change in SOC).
(c) The cell is charged at 0.7C to 4.2 V, with $R$ = 60 mΩ in total and an OCV of $V_{OC} = 3.7\ \text{V} + 0.5\ \text{V} \times z$ over the range of interest. Find $C_{eff}$ and the CV time constant, the SOC at which CV begins, the CC time from 20% SOC, the CV time to a C/20 termination, the total time, and the SOC and charge added in CV.
(d) A coulomb counter has a 50 µA offset. How much charge error does it accumulate in 30 days? Rest OCV readings give SOCs of 85% and 30% either side of a measured 2.1 Ah discharge: find the cell's present capacity and state of health against 4.2 Ah.

**10 [B] · Powering an AI rack.** (22-10)
(a) A 132 kW rack is fed by a busbar whose supply and return conductors each have 40 µΩ. Find the current at 54 V and at 800 V DC. At 54 V, find the loss if all the current ran the full length, and the loss with the load tapped uniformly along it; find the distributed loss at 800 V. Compare the power per conductor of 800 V DC with three-wire 480 V AC at a power factor of 0.95, at equal current per conductor.
(b) A 12-phase regulator converts 12 V to 0.75 V at 600 A, each phase switching at 800 kHz with 100 nH. Find $D$, the current per phase, one phase's ripple, the ripple of the summed current, their ratio and the summed ripple's frequency.
(c) The rail may deviate 30 mV for a 400 A load step. Find the target impedance. With a load line equal to it and $V_{ID}$ = 0.80 V, what is the voltage at 600 A? If the regulator's loop crosses over at 300 kHz, how much bulk capacitance does $\Delta V \approx \Delta I/(2\pi f_cC)$ call for?
(d) The package presents 0.8 pH to 80 µF of die capacitance. Find the resonant frequency, the characteristic impedance and the first droop for 300 A and for 400 A steps. Does the 400 A step meet the 30 mV allowance? What die capacitance would, and, by the $Z_0/2$ rule, what ESR minimizes the first droop?

**11 [B] · Machines.** (22-11)
(a) A permanent-magnet DC motor has $k$ = 0.12 V·s/rad and $R_a$ = 0.25 Ω on 48 V. Find the no-load speed (rad/s and rpm) and the stall torque. At 3 N·m, find the current, the speed and the efficiency (ignoring friction and core loss).
(b) An 8-pole, 50 Hz induction motor runs at 727.5 rpm with an air-gap power of 20 kW. Find the slip, the rotor frequency, the rotor copper loss, the mechanical power and the induced torque.
(c) A 4-pole, 60 Hz induction motor's Thevenin equivalent is 250 V per phase with $R_{th}$ = 0.3 Ω and $X_{th}$ = 0.9 Ω; its rotor has $X_2$ = 0.9 Ω and $R_2$ = 0.35 Ω. Find the slip and speed of maximum torque, the maximum torque, the starting torque and the torque at 3% slip.
(d) A Y-connected synchronous motor on 4.16 kV has $X_s$ = 8 Ω and $E_f$ = 2800 V per phase and draws 1.5 MW. Find the power angle and the pull-out power. Find the armature current, the power factor and the reactive power the motor draws. What $E_f$ would give unity power factor at this load?

**12 [B] · A transmission link.** (22-12)
(a) On a 100 MVA, 345 kV base, find the base current and impedance. A 75 MVA transformer rated 345 kV on its high side has 9% reactance on its own base; a 150 km line has 0.38 Ω/km. Find each reactance in per unit and their sum.
(b) The link connects a bus at 1.02 pu to one at 1.00 pu and carries 200 MW (resistance neglected). Find the power angle, the reactive power leaving bus 1 and arriving at bus 2, the line's reactive consumption and the largest power the link could carry.
(c) At a 345 kV bus with 1.0 pu prefault voltage, $Z_1 = Z_2$ = j0.20 pu and $Z_0$ = j0.10 pu on the bases of (a). Find the three-phase fault current in pu and kA, the fault MVA, and the single-line-to-ground fault current in pu and kA.
(d) A 60 Hz system loses 1,200 MW. Its online machines total 80 GVA with $H$ = 4.5 s. Find the stored kinetic energy and the initial RoCoF. Governors on 30 GW of capacity have 5% droop and the load damping is 1,500 MW/Hz: find the settling frequency deviation and how much of the loss the governors pick up.

**13 [C] · Derivations.** (22-01, 22-07, 22-05, 22-12)
(a) A capacitor $C$ is charged from 0 to $V$ through a resistor $R$ by a step from a source $V$. Derive the energy dissipated in $R$ and show that it does not depend on $R$. Then show that charging in $N$ equal steps dissipates $\tfrac12CV^2/N$. Evaluate the one-step and four-step losses, and the energy drawn from the supply, for a 40 nF domain charged to 0.9 V, and the power at 10,000 wake-ups per second for $N$ = 1 and 4.
(b) Starting from the boost's averaged equations, linearize about the operating point and derive $G_{vd}(s)$, showing the right-half-plane zero. Evaluate $D$, the DC gain, $f_0$, $Q$ and the zero's frequency for a 5 V to 12 V boost at 2 A with $L$ = 3.3 µH and $C$ = 47 µF.
(c) A transformer's core loss is $a\,\Delta B^\beta$ and its copper loss $b/\Delta B^2$ (fixed frequency and window; fewer turns raise the flux swing). Derive the flux swing that minimizes the total and the ratio of the two losses there. A design has 3 W of core loss and 1 W of copper loss at 0.2 T with β = 2.6: find $a$, $b$, the optimal swing, both losses and the total there.
(d) A line of impedance $R + jX$ delivers $P + jQ$ to a receiving bus at $V_r\angle0$. Derive the sending voltage, the approximation $\Delta V \approx (RP + XQ)/V_r$ and the quadrature term $\delta V = (XP - RQ)/V_r$. Evaluate both terms, the approximate and exact $\lvert\mathbf V_s\rvert$, and the corrected estimate $V_r + \Delta V + \delta V^2/(2(V_r + \Delta V))$ for $R$ = 0.02, $X$ = 0.10, $P$ = 0.8, $Q$ = 0.3 and $V_r$ = 1.0, all in per unit.

**14 [C] · Diligence: a vertical-power claim.** (22-10, 22-01)
A start-up pitches a module for a 1.5 kW AI accelerator: "Our module sits directly under the package and converts 48 V to 0.75 V at 2,000 A with 93% efficiency. It saves 150 W per accelerator against lateral power delivery and eliminates PDN droop."
(a) Find the module's input power, loss and input current. If its first stage reaches 97.5% (22-10's OCP full-load target for fixed-ratio bus converters), what must the second stage achieve? Compare with a chain of a 97.5% bus converter and the 87.0% board regulator of 22-10's Intel model: find that chain's efficiency, its input power, and the saving the claimed 93% implies.
(b) In the lateral baseline, the current crosses 25 mm of board, 50 mm wide, on six planes of 2 oz (70 µm) copper per polarity at 20 °C. Find one plane's sheet resistance, the loop resistance, the IR drop and the loss at 2,000 A. How many planes per polarity bring that loss below 150 W?
(c) The package presents 0.4 pH to 150 µF of die capacitance, and the load steps by 1,000 A. Find the first droop, as a voltage and as a percentage of 0.75 V, the resonant frequency, the target impedance for a 5% allowance, and the die capacitance that would meet it.
(d) Your findings in (a) and (b) suggest the "150 W" could be either of two different savings. Explain which applies and whether they add, and list four questions you would ask the start-up's chief architect, with what a strong answer contains.
