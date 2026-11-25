# Solutions 23-03 · DRAM Cells, Arrays and Refresh

Problems: [23-03 problems](../problems/23-03-problems.md) · Chapter: [23-03](../chapters/23-03-dram-cells-arrays-refresh.md)

Every number is recomputed by [verify_23_03.py](../verify/verify_23_03.py).

---

## Solutions

### Solution 23-03.1

The precharge level is 0.55 V and the transfer ratio is $C_s/(C_s + C_{BL})$ (§3.1).

(a) $(1.1 - 0.55) \times 10/70$ = **78.6** mV; (b) $(0 - 0.55) \times 10/70$ = **−78.6** mV; (c) $10/70$ = **0.143**.

(d) $Q = 10\ \text{fF} \times 1.1\ \text{V}$ = 11 fC, or $11 \times 10^{-15}/1.602 \times 10^{-19}$ = **6.87** × 10⁴ electrons.

A larger cell on a longer bitline gives slightly less signal than Example 23-03.1, because the ratio fell from 1/6 to 1/7.

### Solution 23-03.2

(a) $2^{10} \times 16$ = **16384** bits, a 2 KB page.

(b) $8 \times 131{,}072 \times 16{,}384 = 2^3 \times 2^{17} \times 2^{14} = 2^{34}$ = **17179869184** bits = 16 Gib. ✓

(c) $131{,}072/8{,}192$ = **16** rows per bank per REF.

(d) A BL8 burst moves 8 transfers × 16 bits = 128 bits, so $128/16{,}384$ = **0.781** % of the page.

The x16 part trades banks for a wider page: it has half the banks of the x8 part, so it has less bank parallelism, but each activation opens twice as many bits.

### Solution 23-03.3

(a) $32\ \text{ms}/8192$ = **3.906** µs; (b) $16\ \text{ms}/8192$ = **1.953** µs.

(c) $295/3906.25$ = **7.55** %; (d) $295/1953.125$ = **15.1** %.

DDR5's shorter window doubles the refresh rate compared with DDR4 at the same temperature. Same-bank refresh (§3.7) exists to keep this overhead from showing up as lost bandwidth.

### Solution 23-03.4

From §3.2, $C_{BL,max} = C_s(V_{sig}/\Delta V_{min} - 1)$, with $V_{sig}/\Delta V_{min} = 0.40/0.05 = 8$.

(a) $7 \times (8 - 1)$ = **49.0** fF. (b) $N \le (49.0 - 3)/0.07$ = **657.1**, so a power-of-two design uses 512.

(c) $5 \times 7$ = **35.0** fF, so $N \le (35.0 - 3)/0.07$ = **457.1**: the design drops to 256.

(d) 512 cells give $C_{BL} = 512 \times 0.07 + 3$ = 38.84 fF, which needs $C_s \ge 38.84/7$ = **5.55** fF.

Every power-of-two step in bitline length corresponds to a fixed ratio of capacitance. Below about 5.5 fF this array must halve its bitlines.

### Solution 23-03.5

The bitline (1.1 V) is above $V_{WL} - V_{TH}$, so the transistor is saturated throughout (§3.3), with $a = V_{WL} - V_{TH}$.

(a) $a = 1.1 - 0.45$ = **0.65** V.

(b) $k/(2C_s) = 25\ \mu\text{A/V}^2/12\ \text{fF} = 2.083 \times 10^9$ /(V·s), so after 5 ns $kt/(2C_s)$ = 10.42 V⁻¹, and $V = 0.65 - 1/(1/0.65 + 10.42)$ = **0.566** V.

(c) $V = 0.9a$ means $1/(a - V) = 10/a$, so $kt/(2C_s) = 9/a$ and $t = 18C_s/(ka) = 18 \times 6\ \text{fF}/(25\ \mu\text{A/V}^2 \times 0.65\ \text{V})$ = **6.65** ns.

(d) $V_{ARY} + V_{TH}$ = **1.55** V.

The last 10% of the approach takes ever longer: getting from 90% to 99% would take ten times as long again, because the shortfall falls only as $1/t$.

### Solution 23-03.6

(a) $\tau = 50\ \text{fF}/25\ \mu\text{S}$ = **2.00** ns.

(b) $2.00 \times \ln(1.0/0.06)$ = **5.63** ns.

(c) $\tau = 3/\ln(16.67)$ = 1.066 ns, so $g_m = 50\ \text{fF}/1.066\ \text{ns}$ = **46.9** µS.

(d) $2.00 \times \ln(1.0/0.03)$ = **7.01** ns; (e) the difference is $\tau\ln 2 = 2.00 \times 0.693$ = **1.39** ns.

Nearly doubling $g_m$ (with wider latch transistors, which load the bitline and add offset area) buys the same time as doubling the signal.

### Solution 23-03.7

(a) **16** ns; (b) $16 + 16$ = **32** ns; (c) $16 + 16 + 16$ = **48** ns.

(d) $0.4 \times 16 + 0.2 \times 32 + 0.4 \times 48$ = **32.0** ns.

(e) $h^* = t_{RP}/(t_{RP} + t_{RCD}) = 16/32$ = **0.5**.

At this mix an open-page controller averages exactly the closed-page latency (32 ns). Real controllers adapt their policy to the observed hit rate.

### Solution 23-03.8

(a) tRC = 32 + 16 = 48 ns, so $64\ \text{B}/48\ \text{ns}$ = **1.33** GB/s.

(b) $6400 \times 10^6 \times 4\ \text{B}$ = **25.6** GB/s.

(c) $25.6/1.333$ = **19.2** banks.

(d) Requests in flight = throughput × time in service = $(25.6\ \text{GB/s}/64\ \text{B}) \times 48\ \text{ns}$ = **19.2**.

(c) and (d) are the same calculation: each bank holds one request for one tRC, so the number of busy banks is the number of requests in flight (Little's law, 23-01).

### Solution 23-03.9

(a) $I = 6\ \text{fF} \times 0.15\ \text{V}/32\ \text{ms}$ = **28.1** fA.

(b) From 95 to 25 °C is seven halvings: $28.1/2^7$ = **0.220** fA. (c) $32\ \text{ms} \times 2^7$ = **4.10** s.

(d) $2^{34}\,\Phi(\ln(0.032/2)/0.8) = 2^{34}\,\Phi(-5.169)$ = **2.02** × 10³ cells. (e) $2^{34}\,\Phi(\ln(0.016/2)/0.8)$ = **13.6** cells.

A cell that must hold its charge for only 32 ms at 95 °C needs seconds of retention at room temperature. A retention test at room temperature therefore says little about hot operation.

### Solution 23-03.10

(a) $E = 8192 \times 35\ \text{fF} \times 1.1^2/2$ = **0.1735** nJ.

(b) The device has $32 \times 65{,}536 = 2{,}097{,}152$ rows. Refreshing them in 32 ms is $6.554 \times 10^7$ rows/s, and × 0.1735 nJ = **11.4** mW. (c) Twice as many per second: **22.7** mW.

(d) $0.1735\ \text{nJ}/128$ = **1.36** pJ/bit.

DDR5's 32 ms window and twice as many banks make bitline refresh power about double the DDR4 device of Example 23-03.7, at a similar energy per row.

### Solution 23-03.11

(a) $32\ \text{ms}/48\ \text{ns}$ = **6.67** × 10⁵ activations. (b) $3906.25/48$ = **81.4**. (c) $9600 \times 48\ \text{ns}$ = **0.461** ms.

(d) $p = 2\left(1 - (10^{-15})^{1/4800}\right) = 2\left(1 - e^{-34.54/4800}\right)$ = **0.0143**. (e) For 1,000: **0.0679**.

Halving the refresh window would not stop an attack that needs half a millisecond. A target of 10⁻¹⁵ per victim costs PARA 1.4% to 6.8% extra activations.

### Solution 23-03.12

With the transistor linear, $C_s\,dV/dt = k\left[(V_{PP} - V - V_{TH})(V_{ARY} - V) - \tfrac12(V_{ARY} - V)^2\right]$. Put $u = V_{ARY} - V$ and $b = V_{PP} - V_{TH} - V_{ARY}$, so that $V_{PP} - V - V_{TH} = b + u$ and $dV/dt = -du/dt$:

$$
C_s\frac{du}{dt} = -k\left[(b + u)u - \tfrac12u^2\right] = -k\left(bu + \tfrac12u^2\right) .
$$

Separate the variables and use partial fractions (§3.3):

$$
\int\frac{du}{u(b + u/2)} = \frac1b\ln\frac{u}{b + u/2} = -\frac{k}{C_s}t + \text{const},
\qquad
\frac{u}{b + u/2} = \frac{u_0}{b + u_0/2}\,e^{-bkt/C_s} .
$$

For $u \ll 2b$ the left side is $u/b$, so $u \approx b\,\frac{u_0}{b + u_0/2}\,e^{-bkt/C_s}$: an exponential with time constant $C_s/(bk)$.

(a) $b = 2.0 - 0.5 - 1.1 = 0.4$ V, $bk/C_s = 1.0 \times 10^9$ s⁻¹, $u_0/(b + u_0/2) = 1.1/0.95$ = 1.158, so $r = 1.158\,e^{-5} = 7.80 \times 10^{-3}$ and $u = 0.4r/(1 - r/2)$ = **3.13** mV.

(b) $t = \frac{C_s}{bk}\ln\frac{1.158}{0.001/0.4005}$ = 1.0 ns × ln 463.7 = **6.14** ns.

A wordline 0.4 V above $V_{ARY} + V_{TH}$ fills the cell to within a millivolt in about 6 ns, which fits inside tRAS.

### Solution 23-03.13

(a) $A = C t/(\varepsilon_0\varepsilon_r) = 6\ \text{fF} \times 6\ \text{nm}/(8.854 \times 10^{-12} \times 25)$ = **0.163** µm².

(b) $h = A/(\pi d) = 0.163\ \mu\text{m}^2/(\pi \times 25\ \text{nm})$ = **2.07** µm; (c) $2.07\ \mu\text{m}/25\ \text{nm}$ = **82.8**.

(d) Both walls double the area per unit height: **1.04** µm.

(e) $\varepsilon_r = C t/(\varepsilon_0 \cdot 2\pi d h) = 6\ \text{fF} \times 6\ \text{nm}/(8.854 \times 10^{-12} \times 2\pi \times 25\ \text{nm} \times 1.0\ \mu\text{m})$ = **25.9**.

(f) Height scales with thickness: $2.07 \times 5/6$ = **1.73** µm.

The double-walled cylinder needs an inner opening that can be coated with electrode and dielectric. That is why capacitors moved to quasi-cylindrical shapes as diameters shrank (§3.9).

### Solution 23-03.14

(a) $Q(k) = -\ln 0.99/2^{25}$ gives $k$ = **6.19**.

(b) $C_{BL} = 512 \times 0.08 + 4$ = 44.96 fF, so $\Delta V = 0.25 \times 8/52.96$ = **37.8** mV. (c) $\sigma_{os} \le 37.8/6.19$ = **6.10** mV.

(d) $Q(k) = -\ln 0.99/2^{26}$ gives $k$ = **6.30**.

(e) $C_{BL} = 256 \times 0.08 + 4$ = 24.48 fF, so $\Delta V = 0.25 \times 8/32.48$ = **61.6** mV. (f) $61.6/6.30$ = **9.78** mV.

Doubling the number of sense amplifiers raises the sigma needed by only 0.11, while halving the bitline raises the signal by 63%. Shorter bitlines relax the offset requirement a great deal, at the area cost of Example 23-03.2.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 23-03.1a | signal, stored 1 | 78.6 | mV |
| 23-03.1b | signal, stored 0 | -78.6 | mV |
| 23-03.1c | transfer ratio | 0.143 | |
| 23-03.1d0 | stored charge | 11 | fC |
| 23-03.1d | electrons in a stored 1 | 6.87e4 | |
| 23-03.2a | page size | 16384 | bits |
| 23-03.2b | device capacity | 17179869184 | bits |
| 23-03.2c | rows per bank per REF | 16 | |
| 23-03.2d0 | bits per BL8 burst | 128 | bits |
| 23-03.2d | page share of one burst | 0.781 | % |
| 23-03.3a | tREFI, up to 85 °C | 3.906 | µs |
| 23-03.3b | tREFI, 85–95 °C | 1.953 | µs |
| 23-03.3c | refresh overhead, up to 85 °C | 7.55 | % |
| 23-03.3d | refresh overhead, 85–95 °C | 15.1 | % |
| 23-03.4a0 | signal over margin | 8 | |
| 23-03.4a | largest bitline capacitance, 7 fF | 49.0 | fF |
| 23-03.4b | largest cells per bitline, 7 fF | 657.1 | |
| 23-03.4c | largest bitline capacitance, 5 fF | 35.0 | fF |
| 23-03.4cn | largest cells per bitline, 5 fF | 457.1 | |
| 23-03.4d0 | bitline capacitance, 512 cells | 38.84 | fF |
| 23-03.4d | storage capacitance for 512 cells | 5.55 | fF |
| 23-03.5a | limit voltage | 0.65 | V |
| 23-03.5b1 | k/(2C_s) | 2.083e9 | 1/(V·s) |
| 23-03.5b2 | kt/(2C_s) at 5 ns | 10.42 | 1/V |
| 23-03.5b | cell voltage at 5 ns | 0.566 | V |
| 23-03.5c | time to 90% | 6.65 | ns |
| 23-03.5d | lowest wordline for a full 1 | 1.55 | V |
| 23-03.6a | latch time constant | 2.00 | ns |
| 23-03.6b | sensing time, 60 mV | 5.63 | ns |
| 23-03.6c1 | time constant for 3 ns | 1.066 | ns |
| 23-03.6c0 | swing ratio, 60 mV | 16.67 | |
| 23-03.6c | g_m for 3 ns | 46.9 | µS |
| 23-03.6d | sensing time, 30 mV | 7.01 | ns |
| 23-03.6e0 | ln 2 | 0.693 | |
| 23-03.6e | extra time | 1.39 | ns |
| 23-03.7a | row-hit latency | 16 | ns |
| 23-03.7b | row-miss latency | 32 | ns |
| 23-03.7c | row-conflict latency | 48 | ns |
| 23-03.7d | average latency | 32.0 | ns |
| 23-03.7e | break-even hit rate | 0.5 | |
| 23-03.8a0 | tRC | 48 | ns |
| 23-03.8a | random-row bandwidth per bank | 1.33 | GB/s |
| 23-03.8b | channel peak bandwidth | 25.6 | GB/s |
| 23-03.8c | banks needed | 19.2 | |
| 23-03.8d | requests in flight | 19.2 | |
| 23-03.9a | leakage limit | 28.1 | fA |
| 23-03.9b | leakage at 25 °C | 0.220 | fA |
| 23-03.9c | retention at 25 °C | 4.10 | s |
| 23-03.9d1 | normalized log retention, 32 ms | -5.169 | |
| 23-03.9d | cells failing 32 ms | 2.02e3 | |
| 23-03.9e | cells failing 16 ms | 13.6 | |
| 23-03.10a | energy per row activation | 0.1735 | nJ |
| 23-03.10b0 | rows in the device | 2097152 | |
| 23-03.10b1 | rows refreshed per second, 32 ms | 6.554e7 | 1/s |
| 23-03.10b | refresh power, up to 85 °C | 11.4 | mW |
| 23-03.10c | refresh power, 85–95 °C | 22.7 | mW |
| 23-03.10d | activation energy per bit | 1.36 | pJ/bit |
| 23-03.11a | activations in 32 ms | 6.67e5 | |
| 23-03.11b | activations per tREFI | 81.4 | |
| 23-03.11c | time for 9,600 activations | 0.461 | ms |
| 23-03.11d0 | ln of the target | -34.54 | |
| 23-03.11d | PARA probability, 4,800 | 0.0143 | |
| 23-03.11e | PARA probability, 1,000 | 0.0679 | |
| 23-03.12a0 | b | 0.4 | V |
| 23-03.12a1 | bk/C_s | 1.0e9 | 1/s |
| 23-03.12a2 | u_0/(b + u_0/2) | 1.158 | |
| 23-03.12a3 | r at 5 ns | 7.80e-3 | |
| 23-03.12a | shortfall at 5 ns | 3.13 | mV |
| 23-03.12b1 | log argument | 463.7 | |
| 23-03.12b | time to within 1 mV | 6.14 | ns |
| 23-03.13a | electrode area | 0.163 | µm² |
| 23-03.13b | single-walled height | 2.07 | µm |
| 23-03.13c | height-to-diameter ratio | 82.8 | |
| 23-03.13d | double-walled height | 1.04 | µm |
| 23-03.13e | permittivity for a 1 µm cylinder | 25.9 | |
| 23-03.13f | single-walled height, 5 nm film | 1.73 | µm |
| 23-03.14a | sigma, 2²⁵ sense amplifiers | 6.19 | |
| 23-03.14b0 | bitline capacitance, 512 cells | 44.96 | fF |
| 23-03.14b | signal, 512 cells | 37.8 | mV |
| 23-03.14c | largest offset sigma, 512 cells | 6.10 | mV |
| 23-03.14d | sigma, 2²⁶ sense amplifiers | 6.30 | |
| 23-03.14e0 | bitline capacitance, 256 cells | 24.48 | fF |
| 23-03.14e | signal, 256 cells | 61.6 | mV |
| 23-03.14f | largest offset sigma, 256 cells | 9.78 | mV |
| 23-03.14g | sigma increase from doubling sense amplifiers | 0.11 | |
| 23-03.14h | signal increase from halving the bitline | 63 | % |
