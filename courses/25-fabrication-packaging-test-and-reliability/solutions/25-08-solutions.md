# Solutions 25-08 · Thermal Engineering

Problems: [25-08 problems](../problems/25-08-problems.md) · Chapter: [25-08](../chapters/25-08-thermal-engineering.md)

Every number is recomputed by [verify_25_08.py](../verify/verify_25_08.py).

---

## Solutions

### Solution 25-08.1

$R = 100 \times 10^{-6}/(80 \times 8.0 \times 10^{-4})$ = **0.00156** K/W, **4.0** times lower than the polymer TIM despite being four times thicker. Metal TIMs are standard on high-power server parts for this reason; their costs are assembly complexity and, for liquid metals, containment.

### Solution 25-08.2

(a) Excess flux $q = 2/(\pi \times 1^2)$ = **0.637** W/mm²; $\Delta T_{centre} = qa/k = 0.637 \times 10^6 \times 10^{-3}/150$ = **4.24** K; $R_{sp} = 8/(3\pi^2 \times 150 \times 10^{-3})$ = **1.80** K/W. Doubling the radius at fixed power halves the rise.

(b) $2.55 \times \pi \times 1^2$ = **8.0** W; $\Delta T_{centre} = 2.546 \times 10^6 \times 10^{-3}/150$ = **17.0** K. At fixed power density the rise doubles with the radius: large high-density blocks are the hardest to cool.

### Solution 25-08.3

(a) $3 \times 10^{-3}/(400\pi \times 0.005^2)$ = **95.5** mK/W.

(b) $3 \times 10^{-3}/(400\pi \times 0.005 \times 0.008)$ = **59.7** mK/W.

(c) The finite-difference solve (and the verify script's series) give **66.3** mK/W.

(d) $(59.7 - 66.3)/66.3$ = **−10**%. With a smaller source the lid is thick relative to the die, and the heat spreads less than the 45° cone assumes: the rule underestimates the resistance, here by 10%, so it is optimistic. It also no longer matches the "thin lid" condition.

### Solution 25-08.4

(a) Assume a thin fin (temperature uniform across its thickness), constant $k$ and $h$, steady state and unit depth. For a slice $dx$: heat conducted in at $x$, $-kt_f\,\theta'(x)$, minus heat conducted out at $x + dx$, equals heat convected from two faces, $2h\theta\,dx$. So $kt_f\theta'' = 2h\theta$, or $\theta'' = m^2\theta$ with $m^2 = 2h/(kt_f)$. The general solution is $C_1\cosh mx + C_2\sinh mx$; $\theta(0) = \theta_b$ and $\theta'(L) = 0$ give $\theta = \theta_b\cosh m(L - x)/\cosh mL$. The base heat is $-kt_f\theta'(0) = kt_fm\theta_b\tanh mL$; dividing by the ideal $2hL\theta_b$ and using $kt_fm = 2h/m$ gives $\eta_f = \tanh(mL)/mL$.

(b) $m = \sqrt{100/(400 \times 0.001)}$ = 15.8 m⁻¹, $mL$ = 0.632, $\eta_f$ = **0.885**.

(c) $mL = 22.4 \times 0.080$ = 1.79, $\eta_f$ = **0.529**. Copper raises efficiency at the cost of weight and price; doubling the height doubles the area but only raises the heat removed by $2 \times 0.529/0.798$ = **1.33** times. Fins should stop near $mL \approx 1$, beyond which added height buys little.

### Solution 25-08.5

$2400/(1206 \times 20)$ = **0.0995** m³/s = **211** CFM.

### Solution 25-08.6

$T_J - T_{in} = P[1/(2\rho c_p\dot{V}) + R]$, so $P = 60/[1/(2\rho c_p\dot{V}) + 0.035]$.

(a) $\rho c_p\dot{V}$ = 139.3 W/K: $P$ = **1.55e3** W.

(b) 278.7 W/K: $P$ = **1.63e3** W. Doubling the flow buys only 5%: the 0.035 K/W of conduction and convection, not the coolant rise, limits the power.

### Solution 25-08.7

(a) $30 + 8.25 + 2300 \times 0.035$ = **119** °C: still too hot.

(b) $105 - 8.25 - 80.5$ = **16.2** °C: chilled water. A 2.3 kW part on a 0.035 K/W path needs either a much better path or a cold facility loop, which gives back the dry-cooler savings.

### Solution 25-08.8

(a) $72 \times 2.5$ = **180** kW of GPU board power at maximum TBP (our arithmetic; AMD gives no rack figure).

(b) $180{,}000/(4.18 \times 10^6 \times 10) \times 60{,}000$ = **258** L/min.

### Solution 25-08.9

(a) $10^7/9216$ = **1.09** kW per chip. (b) $192 \times 9216$ GB = **1.77** PB. (c) $4614 \times 9216$ TFLOPS = **42.5** EFLOPS, matching Google's figure. The per-chip power includes host CPUs, networking, cooling pumps and conversion losses spread over the chips; a chip TDP covers only the package.

### Solution 25-08.10

(a) $125/90 - 1$ = **39**% and $136/101 - 1$ = **35**% more racks, as NVIDIA states.

(b) $10{,}000/136$ = **73** racks before; $10{,}000/101$ = **99** after. Provisioning to measured rather than nameplate power is worth a third more capacity in the same building, if the software reliably holds the cap.

### Solution 25-08.11

(a) **102** °C. (b) **90.2** °C. A higher activation energy makes damage more sensitive to temperature, so the hottest interval dominates further and the equivalent temperature rises toward 125 °C; a lower one weights all intervals more evenly and pulls it toward the mean of 78 °C.

### Solution 25-08.12

$1.10/1.20 - 1$ = **−8.3**%: the higher profile buys throughput at worse efficiency, which matters when a facility is power-limited.

### Solution 25-08.13

(a) $100/(2.26 \times 10^6)$ = **4.4e-5** kg/s, about 44 mg/s.

(b) $2.26 \times 10^6/(4180 \times 10)$ = **54** times. A small vapor flow moves large heat with almost no temperature drop, which is why a vapor chamber spreads better than solid copper.

### Solution 25-08.14

(a) $A_c$ = 0.3 mm², $P_w$ = 4.3 mm, $D_h = 4 \times 0.3/4.3$ = **0.279** mm. (b) The flow per channel halves with the area, so $v$ stays **0.556** m/s and $Re$ = **239**. (c) $h = 4.36 \times 0.63/2.79 \times 10^{-4}$ = **9.84e3** W/(m²·K). (d) $A = 200 \times 4.3 \times 40$ mm² = **0.0344** m² and $R$ = **0.00295** K/W. (e) $\Delta p$ = **5.94** kPa and the pump power **0.198** W.

Halving the width raises $h$ by **1.87** times and, with nearly twice the wetted area, cuts the ideal-wall resistance by **3.5** times, but the pressure drop rises **3.5** times. The thinner walls would also be poorer fins, so part of the thermal gain is lost.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 25-08.1a | indium TIM resistance | 0.00156 | K/W |
| 25-08.1b | improvement over polymer | 4.0 | |
| 25-08.2a | power density | 0.637 | W/mm² |
| 25-08.2a1 | centre rise | 4.24 | K |
| 25-08.2a2 | spreading resistance | 1.80 | K/W |
| 25-08.2b | power at original density | 8.0 | W |
| 25-08.2b1 | centre rise | 17.0 | K |
| 25-08.3a | 1D footprint | 95.5 | mK/W |
| 25-08.3b | 45° estimate | 59.7 | mK/W |
| 25-08.3c | exact | 66.3 | mK/W |
| 25-08.3d | 45° error | -10 | % |
| 25-08.4b | copper fin efficiency | 0.885 | |
| 25-08.4b0 | copper m | 15.8 | 1/m |
| 25-08.4b1 | copper mL | 0.632 | |
| 25-08.4c | 80 mm aluminium fin efficiency | 0.529 | |
| 25-08.4c0 | mL | 1.79 | |
| 25-08.4c1 | heat gain from doubling height | 1.33 | |
| 25-08.5a | airflow | 0.0995 | m³/s |
| 25-08.5b | airflow | 211 | CFM |
| 25-08.6a | max power, 2 L/min | 1.55e3 | W |
| 25-08.6a0 | flow heat capacity, 4 L/min | 278.7 | W/K |
| 25-08.6b | max power, 4 L/min | 1.63e3 | W |
| 25-08.6c | gain from doubling flow | 5 | % |
| 25-08.7a | junction at 30 °C inlet | 119 | °C |
| 25-08.7b | inlet for 105 °C | 16.2 | °C |
| 25-08.8a | GPU board power | 180 | kW |
| 25-08.8b | water flow | 258 | L/min |
| 25-08.9a | power per chip | 1.09 | kW |
| 25-08.9b | pod HBM | 1.77 | PB |
| 25-08.9c | pod compute | 42.5 | EFLOPS |
| 25-08.10a | more GB200 racks | 39 | % |
| 25-08.10a1 | more Vera Rubin racks | 35 | % |
| 25-08.10b | racks before | 73 | |
| 25-08.10b1 | racks after | 99 | |
| 25-08.11a | equivalent temperature, 1.0 eV | 102 | °C |
| 25-08.11b | equivalent temperature, 0.4 eV | 90.2 | °C |
| 25-08.12a | performance per watt change | -8.3 | % |
| 25-08.13a | evaporating mass flow | 4.4e-5 | kg/s |
| 25-08.13a1 | evaporating mass flow | 44 | mg/s |
| 25-08.13b | latent against sensible | 54 | |
| 25-08.14a | hydraulic diameter | 0.279 | mm |
| 25-08.14b | velocity | 0.556 | m/s |
| 25-08.14b1 | Reynolds number | 239 | |
| 25-08.14c | heat transfer coefficient | 9.84e3 | W/(m²·K) |
| 25-08.14d | wetted area | 0.0344 | m² |
| 25-08.14d1 | resistance | 0.00295 | K/W |
| 25-08.14e | pressure drop | 5.94 | kPa |
| 25-08.14e1 | pump power | 0.198 | W |
| 25-08.14f | h ratio | 1.87 | |
| 25-08.14f1 | resistance ratio | 3.5 | |
| 25-08.14f2 | pressure ratio | 3.5 | |
