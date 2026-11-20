<!-- status: verified -->
# 15-01 · Modeling Dynamic Systems

| | |
|---|---|
| **Course** | [15 · Control Systems](../README.md) |
| **University equivalent** | The modeling chapter of a first course in feedback control: dynamic models of mechanical, electrical, electromechanical and thermal systems, analogies between them, and linearization (Franklin, Powell & Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 2 and §9.2; Ogata, *Modern Control Engineering*, ch. 3) |
| **Prerequisites** | [02-09 Systems of ODEs and the Matrix Exponential](../../02-complex-numbers-des-and-linear-algebra/chapters/02-09-systems-of-odes-and-matrix-exponential.md), [04-01 Mechanics Essentials](../../04-physics-for-ee/chapters/04-01-mechanics-essentials.md), [07-03 Second-Order RLC Transients](../../07-circuit-analysis-2-transient-and-ac/chapters/07-03-second-order-rlc-transients.md), [11-08 The Laplace Transform and System Functions](../../11-signals-and-systems/chapters/11-08-laplace-transform-and-system-functions.md) |
| **Estimated study hours** | 8 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Write the differential equations of electrical, mechanical (translational and rotational), electromechanical and thermal systems from their element laws and interconnection laws.
2. Map a mechanical or thermal system onto an equivalent circuit with the force–voltage, force–current and thermal–electrical analogies, and say where each analogy breaks.
3. Put a model into state-variable form and into transfer-function form, choosing the energy stores as states.
4. Model a DC motor and compute its steady speed, stall torque and electrical and mechanical time constants.
5. Build a lumped thermal model of a chip and its cooling path, and compute junction-temperature transients.
6. Linearize a nonlinear model about an operating point, judge how far the linear model can be trusted, and use the linearization to predict thermal runaway.

---

## 1. Big picture

Control design starts from a model. A feedback loop corrects errors, but how hard it can push, how fast it can respond and whether it stays stable all depend on the dynamics of the thing being controlled, which control engineers call the **plant**. A model is a set of differential equations, usually simplified until it is linear and of low order, that predicts how the plant's outputs respond to its inputs. This chapter builds such models from physics. The same few laws (conservation of charge, energy and momentum, plus one constitutive law per element) describe circuits, mechanisms, motors and heat flow. The equations that result have the same form, so one set of tools (Laplace transforms, block diagrams, state space) serves them all.

- **Every chip contains control loops.** Phase-locked loops lock clocks to a reference. Voltage regulators hold supply rails steady against load steps. Dynamic voltage and frequency scaling (DVFS) and thermal throttling keep a processor under its temperature limit. Each needs a model of what it controls (15-12).
- **Thermal models decide product limits.** A chip's sustained performance is set less by its transistors than by how fast its heat can leave. The heat path is a network of thermal resistances and capacitances that behaves exactly like an RC circuit.
- **Mechanisms with motors** (fans, pumps, disk-drive actuators, robots, camera stabilizers) are electromechanical systems: a circuit coupled to a mass through torque and back-EMF.
- **Nonlinear plants are linearized.** Transistors, pendulums and leakage-dependent heating are nonlinear, but near an operating point a linear model predicts small deviations. This is the same step as the small-signal model of a transistor (10-04).

## 2. Intuition first

**Two ways to store energy, one way to lose it.** A swinging mass on a spring trades kinetic energy ($\tfrac12mv^2$, stored in motion) for potential energy ($\tfrac12kx^2$, stored in the stretched spring) and back, while friction drains a little each cycle. A series RLC circuit does the same with magnetic energy in the inductor ($\tfrac12Li^2$) and electric energy in the capacitor ($\tfrac12Cv^2$), while the resistor turns some into heat. Systems with two kinds of energy store can oscillate; systems with only one kind can only relax exponentially. A hot chip stores heat in its mass, the thermal counterpart of charge on a capacitor, and loses it through thermal resistances. There is no thermal "inertia" that would keep heat flowing once the temperature difference vanishes, so a passive thermal network never oscillates.

**The analogy as a translation dictionary.** Every analogy pairs a **through** variable (one that is the same at both ends of an element: current, force, heat flow) with an **across** variable (one measured between its two ends: voltage, velocity difference, temperature difference). Once the pairs are fixed, the element laws line up:

```text
  electrical              mechanical (force–current)       thermal
  ----------              --------------------------       -------
  current  i   (through)  force     f   (through)          heat flow  P  (W)
  voltage  v   (across)   velocity  v   (across)           temperature T  (K)
  capacitor  i = C dv/dt  mass      f = m dv/dt            heat capacity  P = C_th dT/dt
  resistor   i = v/R      damper    f = b v                thermal resistance  P = ΔT/R_th
  inductor   v = L di/dt  spring    v = (1/k) df/dt        (no thermal counterpart)
```

The analogy is exact for the equations, so a circuit simulator can simulate a mechanism or a heat sink. It breaks in two places. A mass's velocity is measured against an inertial frame, so in the force–current analogy every mass is a capacitor with one terminal at ground. And thermal networks have no inductor, because heat has no momentum.

## 3. Theory

### 3.1 The modeling recipe

Every model in this chapter comes from three ingredients:

1. **Element laws**, one per element, relating its through and across variables: $v = Ri$, $f = m\,dv/dt$, $P = C_{th}\,dT/dt$.
2. **Interconnection laws**: the through variables balance at every junction (Kirchhoff's current law, the sum of forces on a body, conservation of energy at a thermal node), and the across variables add around every loop (Kirchhoff's voltage law, geometric compatibility of displacements).
3. **Simplifying assumptions**, stated explicitly: lumped elements (each property concentrated at a point, valid when the system is small compared with the scale over which things change; 13-04), linear elements, constant parameters, and neglected effects (friction, leakage, air resistance).

The result is a set of ordinary differential equations. Choosing as **state variables** the quantities that describe the stored energy (capacitor voltages, inductor currents, mass velocities, spring forces or displacements, node temperatures) gives one first-order equation per energy store. That set is the **state-space model** (02-09):

$$
\dot{\mathbf{x}} = A\mathbf{x} + B\mathbf{u}, \qquad \mathbf{y} = C\mathbf{x} + D\mathbf{u}.
$$

Here $\mathbf{x}$ is the state vector, $\mathbf{u}$ the inputs and $\mathbf{y}$ the outputs. The number of independent energy stores is the **order** of the system. Taking Laplace transforms with zero initial conditions turns the same equations into a **transfer function** $G(s) = Y(s)/U(s)$ for each input–output pair (11-08), the form the rest of this course designs with (15-02).

### 3.2 Electrical networks

A series RLC circuit driven by a voltage $v_s(t)$ has two energy stores, so two states: the inductor current $i$ and the capacitor voltage $v_C$. Kirchhoff's voltage law and the element laws give

$$
L\frac{di}{dt} = v_s - Ri - v_C, \qquad C\frac{dv_C}{dt} = i,
$$

and in state-space form, with $\mathbf{x} = [i,\ v_C]^T$,

$$
\dot{\mathbf{x}} = \begin{bmatrix} -R/L & -1/L \\ 1/C & 0 \end{bmatrix}\mathbf{x} + \begin{bmatrix} 1/L \\ 0 \end{bmatrix}v_s .
$$

Eliminating $i$ gives the familiar second-order equation $LC\,\ddot v_C + RC\,\dot v_C + v_C = v_s$ and the transfer function

$$
\frac{V_C(s)}{V_s(s)} = \frac{1}{LCs^2 + RCs + 1} = \frac{\omega_n^2}{s^2 + 2\zeta\omega_ns + \omega_n^2},
\qquad \omega_n = \frac{1}{\sqrt{LC}}, \quad \zeta = \frac{R}{2}\sqrt{\frac{C}{L}} .
$$

Here $\omega_n$ (rad/s) is the **natural frequency** and $\zeta$ (dimensionless) the **damping ratio** (07-03). (Control texts write $\omega_n$ for what 07-03 and the notation guide call $\omega_0$, and 15-03 writes the decay rate $\sigma = \zeta\omega_n$ for 07-03's $\alpha$; the quantities are the same. In this course $K$ alone usually means a gain, with subscripts such as $K_t$ and $K_e$ for physical constants.) Every second-order model in this chapter ends in this standard form, and 15-03 reads time-response specifications straight from $\omega_n$ and $\zeta$.

### 3.3 Mechanical systems

**Translation.** A mass $m$ (kg) moves with displacement $x$ (m), held by a spring of stiffness $k$ (N/m) and slowed by a viscous damper with coefficient $b$ (N·s/m). The damper's force is proportional to velocity; real friction is often not (Coulomb friction is constant in magnitude), which is one of the first assumptions to check. Newton's second law sums the forces on the mass, with an applied force $f(t)$:

$$
m\ddot x = f - b\dot x - kx \quad\Longrightarrow\quad m\ddot x + b\dot x + kx = f .
$$

The states are the displacement and the velocity (the spring's potential energy and the mass's kinetic energy). The transfer function from force to displacement is

$$
\frac{X(s)}{F(s)} = \frac{1}{ms^2 + bs + k}, \qquad \omega_n = \sqrt{\frac{k}{m}}, \quad \zeta = \frac{b}{2\sqrt{km}} .
$$

A constant force $F_0$ settles at the static deflection $F_0/k$, as setting $s = 0$ confirms.

**Rotation.** The same law for a body rotating about a fixed axis has moment of inertia $J$ (kg·m²), angle $\theta$ (rad), torsional stiffness $K$ (N·m/rad), rotary damping $B$ (N·m·s/rad) and applied torque $\tau$ (N·m):

$$
J\ddot\theta + B\dot\theta + K\theta = \tau .
$$

Units check: every term is a torque, N·m, since kg·m²·rad/s² = N·m (radians are dimensionless).

### 3.4 Analogies

Comparing the mechanical equation with the series RLC equation written for charge $q$ ($L\ddot q + R\dot q + q/C = v_s$) gives the **force–voltage analogy** (04-01): force ↔ voltage, velocity ↔ current, displacement ↔ charge, mass ↔ $L$, damping $b$ ↔ $R$, stiffness $k$ ↔ $1/C$. Elements that share a velocity in the mechanism (a mass, its damper and its spring moving together) become elements in *series* that share a current.

The **force–current analogy** pairs force with current and velocity with voltage, as in the table of §2: mass ↔ $C$, damping $b$ ↔ $1/R$ (a conductance), stiffness $k$ ↔ $1/L$. Elements that share a velocity become elements in *parallel* that share a voltage, so the circuit has the same topology as the mechanism, which is why many engineers prefer it. Both analogies give the same equations and the same $\omega_n$ and $\zeta$. Which one is "right" is a matter of convenience.

| Mechanical | Force–voltage | Force–current |
|---|---|---|
| force $f$ | voltage $v$ | current $i$ |
| velocity $\dot x$ | current $i$ | voltage $v$ |
| mass $m$ | inductance $L = m$ | capacitance $C = m$ |
| damping $b$ | resistance $R = b$ | conductance $1/R = b$ |
| stiffness $k$ | elastance $1/C = k$ | inverse inductance $1/L = k$ |
| shared velocity | series connection | parallel connection |

![Two circuits side by side. Left, the force-voltage analogue of a mass-spring-damper: a voltage source F(t) drives a single series loop through an inductor L = m, a resistor R = b and a capacitor C = 1/k, and the loop current is the velocity. Right, the force-current analogue: a current source F(t) feeds three elements in parallel, a capacitor C = m, a resistor R = 1/b and an inductor L = 1/k, and the common node voltage is the velocity.](../../../assets/figures/15-01/analogues.svg)

*Figure 1. The mass–spring–damper's two analogue circuits. Elements sharing one velocity are in series in the force–voltage analogue and in parallel in the force–current analogue.*

### 3.5 Electromechanical systems: the DC motor

![The DC motor's armature circuit: a voltage source v_a drives current i through a resistor R and an inductor L into a second source, the back-EMF e_b = K_e times omega, which opposes the current. Below the circuit, the torque relation tau_em = K_t i and the mechanical equation J times d omega/dt = K_t i - b omega - tau_L.](../../../assets/figures/15-01/motor-circuit.svg)

*Figure 2. The armature circuit. The back-EMF source couples the electrical loop to the mechanical speed; the current couples back through the torque.*

A permanent-magnet DC motor couples a circuit to a rotating mass through two laws that are really one law seen from two sides (04-06, 04-07):

- the **torque** on the rotor is proportional to the armature current, $\tau_{em} = K_ti$ (the electromagnetic torque; $\tau_m$ is reserved below for the mechanical time constant), where $K_t$ (N·m/A) is the **torque constant**;
- the spinning rotor generates a **back-EMF** proportional to its speed $\omega$ (rad/s), $e_b = K_e\omega$, with $K_e$ in V·s/rad.

**Derivation that $K_t = K_e$.** The electrical power that disappears into the back-EMF, $e_bi = K_e\omega i$, must reappear as mechanical power, $\tau_{em}\omega = K_ti\omega$, if the coupling itself stores and loses nothing. Equating the two gives $K_t = K_e$ in SI units, so we write both as $K$. (Units check: N·m/A = J/(A·rad) = V·A·s/(A·rad) = V·s/rad.)

With armature resistance $R$ and inductance $L$, rotor inertia $J$, viscous friction $B$ and a load torque $\tau_L$:

$$
L\frac{di}{dt} = v - Ri - K\omega, \qquad J\frac{d\omega}{dt} = Ki - B\omega - \tau_L .
$$

The two states are the current (magnetic energy) and the speed (kinetic energy). With $\tau_L = 0$, the transfer function from applied voltage to speed is

$$
\frac{\Omega(s)}{V(s)} = \frac{K}{(Ls + R)(Js + B) + K^2} .
$$

Its useful consequences:

- **Steady speed** ($s = 0$): $\omega_{ss} = KV/(RB + K^2)$. With negligible friction, $\omega_{ss} \approx V/K$: the motor speeds up until its back-EMF nearly cancels the supply.
- **Stall** ($\omega = 0$): the current is $V/R$ and the torque $KV/R$. A stalled motor draws its largest current, because no back-EMF opposes the supply.
- **Two time constants.** The electrical time constant is $\tau_e = L/R$. When $\tau_e$ is much shorter than the mechanical dynamics, set $L \to 0$: then $i = (v - K\omega)/R$, and the speed obeys $J\dot\omega = (K/R)(v - K\omega) - B\omega$, a first-order system with **mechanical time constant**

$$
\tau_m = \frac{RJ}{RB + K^2} .
$$

The back-EMF acts like extra damping, $K^2/R$, which is why an unloaded motor reaches speed in milliseconds even with little friction. Dropping the fast pole to get a lower-order model is **model reduction**, used constantly in control. Example 15-01.2 checks how good the approximation is.

### 3.6 Thermal systems

Heat flow $P$ (W) is the through variable and temperature $T$ (K or °C; differences are the same in both) is the across variable. Two element laws describe a lumped thermal network:

- a **thermal resistance** $R_{th}$ (K/W) carries heat in proportion to the temperature difference across it, $P = \Delta T/R_{th}$. For conduction through a slab of thickness $t$, area $A$ and thermal conductivity $k$ (W/(m·K)), $R_{th} = t/(kA)$, the analogue of $R = \rho\ell/A$;
- a **thermal capacitance** $C_{th}$ (J/K) stores heat: $P = C_{th}\,dT/dt$, with $C_{th} = mc$ for a mass $m$ of material with specific heat $c$ (J/(kg·K)). Every thermal capacitance has its other terminal at a fixed reference temperature, like the force–current analogy's masses.

Conservation of energy at each node (heat in = heat stored + heat out) is the thermal Kirchhoff current law. A single node, a chip dissipating $P$ with capacitance $C_{th}$ and resistance $R_{th}$ to ambient at $T_A$, obeys

$$
C_{th}\frac{dT}{dt} = P - \frac{T - T_A}{R_{th}} ,
$$

which is an RC circuit driven by a current source. A power step gives $T(t) = T_A + PR_{th}(1 - e^{-t/\tau})$ with $\tau = R_{th}C_{th}$ (07-02).

![The two-node thermal network of Example 15-01.3 drawn as a circuit: a current source P injects heat into node T_J, which has capacitance C_J = 5 J/K to the reference; a resistor R_JC = 0.15 K/W connects T_J to node T_C, which has capacitance C_H = 300 J/K to the reference; a resistor R_CA = 0.35 K/W connects T_C to a voltage source representing the ambient temperature T_A = 30 degrees C. Heat flow corresponds to current and temperature to voltage.](../../../assets/figures/15-01/thermal-network.svg)

*Figure 3. Example 15-01.3's processor and heat sink as a circuit. Each thermal capacitance connects to the temperature reference, the thermal ground.*

**A chip's heat path.** Heat made in the transistors crosses the silicon, a thermal interface material (TIM), a heat spreader or lid, a second TIM and a heat sink, and finally passes to the air. Vendors summarize the path by **junction-to-case** and **case-to-ambient** resistances, $R_{JC}$ and $R_{CA}$, and the **junction temperature** $T_J$ (the transistors' temperature) is the quantity limits are set on. The masses involved differ enormously. A 10 mm × 10 mm silicon die 0.75 mm thick has a volume of 0.075 cm³; at 2.329 g/cm³ and 0.7 J/(g·K) [2, R-228] its heat capacity is only **0.122** J/K, while a heat sink of a few hundred grams has hundreds of joules per kelvin. So a thermal network has widely separated time constants: the die responds in milliseconds, the spreader in seconds and the heat sink in minutes. A one-node model catches the slowest of them and misses the fast junction rise that a sudden load causes (Example 15-01.3).

The heat-flow analogy has limits. Thermal resistance and capacitance change with temperature, conduction spreads in three dimensions rather than along a line, and the true network is distributed, not lumped. Lumped thermal models are still standard because they are simple and their parameters can be measured; the network of resistances and capacitances is fitted to measured heating curves. Data-sheet thermal resistances also come with conditions: $R_{\theta JA}$ "is not a characteristic of the package by itself but of the package, PCB, and other environmental factors" [1, R-227], so it describes a standard test board, not your system.

### 3.7 Linearization about an operating point

Most real plants are nonlinear: $\dot{\mathbf{x}} = \mathbf{f}(\mathbf{x}, \mathbf{u})$. An **equilibrium** (or **operating point**) is a pair $(\mathbf{x}^*, \mathbf{u}^*)$ with $\mathbf{f}(\mathbf{x}^*, \mathbf{u}^*) = 0$: if the system starts there with that input, it stays. Write small deviations as $\delta\mathbf{x} = \mathbf{x} - \mathbf{x}^*$ and $\delta\mathbf{u} = \mathbf{u} - \mathbf{u}^*$ and expand $\mathbf{f}$ in a Taylor series:

$$
\dot{\delta\mathbf{x}} = \mathbf{f}(\mathbf{x}^*, \mathbf{u}^*) + \frac{\partial\mathbf{f}}{\partial\mathbf{x}}\bigg|_*\delta\mathbf{x} + \frac{\partial\mathbf{f}}{\partial\mathbf{u}}\bigg|_*\delta\mathbf{u} + \text{(second-order terms)} .
$$

The first term is zero at an equilibrium, and for small deviations the second-order terms are negligible, leaving a linear model

$$
\dot{\delta\mathbf{x}} = A\,\delta\mathbf{x} + B\,\delta\mathbf{u}, \qquad A = \frac{\partial\mathbf{f}}{\partial\mathbf{x}}\bigg|_*, \quad B = \frac{\partial\mathbf{f}}{\partial\mathbf{u}}\bigg|_* ,
$$

where $A$ and $B$ are **Jacobian** matrices (01-10) evaluated at the operating point. The linear model is only as good as the neglected terms are small, and it can differ from one operating point to another. That is the same lesson as the transistor small-signal model, which is exactly this procedure applied to $i_D(v_{GS}, v_{DS})$ (10-04).

> **Math refresher — Taylor expansion in one variable.** For a smooth function, $g(x^* + \delta) = g(x^*) + g'(x^*)\delta + \tfrac12g''(x^*)\delta^2 + \ldots$ The linear term dominates while $\lvert\tfrac12g''\delta^2\rvert \ll \lvert g'\delta\rvert$, i.e. while $\lvert\delta\rvert \ll 2\lvert g'/g''\rvert$. That ratio is a quick estimate of how far the linearization can be trusted.

**The pendulum.** A rigid pendulum of length $L$ (a point mass on a massless rod) under gravity $g$, with angle $\theta$ from straight down and applied torque per unit $mL^2$ called $u$, obeys $\ddot\theta = -(g/L)\sin\theta + u$. It has two equilibria with $u^* = 0$:

- hanging down, $\theta^* = 0$: $\sin\theta \approx \theta$, so $\ddot{\delta\theta} = -(g/L)\delta\theta$, an oscillator with $\omega_0 = \sqrt{g/L}$;
- inverted, $\theta^* = \pi$: $\sin(\pi + \delta) = -\sin\delta \approx -\delta$, so $\ddot{\delta\theta} = +(g/L)\delta\theta$, whose solutions grow as $e^{\sqrt{g/L}\,t}$. The linear model has a pole in the right half-plane: the inverted pendulum is **unstable**, and only feedback can hold it up (the classic control demonstration, 15-10).

**Thermal runaway as a linearization.** A chip's leakage power rises steeply with temperature (09-10). A common model is $P_L(T) = P_{L0}\,e^{(T - T_0)/T_x}$, where $T_x$ sets how fast leakage grows. Adding a temperature-independent dynamic power $P_d$, the one-node thermal model becomes nonlinear:

$$
C\frac{dT}{dt} = P_d + P_L(T) - \frac{T - T_A}{R} \equiv f(T) .
$$

Equilibria satisfy $f(T^*) = 0$: heat generated equals heat removed. Linearizing about $T^*$:

$$
C\,\dot{\delta T} = \left(\frac{dP_L}{dT}\bigg|_* - \frac{1}{R}\right)\delta T = -\frac{1 - G}{R}\,\delta T, \qquad G = R\frac{dP_L}{dT}\bigg|_* = \frac{RP_L(T^*)}{T_x} .
$$

$G$ is a **loop gain**: a rise $\delta T$ raises leakage by $(dP_L/dT)\delta T$, which raises the temperature by $R$ times that. If $G < 1$, the deviation decays with time constant

$$
\tau_{\text{eff}} = \frac{RC}{1 - G} ,
$$

slower than the passive $RC$ because the positive feedback partly cancels the cooling. If $G > 1$, the deviation grows: **thermal runaway**. Two different things must be kept apart here. At a given thermal resistance there are usually two equilibria: a stable one with $G < 1$ and an unstable one with $G > 1$ (an equilibrium with $G > 1$ exists, but any disturbance grows away from it). As $R$ rises the two move together, and at the critical resistance $R_{crit}$, where $G$ reaches 1, they merge: the heat-generated curve touches the heat-removed line tangentially. Above $R_{crit}$ no equilibrium exists at all and the temperature runs away from any starting point (Example 15-01.4). This is the same mechanism as thermal runaway in a bipolar output stage (12-07), and the loop-gain idea is the subject of 15-04.

![Two plots. Left: junction and case temperatures of Example 15-01.3 after a 100 W step, on a logarithmic time axis from 0.01 to 1600 s. The junction rises about 15 K within a few seconds while the case stays near 30 °C, then both climb together toward 80 °C and 65 °C over a few hundred seconds. Right: heat generated, 60 W plus a leakage term growing exponentially with temperature, against straight lines of heat removed for R = 0.5 K/W and 0.628 K/W. The 0.5 K/W line crosses the curve twice, at a stable point near 64 °C and an unstable one near 125 °C; the 0.628 K/W line just touches the curve near 93 °C.](../../../assets/figures/15-01/thermal.svg)

*Figure 4. Left: a thermal network's two time scales (Example 15-01.3). Right: leakage feedback (Example 15-01.4). An equilibrium is a crossing of the heat-generated curve and the heat-removed line; where the curve is steeper than the line ($G > 1$) the crossing is unstable, and once the line is tangent (the dashed critical resistance) the equilibria vanish.*

> **Going deeper — when linearization fails.** A linear model can be trusted only near its operating point, and only if the operating point is hyperbolic: no eigenvalue of $A$ on the imaginary axis. The Hartman–Grobman theorem says that near a hyperbolic equilibrium, the nonlinear system's trajectories look like the linear model's. If an eigenvalue sits on the imaginary axis (the pendulum without friction, or $G = 1$ exactly), the neglected nonlinear terms decide stability, and the linear model says nothing. Large signals need the nonlinear model itself, or gain scheduling: a family of linear models, one per operating point, with the controller switched between them.

## 4. Worked examples

### Example 15-01.1 · A mass, a spring and its two circuits (tier A)

**Setup.** A mass of 0.5 kg hangs on a spring with $k$ = 200 N/m and a damper with $b$ = 4 N·s/m. Find $\omega_n$, $\zeta$ and the static deflection under a constant 10 N force. Give the element values of the force–voltage and force–current analogue circuits, and the peak displacement after the force is applied as a step.

**Solution.** $\omega_n = \sqrt{k/m} = \sqrt{400}$ = **20** rad/s. $\zeta = b/(2\sqrt{km}) = 4/(2\sqrt{100})$ = **0.2**. The static deflection is $F_0/k$ = 10/200 = **0.05** m.

- Force–voltage: $L$ = 0.5 H, $R$ = 4 Ω, $C = 1/k$ = **5** mF in series, driven by a 10 V step. The capacitor's charge plays the displacement: $q = Cv_C$ settles at 5 mF × 10 V = 0.05 C.
- Force–current: $C$ = 0.5 F, $R = 1/b$ = **0.25** Ω and $L = 1/k$ = **5** mH in parallel, driven by a 10 A step; the node voltage plays the velocity.

With $\zeta$ = 0.2 the response overshoots (07-03): the peak is $1 + e^{-\pi\zeta/\sqrt{1 - \zeta^2}}$ = 1 + 0.5266 times the final value, so $x_{\max}$ = **0.0763** m, reached at $t_p = \pi/(\omega_n\sqrt{1 - \zeta^2})$ = **0.160** s.

**Units check.** $\sqrt{(\text{N/m})/\text{kg}} = \sqrt{1/\text{s}^2}$ = 1/s. For $\zeta$: $b$ has units N·s/m = kg/s, and $\sqrt{km} = \sqrt{(\text{N/m})\,\text{kg}} = \sqrt{\text{kg}^2/\text{s}^2}$ = kg/s, so $\zeta$ is dimensionless.

**Sanity check.** The lab's ngspice netlist simulates the force–voltage circuit and finds the same peak, 0.0763 (as 5 mF × 15.27 V), within 0.1% [labs/15-01-lab](../labs/15-01-lab/README.md).

### Example 15-01.2 · A DC motor and its two time constants (tier B)

**Setup.** A small DC motor has $R$ = 2 Ω, $L$ = 1 mH, $K$ = 0.05 V·s/rad, $J$ = 2 × 10⁻⁵ kg·m² and $B$ = 1 × 10⁻⁵ N·m·s/rad. At 12 V with no load, find the steady speed, the running current, the stall current and torque, and the electrical and mechanical time constants. How good is the first-order model?

**Solution.**

- Steady speed: $\omega_{ss} = KV/(RB + K^2) = 0.6/(2 \times 10^{-5} + 0.0025)$ = **238.1** rad/s, or **2274** rpm. With no friction it would be $V/K$ = 240 rad/s.
- Running current: in steady state the motor torque balances friction, $Ki = B\omega$, so $i = B\omega_{ss}/K$ = **0.0476** A.
- Stall: $i = V/R$ = **6** A, torque $K \times 6$ = **0.3** N·m. The stall current is **126** times the running current.
- Time constants: $\tau_e = L/R$ = **0.5** ms; $\tau_m = RJ/(RB + K^2) = 4 \times 10^{-5}/0.00252$ = **15.87** ms.

The exact poles are the roots of $LJs^2 + (LB + RJ)s + (RB + K^2) = 0$, that is $2 \times 10^{-8}s^2 + 4.001 \times 10^{-5}s + 0.00252 = 0$: $s$ = −65.1 and −1935.4 s⁻¹, time constants **15.36** ms and **0.517** ms. The first-order model's 15.87 ms is **3.3**% long. The two exact time constants add up to almost exactly $\tau_m$ (15.36 + 0.52 = **15.88** ms): the first-order model folds the small electrical lag into the mechanical one. That is a good approximation here, where the two time constants differ by a factor of **30**.

**Units check.** $K^2/R$: (V·s/rad)²/Ω = V·s²·A/rad², the same units as $B$ (N·m·s/rad = V·A·s²/rad²).

**Sanity check.** The back-EMF damping $K^2/R$ = **1.25 × 10⁻³** N·m·s/rad is **125** times the friction $B$, so the mechanical time constant is almost exactly $RJ/K^2$ = **16** ms: electrical braking, not friction, sets how quickly the motor settles.

### Example 15-01.3 · A processor and its heat sink (tier B)

**Setup.** A processor dissipating 100 W has an illustrative two-node thermal model: junction capacitance $C_J$ = 5 J/K (die, lid and nearby spreader), junction-to-case resistance $R_{JC}$ = 0.15 K/W, heat-sink capacitance $C_H$ = 300 J/K and case-to-ambient resistance $R_{CA}$ = 0.35 K/W, with ambient $T_A$ = 30 °C. Starting from ambient, the 100 W load switches on. Find the final junction and case temperatures, the two time constants, and $T_J$ after 1 s, 5 s, 60 s and 300 s.

**Solution.** In steady state all 100 W flows through both resistances: $T_J = T_A + P(R_{JC} + R_{CA})$ = 30 + 50 = **80** °C, and $T_C = T_A + PR_{CA}$ = **65** °C.

With states $\theta_J = T_J - T_A$ and $\theta_C = T_C - T_A$, the node equations are

$$
C_J\dot\theta_J = P - \frac{\theta_J - \theta_C}{R_{JC}}, \qquad C_H\dot\theta_C = \frac{\theta_J - \theta_C}{R_{JC}} - \frac{\theta_C}{R_{CA}} ,
$$

so

$$
A = \begin{bmatrix} -1/(R_{JC}C_J) & 1/(R_{JC}C_J) \\ 1/(R_{JC}C_H) & -(1/R_{JC} + 1/R_{CA})/C_H \end{bmatrix} = \begin{bmatrix} -1.3333 & 1.3333 \\ 0.02222 & -0.03175 \end{bmatrix} \text{ s}^{-1} .
$$

Its eigenvalues are −1.356 and −0.00937 s⁻¹, time constants **0.738** s and **106.8** s. The junction first rises quickly, about $PR_{JC}$ = 15 K above the still-cool case, then both climb slowly together as the heat sink warms. Solving $\theta(t) = (e^{At} - I)A^{-1}\mathbf{b}$ with $\mathbf{b} = [P/C_J,\ 0]^T$ (02-09):

| $t$ | 1 s | 5 s | 60 s | 300 s |
|---|---|---|---|---|
| $T_J$ (°C) | **41.1** | **46.1** | **59.8** | **77.9** |

**Units check.** $1/(R_{JC}C_J)$: 1/((K/W)(J/K)) = W/J = 1/s.

**Sanity check.** The time constants are close to $R_{JC}C_J$ = **0.75** s and $R_{CA}C_H$ = **105** s: the junction charges its own small capacitance through $R_{JC}$, the heat sink charges through $R_{CA}$, and the coupling shifts each a little. A one-node model with $\tau$ ≈ 107 s would predict only **30.5** °C at 1 s. It entirely misses the fast 15 K step that matters for short bursts of load and for turbo modes.

### Example 15-01.4 · When leakage runs away (tier C)

**Setup.** A chip has dynamic power $P_d$ = 60 W and leakage $P_L(T) = 5\ \text{W} \times e^{(T - 25\,°\text{C})/30\ \text{K}}$ (illustrative values). Its one-node thermal model has $R$ = 0.5 K/W and $C$ = 50 J/K, with $T_A$ = 25 °C. Find the operating temperature, the loop gain and the effective time constant there. What is the largest $R$ for which an equilibrium exists?

**Solution.** The equilibrium solves $T = T_A + R(P_d + P_L(T))$. The right side curves upward, so there may be two solutions or none. A calculator finds the lower one by iterating the equation itself, $T_{k+1} = T_A + R(P_d + P_L(T_k))$, from the no-leakage-growth guess 57.5 °C: 62.39, 63.69, 64.08, 64.20, … Each step shrinks the error by about the loop gain $G$ (found below), which is why the iteration converges here and would fail for $G > 1$. The limit is **64.25** °C, where leakage is **18.50** W, so the chip dissipates **78.5** W. (Had leakage stayed at its 25 °C value, the chip would sit at 25 + 0.5 × 65 = **57.5** °C: the leakage feedback adds about **7** K.)

The loop gain there is $G = RP_L/T_x = 0.5 \times 18.50/30$ = **0.308**, so a small disturbance decays with $\tau_{\text{eff}} = RC/(1 - G) = 25/0.692$ = **36.1** s instead of the passive 25 s.

The second, upper solution, **124.9** °C, has $G > 1$: it is an unstable equilibrium. Above it, heat generation outruns removal and the temperature runs away. The equilibria merge, and then vanish, when the heat-removed line is tangent to the generation curve: $G = 1$, that is $RP_L = T_x$, and the equilibrium equation hold together. Substituting $RP_L = T_x$ into the equilibrium gives $T_{crit} = T_A + RP_d + T_x$; putting that temperature into $P_L(T) = T_x/R$ gives one equation for $R$,

$$
R\,e^{RP_d/T_x} = \frac{T_x}{P_{L0}}\,e^{-(T_A - T_0 + T_x)/T_x} ,
$$

here $R\,e^{2R} = 6/e = 2.207$. A few trials (or Newton's method) give the critical resistance $R_{\text{crit}}$ = **0.628** K/W, and then $T_{crit} = 25 + 0.628 \times 60 + 30$ = **92.7** °C. A heat sink only **26**% worse than the design, or a fan failure that raises $R$ beyond 0.628 K/W, leaves the chip with no thermal equilibrium at all, unless something cuts the power.

**Units check.** $RP_L/T_x$: (K/W)(W)/K, dimensionless, as a loop gain must be.

**Sanity check.** The lab simulates the nonlinear model from 25 °C: with $R$ = 0.5 it settles at 64.25 °C with the predicted time constant, and with $R$ = 0.65 the temperature passes 150 °C in finite time. This is why processors measure their own temperature and throttle (15-12).

### Example 15-01.5 · A pendulum, upright and hanging (tier C)

**Setup.** A pendulum of length 0.5 m swings under $g$ = 9.81 m/s². (a) Find the linearized natural frequency and period about $\theta^* = 0$. (b) For a release from 30° and from 90°, compare the true period with the linear one. (c) Linearize about $\theta^* = \pi$ and find how fast a small tilt grows.

**Solution.** (a) $\omega_0 = \sqrt{g/L} = \sqrt{19.62}$ = **4.429** rad/s, period $T_0 = 2\pi/\omega_0$ = **1.4185** s.

(b) The nonlinear pendulum's period from amplitude $\theta_0$ is exact in terms of the complete elliptic integral of the first kind, $T = 4\sqrt{L/g}\,K(\sin^2(\theta_0/2))$ (with $K$ written in terms of its parameter $m = k^2$). At 30°, $T$ = **1.4432** s, **1.74**% longer than the linear prediction. At 90°, $T$ = **1.6743** s, **18.0**% longer. The linear model is excellent for small swings and poor for large ones, as the Taylor estimate predicts: $\sin\theta \approx \theta$ is off by about $\theta^3/6$, the first neglected term: **4.6**% of $\theta$ at 30° and **41**% at 90° by that estimate, against exact errors of **4.5**% and **36**%. A hand check needs no elliptic integral: the first term of its series gives $T \approx T_0(1 + \theta_0^2/16)$, that is +1.71% at 30° ($\theta_0$ = 0.524 rad), against the exact 1.74%; at 90° the same term gives only +15.4% against 18.0%, because the higher terms of the series matter for large swings. (The elliptic-integral formula itself comes from integrating the energy equation over a quarter swing, beyond this course.)

(c) About $\theta^* = \pi$ the linear model is $\ddot{\delta\theta} = +\omega_0^2\,\delta\theta$, with poles at $\pm\omega_0$ = ±4.429 s⁻¹. The unstable pole makes a small tilt grow as $e^{4.429t}$, doubling every $\ln 2/4.429$ = **0.156** s. A controller must act within a fraction of that time to balance it.

**Units check.** $\sqrt{g/L}$: $\sqrt{(\text{m/s}^2)/\text{m}}$ = 1/s.

**Sanity check.** The verify script integrates the nonlinear equation numerically and measures both periods, confirming the elliptic-integral values to the published precision.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 15-01.1a | natural frequency | 20 | rad/s |
| Ex 15-01.1b | damping ratio | 0.2 | — |
| Ex 15-01.1c | static deflection | 0.05 | m |
| Ex 15-01.1d | force–voltage capacitance | 5 | mF |
| Ex 15-01.1e | force–current resistance | 0.25 | Ω |
| Ex 15-01.1f | force–current inductance | 5 | mH |
| Ex 15-01.1g | peak displacement | 0.0763 | m |
| Ex 15-01.1h | time of the peak | 0.160 | s |
| Ex 15-01.2a | steady speed | 238.1 | rad/s |
| Ex 15-01.2b | steady speed | 2274 | rpm |
| Ex 15-01.2c | running current | 0.0476 | A |
| Ex 15-01.2d | stall current | 6 | A |
| Ex 15-01.2e | stall torque | 0.3 | N·m |
| Ex 15-01.2f | electrical time constant | 0.5 | ms |
| Ex 15-01.2g | mechanical time constant | 15.87 | ms |
| Ex 15-01.2h | exact slow time constant | 15.36 | ms |
| Ex 15-01.2i | exact fast time constant | 0.517 | ms |
| Ex 15-01.3a | final junction temperature | 80 | °C |
| Ex 15-01.3b | final case temperature | 65 | °C |
| Ex 15-01.3c | fast time constant | 0.738 | s |
| Ex 15-01.3d | slow time constant | 106.8 | s |
| Ex 15-01.3e | junction at 1 s | 41.1 | °C |
| Ex 15-01.3f | junction at 5 s | 46.1 | °C |
| Ex 15-01.3g | junction at 60 s | 59.8 | °C |
| Ex 15-01.3h | junction at 300 s | 77.9 | °C |
| Ex 15-01.4a | operating temperature | 64.25 | °C |
| Ex 15-01.4b | leakage there | 18.50 | W |
| Ex 15-01.4c | loop gain | 0.308 | — |
| Ex 15-01.4d | effective time constant | 36.1 | s |
| Ex 15-01.4e | unstable equilibrium | 124.9 | °C |
| Ex 15-01.4f | critical thermal resistance | 0.628 | K/W |
| Ex 15-01.4g | temperature at the critical point | 92.7 | °C |
| Ex 15-01.5a | linear natural frequency | 4.429 | rad/s |
| Ex 15-01.5b | linear period | 1.4185 | s |
| Ex 15-01.5c | period from 30° | 1.4432 | s |
| Ex 15-01.5d | excess at 30° | 1.74 | % |
| Ex 15-01.5e | period from 90° | 1.6743 | s |
| Ex 15-01.5f | excess at 90° | 18.0 | % |
| Ex 15-01.5g | doubling time, inverted | 0.156 | s |
| Txt 15-01.a | die heat capacity | 0.122 | J/K |
| Ex 15-01.2j | first-order model's excess | 3.3 | % |
| Ex 15-01.2k | sum of the exact time constants | 15.88 | ms |
| Ex 15-01.2l | ratio of the time constants | 30 | — |
| Ex 15-01.2m | stall against running current | 126 | — |
| Ex 15-01.2n | back-EMF damping | 1.25e-3 | N·m·s/rad |
| Ex 15-01.2o | back-EMF damping against friction | 125 | — |
| Ex 15-01.2p | RJ/K² | 16 | ms |
| Ex 15-01.3i | R_JC C_J | 0.75 | s |
| Ex 15-01.3j | R_CA C_H | 105 | s |
| Ex 15-01.3k | one-node model at 1 s | 30.5 | °C |
| Ex 15-01.4h | total power | 78.5 | W |
| Ex 15-01.4i | temperature with leakage frozen | 57.5 | °C |
| Ex 15-01.4j | rise added by leakage feedback | 7 | K |
| Ex 15-01.4k | heat-sink margin to runaway | 26 | % |
| Ex 15-01.5h | sin θ linearization error at 30° | 4.6 | % |
| Ex 15-01.5i | sin θ linearization error at 90° | 41 | % |
| Ex 15-01.5j | exact sin θ error at 30° | 4.5 | % |
| Ex 15-01.5k | exact sin θ error at 90° | 36 | % |
| Txt 15-01.b | sin θ linearization error at 17° | 1.5 | % |
| Txt 15-01.c | junction rise per 0.01 K/W at 700 W | 7 | K |

## 5. Simulate it

The lab, [labs/15-01-lab](../labs/15-01-lab/README.md), provides `plants.py` (the chapter's models as state-space matrices and nonlinear right-hand sides), a notebook and two ngspice netlists. You:

1. **Simulate a mechanism as a circuit.** `analog_msd.cir` is the force–voltage circuit of Example 15-01.1; the notebook integrates the mechanical equation and overlays the two.
2. **Spin up the motor** with the full second-order model and the first-order approximation.
3. **Heat the processor.** `thermal_two_node.cir` is Example 15-01.3's network in ngspice, with temperatures as voltages and heat flows as currents.
4. **Push the leakage loop** past its critical resistance and watch it run away.

**Guided exercise (predict, then run).** **Before Part 3,** predict $T_J$ 1 s after the load step from a one-node model with $\tau$ = 107 s, then from the two-node model. (One node: about 30.5 °C, since $50 \times (1 - e^{-1/107})$ ≈ 0.5 K. Two nodes: 41.1 °C. The fast junction node is invisible to the one-node model.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Model order (more states) | Fidelity: captures fast modes such as the junction's thermal rise or the motor's electrical lag | Harder analysis and design; more parameters to identify | Control engineer |
| Linear model about one operating point | Simple design and analysis with the tools of this course | Valid only near that point; may miss runaway or saturation | Control engineer |
| Lumped against distributed thermal model | A few resistances and capacitances, measurable | Misses spreading and hot spots; needs calibration against measurement | Thermal and package engineers |
| Lower thermal resistance (bigger heat sink, better TIM, liquid cooling) | Lower junction temperature; more margin against runaway | Cost, size, weight, fan or pump power and noise | System and thermal architects |
| Larger thermal capacitance | Absorbs short bursts (turbo, sprint) | Slower cool-down; does not change sustained temperature | Product architect |
| Higher motor constant $K$ | More torque per ampere, more back-EMF damping | Lower top speed per volt ($\approx V/K$); bigger magnet or more turns | Motor and drive designers |

## 7. Numbers to know

| Quantity | Typical value | Source |
|---|---|---|
| Silicon thermal conductivity, 300 K | 130–148 W/(m·K) (sources differ with sample purity) | [2, R-228] |
| Silicon specific heat, density | 0.7 J/(g·K); 2.329 g/cm³ | [2, R-228] |
| Heat capacity of a 10 × 10 × 0.75 mm³ die | about 0.12 J/K | Derived (§3.6) |
| Thermal time constants of a chip's cooling path | milliseconds (die), seconds (spreader), minutes (heat sink) | Example 15-01.3 (illustrative) |
| Motor: stall current against running current | often tens of times larger | Example 15-01.2 |
| Linearization of $\sin\theta$ | error about 1.5% of θ at 17°, 4.6% at 30° | §3.7 (from $\theta^2/6$) |
| Pendulum period error from amplitude | +1.7% at 30°, +18% at 90° | Example 15-01.5 |

## 8. Common mistakes

- **Forgetting the reference node.** Every mass in the force–current analogy, and every thermal capacitance, is a capacitor to ground (the inertial frame or the reference temperature). Connecting it between two moving or heated nodes gives wrong dynamics.
- **Mixing $K_t$ and $K_e$ units.** In SI units they are equal (N·m/A = V·s/rad). Data sheets often give $K_e$ in V per 1000 rpm; convert before equating.
- **Using a one-node thermal model for fast events.** It gets the final temperature right and the first seconds wrong (Example 15-01.3).
- **Treating $R_{\theta JA}$ as a package property.** It is measured on a standard board under standard conditions; your board and airflow differ [1, R-227].
- **Linearizing at the wrong point,** or forgetting that the linear model changes with the operating point. A controller tuned at one temperature or speed may misbehave at another.
- **Trusting a linearization near a tangency.** At $G \approx 1$ the linear model predicts a very slow mode, but the real system may have no equilibrium nearby at all.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Thermal metrics have conditions.** TI's application note on package thermal metrics (revised March 2024) stresses that $R_{\theta JA}$ "is not a characteristic of the package by itself but of the package, PCB, and other environmental factors", and recommends using it to compare packages. For estimating junction temperature in a system it describes the $\Psi_{JT}$ metric (JESD51-2), which is "not a true thermal resistance" because only part of the heat flows through the package top [1, R-227] **[Established]**.
- **Accelerator power makes every 0.01 K/W count.** NVIDIA lists the H100 SXM at up to 700 W, configurable (14-13, [R-220](../../../reference/research-log.md#r-220--nvidia-h100-hopper-specifications)) **[Established]**. At that power, every 0.01 K/W of thermal resistance is **7** K of junction temperature, which is why accelerator thermal design is now a system-level discipline (Course 25).
- **Models are fitted, not derived.** Industrial practice builds detailed thermal models with finite-element tools and reduces them to compact resistor–capacitor networks whose parameters are fitted to measured or simulated heating curves, so that system designers can simulate them quickly. The reduction step is exactly the model reduction of §3.5 **[Established]** (textbook practice; vendor-specific tools vary).

### Why it matters commercially

- **Sustained performance is a thermal number.** A phone or laptop chip's sustained clock is set by the power its enclosure can shed at a skin-temperature limit; peak clocks last as long as the thermal capacitance allows (15-12, Course 25).
- **Cooling cost scales with power.** Heat that must be removed sets the size of heat sinks, fans, cold plates and pumps, and the power those fans and pumps draw; the datacenter chapters quantify it (Course 22, 22-10) **[Established]** as a principle, without a market-share figure here.
- **Motor-driven products** (fans, pumps, HDD actuators, drones, robots) are sold on response time and efficiency, which come straight from $K$, $R$ and $J$.

### Marketing vs Reality

- **"Runs cool at 45 °C/W."** *Reality:* that $R_{\theta JA}$ is for a JEDEC test board; on a small, dense board the figure can be much worse. *Sanity check:* ask for the board and airflow conditions, and for $\Psi_{JT}$ or $R_{JC}$ to use with your own heat path [1, R-227].
- **"Peak performance of X."** *Reality:* if the thermal path cannot remove the power, the peak lasts only seconds. *Sanity check:* ask for sustained performance after the thermal time constants have elapsed, minutes, not seconds.
- **"Our model predicts temperature within 1 °C."** *Reality:* only near the operating points where it was calibrated. *Sanity check:* ask at which powers and airflows it was validated.

### Questions for engineering leaders

1. **"What is the junction temperature at sustained full load, and what is the margin to the limit?"**
   *Strong:* a number from measurement, with the thermal network behind it and the worst-case ambient. *Evasive:* "it is within spec."
2. **"How long can the part sustain peak power before throttling?"**
   *Strong:* a time derived from the thermal capacitances and the power, validated on hardware. *Evasive:* only peak numbers.
3. **"Is there any operating corner where leakage feedback threatens runaway?"**
   *Strong:* the loop gain $R\,dP/dT$ at the hottest corner, with throttling as a backstop. *Evasive:* "leakage is small."
4. **"Which model does the controller use, and over what range was it validated?"**
   *Strong:* the plant model, its operating points and its measured error. *Evasive:* "it is tuned empirically."

## 10. Concept check

**Q1.** Why can a mass–spring–damper oscillate while a passive thermal network cannot?

<details><summary>Answer</summary>

Oscillation needs two kinds of energy store exchanging energy (kinetic and potential, or magnetic and electric). A thermal network has only one kind, heat stored in thermal capacitances, and no thermal inductance, so all its poles are real and its responses are sums of decaying exponentials.

</details>

**Q2.** In the force–current analogy, why does every mass become a capacitor to ground?

<details><summary>Answer</summary>

A mass's velocity (the across variable) is measured relative to an inertial frame, the mechanical "ground". Its element law $f = m\,dv/dt$ matches $i = C\,dv/dt$ for a capacitor between the node and ground.

</details>

**Q3.** Why are a DC motor's torque constant and back-EMF constant equal in SI units?

<details><summary>Answer</summary>

Energy conservation: the electrical power absorbed by the back-EMF, $K_e\omega i$, must equal the mechanical power delivered, $K_ti\omega$, so $K_t = K_e$.

</details>

**Q4.** Why does a stalled motor draw so much more current than a running one?

<details><summary>Answer</summary>

At stall there is no back-EMF, so the whole supply voltage drives current through the small armature resistance: $V/R$. Running, the back-EMF nearly cancels the supply.

</details>

**Q5.** A one-node thermal model has $\tau$ = 100 s. Why might it badly underestimate the junction temperature 1 s after a load step?

<details><summary>Answer</summary>

The junction has a small local thermal capacitance and a resistance to the case; it rises by about $PR_{JC}$ within a few seconds (time constant about 0.74 s in Example 15-01.3), long before the bulk heats. A one-node model lumps all capacitance together and misses this fast mode.

</details>

**Q6.** What does the loop gain $G = R\,dP/dT$ tell you about a chip's thermal stability?

<details><summary>Answer</summary>

It is the fraction by which a temperature rise feeds back into itself through extra leakage. For $G < 1$ disturbances decay, with time constant $RC/(1 - G)$. An equilibrium with $G > 1$ exists but is unstable. When the thermal resistance reaches the critical value at which $G = 1$, the stable and unstable equilibria merge; above it no equilibrium exists and the temperature runs away.

</details>

**Q7.** Why is the inverted pendulum unstable, in terms of its linearized model?

<details><summary>Answer</summary>

Linearized about $\theta = \pi$, gravity pushes the pendulum further from upright in proportion to its tilt: $\ddot{\delta\theta} = +(g/L)\delta\theta$. That has a real pole at $+\sqrt{g/L}$, in the right half-plane, so small tilts grow exponentially.

</details>

Practice: [Problems 15-01](../problems/15-01-problems.md) · [Solutions](../solutions/15-01-solutions.md)

## 11. Key terms

[Plant](../../../reference/glossary.md#plant) · [State variable](../../../reference/glossary.md#state-variable) · [State-space model](../../../reference/glossary.md#state-space-model) · [Force–voltage analogy](../../../reference/glossary.md#force-voltage-analogy) · [Force–current analogy](../../../reference/glossary.md#force-current-analogy) · [Torque constant](../../../reference/glossary.md#torque-constant) · [Back-EMF](../../../reference/glossary.md#back-emf) · [Mechanical time constant](../../../reference/glossary.md#mechanical-time-constant) · [Model reduction](../../../reference/glossary.md#model-reduction) · [Thermal resistance](../../../reference/glossary.md#thermal-resistance) · [Thermal capacitance](../../../reference/glossary.md#thermal-capacitance) · [Junction temperature](../../../reference/glossary.md#junction-temperature) · [Operating point](../../../reference/glossary.md#operating-point) · [Linearization](../../../reference/glossary.md#linearization) · [Jacobian](../../../reference/glossary.md#jacobian) · [Thermal runaway](../../../reference/glossary.md#thermal-runaway)

## 12. Connections

- **Builds on:** systems of ODEs and the matrix exponential ([02-09](../../02-complex-numbers-des-and-linear-algebra/chapters/02-09-systems-of-odes-and-matrix-exponential.md)); mechanics and the force–voltage analogy ([04-01](../../04-physics-for-ee/chapters/04-01-mechanics-essentials.md)); motors and back-EMF ([04-07](../../04-physics-for-ee/chapters/04-07-faraday-lenz-and-inductance.md)); RLC transients ([07-03](../../07-circuit-analysis-2-transient-and-ac/chapters/07-03-second-order-rlc-transients.md)); small-signal linearization ([10-04](../../10-electronics-1/chapters/10-04-small-signal-models.md)); transfer functions ([11-08](../../11-signals-and-systems/chapters/11-08-laplace-transform-and-system-functions.md)); thermal runaway in output stages ([12-07](../../12-electronics-2/chapters/12-07-output-stages.md)).
- **Next:** [15-02 Transfer Functions and Block Diagrams](15-02-transfer-functions-and-block-diagrams.md), which connects these models into systems.
- **Used later:** time response from pole locations ([15-03](15-03-time-response.md)); loop gain and sensitivity ([15-04](15-04-feedback-and-steady-state-error.md)); state space, controllability and pole placement ([15-10](15-10-state-space-introduction.md)); thermal and regulator loops ([15-12](15-12-control-applications-pll-regulators-thermal.md)); converter dynamics ([22-07](../../22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md)); electric machines ([22-11](../../22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md)); thermal engineering of packages ([25-08](../../25-fabrication-packaging-test-and-reliability/chapters/25-08-thermal-engineering.md)).

## 13. Further study

- G. F. Franklin, J. D. Powell and A. Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 2 (dynamic models of mechanical, electrical, electromechanical and heat-flow systems) and the linearization section of ch. 9.
- K. Ogata, *Modern Control Engineering*, ch. 3 (mathematical modeling of mechanical and electrical systems) and ch. 4 (fluid and thermal systems).
- K. J. Åström and R. M. Murray, *Feedback Systems*, ch. 2–3 (system modeling and examples; free online).
- MIT OpenCourseWare 2.04A, *Systems and Controls*: the modeling lectures.

## 14. Sources

1. D. Edwards and H. Nguyen, "Semiconductor and IC Package Thermal Metrics," Texas Instruments application note SPRA953D (Dec 2003, revised Mar 2024). [R-227](../../../reference/research-log.md#r-227--semiconductor-and-ic-package-thermal-metrics-ti-spra953d)
2. Ioffe Institute, *New Semiconductor Materials: Characteristics and Properties*, silicon thermal and mechanical properties; V. Palankovski, doctoral thesis (TU Wien), silicon thermal conductivity. [R-228](../../../reference/research-log.md#r-228--silicon-thermal-properties)

The modeling methods, analogies and linearization are textbook material (Further study). Every number in the examples is recomputed by the verify script, by numerical integration of the original equations, eigenvalues, root finding and ngspice.
