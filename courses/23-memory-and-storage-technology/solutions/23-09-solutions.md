# Solutions 23-09 · Compute-in-Memory and Near-Memory Computing

Problems: [23-09 problems](../problems/23-09-problems.md) · Chapter: [23-09](../chapters/23-09-compute-in-memory.md)

Every number is recomputed by [verify_23_09.py](../verify/verify_23_09.py).

---

## Solutions

### Solution 23-09.1

(a) $0.1 \times 20 + 0.2 \times 10 + 0.05 \times 0$ = **4.0** µA.

(b) $0.1 \times 5 + 0.2 \times 15 + 0.05 \times 25$ = **4.75** µA.

Volts times microsiemens give microamps.

### Solution 23-09.2

$G^+ = (0.5, 5.5, 15.5)$ µS and $G^- = (10.5, 0.5, 0.5)$ µS.

(a) $0.1 \times 0.5 + 0.1 \times 5.5 + 0.2 \times 15.5$ = **3.70** µA.

(b) $0.1 \times 10.5 + 0.1 \times 0.5 + 0.2 \times 0.5$ = **1.20** µA.

(c) $3.70 - 1.20$ = **2.50** µA.

(d) With inputs (1, 1, 2) in units of 0.1 V, the dot product is $-2 + 1 + 6$ = **5**, and $5 \times 0.1\ \text{V} \times 5\ \mu\text{S}$ = 2.50 µA. ✓ The $G_{min}$ offset contributes 0.2 µA to each column and cancels.

### Solution 23-09.3

(a) SNR $= 6.02 \times 8 + 1.76$ = **49.9** dB, so $\sigma = 10^{-49.92/20}$ = **0.319** %.

(b) SNR = **25.8** dB, so $\sigma$ = **5.1** %.

Eight effective analog bits need device matching of a few tenths of a percent, far tighter than resistive memories achieve. This is why high-precision analog CIM is so hard.

### Solution 23-09.4

(a) Signal $(M\bar{p})^2$, error variance $M\sigma^2\bar{p}^2$, so SNR $= M/\sigma^2 = 6400$ = **38.1** dB.

(b) SNR $= 1/\sigma^2 = 100$ = **20.0** dB.

Equal positive terms add coherently while errors add in quadrature, so rows help. Zero-mean terms add like the errors, so they do not. Real layers are closer to (b).

### Solution 23-09.5

(a) $128 \times 3 \times 1$ = **384**.

(b) $\log_2 385$ = **8.59** bits; (c) **9** bits.

(d) $10\ \text{fJ} \times 2^9$ = **5.12** pJ.

(e) The 2-bit input is applied in one step, so each MAC shares one 9-bit conversion with the other 127 rows: $5.12\ \text{pJ}/128$ = **40.0** fJ per MAC.

### Solution 23-09.6

(a) $2\ \text{fJ} \times 2^7 \times 64/512$ = **32** fJ, so $2/32\ \text{fJ}$ = **62.5** TOPS/W.

(b) $2\ \text{fJ} \times 2^7 \times 16/512$ = **8** fJ, so **250** TOPS/W.

A better ADC, fewer bits per conversion and more rows each raise the ceiling. These ceilings exclude the array, drivers and digital logic.

### Solution 23-09.7

(a) $16 \times 256\ \text{bits}/8/4\ \text{ns}$ = **128** GB/s; (b) $16 \times 8\ \text{Gb/s}/8$ = **16** GB/s; (c) **8**.

Logic at the banks can reach eight times the bandwidth the pins deliver, which is the whole case for PIM.

### Solution 23-09.8

The model holds $13 \times 10^9 \times 4/8 = 6.5$ GB.

(a) $4 \times 76.8/6.5$ = **47.3** tokens/s; (b) $4 \times 614/6.5$ = **378** tokens/s.

These are upper bounds that ignore compute, the KV cache and overheads.

### Solution 23-09.9

(a) $1/(0.4 + 0.6/8)$ = **2.11**; (b) $1/(0.1 + 0.9/8)$ = **4.71**; (c) $1/0.1$ = **10**.

Even infinite PIM speed cannot beat the unaccelerated 10%.

### Solution 23-09.10

(a) $(2 + 3)/0.85$ = **5.88** W.

(b) $40/5.882$ = **6.8** TOPS/W; (c) $40/2$ = **20** TOPS/W.

The same silicon is "20 TOPS/W" or "6.8 TOPS/W" depending on where the boundary is drawn.

### Solution 23-09.11

(a) $100 \times 0.4/7$ = **5.71** TOPS/W; (b) $100/10$ = **10** TOPS/W.

Low utilization costs efficiency whenever power does not fall in proportion to work.

### Solution 23-09.12

(a) KCL at the column: $\sum G_i(0.2 - V_c) = V_c/R_s$, so $V_c = \dfrac{40\ \mu\text{S} \times 0.2}{40\ \mu\text{S} + 1\ \text{mS}}$ = **7.69** mV.

(b) $V_c/R_s$ = **7.69** µA; (c) $1 - 7.692/8$ = **3.85** % low.

(d) The error is $G_{\Sigma}R_s/(1 + G_{\Sigma}R_s)$. Setting it to 1%: $R_s = 0.01/(0.99 \times 40\ \mu\text{S})$ = **253** Ω.

The error depends on the column's total conductance, which depends on the data: a sense resistor turns into a data-dependent nonlinearity. A transimpedance amplifier holding the column at 0 V removes it.

### Solution 23-09.13

(a) $2/(100 \times 10^{12})$ = **20** fJ per MAC.

(b) 64 conversions per MAC are shared by 256 rows, so each conversion may use $20\ \text{fJ} \times 256/64$ = **80** fJ.

(c) $80\ \text{fJ}/2^8$ = **0.31** fJ per step; (d) $5/0.3125$ = **16** times better.

Unless its ADCs are far beyond the chapter's assumed figure, the claim needs something else: lower effective precision than "8-bit" suggests, fewer conversions per MAC (multibit inputs, larger arrays, analog accumulation across bits), or a measurement boundary that leaves out the ADCs. Ask which.

### Solution 23-09.14

(a) The ideal output is $y_0 = \sum_iw_ix_i$. With independent zero-mean weights, the cross terms vanish, so $E[y_0^2] = \sum_iE[w_i^2]E[x_i^2] = Ms_w^2s_x^2$. The error is $e = \sum_in_ix_i$, with $n_i$ the absolute weight error of standard deviation $\sigma_{FS}cs_w$, so $E[e^2] = Mc^2\sigma_{FS}^2s_w^2s_x^2$. Therefore

$$
\text{SNR}_a = \frac{E[y_0^2]}{E[e^2]} = \frac{1}{c^2\sigma_{FS}^2} .
$$

The relative-error model gives $1/\sigma^2$: an error fixed relative to full scale costs a factor $c^2$, because most weights are much smaller than full scale but carry the same absolute error.

(b) $1/(9 \times 10^{-4})$ = **1111**, or **30.46** dB; ENOB $= (30.46 - 1.76)/6.02$ = **4.77** bits.

(c) The relative model gives 40.0 dB, so the penalty is $20\log_{10}3$ = **9.54** dB, about 1.6 bits.

(d) Six bits need $6.02 \times 6 + 1.76$ = **37.88** dB, an SNR of **6138**, so $\sigma_{FS} = 1/(3\sqrt{6138})$ = **0.425** %.

Matching to a few tenths of a percent of full scale is hard for resistive devices, which is why analog chips program iteratively with verify, and why a weight distribution with long tails (a large crest factor) is expensive in analog.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 23-09.1a | column 1 current | 4.0 | µA |
| 23-09.1b | column 2 current | 4.75 | µA |
| 23-09.2a | positive-column current | 3.70 | µA |
| 23-09.2b | negative-column current | 1.20 | µA |
| 23-09.2c | differential output | 2.50 | µA |
| 23-09.2d | exact dot product | 5 | |
| 23-09.2e | offset per column | 0.2 | µA |
| 23-09.3a0 | SNR for 8 bits | 49.9 | dB |
| 23-09.3a1 | SNR for 8 bits, 4 s.f. | 49.92 | dB |
| 23-09.3a | sigma for 8 bits | 0.319 | % |
| 23-09.3b0 | SNR for 4 bits | 25.8 | dB |
| 23-09.3b | sigma for 4 bits | 5.1 | % |
| 23-09.4a0 | SNR ratio, coherent | 6400 | |
| 23-09.4a | SNR, coherent | 38.1 | dB |
| 23-09.4b0 | SNR ratio, zero-mean | 100 | |
| 23-09.4b | SNR, zero-mean | 20.0 | dB |
| 23-09.5a | largest column sum | 384 | |
| 23-09.5b | exact resolution | 8.59 | bits |
| 23-09.5c | ADC bits | 9 | bits |
| 23-09.5d | energy per conversion | 5.12 | pJ |
| 23-09.5e | ADC energy per MAC | 40.0 | fJ |
| 23-09.6a0 | ADC energy per 8-bit MAC | 32 | fJ |
| 23-09.6a | TOPS/W ceiling, 8-bit | 62.5 | TOPS/W |
| 23-09.6b0 | ADC energy per 4-bit MAC | 8 | fJ |
| 23-09.6b | TOPS/W ceiling, 4-bit | 250 | TOPS/W |
| 23-09.7a | internal bandwidth | 128 | GB/s |
| 23-09.7b | external bandwidth | 16 | GB/s |
| 23-09.7c | ratio | 8 | |
| 23-09.8a0 | model size | 6.5 | GB |
| 23-09.8a | token rate, LPDDR5X | 47.3 | tokens/s |
| 23-09.8b | token rate, LPDDR5X-PIM | 378 | tokens/s |
| 23-09.9a | speedup, 60% | 2.11 | |
| 23-09.9b | speedup, 90% | 4.71 | |
| 23-09.9c | limit, 90% | 10 | |
| 23-09.10a | card input power | 5.88 | W |
| 23-09.10a1 | card input power, 4 s.f. | 5.882 | W |
| 23-09.10b | card TOPS/W | 6.8 | TOPS/W |
| 23-09.10c | chip-core TOPS/W | 20 | TOPS/W |
| 23-09.11a | effective TOPS/W | 5.71 | TOPS/W |
| 23-09.11b | peak TOPS/W | 10 | TOPS/W |
| 23-09.12a | column voltage | 7.69 | mV |
| 23-09.12b | column current | 7.69 | µA |
| 23-09.12b1 | column current, 4 s.f. | 7.692 | µA |
| 23-09.12c | error | 3.85 | % |
| 23-09.12d | largest sense resistance | 253 | Ω |
| 23-09.13a | energy per MAC | 20 | fJ |
| 23-09.13b | energy per conversion | 80 | fJ |
| 23-09.13c | required FoM | 0.31 | fJ |
| 23-09.13c1 | required FoM, exact | 0.3125 | fJ |
| 23-09.13d | improvement needed | 16 | |
| 23-09.14b0 | SNR ratio | 1111 | |
| 23-09.14b1 | SNR | 30.46 | dB |
| 23-09.14b | effective bits | 4.77 | bits |
| 23-09.14c | penalty against relative model | 9.54 | dB |
| 23-09.14c1 | penalty in bits | 1.6 | bits |
| 23-09.14d0 | SNR for 6 bits | 37.88 | dB |
| 23-09.14d1 | SNR ratio for 6 bits | 6138 | |
| 23-09.14d | full-scale sigma for 6 bits | 0.425 | % |
