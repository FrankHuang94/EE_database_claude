<!-- status: verified -->
# 20-01 · Analog Design Fundamentals in Nanometer CMOS

| | |
|---|---|
| **Course** | [20 · Analog and Mixed-Signal IC Design](../README.md) |
| **University equivalent** | The transistor-level design methodology that opens a first-year graduate analog IC course: weak, moderate and strong inversion, the inversion coefficient, the $g_m/I_D$ sizing method with lookup tables, and the device figures of merit $f_T$ and intrinsic gain (Jespers & Murmann, *Systematic Design of Analog CMOS Circuits Using Pre-Computed Lookup Tables*; Enz & Vittoz, *Charge-Based MOS Transistor Modeling*; Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed., the device-physics and nanometer-design chapters) |
| **Prerequisites** | [09-09](../../09-semiconductor-devices/chapters/09-09-long-channel-mosfet.md) (square law, subthreshold current, $f_T$), [09-10](../../09-semiconductor-devices/chapters/09-10-short-channel-effects-and-leakage.md) (velocity saturation, DIBL), [10-04](../../10-electronics-1/chapters/10-04-small-signal-models.md) ($g_m$, $r_o$), [12-02](../../12-electronics-2/chapters/12-02-active-loads-cascodes-multistage.md) (intrinsic gain and cascodes), [12-03](../../12-electronics-2/chapters/12-03-frequency-response-miller-poles-zeros.md) (gain–bandwidth) |
| **Estimated study hours** | 8 |
| **Last verified** | 2026-11-24 |

**Learning objectives.** After this chapter you can:

1. Derive a MOSFET model valid from weak to strong inversion, define the inversion coefficient, and derive the transconductance efficiency $g_m/I_D$ from it.
2. Compute a transistor's $g_m/I_D$, current density, transit frequency and intrinsic gain from its inversion coefficient and channel length, and explain each trade-off.
3. Size a transistor for a target $g_m$ with the $g_m/I_D$ method: choose $g_m/I_D$ and $L$, then compute $I_D$ and $W$.
4. Explain why $(g_m/I_D) \cdot f_T$ peaks in moderate inversion for short channels, and choose an operating region for a power, speed or gain target.
5. Show why biasing by current makes a design insensitive to threshold corners, and estimate how temperature moves $g_m$ at fixed current.

## 1. Big picture

Every analog block on a chip, from the op-amp in a sensor front end to the comparator in a SerDes receiver, is built from transistors whose sizes and bias currents someone had to choose. In older processes that choice was made with the square law of 09-09: pick an overdrive voltage, read off $g_m = 2I_D/V_{ov}$, solve for $W/L$. In nanometer CMOS that recipe fails. Supplies of 0.8 to 1.2 V leave little room for overdrive, so transistors run near threshold, where the square law is wrong by a factor of two or more; short channels saturate their carriers' velocity; and the threshold voltage itself shifts with length, drain voltage and corner. The **$g_m/I_D$ method** replaces the square law with the transistor's actual curves, normalized so that one table serves every width. The designer chooses, for each transistor, a **transconductance efficiency** $g_m/I_D$ (how much $g_m$ each microampere buys) and a length; everything else follows.

- **It sets the power of every analog block.** The bias current a block needs is the $g_m$ it must deliver divided by the $g_m/I_D$ it runs at. A wearable's sensor interface runs transistors near the weak-inversion limit of about 30 S/A; a 112 Gb/s receiver runs them at 5 to 10 S/A to buy speed.
- **It exposes the three-way trade.** Efficiency ($g_m/I_D$), speed ($f_T$) and gain ($g_m r_o$) cannot all be high at once; the inversion level and the length decide which one is given up.
- **It ports across nodes.** The method's charts have the same shape in every bulk, SOI or FinFET process, so a design intent stated as "$g_m/I_D$ = 15 at $L$ = 3 $L_{min}$" survives a process migration far better than a set of widths.
- **It is how design is reviewed.** Asking a team at what $g_m/I_D$ and length its critical transistors operate is the fastest way to learn whether a block is power-optimized, speed-limited or simply over-designed.

## 2. Intuition first

Think of $g_m/I_D$ as **fuel economy** and $f_T$ as **top speed**. A transistor in weak inversion is a car cruising at low revs: superb economy (each microampere buys the most transconductance physics allows), but it is a big, slow car, because a small current per unit width means a wide device whose gate capacitance limits its speed. In strong inversion the transistor is revved hard: fast, compact, but each microampere buys little transconductance. **Moderate inversion** is the gear in between, where most nanometer analog design now lives: a good share of the economy and a good share of the speed.

The length is the second control. A long channel is like a heavy flywheel: it holds the drain current steady against drain-voltage changes (high output resistance, high intrinsic gain), but it is slow, because carriers take longer to cross and the gate capacitance grows with area. Short channels are fast but leaky in this sense: their output resistance falls, and with it the gain available from one transistor.

Where the analogy breaks: a car's economy and top speed are separate properties of one engine, but a transistor's three figures of merit are all set by just two choices, the inversion level and the length. Once those are picked, the width only scales current and capacitance together. That is why the $g_m/I_D$ method can tabulate everything per unit width and size the width last.

```mermaid
flowchart LR
  S[Specification: gain-bandwidth, load, noise, gain] --> G[Required g_m and C]
  G --> C[Choose g_m/I_D for each device: efficiency vs speed]
  C --> L[Choose L: intrinsic gain vs f_T and area]
  L --> T[Look up current density I_D/W at that g_m/I_D and L]
  T --> W[I_D = g_m / (g_m/I_D); W = I_D / (I_D/W)]
  W --> K[Check f_T margin, gain, headroom, matching]
  K -->|not met| C
```

*Figure 1. The $g_m/I_D$ design loop. The specification fixes the transconductance and capacitance; the designer chooses two dimensionless knobs per transistor, and the width falls out last.*

## 3. Theory

### 3.1 Why the square law is not enough

The square law of 09-09, $I_D = \frac{\mu C_{ox}}{2n}\frac WL V_{ov}^2$ with $V_{ov} = V_{GS} - V_{TH}$, rests on two assumptions: the channel carries only drift current, and carriers move at a velocity proportional to the field. Both fail in today's analog operating points.

- **Weak inversion.** Below threshold the current is diffusion, exponential in $V_{GS}$ (09-09 §3.7), and $g_m/I_D$ saturates at $1/(nV_T)$, about 30 S/A at room temperature. The square law's $g_m/I_D = 2/V_{ov}$ grows without bound as $V_{ov} \to 0$, which is impossible.
- **Moderate inversion.** Between the two regimes, drift and diffusion are comparable and neither formula holds. This is exactly where low-voltage analog transistors sit: with 0.9 V supplies and several transistors stacked, each gets 100 to 200 mV of headroom.
- **Velocity saturation.** In short channels at large overdrive, carriers reach $v_{sat}$ (09-10), the current becomes roughly linear in $V_{ov}$ and $g_m$ stops growing with current.

A further practical problem is that $V_{TH}$ is not a single number: it depends on length, drain voltage (DIBL) and corner, and a design stated in volts of overdrive inherits all of that uncertainty. The cure is a model that spans every regime and a design variable that does not reference $V_{TH}$ at all.

### 3.2 A model valid from weak to strong inversion

**The variables.** Let the source be at 0 V and define the **pinch-off voltage** $V_P = (V_{GS} - V_{TH})/n$, where $n$ is the slope factor of 09-09 (written $m$ there), about 1.2 to 1.4: the gate moves the channel potential by $1/n$ of its own change. At any point along the channel let $V_{ch}$ be the channel (quasi-Fermi) potential, which rises from 0 at the source to $V_{DS}$ at the drain, and let $Q_i$ be the inversion charge per unit area. Normalize the charge as

$$
q = \frac{-Q_i}{2nC_{ox}V_T},
$$

with $V_T = kT/q_e$ the thermal voltage (25.85 mV at 300 K; $q_e$ is the electron charge, written so to keep $q$ for the normalized charge).

**The charge–potential relation.** In strong inversion the charge is linear in the potential, $-Q_i = nC_{ox}(V_P - V_{ch})$, so $V_P - V_{ch} = 2V_Tq$. In weak inversion the charge is a Boltzmann exponential of the potential, $q \propto e^{(V_P - V_{ch})/V_T}$, so $V_P - V_{ch} = V_T\ln q$ plus a constant. The charge-based model of Enz and Vittoz combines the two as

$$
\frac{V_P - V_{ch}}{V_T} = 2q + \ln q ,
$$

which reduces to each limit where the other term is negligible and follows from the charge-sheet model when the surface potential is linearized in the inversion charge [1, 2]. We take it as the model's starting point.

> **Going deeper — where $2q + \ln q$ comes from.** In the charge-sheet model the inversion charge is $-Q_i = C_{ox}(V_G - V_{FB} - \psi_s) - Q_{dep}(\psi_s)$, and the electron density at the surface sets $\psi_s - V_{ch}$ through a Boltzmann factor. Expanding the depletion charge to first order around the pinch-off surface potential makes $-Q_i$ linear in $\psi_s$ with slope $nC_{ox}$, and the Boltzmann factor contributes the logarithm. The result is exact in both limits and within a few percent in between; the full EKV model adds mobility degradation, short-channel effects and the charges needed for capacitances [2].

**The current.** Current flows by drift in the field and diffusion down the charge gradient; with the channel potential defined as the quasi-Fermi potential, both are captured by $I_D = -\mu W Q_i\,dV_{ch}/dx$. Differentiating the charge–potential relation gives $dV_{ch} = -V_T(2 + 1/q)\,dq$, so

$$
I_D\,dx = \mu W(2nC_{ox}V_Tq)\,V_T\left(2 + \frac1q\right)(-dq) = -2n\mu C_{ox}WV_T^2\,(2q + 1)\,dq .
$$

Integrate from the source ($x = 0$, charge $q_s$) to the drain ($x = L$, charge $q_d$); $I_D$ is the same everywhere:

$$
I_D = 2n\mu C_{ox}\frac WL V_T^2\Big[(q_s^2 + q_s) - (q_d^2 + q_d)\Big] .
$$

> **Math refresher — changing the variable of integration.** The current is constant along the channel, but the charge and potential vary in a way we do not know as functions of $x$. Writing $dx$ in terms of $dq$ moves the integral to a variable whose limits we do know (the charges at the two ends), exactly as 09-09 did for the gate charge. The same trick underlies 19-02's step-delay integral.

In saturation the drain end is nearly empty, $q_d \to 0$, and

$$
I_D = I_{spec}\,(q^2 + q), \qquad I_{spec} = 2n\mu C_{ox}\frac WL V_T^2 ,
$$

where $q$ now means the source charge. $I_{spec}$, the **specific current**, is a property of the device size and the process: for the illustrative 130 nm-class process used in this chapter ("T130": μ = 350 cm²/V·s, $C_{ox}$ = 8.6 fF/µm², $n$ = 1.3, $V_{TH}$ = 0.45 V, $v_{sat}$ = 8 × 10⁶ cm/s), a square device ($W = L$) has $I_{spec,\square}$ = **0.523** µA.

**The inversion coefficient.** The ratio

$$
IC = \frac{I_D}{I_{spec}} = q^2 + q
$$

measures how strongly the channel is inverted, using only the current and the size. By convention $IC < 0.1$ is **weak inversion**, $0.1 < IC < 10$ **moderate inversion** and $IC > 10$ **strong inversion**, with $IC = 1$ the geometric center of moderate inversion. The $q^2$ term of the current is drift and the $q$ term diffusion; they are equal at $q = 1$, that is $IC = 2$. Solving the quadratic, $q = (\sqrt{1 + 4IC} - 1)/2$.

**Limits.** In strong inversion $q \gg 1$, $V_P \approx 2V_Tq$, and $I_D \approx I_{spec}q^2 = I_{spec}V_P^2/(4V_T^2) = \frac{\mu C_{ox}}{2n}\frac WL V_{ov}^2$: the square law of 09-09. In weak inversion $q \ll 1$, $q \approx e^{V_P/V_T}$, and $I_D \approx I_{spec}e^{(V_{GS} - V_{TH})/(nV_T)}$: the exponential of 09-09 §3.7. The model is one formula for both.

**Overdrive as a function of $IC$.** From the charge–potential relation at the source,

$$
V_{ov} = V_{GS} - V_{TH} = nV_T\,(2q + \ln q) .
$$

At $IC = 1$, $q = 0.618$ and $V_{ov} = nV_T(1.236 - 0.481)$ = **0.755** $nV_T$, about **25** mV for T130; at $IC = 0.1$ it is **−74** mV. Weak inversion means a *negative* overdrive: the gate sits below threshold, a fact the square law cannot express.

### 3.3 Transconductance efficiency

In saturation $g_m = \partial I_D/\partial V_{GS}$. With $dV_P = dV_{GS}/n$ and, from the charge–potential relation at the source, $dq/dV_P = q/[V_T(2q + 1)]$,

$$
g_m = I_{spec}(2q + 1)\frac{dq}{dV_{GS}} = I_{spec}(2q + 1)\frac{q}{nV_T(2q + 1)} = \frac{I_{spec}\,q}{nV_T} .
$$

Dividing by $I_D = I_{spec}(q^2 + q)$,

$$
\boxed{\frac{g_m}{I_D} = \frac{1}{nV_T\,(1 + q)} = \frac{1}{nV_T}\cdot\frac{2}{1 + \sqrt{1 + 4IC}}} .
$$

This one expression is the heart of the method.

- **Weak inversion** ($IC \to 0$): $g_m/I_D \to 1/(nV_T)$, **29.8** S/A for $n$ = 1.3 at 300 K. No MOSFET does better; a bipolar transistor's $1/V_T$ = **38.7** S/A is the same physics without the gate's capacitive divider.
- **Strong inversion** ($IC \gg 1$): $g_m/I_D \to 1/(nV_T\sqrt{IC})$. Since $V_{ov} \approx 2nV_T\sqrt{IC}$ there, this is $2/V_{ov}$, the square law's answer.
- **The center of moderate inversion** ($IC = 1$): $g_m/I_D = 0.618/(nV_T)$, **62** % of the maximum.

![Log-log plot of g_m/I_D against the inversion coefficient from 0.001 to 1000, with the weak, moderate and strong regions shaded: the charge-based model is flat at the weak-inversion limit 1/(nV_T) and falls in strong inversion; with velocity saturation at 0.15 µm it falls faster at high inversion; the square law's 2/V_ov rises without bound as the overdrive approaches zero, crossing above the limit in moderate inversion](../../../assets/figures/20-01/gmid-vs-ic.svg)

*Figure 2. Transconductance efficiency against inversion coefficient for T130. The model saturates at $1/(nV_T)$ in weak inversion and approaches the square law in strong inversion; between them the square law is not just inaccurate but impossible, exceeding the physical limit. Velocity saturation (0.15 µm) matters only in strong inversion.*

Notice what is absent. The expression contains no $W$ and no $V_{TH}$: $g_m/I_D$ is a function of the inversion level only. Because $IC = I_D/I_{spec}$ and $I_{spec} \propto W/L$, choosing $g_m/I_D$ fixes the **current density** $I_D/W$ at a given length,

$$
\frac{I_D}{W} = \frac{I_{spec,\square}}{L}\,IC ,
$$

and any width then gives a transistor with the same $g_m/I_D$, $f_T$ and gain. That is why a single lookup table, computed per unit width, sizes every transistor of that length.

### 3.4 Short channels: velocity saturation

At large inversion in a short channel, carriers near the drain reach their saturation velocity and the current becomes $I_D \approx WC_{ox}v_{sat}V_{ov}$ (09-10). A simple way to add this to the model, which this chapter adopts, is to divide the long-channel current by $1 + \lambda_cq$:

$$
I_D = I_{spec}\,\frac{q^2 + q}{1 + \lambda_cq}, \qquad \lambda_c = \frac{L_{sat}}{L}, \qquad L_{sat} = \frac{\mu V_T}{v_{sat}} .
$$

Check the limit: for large $q$, $I_D \to I_{spec}\,q/\lambda_c = 2n\mu C_{ox}\frac WL V_T^2 q\cdot\frac{Lv_{sat}}{\mu V_T} = 2nC_{ox}WV_Tv_{sat}\,q$, and with $q \approx V_{ov}/(2nV_T)$ this is $WC_{ox}v_{sat}V_{ov}$, as required. For T130, $L_{sat}$ = **11.3** nm, so $\lambda_c$ is **0.075** at $L$ = 0.15 µm and **0.023** at 0.5 µm. The full EKV model uses a similar parameter with a smoother form [2]; this one keeps the algebra short.

The inversion coefficient is now $IC = (q^2 + q)/(1 + \lambda_cq)$, and differentiating as in §3.3 (with $dI_D/dq$ from the quotient rule) gives

$$
\frac{g_m}{I_D} = \frac{1}{nV_T}\cdot\frac{\lambda_cq^2 + 2q + 1}{(2q + 1)(1 + \lambda_cq)(1 + q)} ,
$$

which reduces to $1/[nV_T(1 + q)]$ when $\lambda_c = 0$ (Problem 20-01.12). In deep strong inversion it tends to $1/(2nV_Tq)$, falling as $1/IC$ instead of $1/\sqrt{IC}$: once velocity saturates, extra current no longer buys extra $g_m$. In weak and moderate inversion the correction is small, which is one more reason analog designers stay there.

### 3.5 Speed: the transit frequency

The **transit frequency** $f_T$ is the frequency at which a transistor's small-signal current gain, $g_m/(2\pi fC_{gg})$, falls to one (09-09, 12-03); $C_{gg}$ is the total gate capacitance. It is the transistor's intrinsic speed limit: a stage driving a capacitive load cannot have useful gain much beyond a fraction of $f_T$, and designers keep $f_T$ at least 5 to 10 times above the frequencies a circuit must handle.

Take $C_{gg} \approx \tfrac23WLC_{ox}$, the strong-inversion value of 09-09 (an assumption: in weak inversion $C_{gg}$ is smaller, so this underestimates $f_T$ there). Write $g_m = I_{spec}\Delta/(nV_T)$, where $\Delta = d(IC)/d(V_P/V_T)$ is the normalized transconductance: $\Delta = q$ without velocity saturation, as §3.3 showed, and with it the quotient-rule result below. Then

$$
f_T = \frac{g_m}{2\pi C_{gg}} = \frac{2n\mu C_{ox}\frac WL V_T^2\cdot\frac{\Delta}{nV_T}}{2\pi\cdot\frac23WLC_{ox}} = \frac{3\mu V_T}{2\pi L^2}\,\Delta ,
\qquad \Delta = \frac{q\,(\lambda_cq^2 + 2q + 1)}{(2q + 1)(1 + \lambda_cq)^2} ,
$$

- **Long channel, strong inversion:** $\Delta = q \approx V_{ov}/(2nV_T)$ gives $f_T = 3\mu V_{ov}/(4\pi nL^2)$, exactly 09-09's result.
- **Weak inversion:** $\Delta \approx q \approx IC$, so $f_T$ is proportional to the current density: halving $IC$ halves $f_T$.
- **Velocity saturation:** $\Delta \to 1/(2\lambda_c)$, and $f_T \to 3v_{sat}/(4\pi L)$: **127** GHz for T130 at $L$ = 0.15 µm. The speed limit now falls only as $1/L$, not $1/L^2$.

Real transistors fall short of this limit because overlap and fringing capacitances add to $C_{gg}$, and mobility degrades at high field; foundry models capture both. The shape survives: $f_T$ rises steeply with $IC$ through weak and moderate inversion and flattens in strong inversion.

### 3.6 Gain: the intrinsic gain

A transistor's output conductance $g_{ds} = 1/r_o$ comes from channel-length modulation and, in short channels, drain-induced barrier lowering (09-10). Write $g_{ds} = I_D/V_A$ with an Early voltage $V_A$ that, to first order, grows in proportion to length, $V_A = V_A'L$. The **intrinsic gain**, the most voltage gain one transistor with an ideal current-source load can give (12-02), is then

$$
A_i = g_mr_o = \frac{g_m}{I_D}\,V_A = \frac{g_m}{I_D}\,V_A'L .
$$

Two levers raise it: run at higher $g_m/I_D$ (weaker inversion) or use a longer channel. Both cost speed, since $f_T$ falls with $1/L^2$ (or $1/L$ when velocity-saturated) and with falling $IC$. For T130 we take $V_A'$ = 8 V/µm (an illustrative value: it varies by process, by length and with $V_{DS}$, and in FinFET processes it is lower). At $g_m/I_D$ = 15 S/A that gives $A_i$ = 18 at 0.15 µm and 120 at 1 µm. Many modern processes cannot reach 40 dB in one transistor at minimum length, which is why cascodes (12-02) and gain-boosting are everywhere in nanometer analog design (20-02, 20-12).

### 3.7 Area, capacitance and the cost of efficiency

At fixed $g_m$, choosing a higher $g_m/I_D$ reduces the current $I_D = g_m/(g_m/I_D)$, but lowers $IC$ even faster. The width follows from the current density, $W = I_DL/(I_{spec,\square}\,IC)$, so the gate area is

$$
WL = \frac{I_D L^2}{I_{spec,\square}\,IC} .
$$

In weak inversion $IC$ is small and the transistor is wide. The extra area is not all bad: matching improves with area (Pelgrom's law, 20-11), and flicker noise falls with it. But the gate capacitance grows with area too, which loads whatever drives the transistor and is the physical reason $f_T$ falls. A transistor that is 10 times wider for 20% more $g_m$ per microampere is rarely a good trade except where power is everything.

### 3.8 The sweet spot: $(g_m/I_D) \cdot f_T$

A circuit designer who cares both about power and about speed wants a high product of efficiency and speed. Using §3.3 and §3.5 for a long channel ($\lambda_c = 0$),

$$
\frac{g_m}{I_D}\,f_T = \frac{1}{nV_T(1 + q)}\cdot\frac{3\mu V_Tq}{2\pi L^2} = \frac{3\mu}{2\pi nL^2}\cdot\frac{q}{1 + q} ,
$$

which rises monotonically toward $3\mu/(2\pi nL^2)$: without velocity saturation, more current always helps the product a little. With velocity saturation, $f_T$ flattens while $g_m/I_D$ keeps falling, and the product has a maximum. For T130 at $L$ = 0.15 µm the maximum is at $IC$ ≈ **6.9**, $g_m/I_D$ ≈ **8.0** S/A: moderate inversion, close to its upper edge. At longer lengths velocity saturation weakens, and the peak moves into strong inversion and flattens. This is the quantitative basis for the rule of thumb that broadband nanometer circuits run near $g_m/I_D$ ≈ 10 S/A, while circuits that care only about power push toward 20 to 25 S/A.

![Log-log plot of the product of g_m/I_D and f_T against inversion coefficient for three channel lengths; each curve rises through weak inversion, peaks (marked with a dot) and falls in strong inversion; the peak is highest and furthest left for the 0.15 µm channel and moves right and down for 0.5 µm and 1 µm](../../../assets/figures/20-01/sweet-spot.svg)

*Figure 4. The efficiency–speed product for T130. Velocity saturation creates a peak; it sits in moderate inversion for short channels and moves into strong inversion as the channel lengthens.*

### 3.9 The sizing procedure

In practice the curves come not from a closed-form model but from SPICE simulations of one transistor per length with the foundry's models, swept in $V_{GS}$ at a representative $V_{DS}$ and tabulated per unit width [3]. The procedure for one transistor is:

1. **From the specification, find the transconductance it must have.** For a stage whose bandwidth is set by its load, $g_m = 2\pi\,\text{GBW}\,C_L$ (12-03); for a noise-limited stage, $g_m$ follows from the allowed thermal-noise density (12-10).
2. **Choose $g_m/I_D$:** high (20–25 S/A) for low power and low offset, low (5–10 S/A) for speed or large signal swing, often 10–18 S/A as a balance.
3. **Choose $L$** for intrinsic gain (and matching), checking that $f_T$ stays well above the signal frequencies.
4. **Compute the current** $I_D = g_m/(g_m/I_D)$.
5. **Look up the current density** $I_D/W$ at that $g_m/I_D$ and $L$, and compute $W = I_D/(I_D/W)$.
6. **Check** the resulting capacitance against the load, $f_T$ against the bandwidth, $V_{DS,sat}$ (about 4–5 $V_T$ in weak inversion, about $V_{ov}$ in strong) against the headroom, and iterate.

Every step but the last is algebra on the tables, which is why the method is easy to automate and to review.

![Three panels against g_m/I_D from 3 to 28 S/A for channel lengths 0.15, 0.5 and 1 µm: current density falls by orders of magnitude from left to right, f_T falls similarly and is highest for the shortest channel, and intrinsic gain rises in straight lines whose slope is proportional to the length](../../../assets/figures/20-01/design-chart.svg)

*Figure 3. The $g_m/I_D$ design chart for T130. Read a column at the chosen $g_m/I_D$: the left panel gives the current density that sizes $W$, the middle the speed, the right the gain. Longer channels trade speed and current density for gain.*

### 3.10 Corners and temperature

**Threshold corners.** Suppose the threshold shifts by $\Delta V_{TH}$ (a process corner, or a different length). If a transistor is biased by a fixed *gate voltage*, its current changes: by a factor $e^{-\Delta V_{TH}/(nV_T)}$ in weak inversion and roughly $(1 - \Delta V_{TH}/V_{ov})^2$ in strong inversion. If it is biased by a fixed *current*, as analog circuits almost always are (current mirrors, 10-08), then $IC = I_D/I_{spec}$ does not involve $V_{TH}$ at all, and neither do $g_m/I_D$, $g_m$ or $f_T$ in this model. The gate voltage moves to absorb the shift. This is the deepest reason to design with currents and current densities rather than overdrive voltages: the quantities that set gain and bandwidth inherit the process's tight mobility and capacitance tolerances, not its loose threshold tolerance.

**Temperature.** At fixed current, temperature still matters, through $V_T \propto T$ and through mobility, which falls roughly as $T^{-3/2}$ (09-03). Then $I_{spec} \propto \mu V_T^2 \propto T^{1/2}$, so $IC \propto T^{-1/2}$ falls slowly as the chip heats, while the $1/(nV_T)$ prefactor of $g_m/I_D$ falls as $1/T$. In weak inversion $g_m$ at fixed current therefore drops in proportion to $1/T$; in strong inversion, as $\sqrt{\mu} \propto T^{-3/4}$. Either way a bias current that is constant over temperature gives a transconductance, and hence a bandwidth, that falls as the chip heats. Bias circuits that make $g_m$ (rather than $I_D$) constant over temperature fix this, and are a standard building block (20-03).

## 4. Worked examples

All examples use the T130 process of §3.2 (μ = 350 cm²/V·s, $C_{ox}$ = 8.6 fF/µm², $n$ = 1.3, $V_{TH}$ = 0.45 V, $v_{sat}$ = 8 × 10⁶ cm/s, $V_A'$ = 8 V/µm) at 300 K ($V_T$ = 25.85 mV) unless stated, with velocity saturation included through $\lambda_c$.

### Example 20-01.1 · Where is this transistor operating? (tier A)

**Setup.** An NMOS with $W/L$ = 10 µm/0.5 µm carries $I_D$ = 20 µA in saturation. Find its specific current, inversion coefficient and region, $g_m/I_D$ (without and with velocity saturation), $g_m$ and overdrive. What would the square law predict for $g_m/I_D$ at that overdrive?

**Solution.** $I_{spec} = 2 \times 1.3 \times 350 \times 10^{-4} \times 8.6 \times 10^{-3} \times 20 \times (0.02585)^2$ A = **10.46** µA. $IC = 20/10.46$ = **1.912**: moderate inversion. Without velocity saturation, $q = (\sqrt{1 + 4 \times 1.912} - 1)/2 = 0.970$ and $g_m/I_D = 1/(1.3 \times 0.02585 \times 1.970)$ = **15.10** S/A. With $\lambda_c$ = 0.0226 the model gives **14.77** S/A, so $g_m = 14.77 \times 20$ µA = **295.5** µS, and the overdrive $nV_T(2q + \ln q)$ is **65.7** mV. The square law at 65.7 mV would claim $2/V_{ov}$ = **30.5** S/A, more than the weak-inversion limit of 29.8 S/A: the square law is not merely inaccurate here but physically impossible.

**Units check.** (m²/V·s)(F/m²)(V²) = (m²/V·s)(C/V·m²)(V²) = C/s = A.

**Sanity check.** At $IC \approx 2$, where drift and diffusion are equal, $g_m/I_D$ should be about half the weak-inversion maximum: 15.1/29.8 = **0.51**.

### Example 20-01.2 · Sizing an input pair for gain–bandwidth (tier B)

**Setup.** A single-stage OTA must reach a gain–bandwidth of 100 MHz driving 2 pF. Size one input transistor at $g_m/I_D$ = 15 S/A and $L$ = 0.5 µm. Check its gate capacitance and $f_T$, and compare with a square-law design at the same $g_m/I_D$.

**Solution.** $g_m = 2\pi \times 100\ \text{MHz} \times 2\ \text{pF}$ = **1257** µS. $I_D = 1257/15$ = **83.8** µA. At $L$ = 0.5 µm, $g_m/I_D$ = 15 S/A needs $IC$ = **1.829**, a current density of **1.913** A/m (µA/µm), so $W = 83.8/1.913$ = **43.8** µm. Its gate capacitance $\tfrac23WLC_{ox}$ is **125.5** fF, **6.3** % of the load, and $f_T$ = **1.59** GHz, **16** times the GBW. A square-law design would set $V_{ov} = 2/15$ = 133 mV and solve $I_D = \frac{\mu C_{ox}}{2n}\frac WLV_{ov}^2$ for $W$ = **20.4** µm: less than half the needed width, giving a transistor in stronger inversion with too little $g_m$ for its current.

**Units check.** (Hz)(F) = S; A/(A/m) = m.

**Sanity check.** The intrinsic gain at this point is $15 \times 8 \times 0.5$ = **60**, ample for a single-stage OTA with a cascoded load.

### Example 20-01.3 · Choosing the length for gain (tier B)

**Setup.** A stage needs an intrinsic gain of at least 50 per transistor at $g_m/I_D$ = 15 S/A. Find the minimum length, and the $f_T$ and current density there. Compare with $L$ = 0.15 µm and 1 µm.

**Solution.** $A_i = (g_m/I_D)V_A'L$ gives $L = 50/(15 \times 8\ \text{V/µm})$ = **0.417** µm. There $f_T$ = **2.27** GHz and $I_D/W$ = **2.27** µA/µm. At 0.15 µm the gain is only **18** but $f_T$ = **15.5** GHz; at 1 µm the gain is **120** and $f_T$ = **0.41** GHz.

**Units check.** (A/V/A)(V/µm)(µm) is dimensionless.

**Sanity check.** Between 0.15 µm and 1 µm, $f_T$ falls **38**-fold, less than the **44**-fold of the long-channel $1/L^2$ law: at 0.15 µm velocity saturation already holds $f_T$ below its long-channel value.

### Example 20-01.4 · The efficiency–speed sweet spot (tier C)

**Setup.** For $L$ = 0.15 µm, tabulate $f_T$ and the product $(g_m/I_D) f_T$ at $g_m/I_D$ = 25, 15, 10 and 5 S/A, and find where the product peaks.

**Solution.** From the model:

| $g_m/I_D$ (S/A) | $IC$ | $f_T$ (GHz) | $(g_m/I_D)f_T$ (GHz/V) |
|---|---|---|---|
| 25 | **0.205** | **3.31** | **82.7** |
| 15 | **1.60** | **15.5** | **232** |
| 10 | **4.30** | **27.7** | **277** |
| 5 | **16.4** | **52.8** | **264** |

Maximizing numerically, the product peaks at $IC$ = **6.86**, $g_m/I_D$ = **8.00** S/A and $f_T$ = **35.4** GHz, with a product of **283** GHz/V.

**Units check.** (A/V/A)(1/s) = 1/(V·s).

**Sanity check.** The peak is flat: from 10 to 5 S/A the product changes by less than 5% while $f_T$ rises **1.9** times, which is why designers can move along this flat top to trade a little efficiency for a lot of speed.

### Example 20-01.5 · Corners and temperature (tier B)

**Setup.** The transistor of Example 1 is biased at its 20 µA operating point. (a) If its gate voltage (0.516 V) were held fixed instead, what current would flow if the threshold rose or fell by 50 mV? (b) With the current fixed at 20 µA, how does $g_m$ change between −40 °C and 100 °C, taking μ ∝ $T^{-3/2}$ and ignoring the threshold's own temperature coefficient (which current bias cancels)?

**Solution.** (a) With $V_{TH}$ = 0.50 V the current falls to **8.61** µA (×0.430); with 0.40 V it rises to **38.5** µA (×1.92). A 50 mV corner, routine in practice, more than doubles or halves the current, and $g_m$ with it. (b) At fixed current: at −40 °C (233.15 K) $IC$ = **2.17**, $g_m/I_D$ = **18.13** S/A and $g_m$ = **362.6** µS; at 100 °C (373.15 K) $IC$ = **1.71**, $g_m/I_D$ = **12.35** S/A and $g_m$ = **247.0** µS, against 295.5 µS at 27 °C. Current bias removes the threshold sensitivity of (a), but $g_m$ still falls by **32** % from −40 °C to 100 °C.

**Units check.** A/(A/V) = V; S = A/V.

**Sanity check.** In moderate inversion the temperature effect lies between the weak-inversion $1/T$ law (a **38** % fall from 233 K to 373 K) and the strong-inversion $T^{-3/4}$ law (a **30** % fall); 32% sits between them.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 20-01.1a | specific current | 10.46 | µA |
| Ex 20-01.1b | inversion coefficient | 1.912 | — |
| Ex 20-01.1c | g_m/I_D without velocity saturation | 15.10 | S/A |
| Ex 20-01.1d | g_m/I_D with velocity saturation | 14.77 | S/A |
| Ex 20-01.1e | g_m | 295.5 | µS |
| Ex 20-01.1f | overdrive | 65.7 | mV |
| Ex 20-01.1g | square-law g_m/I_D at that overdrive | 30.5 | S/A |
| Ex 20-01.2a | required g_m | 1257 | µS |
| Ex 20-01.2b | drain current | 83.8 | µA |
| Ex 20-01.2c | inversion coefficient | 1.829 | — |
| Ex 20-01.2d | current density | 1.913 | µA/µm |
| Ex 20-01.2e | width | 43.8 | µm |
| Ex 20-01.2f | gate capacitance | 125.5 | fF |
| Ex 20-01.2g | f_T | 1.59 | GHz |
| Ex 20-01.2h | square-law width | 20.4 | µm |
| Ex 20-01.2i | intrinsic gain | 60 | — |
| Ex 20-01.3a | minimum length | 0.417 | µm |
| Ex 20-01.3b | f_T at that length | 2.27 | GHz |
| Ex 20-01.3c | current density at that length | 2.27 | µA/µm |
| Ex 20-01.3d | intrinsic gain at 0.15 um | 18 | — |
| Ex 20-01.3e | f_T at 0.15 um | 15.5 | GHz |
| Ex 20-01.3f | intrinsic gain at 1 um | 120 | — |
| Ex 20-01.3g | f_T at 1 um | 0.41 | GHz |
| Ex 20-01.4a | IC at 25 S/A | 0.205 | — |
| Ex 20-01.4b | f_T at 25 S/A | 3.31 | GHz |
| Ex 20-01.4c | product at 25 S/A | 82.7 | GHz/V |
| Ex 20-01.4d | IC at 15 S/A | 1.60 | — |
| Ex 20-01.4e | product at 15 S/A | 232 | GHz/V |
| Ex 20-01.4f | IC at 10 S/A | 4.30 | — |
| Ex 20-01.4g | f_T at 10 S/A | 27.7 | GHz |
| Ex 20-01.4h | product at 10 S/A | 277 | GHz/V |
| Ex 20-01.4i | IC at 5 S/A | 16.4 | — |
| Ex 20-01.4j | f_T at 5 S/A | 52.8 | GHz |
| Ex 20-01.4k | product at 5 S/A | 264 | GHz/V |
| Ex 20-01.4l | IC at the peak | 6.86 | — |
| Ex 20-01.4m | g_m/I_D at the peak | 8.00 | S/A |
| Ex 20-01.4n | f_T at the peak | 35.4 | GHz |
| Ex 20-01.4o | peak product | 283 | GHz/V |
| Ex 20-01.5a | current, threshold up 50 mV | 8.61 | µA |
| Ex 20-01.5b | current, threshold down 50 mV | 38.5 | µA |
| Ex 20-01.5c | IC at -40 C | 2.17 | — |
| Ex 20-01.5d | g_m/I_D at -40 C | 18.13 | S/A |
| Ex 20-01.5e | g_m at -40 C | 362.6 | µS |
| Ex 20-01.5f | IC at 100 C | 1.71 | — |
| Ex 20-01.5g | g_m/I_D at 100 C | 12.35 | S/A |
| Ex 20-01.5h | g_m at 100 C | 247.0 | µS |
| Ex 20-01.5i | fall of g_m from -40 C to 100 C | 32 | % |
| Txt 20-01.a | specific current of a square T130 device | 0.523 | µA |
| Txt 20-01.b | weak-inversion g_m/I_D limit, n = 1.3, 300 K | 29.8 | S/A |
| Txt 20-01.c | lambda_c at 0.15 um | 0.075 | — |
| Txt 20-01.d | velocity-saturated f_T limit at 0.15 um | 127 | GHz |
| Txt 20-01.e | IC at the T130 sweet spot, 0.15 um | 6.9 | — |
| Txt 20-01.f | g_m/I_D at the sweet spot | 8.0 | S/A |
| Txt 20-01.g | overdrive at IC = 1 in units of nV_T | 0.755 | — |
| Txt 20-01.h | overdrive at IC = 1 | 25 | mV |
| Txt 20-01.i | overdrive at IC = 0.1 | -74 | mV |
| Txt 20-01.j | bipolar g_m/I_C at 300 K | 38.7 | S/A |
| Txt 20-01.k | g_m/I_D at IC = 1 as a share of the maximum | 62 | % |
| Txt 20-01.l | L_sat | 11.3 | nm |
| Txt 20-01.m | lambda_c at 0.5 um | 0.023 | — |
| Txt 20-01.n | weak-inversion limit, n = 1.4 | 28 | S/A |
| Txt 20-01.o | weak-inversion limit, n = 1.2 | 32 | S/A |
| Txt 20-01.p | 4 V_T at 300 K | 103 | mV |
| Txt 20-01.q | SKY130 nfet_01v8 C_ox from t_ox = 4.148 nm | 8.3 | fF/µm² |
| Ex 20-01.1h | ratio to the weak-inversion maximum | 0.51 | — |
| Ex 20-01.2j | gate capacitance as a share of the load | 6.3 | % |
| Ex 20-01.2k | f_T over GBW | 16 | — |
| Ex 20-01.3h | f_T ratio from 0.15 um to 1 um | 38 | — |
| Ex 20-01.3i | long-channel 1/L^2 ratio | 44 | — |
| Ex 20-01.4p | f_T ratio from 10 to 5 S/A | 1.9 | — |
| Ex 20-01.5j | weak-inversion fall, 233 K to 373 K | 38 | % |
| Ex 20-01.5k | strong-inversion fall, 233 K to 373 K | 30 | % |

## 5. Simulate it

The lab ([labs/20-01-lab](../labs/20-01-lab/README.md)) implements the chapter's model for the T130 process in `gmid.py` and uses it as a stand-in for the foundry lookup tables a designer would generate with SPICE; an ngspice netlist checks the intrinsic-gain relation on a level-1 transistor.

**Predict, then run.**

1. Predict $g_m/I_D$ at $IC$ = 0.01, 1 and 100, and the overdrive below which the square law's $2/V_{ov}$ exceeds the weak-inversion limit; then plot all three curves of Figure 2 (Part 1).
2. Predict which of the design chart's curves move with $L$ and which do not; then build the chart and re-size Example 20-01.2 from a lookup table by interpolation (Part 2).
3. Predict whether the peak of $(g_m/I_D) f_T$ moves to weaker or stronger inversion as $L$ grows, and find it for three lengths (Part 3).
4. Predict the current change for a ±50 mV threshold shift with the gate voltage fixed, and the $g_m$ change from −40 °C to 125 °C with the current fixed (Part 4).
5. Predict the gain of `gain.cir` from $g_m/I_D$ and $V_A$, then run `ngspice -b gain.cir` (Part 5).

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Higher $g_m/I_D$ (weaker inversion) | Current for a given $g_m$; intrinsic gain; matching per unit of $g_m$ | $f_T$, area, gate capacitance; slower slewing per unit current | Analog block designer |
| Lower $g_m/I_D$ (stronger inversion) | $f_T$, compactness, drain-current matching of mirrors | Current and power; headroom ($V_{DS,sat}$ grows) | Analog block designer |
| Longer channel | Intrinsic gain, matching, flicker noise | $f_T$ (as $1/L^2$ until velocity saturation), area, capacitance | Analog block designer |
| Minimum length | $f_T$, area | Gain, matching, output resistance; more DIBL and variability | Designer, constrained by process |
| Bias by current, not voltage | Insensitivity of $g_m$ and $f_T$ to $V_{TH}$ corners | A reference current and mirrors; their own errors | Bias-circuit designer (20-03) |
| Constant-$g_m$ bias | $g_m$ and bandwidth stable over temperature | Current rises with temperature; bias-circuit complexity | Bias-circuit designer |
| Lookup tables from foundry models | Accuracy at every inversion level and length | Table generation and upkeep per process and corner | CAD and design-methodology team |

## 7. Numbers to know

| Quantity | Typical value | Note |
|---|---|---|
| Weak-inversion limit of $g_m/I_D$ | $1/(nV_T)$: **28** to **32** S/A at 300 K for $n$ = 1.4 to 1.2 | Physics; falls as $1/T$ |
| Bipolar $g_m/I_C$ | 38.7 S/A at 300 K | The MOSFET's ceiling without the $1/n$ divider |
| $g_m/I_D$ at $IC$ = 1 | 62% of the limit | Center of moderate inversion |
| Working range of $g_m/I_D$ | about 5 to 25 S/A | Low for speed, high for power |
| Square-law error | "20–60%" in strong inversion; "a factor of two or even more" in moderate inversion | Jespers and Murmann [3] |
| $V_{DS,sat}$ | about $4V_T$ ≈ **103** mV in weak inversion; about $V_{ov}$ in strong | Current within 2% of saturation at $4V_T$ |
| Velocity-saturated $f_T$ limit | $3v_{sat}/(4\pi L)$: 127 GHz at 0.15 µm (T130 model) | Real devices lower: overlap and wiring capacitance |
| Measured peak NMOS $f_T$, 32 nm to 12 nm | 300 to 450 GHz | Peak current density, RF layout; as of Nov 2026 [R-322] |
| IRDS intrinsic delay $CV/I$ | 1.061 ps (2024) to 0.624 ps (2039) | NMOS, FO3 load [R-314] |
| FinFET self-gain $g_m/g_{ds}$ | 40 (N) and 34 (P) in a 14 nm FinFET process | Single company; bias not stated [R-322] |
| SKY130 thin-oxide NMOS | $L_{min}$ = 0.15 µm, $t_{ox}$ = 4.148 nm ($C_{ox}$ ≈ **8.3** fF/µm²), BSIM4 4.5 models | Open PDK [R-322]; close to T130's 8.6 fF/µm² |

## 8. Common mistakes

- **Designing with the square law in moderate inversion.** At 100–200 mV of overdrive the square law overstates $g_m/I_D$ and undersizes transistors by a factor of two (Example 20-01.2).
- **Treating overdrive as the design variable.** $V_{ov}$ references a threshold that moves with corner, length and $V_{DS}$; $g_m/I_D$ and current density do not.
- **Biasing transistors with fixed gate voltages.** A 50 mV threshold corner then halves or doubles the current (Example 20-01.5). Bias with currents and mirrors.
- **Chasing the weak-inversion limit everywhere.** Above about 20 S/A each extra S/A costs a large factor in area and $f_T$ for little saving in current.
- **Using minimum length for analog by default.** Minimum length maximizes $f_T$ but minimizes intrinsic gain and matching; analog transistors that need gain or matching usually run at several times minimum length, chosen from the design chart rather than by habit.
- **Forgetting that $f_T$ is an upper bound.** Overlap, wiring and load capacitances mean a circuit's useful bandwidth is a fraction of $f_T$; keep a margin of 5 to 10.
- **Ignoring temperature.** At fixed current, $g_m$ falls by roughly a third from −40 °C to 100 °C in moderate inversion (Example 20-01.5).

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **A thirty-year-old method, now the default [Established].** Silveira, Flandre and Jespers proposed basing synthesis on "the relation between the ratio of the transconductance over dc drain current gm/ID and the normalized current ID/(W/L)", noting that gm/ID "is a universal characteristic of all the transistors belonging to a same process" [4]. Jespers and Murmann's 2017 book made pre-computed lookup tables the standard route and calls moderate inversion "a design 'sweet spot'" in nanometer technologies [3, R-322].
- **Open tools make it reproducible [Established].** Murmann's companion repository (AGPL-3.0, last updated Oct 2025) provides lookup-table sweeps for the open SKY130, IHP SG13G2 and GF180MCU processes; pygmid (Apache-2.0, last commit Jan 2026) reads such tables in Python; and Mosplot (Apache-2.0, active Sep 2026) "sizes complete circuits automatically across process corners". The open PDKs ship BSIM4 4.5 models for SKY130 and GF180MCU. The tables' author warns that SKY130's PMOS models "look non-physical in moderate and weak inversion" and "should probably not be used for designs with VGS−Vt < 150 mV" [R-322]: open models are for learning, not for signoff.
- **Peak $f_T$ has stopped climbing [Industry estimate].** Published peak NMOS $f_T$: 445 GHz for Intel's 32 nm process (from 209 GHz at 90 nm), 349 GHz for a 28 nm low-power bulk process, 347 GHz for GlobalFoundries' 22FDX, 314 GHz for its 14 nm FinFET and 305 GHz for a 12 nm low-threshold FinFET [R-322]. Each is an established measurement; reading them as a plateau of roughly 300 to 450 GHz since 32 nm is this chapter's interpretation. The IEEE IRDS 2024 roadmap now shows CMOS peak $f_T$ only as TCAD projections and removed $f_{MAX}$ from its CMOS tables because it is "strongly dependent on the device layout" [R-322]. A 5 nm FinFET measured with a single gate contact reached only about 100 GHz, a reminder that parasitics dominate small devices [R-322].
- **FinFETs recovered intrinsic gain [Established, single-company data].** GlobalFoundries reported a "self-gain (Gm/Gds) 40 and 34" for its 14 nm N and P FinFETs, and Samsung a "3.8 times higher intrinsic gain (gm/gds)" for its 14 nm RF FinFET than its 28 nm planar device [R-322]. Neither abstract states the bias or length, so compare such numbers only at stated operating points.
- **Design automation [Vendor claim; Established for academic papers].** Synopsys reports that Credo migrated a VCO from 5 nm to 7 nm with its ASO.ai tool, "reducing the migration efforts from multiple weeks to just a few hours", "up to 100X productivity improvement" (2024); Cadence claimed "more than a 3X improvement in design throughput" for Virtuoso Studio (2023) [R-322]. In academic work, BAG2 generated circuits in five processes from one code base (CICC 2018), MAGICAL produced a 40 nm delta-sigma ADC layout in "around 90 seconds" with measured SNDR "within 2dB" of the manual design (CICC 2021), and ALIGN, still active in 2026, generates RF layouts "in hours compared to weeks" [R-322]. No independent benchmark of the commercial tools was found.

### Why it matters commercially

- **Analog is where respins come from [Industry estimate].** The Siemens-sponsored Wilson Research Group survey attributed respins to "tuning analog circuits" in about 41% of cases in 2020, and saw the issue repeat in 2022 (multiple causes allowed; the survey's recruitment changed after 2022, so later years are not directly comparable) [R-322].
- **Analog does not port.** Every node migration means re-sizing; methods and generators that state design intent as $g_m/I_D$ and length are what make analog reuse and migration practical, which is exactly what the AI migration tools sell.
- **Always-on analog sets battery life.** In wearables and IoT, the references, sensor front ends and wake-up circuits that never sleep run in weak or moderate inversion; their bias currents, chosen with this chapter's method, are a direct term in standby power.
- **No credible public figure exists for analog's share of SoC area or engineering cost** [R-322]; treat any quoted share as an anecdote unless its source and method are given.

### Marketing vs Reality

- **"Our process reaches an $f_T$ of 350 GHz."** That is the peak, at the highest current density and with an RF-optimized layout. Analog circuits run at 10 to 20 S/A, where $f_T$ is several times lower (in T130, 15.5 GHz at 15 S/A against a 127 GHz limit at the same length). Ask at what $g_m/I_D$, length and layout the number holds.
- **"Great analog performance."** Ask for intrinsic gain at the lengths the design will use, threshold matching, flicker noise, and whether the models were characterized in moderate inversion; the SKY130 PMOS caveat shows that this is not automatic.
- **"AI sizes analog circuits 100 times faster."** The published figures are single-customer case studies. Ask for the baseline (an expert with the same lookup tables, or a manual first pass?), whether the result was signed off at every corner, and whether silicon was measured. The academic parity results (within 2 dB of manual SNDR) are the better calibration.
- **"Weak inversion saves power."** It saves current per unit of $g_m$, but costs area, capacitance and $f_T$ (Example 20-01.4: 3.3 GHz at 25 S/A against 27.7 GHz at 10 S/A). Ask what the area and speed cost was, and whether the block was speed- or power-limited to begin with.

### Questions for engineering leaders

1. *"At what $g_m/I_D$ and length do your critical analog transistors operate, and why there?"* Strong: numbers per block, tied to the power, speed or gain constraint that set them. Evasive: overdrive voltages, or "we use the foundry's recommended sizes".
2. *"How do your designs move to the next node?"* Strong: design intent captured as $g_m/I_D$, lengths and generators, with a measured migration effort. Evasive: "we redesign each time" with no estimate, or "the AI tool does it" with no signoff data.
3. *"How do you bias your blocks over corners and temperature?"* Strong: current or constant-$g_m$ biasing, with simulated $g_m$ spread over PVT. Evasive: fixed gate voltages, or no temperature data.
4. *"What fraction of your recent respins were analog, and what caused them?"* Strong: a root-cause list (models outside their characterized range, corners missed, layout parasitics). Evasive: no data.
5. *"How well are your device models characterized in moderate inversion?"* Strong: measured $g_m/I_D$ curves compared with the models. Evasive: "we trust the PDK".

## 10. Concept check

**Q1.** Why does $g_m/I_D$ have an upper limit for a MOSFET, and what sets it?

<details><summary>Answer</summary>

In weak inversion the current is diffusion over a barrier, exponential in the surface potential, so $g_m/I_D = 1/(nV_T)$: the thermal voltage sets the exponential's slope and the slope factor $n$ the fraction of the gate voltage that reaches the surface. No bias can do better; stronger inversion only lowers it.

</details>

**Q2.** Two transistors of the same length carry the same current, one twice as wide as the other. Which has the higher $g_m$, and which the higher $f_T$?

<details><summary>Answer</summary>

The wider one runs at half the inversion coefficient, so it has the higher $g_m/I_D$ and therefore the higher $g_m$. It also has twice the gate capacitance, and its $f_T$, which depends only on the inversion level, is lower.

</details>

**Q3.** Why is $IC$ a better design variable than $V_{GS} - V_{TH}$?

<details><summary>Answer</summary>

$IC = I_D/I_{spec}$ depends only on the current and the device size (through $I_{spec} \propto \mu C_{ox}W/L$), so it is immune to the threshold's uncertainty, and it describes weak, moderate and strong inversion with one number. The overdrive is negative in weak inversion, nearly meaningless in moderate inversion, and inherits every threshold shift.

</details>

**Q4.** Without velocity saturation, the product $(g_m/I_D)f_T$ rises monotonically with inversion. Why then do short-channel designs find a sweet spot in moderate inversion?

<details><summary>Answer</summary>

Velocity saturation caps $f_T$ near $3v_{sat}/(4\pi L)$ in strong inversion, while $g_m/I_D$ keeps falling, now as $1/IC$. Beyond the point where $f_T$ flattens, more current buys no speed and loses efficiency, so the product peaks; for short channels that happens in moderate inversion.

</details>

**Q5.** A transistor's intrinsic gain must double. What two changes would do it, and what does each cost?

<details><summary>Answer</summary>

Double the length (gain $\propto L$ through $V_A$), at roughly a quarter of the $f_T$ and twice the area per unit width; or double $g_m/I_D$ toward weak inversion, at much lower $f_T$ and current density (more area). Neither is free; cascoding (12-02) multiplies the gain instead of trading for it.

</details>

**Q6.** Why does biasing with a current make $g_m$ insensitive to threshold corners but not to temperature?

<details><summary>Answer</summary>

At fixed current the inversion coefficient $I_D/I_{spec}$ does not contain $V_{TH}$; the gate voltage shifts to absorb any threshold change. Temperature, however, changes $V_T$ (which scales $g_m/I_D$ directly) and the mobility in $I_{spec}$ (which shifts $IC$), so $g_m$ still falls as the chip heats unless the bias is designed to hold $g_m$ constant.

</details>

[Problem set 20-01](../problems/20-01-problems.md) · [Worked solutions](../solutions/20-01-solutions.md)

## 11. Key terms

[Inversion coefficient](../../../reference/glossary.md#inversion-coefficient) · [Specific current](../../../reference/glossary.md#specific-current) · [Moderate inversion](../../../reference/glossary.md#moderate-inversion) · [Weak inversion](../../../reference/glossary.md#weak-inversion) · [Transconductance efficiency](../../../reference/glossary.md#transconductance-efficiency) · [gm/ID design method](../../../reference/glossary.md#gm-id-design-method) · [Charge-based (EKV) model](../../../reference/glossary.md#charge-based-ekv-model) · [Transit frequency](../../../reference/glossary.md#transit-frequency) · [Intrinsic gain](../../../reference/glossary.md#intrinsic-gain) · [Velocity saturation](../../../reference/glossary.md#velocity-saturation) · [Pelgrom's law](../../../reference/glossary.md#pelgroms-law) · [PVT corner](../../../reference/glossary.md#pvt-corner)

## 12. Connections

- **Builds on:** the long-channel model, subthreshold current and $f_T$ of [09-09](../../09-semiconductor-devices/chapters/09-09-long-channel-mosfet.md); velocity saturation and DIBL in [09-10](../../09-semiconductor-devices/chapters/09-10-short-channel-effects-and-leakage.md); small-signal $g_m$ and $r_o$ in [10-04](../../10-electronics-1/chapters/10-04-small-signal-models.md); intrinsic gain and cascodes in [12-02](../../12-electronics-2/chapters/12-02-active-loads-cascodes-multistage.md); gain–bandwidth in [12-03](../../12-electronics-2/chapters/12-03-frequency-response-miller-poles-zeros.md); the minimum-energy logic of [19-06](../../19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md), which runs digital gates in the same weak-inversion regime.
- **Used next:** the two-stage op-amp of [20-02](20-02-two-stage-op-amp-design.md) is sized transistor by transistor with this method; the bandgap of [20-03](20-03-bandgap-references.md) uses weak-inversion and bipolar exponentials; comparators and sample-and-holds ([20-05](20-05-comparators-and-sample-and-hold.md)) trade $g_m/I_D$ for speed; matching and PVT are developed in [20-11](20-11-layout-matching-pvt.md), and the scaling argument of this chapter returns in [20-12](20-12-why-analog-does-not-scale.md).

## 13. Further study

- P. G. A. Jespers and B. Murmann, *Systematic Design of Analog CMOS Circuits Using Pre-Computed Lookup Tables* (Cambridge University Press): the method in full, with lookup tables for real processes.
- C. C. Enz and E. A. Vittoz, *Charge-Based MOS Transistor Modeling: The EKV Model for Low-Power and RF IC Design* (Wiley, 2006): the model of §3.2–3.4, derived from the charge sheet.
- B. Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed. (McGraw-Hill, 2017): the device-physics and nanometer-design chapters, for the same trade-offs in a design-oriented setting.
- B. Razavi's analog circuit design lectures (UCLA, public video), and B. Murmann's analog IC design course materials (Stanford EE214).

## 14. Sources

1. C. C. Enz, F. Krummenacher and E. A. Vittoz, "An analytical MOS transistor model valid in all regions of operation and dedicated to low-voltage and low-current applications," *Analog Integrated Circuits and Signal Processing* 8, 1995.
2. C. C. Enz and E. A. Vittoz, *Charge-Based MOS Transistor Modeling: The EKV Model for Low-Power and RF IC Design*, Wiley, 2006.
3. P. G. A. Jespers and B. Murmann, *Systematic Design of Analog CMOS Circuits: Using Pre-Computed Lookup Tables*, Cambridge University Press, 2017 — [R-322].
4. F. Silveira, D. Flandre and P. G. A. Jespers, "A gm/ID based methodology for the design of CMOS analog circuits and its application to the synthesis of a silicon-on-insulator micropower OTA," *IEEE J. Solid-State Circuits* 31(9), pp. 1314–1319, 1996 — [R-322].
5. [R-322] Open gm/ID tools; SKY130 and GF180MCU models; published $f_T$ and self-gain data; IRDS 2024 Outside System Connectivity; analog design-automation claims; the Wilson Research Group respin data.
6. [R-314] IEEE IRDS 2024 More Moore tables (intrinsic delay $CV/I$).
