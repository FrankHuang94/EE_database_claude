# Course 15 · Final Exam (Control Systems)

**Time limit:** 210 minutes.
**Allowed:** a scientific calculator, and the [Course 15 equation sheet](../../../reference/equation-sheets/15-control-systems.md) printed without its chapter links. No notes, no Python, no simulator.

**Instructions.**

- Answer all 14 questions and show every step.
- Question 1 [A] is worth 8 points (2 per part), each [B] 8, and Questions 13 and 14 [C] 12 each (Question 13: 4 per part; Question 14: 3 per part): 120 points in total. 84 or more (70%) is a strong pass.
- Within a question the lettered parts carry equal weight, except Question 8 (3, 3 and 2 points).
- Give numerical answers to 3–4 significant figures, with units.
- Question 13 asks for derivations; Question 14 is a diligence question, partly graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These are the conventions of the chapters' problem sets.

- Unity negative feedback unless stated: $L = CP$, $T = L/(1 + L)$, $S = 1/(1 + L)$.
- Settling times use the 2% band; overshoot is a percentage of the final value.
- Phase margins in degrees; gain margins as ratios (and dB where asked).
- PLLs use the phase-domain model of 15-12 with the loop filter $R$ in series with $C$, and $C_2$ across both.
- Symbols are reused as in the chapters: $T$ is the complementary sensitivity, but also a time constant or sample period where the question says so; $K_v$ is the velocity error constant in Questions 4 and 9 and the VCO gain in Question 12; $N$ is the PLL divider ratio.

---

**1 [A] · Modeling.** (15-01)
A sensor die dissipates 20 W through a thermal resistance of 2.5 K/W to a 25 °C ambient; its thermal capacitance is 4 J/K.
(a) Find its final temperature.
(b) Find its time constant.
(c) Find its temperature 10 s after the power is switched on, starting from ambient.
(d) Leakage adds 0.1 W per kelvin of temperature rise. Find the loop gain $G$ of this positive feedback and the new time constant of small deviations.

**2 [B] · Loops and block diagrams.** (15-02, 15-04)
A controller $C = K$ drives a plant $P = 10/[s(s + 2)]$ in a unity-feedback loop.
(a) Find $T(s)$.
(b) For $K$ = 1, find $\omega_n$ and $\zeta$.
(c) A unit step disturbance enters at the plant's input. Find the steady-state output it causes for $K$ = 1.
(d) Find $\lvert S(j\omega)\rvert$ at $\omega$ = 1 rad/s for $K$ = 1, and say what it means.

**3 [B] · Time response.** (15-03)
For Question 2's loop with $K$ = 1:
(a) Find the percent overshoot.
(b) Find the peak time.
(c) Estimate the 2% settling time with $4/(\zeta\omega_n)$.
(d) Find the gain $K$ that gives 10% overshoot.

**4 [B] · Steady-state error and disturbances.** (15-04, 15-05)
A loop has $C = 20(s + 2)/(s + 10)$ and $P = 1/[s(s + 4)]$.
(a) Find the system type and the position, velocity and acceleration error constants.
(b) Find the steady-state errors to a unit step, a unit ramp and a unit parabola.
(c) Confirm with Routh that the closed loop is stable.
(d) A unit step disturbance enters at the plant's input. Find the steady-state output, and say what change to $C$ would reject it.

**5 [B] · Routh–Hurwitz.** (15-05)
The characteristic polynomial of a loop is $s^4 + 2s^3 + 3s^2 + 2s + K$.
(a) Build the Routh array in terms of $K$.
(b) Find the range of $K$ for stability.
(c) At the upper limit, find the frequency of oscillation.
(d) How many right-half-plane poles are there for $K$ = 3?

**6 [B] · Root locus.** (15-06)
$L = K/[s(s + 2)(s + 4)]$.
(a) Find the asymptotes' centroid and angles.
(b) Find the breakaway point and the gain there.
(c) Find the gain and frequency at which the locus crosses the imaginary axis.
(d) Find the gain that places the dominant pair at $\zeta$ = 0.5, the pair's location, and the third pole.

**7 [B] · Frequency response.** (15-07)
$L = 40/[s(s + 2)(s + 10)]$.
(a) Find the gain crossover frequency and the phase margin.
(b) Find the phase crossover frequency and the gain margin, as a ratio and in dB.
(c) Find the delay margin.
(d) The open loop is stable. How many times does the Nyquist plot of $L$ encircle −1 clockwise for the gain as given, and for a gain 8 times larger? How many closed-loop poles are in the right half-plane in each case?

**8 [B] · PID tuning.** (15-08)
A plant is $1/(s + 1)^3$.
(a) From the Bode plot (the frequency where the plant's phase is −180° and its magnitude there), find the ultimate gain $K_u$ and the ultimate period $P_u$.
(b) Find the Ziegler–Nichols PID settings $K_p = 0.6K_u$, $T_i = P_u/2$, $T_d = P_u/8$, and the corresponding $K_i$ and $K_d$.
(c) The actuator saturates during a large setpoint step. Explain integrator windup and one remedy.

**9 [B] · Lead compensation.** (15-09)
A lead compensator $C(s) = K(1 + \alpha Ts)/(1 + Ts)$, $\alpha > 1$, controls the plant $P = 4/[s(s + 2)]$. The loop $CP$ must have $K_v$ = 20 s⁻¹ and a phase margin of at least 50°.
(a) Find the gain $K$, and the crossover and phase margin of $KP$ alone (the uncompensated loop).
(b) Allowing 10° of extra lead, find the maximum phase the lead must supply and its ratio $\alpha$.
(c) Place the lead's maximum phase at the new crossover: find $\omega_m$, $T$, and the lead's zero and pole.
(d) Find the compensated phase margin.

**10 [B] · State space.** (15-10)
$A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $C = \begin{bmatrix} 1 & 0 \end{bmatrix}$.
(a) Find the eigenvalues and the transfer function.
(b) Is the system controllable? Show why.
(c) Find the state-feedback gain $K$ that places the closed-loop poles at $-4 \pm j4$, and the reference gain $N$ for zero steady-state step error.
(d) Find the observer gain $L$ that places the observer poles at −10, −10.

**11 [B] · Digital control.** (15-11)
(a) Map the pole $s = -1 + j2$ to the z-plane with $T$ = 0.1 s (magnitude and angle).
(b) Find the ZOH equivalent of $3/(s + 3)$ for $T$ = 0.1 s.
(c) Write the Tustin difference equation for a PI controller with $K_p$ = 2 and $K_i$ = 4 s⁻¹ at $T$ = 0.05 s.
(d) Estimate the phase a zero-order hold costs at a 10 rad/s crossover with $T$ = 20 ms.

**12 [B] · A PLL loop filter.** (15-12)
A PLL has a 20 MHz reference, $N$ = 40, $I_{cp}$ = 200 µA and $K_v$ = 2π × 400 MHz/V. Design the maximum-margin loop filter for a 500 kHz crossover with 50° of phase margin.
(a) Find $\sqrt b$ and $b$.
(b) Find $\tau_z$, $\tau_p$ and $K$.
(c) Find $C + C_2$, $C_2$, $C$ and $R$.
(d) Estimate the phase cost of PFD sampling, and say whether the crossover respects the usual rule.

**13 [C] · Derivations.** (15-04, 15-09, 15-11)
(a) Using the final value theorem, derive the steady-state error of a type-1 unity-feedback loop to a unit ramp, and evaluate it for Question 4's loop.
(b) Derive the maximum phase of the lead $C(s) = (1 + \alpha Ts)/(1 + Ts)$, $\alpha > 1$, and the frequency where it occurs. Evaluate both for $\alpha$ = 4 and $T$ = 0.05 s.
(c) Derive the frequency response of a zero-order hold, $H(s) = (1 - e^{-sT})/(sT)$, showing that its phase is exactly $-\omega T/2$ below the sampling frequency. Evaluate the phase and magnitude at $\omega$ = 50 rad/s with $T$ = 10 ms.

**14 [C] · Diligence: a power-management start-up.** (15-07, 15-11, 15-12)
A start-up selling a digital PMIC for phone SoCs claims: "a 1 MHz control bandwidth at a 2 MHz switching frequency", "our regulator holds a 5 A load step to within 20 mV with only 200 µF of output capacitance at a 50 kHz crossover", and "our predictive firmware lets the SoC sustain its 12 W burst indefinitely". The phone's thermal path from junction to ambient totals 12 K/W, the junction limit is 95 °C and the ambient 35 °C.
(a) With a total digital delay of 1.5 switching periods, find the phase that delay costs at 1 MHz, and the largest crossover for which it costs at most 30°.
(b) Using the transconductance model, find the droop of a load-line design and of a critically damped PI design at the stated crossover and capacitance (remember that the PI loop's crossover is $1.029\,g/C$), and the crossover each would need to meet 20 mV. Compare with (a).
(c) Find the sustained power the thermal path allows, and how many times the claimed sustained power exceeds it.
(d) List four questions you would ask the founders, and what a strong answer looks like for each.
