# Equation Sheet · 06 Circuit Analysis I (DC)

The relations to know cold from Course 06, each with its conditions and the chapter that derives it. Conventions: passive sign convention (current enters the + terminal of an element that absorbs $p = vi > 0$); node 0 is ground. Copper (IACS, 20 °C): $\rho$ = 1.7241 µΩ·cm, $\alpha$ = 0.00393 /°C.

## Variables, power and the lumped abstraction

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $i = dq/dt$; $q = \int i\,dt$; 1 A = 1 C/s; 1 Ah = 3600 C | Charge conservation | [06-01](../../courses/06-circuit-analysis-1-dc/chapters/06-01-charge-current-voltage-power.md) |
| $p = vi$ absorbed (passive convention); $w = \int p\,dt$; 1 Wh = 3600 J | $p < 0$ means the element delivers power | [06-01](../../courses/06-circuit-analysis-1-dc/chapters/06-01-charge-current-voltage-power.md) |
| Tellegen: $\sum_k v_ki_k = 0$ over all elements | Any lumped circuit; the standard check on a solution | [06-01](../../courses/06-circuit-analysis-1-dc/chapters/06-01-charge-current-voltage-power.md) |
| Lumped if size ≪ wavelength ($\ell < \lambda/10$) or wire delay < about 1/6 of the rise time | Otherwise use transmission lines | [06-01](../../courses/06-circuit-analysis-1-dc/chapters/06-01-charge-current-voltage-power.md) |
| Delivering power $P$ at voltage $V$ loses $P^2R/V^2$ in a resistance $R$ | Why power is moved at high voltage | [06-01](../../courses/06-circuit-analysis-1-dc/chapters/06-01-charge-current-voltage-power.md) |

## Elements

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $v = iR$; $p = i^2R = v^2/R$; $G = 1/R$ (S) | Linear resistor | [06-02](../../courses/06-circuit-analysis-1-dc/chapters/06-02-circuit-elements-and-ohms-law.md) |
| $R = \rho L/A$; sheet $R_\square = \rho/t$, $R = R_\square L/W$ (squares) | 1 oz copper: 35 µm, ≈ 0.49 mΩ/□ | [06-02](../../courses/06-circuit-analysis-1-dc/chapters/06-02-circuit-elements-and-ohms-law.md) |
| $R(T) = R_0[1 + \alpha(T - T_0)]$ | Copper +0.393%/°C; resistor TCR in ppm/°C | [06-02](../../courses/06-circuit-analysis-1-dc/chapters/06-02-circuit-elements-and-ohms-law.md) |
| Rating: $V_{max} = \sqrt{PR}$, $I_{max} = \sqrt{P/R}$ | At the rated ambient | [06-02](../../courses/06-circuit-analysis-1-dc/chapters/06-02-circuit-elements-and-ohms-law.md) |
| Real source: $v = V_s - iR_s$ (or $i = I_s - v/R_p$) | Internal resistance | [06-02](../../courses/06-circuit-analysis-1-dc/chapters/06-02-circuit-elements-and-ohms-law.md) |
| AWG diameter $d_n = 0.127\ \text{mm}\times92^{(36 - n)/39}$ | 16 AWG: 1.291 mm, 13.17 mΩ/m; 3 gauges ≈ half the area | [06-11](../../courses/06-circuit-analysis-1-dc/chapters/06-11-practical-dc-circuits-and-measurement.md) |

## Kirchhoff's laws and simple networks

| Relation | Conditions / notes | Chapter |
|---|---|---|
| KCL $\sum i_{in} = 0$ at a node; KVL $\sum v = 0$ around a loop | Lumped circuits | [06-01](../../courses/06-circuit-analysis-1-dc/chapters/06-01-charge-current-voltage-power.md), [06-03](../../courses/06-circuit-analysis-1-dc/chapters/06-03-kirchhoffs-laws.md) |
| $n$ nodes, $b$ branches: $n - 1$ independent KCL, $b - n + 1$ independent KVL | Connected circuit | [06-03](../../courses/06-circuit-analysis-1-dc/chapters/06-03-kirchhoffs-laws.md) |
| Series $R_1 + R_2$; parallel $R_1R_2/(R_1 + R_2)$ | | [06-03](../../courses/06-circuit-analysis-1-dc/chapters/06-03-kirchhoffs-laws.md) |
| Voltage divider $v_2 = vR_2/(R_1 + R_2)$; current divider $i_k = i\,G_k/\sum G$ | Unloaded | [06-03](../../courses/06-circuit-analysis-1-dc/chapters/06-03-kirchhoffs-laws.md) |
| Loaded divider: loading error ≈ $-R_{th}/R_L$ | $R_{th} = R_1\parallel R_2$ | [06-03](../../courses/06-circuit-analysis-1-dc/chapters/06-03-kirchhoffs-laws.md) |
| Bridge $v_{out} = V\dfrac{R_2R_3 - R_1R_4}{(R_1 + R_2)(R_3 + R_4)}$; balanced if $R_1R_4 = R_2R_3$ | Quarter bridge: $v_{out} \approx (V/4)\,\Delta R/R$; half 2×, full 4× | [06-03](../../courses/06-circuit-analysis-1-dc/chapters/06-03-kirchhoffs-laws.md) |
| Δ→Y: $R_a = R_{ab}R_{ca}/(R_{ab} + R_{bc} + R_{ca})$ (and cyclic) | Y→Δ: $R_{ab} = (R_aR_b + R_bR_c + R_cR_a)/R_c$ | [06-03](../../courses/06-circuit-analysis-1-dc/chapters/06-03-kirchhoffs-laws.md) |

## Systematic analysis

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Nodal: $\mathbf{G}\mathbf{v} = \mathbf{i}_s$; $G_{kk}$ = sum of conductances at node $k$, $G_{kj}$ = −(conductance between $k$ and $j$) | Independent current sources; $\mathbf{G}$ symmetric | [06-04](../../courses/06-circuit-analysis-1-dc/chapters/06-04-nodal-analysis.md) |
| Floating voltage source: supernode (KCL around both nodes) + constraint $v_a - v_b = V_s$ | Grounded source: the node voltage is known | [06-04](../../courses/06-circuit-analysis-1-dc/chapters/06-04-nodal-analysis.md) |
| MNA: $\begin{bmatrix}\mathbf{G} & \mathbf{B}\\ \mathbf{B}^T & 0\end{bmatrix}\begin{bmatrix}\mathbf{v}\\ \mathbf{i}_V\end{bmatrix} = \begin{bmatrix}\mathbf{i}_s\\ \mathbf{v}_s\end{bmatrix}$ | What SPICE solves | [06-04](../../courses/06-circuit-analysis-1-dc/chapters/06-04-nodal-analysis.md) |
| Mesh: $\mathbf{R}\mathbf{i} = \mathbf{v}_s$; $R_{kk}$ = resistance around mesh $k$, $R_{kj}$ = −(shared resistance) | Planar circuits; voltage sources | [06-05](../../courses/06-circuit-analysis-1-dc/chapters/06-05-mesh-analysis.md) |
| Shared current source: supermesh (KVL around both meshes) + constraint $i_a - i_b = I_s$ | Outer current source: the mesh current is known | [06-05](../../courses/06-circuit-analysis-1-dc/chapters/06-05-mesh-analysis.md) |
| Unknowns: nodal $n - 1$ (minus voltage sources); mesh $b - n + 1$ (minus current sources) | Choose the smaller system | [06-05](../../courses/06-circuit-analysis-1-dc/chapters/06-05-mesh-analysis.md) |

## Dependent sources and transistor-like models

| Relation | Conditions / notes | Chapter |
|---|---|---|
| VCVS $\mu v_x$; VCCS $g_mv_x$; CCVS $r_mi_x$; CCCS $\beta i_x$ | SPICE E, G, H, F | [06-06](../../courses/06-circuit-analysis-1-dc/chapters/06-06-dependent-sources.md) |
| Write the controlling variable in terms of the unknowns, then solve; $\mathbf{G}$ becomes nonsymmetric | Nodal or mesh | [06-06](../../courses/06-circuit-analysis-1-dc/chapters/06-06-dependent-sources.md) |
| Port resistance $R = v_t/i_t$ with independent sources off and dependent sources kept | Test-source method; $R$ can be negative | [06-06](../../courses/06-circuit-analysis-1-dc/chapters/06-06-dependent-sources.md) |
| Emitter degeneration: $R_{in} = r_\pi + (\beta + 1)R_E$; gain $\approx -\beta R_C/R_{in}$ | CCCS model of a bipolar transistor | [06-06](../../courses/06-circuit-analysis-1-dc/chapters/06-06-dependent-sources.md) |
| Finite-gain feedback: $G = G_{ideal}/(1 + G_{ideal}/A)$, error ≈ $1/(A\beta)$ | Non-inverting; loop gain $A\beta$ | [06-06](../../courses/06-circuit-analysis-1-dc/chapters/06-06-dependent-sources.md) |

## Linearity, superposition and equivalents

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Response = $\sum_k$ (gain$_k$ × source$_k$) | Linear circuits; turn off a V source = short, I source = open; keep dependent sources | [06-07](../../courses/06-circuit-analysis-1-dc/chapters/06-07-linearity-and-superposition.md) |
| Power does not superpose: $(v_1 + v_2)^2/R \ne v_1^2/R + v_2^2/R$ | Superpose $v$ and $i$, then compute $p$ | [06-07](../../courses/06-circuit-analysis-1-dc/chapters/06-07-linearity-and-superposition.md) |
| Source transformation: $V_s$ in series with $R$ ⇔ $I_s = V_s/R$ in parallel with $R$ | Equivalent at the terminals only | [06-07](../../courses/06-circuit-analysis-1-dc/chapters/06-07-linearity-and-superposition.md) |
| Worst case: add the magnitudes of sensitivity × tolerance; RSS: $\sqrt{\sum(\text{sens}\times\sigma)^2}$ | RSS of uniform limits is exceeded by a few percent of units | [06-07](../../courses/06-circuit-analysis-1-dc/chapters/06-07-linearity-and-superposition.md) |
| Thévenin $V_{th} = v_{oc}$; Norton $I_N = i_{sc}$; $R_{th} = v_{oc}/i_{sc}$ | Or $R_{th}$ by test source (dependent sources) | [06-08](../../courses/06-circuit-analysis-1-dc/chapters/06-08-thevenin-and-norton.md) |
| Two loads: $V_{th}$ and $R_{th}$ from two (load, voltage) pairs | Measuring an equivalent | [06-08](../../courses/06-circuit-analysis-1-dc/chapters/06-08-thevenin-and-norton.md) |
| Max power: $R_L = R_{th}$, $P_{max} = V_{th}^2/(4R_{th})$, $\eta$ = 50% | Given source, choose the load | [06-09](../../courses/06-circuit-analysis-1-dc/chapters/06-09-maximum-power-transfer.md) |
| $\eta = R_L/(R_L + R_{th})$; $p/p_{max} = 4\eta(1 - \eta)$ | Any linear source | [06-09](../../courses/06-circuit-analysis-1-dc/chapters/06-09-maximum-power-transfer.md) |

## Op-amps

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Ideal rules: $i_+ = i_- = 0$; $v_+ = v_-$ | Negative feedback, output not saturated | [06-10](../../courses/06-circuit-analysis-1-dc/chapters/06-10-ideal-op-amp.md) |
| Inverting $-R_2/R_1$ ($R_{in} = R_1$); non-inverting $1 + R_2/R_1$ ($R_{in}$ ≈ ∞); follower 1 | Noise gain $1 + R_2/R_1$ in both | [06-10](../../courses/06-circuit-analysis-1-dc/chapters/06-10-ideal-op-amp.md) |
| Summer $v_{out} = -R_f\sum v_k/R_k$; transimpedance $v_{out} = -R_fi_{in}$ | Virtual ground | [06-10](../../courses/06-circuit-analysis-1-dc/chapters/06-10-ideal-op-amp.md) |
| Difference amp $G(v_2 - v_1)$ if $R_4/R_3 = R_2/R_1 = G$; $A_{cm} = (b - a)/(1 + b)$ with $a = R_2/R_1$, $b = R_4/R_3$ | CMRR $= G/\lvert A_{cm}\rvert$ ≈ $(1 + G)/(4t)$ worst case | [06-10](../../courses/06-circuit-analysis-1-dc/chapters/06-10-ideal-op-amp.md) |
| In-amp $(1 + 2R/R_G)(R_2/R_1)(v_+ - v_-)$ | CMRR × first-stage gain | [06-10](../../courses/06-circuit-analysis-1-dc/chapters/06-10-ideal-op-amp.md) |
| Output errors: $V_{OS}\times$ noise gain; $I_B$ at −: $I_BR_2$; $I_B$ at +: $I_BR_s\times$ noise gain | Signs: PNP inputs push current out; compensate with $R_1\parallel R_2$ → $I_{OS}R_2$ | [06-10](../../courses/06-circuit-analysis-1-dc/chapters/06-10-ideal-op-amp.md) |

## Measurement

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Voltmeter: $V_m = V_{th}R_{in}/(R_{th} + R_{in})$, error ≈ $-R_{th}/R_{in}$; correct with $V_m(1 + R_{th}/R_{in})$ | Handheld ≈ 10 MΩ; bench high-Z > 10 GΩ | [06-11](../../courses/06-circuit-analysis-1-dc/chapters/06-11-practical-dc-circuits-and-measurement.md) |
| Ammeter: $I_m = I_0/(1 + R_A/R_{th})$; burden $I_mR_A$ | | [06-11](../../courses/06-circuit-analysis-1-dc/chapters/06-11-practical-dc-circuits-and-measurement.md) |
| Accuracy ±(a% of reading + $n$ counts); relative errors of products add (worst case) or RSS | Count = resolution of the range in use | [06-11](../../courses/06-circuit-analysis-1-dc/chapters/06-11-practical-dc-circuits-and-measurement.md) |
| Two-wire $R + 2R_{lead}$; four-wire residual ≈ $-(R + R_s)/R_{in}$ | Kelvin: force and sense separately | [06-11](../../courses/06-circuit-analysis-1-dc/chapters/06-11-practical-dc-circuits-and-measurement.md) |
| Remote sense: $v_{load} = V_{set}$, $v_{supply} = V_{set} + I(R_{w+} + R_{w-})$ | Needs headroom; cable still dissipates $I^2R$ | [06-11](../../courses/06-circuit-analysis-1-dc/chapters/06-11-practical-dc-circuits-and-measurement.md) |
