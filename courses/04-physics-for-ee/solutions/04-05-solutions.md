# Solutions 04-05 · Current, Resistance and Conduction

Problems: [04-05 problems](../problems/04-05-problems.md) · Chapter: [04-05](../chapters/04-05-current-resistance-and-conduction.md). Every number below is recomputed by [verify_04_05.py](../verify/verify_04_05.py).

---

## Solutions

### Solution 04-05.1

(a) $I = Q/t = 3/2 = $ **1.5 A**.

(b) $1.5/1.602\times10^{-19} = $ **9.362×10¹⁸** electrons per second.

(c) 3000 mAh = 3 A × 3600 s = **10,800 C**.

### Solution 04-05.2

(a) $J = 10/2.5 = $ **4 A/mm²**, which is $4\times10^6$ A/m².

(b) $v_d = J/(ne) = 4\times10^6/(8.491\times10^{28}\times1.602\times10^{-19}) = $ **294.0 µm/s**: about a meter an hour.

### Solution 04-05.3

(a) $R = \rho L/A = 1.68\times10^{-8}\times100/1.5\times10^{-6} = $ **1.12 Ω**.

(b) $A = \pi(0.25\times10^{-3})^2 = 1.963\times10^{-7}$ m², so $R = 1.10\times10^{-6}\times1/1.963\times10^{-7} = $ **5.602 Ω**: nichrome is 65 times more resistive than copper, which is why heaters use it.

### Solution 04-05.4

(a) $\rho = 1.68\times(1 + 0.00393\times80) = $ **2.208 µΩ·cm**.

(b) $\tau = m/(ne^2\rho) = 9.109\times10^{-31}/(8.491\times10^{28}\times2.567\times10^{-38}\times2.208\times10^{-8}) = $ **18.93 fs**.

(c) $\lambda = v_F\tau = 1.57\times10^6\times18.93\times10^{-15} = $ **29.71 nm**. (The Fermi speed barely changes with temperature; the extra collisions shorten τ.)

### Solution 04-05.5

(a) $\rho = 1/(e\,n\,\mu_n) = 1/(1.602\times10^{-19}\times10^{15}\times1400) = $ **4.458 Ω·cm**.

(b) $R_s = \rho/t = 4.458/(2\times10^{-4}\ \text{cm}) = $ **2.229×10⁴ Ω/□**.

(c) $10\times22.29\ \text{kΩ} = $ **222.9 kΩ**.

(d) $1/(1.602\times10^{-19}\times10^{15}\times470) = $ **13.28 Ω·cm**: holes are less mobile, so p-type silicon is about three times more resistive at the same doping.

### Solution 04-05.6

(a) $L/W = 50$ squares, so $R = 50\times100 = $ **5000 Ω**.

(b) $10\ \text{kΩ}/100\ \Omega$ = 100 squares; at 2 µm width that is **200 µm** long (in practice folded into a meander).

### Solution 04-05.7

$T = 20 + (4.80/4.00 - 1)/0.00393 = $ **70.89 °C**.

### Solution 04-05.8

(a) $I_{\max} = \sqrt{P/R} = \sqrt{0.025} = $ **0.1581 A**; $V_{\max} = \sqrt{PR} = $ **1.581 V**.

(b) $p = \rho J^2 = 1.68\times10^{-8}\times(4\times10^6)^2 = $ **2.688×10⁵ W/m³**. Per meter of 2.5 mm² wire: $2.688\times10^5\times2.5\times10^{-6} = $ **0.672 W/m**, which the insulation and air must carry away.

### Solution 04-05.9

(a) $3 - 1 - 1.5 = $ **0.5 mA** net inflow.

(b) $dV/dt = I/C = 0.5\times10^{-3}/10\times10^{-12} = 5\times10^7$ V/s = **50 V/µs**.

(c) KCL (currents into a node sum to zero) holds only when the node's stored charge is negligible. With capacitance, the imbalance goes into charging it; strictly, the capacitor's current is just another branch, and with it included KCL is restored.

### Solution 04-05.10

(a) $\Delta V = IR = 100\times0.2\times10^{-3} = $ **20 mV**, 2% of the rail.

(b) $P = I^2R = 10^4\times0.2\times10^{-3} = $ **2 W**.

(c) $R = 0.01\times1/100 = $ **0.1 mΩ**. Sub-milliohm budgets are why high-current processors use many parallel power pins, thick package planes and voltage regulators close to the die.

### Solution 04-05.11

(a) With $w(x) = w_1 + (w_2 - w_1)x/L$ and $dx = L\,dw/(w_2 - w_1)$,

$$
R = \int_0^L\frac{\rho\,dx}{t\,w(x)} = \frac{\rho L}{t(w_1 - w_2)}\ln\frac{w_1}{w_2} = \frac{1.68\times10^{-8}\times0.05\times\ln2}{34.06\times10^{-6}\times0.25\times10^{-3}} ,
$$

which is **68.38 mΩ**.

(b) At the average width 0.375 mm: $\rho L/(tw) = $ **65.77 mΩ**, 4% low. The narrow end counts for more, because resistance adds as $1/w$.

### Solution 04-05.12

(a) Current crosses cylindrical shells of area $2\pi rL$ in series: $R = \int_a^b\rho\,dr/(2\pi rL) = \rho\ln(b/a)/(2\pi L) = 10^{13}\times\ln3.278/(2\pi\times1.5) = $ **1.260×10¹² Ω**.

(b) $C = 2\pi\varepsilon_r\varepsilon_0L/\ln(b/a) = $ **158.2 pF**.

(c) Between two electrodes in one uniform material, the field is the same whether the material conducts or stores charge. With $\pm Q$ on the electrodes, $C = Q/V$ where $Q = \oint\varepsilon\vec E\cdot\hat n\,dA$; the leakage current is $I = \oint\sigma\vec E\cdot\hat n\,dA = (\sigma/\varepsilon)Q$, so $R = V/I = \varepsilon V/(\sigma Q) = \varepsilon/(\sigma C)$, and $RC = \varepsilon/\sigma = \rho\varepsilon$. Here $RC = 10^{13}\times2.25\times8.854\times10^{-12} = $ **199.2 s**, matching (a)×(b). This is the time a charged cable takes to discharge through its own insulation.

### Solution 04-05.13

(a) Copper: $1.68\times10^{-8}/562.5\times10^{-18}$ = **29.87 Ω/µm**. Molybdenum: $5.3\times10^{-8}/800\times10^{-18}$ = **66.25 Ω/µm**. With bulk values, copper wins easily.

(b) Copper: $6.0\times10^{-8}/562.5\times10^{-18}$ = **106.7 Ω/µm**. Molybdenum: $9.0\times10^{-8}/800\times10^{-18}$ = **112.5 Ω/µm**. Nearly even.

(c) Molybdenum wins when $\rho_{\text{Cu}}/562.5 > 9.0/800$, i.e. $\rho_{\text{Cu}} > 9.0\times562.5/800 = $ **6.328 µΩ·cm**. As lines narrow, copper's barrier tax and its long mean free path (stronger size effect) push it toward this crossover, which is why the industry is evaluating barrierless metals.

### Solution 04-05.14

(a) $w = I/(J_{\max}t) = 2\times10^{-3}/(10^{10}\ \text{A/m}^2\times10^{-7}\ \text{m}) = $ **2 µm**.

(b) $R = \rho L/(wt) = 1.68\times10^{-8}\times10^{-4}/(2\times10^{-6}\times10^{-7}) = $ **8.4 Ω**, so the drop is **16.8 mV**. Even when electromigration is satisfied, IR drop can force wider rails.

### Solution 04-05.15

(a) With $E = \text{Re}(\mathbf Ee^{j\omega t})$ and $v = \text{Re}(\mathbf Ve^{j\omega t})$, the ODE gives $j\omega m\mathbf V = -e\mathbf E - m\mathbf V/\tau$, so $\mathbf V = -e\tau\mathbf E/[m(1 + j\omega\tau)]$. Then $\mathbf J = -ne\mathbf V = \sigma_0\mathbf E/(1 + j\omega\tau)$ with $\sigma_0 = ne^2\tau/m$.

(b) The phase lag is $\arctan(\omega\tau)$, 45° at $\omega\tau = 1$: $f = 1/(2\pi\tau) = 1/(2\pi\times24.88\times10^{-15}) = $ **6.398 THz**.

(c) At 10 GHz, $\omega\tau \approx 0.0016$: copper's conductivity is essentially its DC value. What changes at gigahertz is not σ but *where* current flows: the skin effect confines it near the surface ([04-07](../chapters/04-07-faraday-lenz-and-inductance.md)).

### Solution 04-05.16

(a) $d/dk\,[k t_b + 0.38RC/k] = t_b - 0.38RC/k^2 = 0$ gives $k = \sqrt{0.38RC/t_b} = \sqrt{0.38\times3702/10} = $ **11.86**.

(b) With 12: $12\times10 + 0.38\times3702/12 = 120 + 117.2 = $ **237.2 ps**.

(c) Unrepeated: $0.38\times3702 = $ **1407 ps**, about six times slower. The optimum balances repeater delay against wire delay, each about half the total.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 04-05.1a | current | 1.5 | A |
| 04-05.1b | electrons per second in 1.5 A | 9.362×10^18 | s⁻¹ |
| 04-05.1c | charge in 3000 mAh | 10800 | C |
| 04-05.2a | current density | 4 | A/mm² |
| 04-05.2b | drift speed | 294.0 | µm/s |
| 04-05.3a | copper wire resistance | 1.12 | Ω |
| 04-05.3b | nichrome wire resistance | 5.602 | Ω |
| 04-05.4a | copper resistivity at 100 °C | 2.208 | µΩ·cm |
| 04-05.4b | mean free time at 100 °C | 18.93 | fs |
| 04-05.4c | mean free path at 100 °C | 29.71 | nm |
| 04-05.5a | n-type resistivity | 4.458 | Ω·cm |
| 04-05.5b | sheet resistance | 2.229×10^4 | Ω/□ |
| 04-05.5c | 10-square resistor | 222.9 | kΩ |
| 04-05.5d | p-type resistivity | 13.28 | Ω·cm |
| 04-05.6a | thin-film resistor | 5000 | Ω |
| 04-05.6b | length for 10 kΩ | 200 | µm |
| 04-05.7a | coil temperature | 70.89 | °C |
| 04-05.8a | maximum current | 0.1581 | A |
| 04-05.8b | maximum voltage | 1.581 | V |
| 04-05.8c | power density at 4 A/mm² | 2.688×10^5 | W/m³ |
| 04-05.8d | heat per meter | 0.672 | W/m |
| 04-05.9a | net current into the node | 0.5 | mA |
| 04-05.9b | voltage slew | 50 | V/µs |
| 04-05.10a | IR drop | 20 | mV |
| 04-05.10b | power lost | 2 | W |
| 04-05.10c | resistance for 1% drop | 0.1 | mΩ |
| 04-05.11a | tapered trace resistance | 68.38 | mΩ |
| 04-05.11b | uniform trace at average width | 65.77 | mΩ |
| 04-05.12a | leakage resistance | 1.260×10^12 | Ω |
| 04-05.12b | cable capacitance | 158.2 | pF |
| 04-05.12c | RC time | 199.2 | s |
| 04-05.13a | Cu with barrier, bulk ρ | 29.87 | Ω/µm |
| 04-05.13b | Mo barrierless, bulk ρ | 66.25 | Ω/µm |
| 04-05.13c | Cu with barrier, 6.0 µΩ·cm | 106.7 | Ω/µm |
| 04-05.13d | Mo barrierless, 9.0 µΩ·cm | 112.5 | Ω/µm |
| 04-05.13e | crossover copper resistivity | 6.328 | µΩ·cm |
| 04-05.14a | minimum rail width | 2 | µm |
| 04-05.14b | rail resistance per 100 µm | 8.4 | Ω |
| 04-05.14c | rail drop at 2 mA | 16.8 | mV |
| 04-05.15a | 45° frequency in copper | 6.398 | THz |
| 04-05.16a | optimal number of repeaters | 11.86 | — |
| 04-05.16b | delay with 12 repeaters | 237.2 | ps |
| 04-05.16c | unrepeated delay | 1407 | ps |
