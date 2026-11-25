# Solutions 23-06 · NAND Flash and 3D NAND

Problems: [23-06 problems](../problems/23-06-problems.md) · Chapter: [23-06](../chapters/23-06-nand-flash-and-3d-nand.md)

Every number is recomputed by [verify_23_06.py](../verify/verify_23_06.py).

---

## Solutions

### Solution 23-06.1

(a) $q/C_{CG} = 1.602 \times 10^{-19}/20 \times 10^{-18}$ = **8.01** mV per electron.

(b) $2\ \text{V}/8.011\ \text{mV}$ = **250** electrons.

(c) $5.6/(8 - 1)$ = **0.8** V; (d) $0.8/8.011\ \text{mV}$ = **99.9** electrons.

A larger coupling capacitance means fewer volts per electron, so each level needs more electrons. That costs program time and energy but makes the cell less sensitive to losing a few of them.

### Solution 23-06.2

(a) $\alpha_G = 18/(18 + 12)$ = **0.6**.

(b) $V_{TH0}/\alpha_G = 0.9/0.6$ = **1.5** V. The control gate must supply more than the node's own threshold, because only 60% of its voltage reaches the node.

(c) $160 \times 1.602 \times 10^{-19}/18 \times 10^{-18}$ = **1.42** V; (d) $1.5 + 1.424$ = **2.92** V.

The shift depends only on $C_{CG}$, not on $C_{other}$ (§3.1): $\Delta V_{TH} = -Q/C_{CG}$.

### Solution 23-06.3

(a) $9\ \text{V}/6\ \text{nm} = 1.5 \times 10^9$ V/m = **15** MV/cm.

(b) $J = 1.25 \times 10^{-6} \times (1.5 \times 10^9)^2 \times e^{-2.33 \times 10^{10}/1.5 \times 10^9} = 2.81 \times 10^{12} \times e^{-15.53}$ = **5.05** × 10⁵ A/m².

(c) $5.047 \times 10^5 \times (40\ \text{nm})^2 = 5.047 \times 10^5 \times 1.6 \times 10^{-15}$ = **0.808** nA.

(d) $50 \times 1.602 \times 10^{-19}/0.8076\ \text{nA}$ = **9.92** ns.

(e) The ratio is $(15/13)^2 \exp[233(1/13 - 1/15)]$, with fields in MV/cm and $B$ = 233 MV/cm, giving **14.5**. A 15% rise in field gives a fourteenfold rise in current, almost all from the exponential.

### Solution 23-06.4

(a) During pulse $k$ the storage node sits at $V_{FG} = \alpha_G V_{pgm,k} + Q/C_T$ (§3.1). If every pulse ends at the same $V_{FG}^*$, then for pulses $k$ and $k + 1$

$$
\alpha_G V_{pgm,k} + \frac{Q_k}{C_T} = \alpha_G V_{pgm,k+1} + \frac{Q_{k+1}}{C_T} ,
$$

so $Q_{k+1} - Q_k = -\alpha_G C_T (V_{pgm,k+1} - V_{pgm,k}) = -C_{CG}\,\Delta V_{pgm}$, using $\alpha_G C_T = C_{CG}$. The charge added is $C_{CG}\Delta V_{pgm}$ in magnitude (electrons, so negative), and the threshold shift is $\Delta V_{TH} = -\Delta Q/C_{CG} = \Delta V_{pgm}$.

(b) $16 \times 10^{-18} \times 0.3/1.602 \times 10^{-19}$ = **30.0** electrons.

(c) No. The added charge is $C_{CG}\Delta V_{pgm}$ whatever $C_{other}$ is. The coupling ratio sets how high the first pulses must go before tunneling starts, not the steady-state step.

### Solution 23-06.5

(a) $(5 - (-3))/0.2$ = **40** pulses; (b) $40 \times 25\ \mu\text{s}$ = **1.00** ms.

(c) $8/0.1$ = **80** pulses; (d) $80 \times 25\ \mu\text{s}$ = **2.00** ms.

Halving the step halves the width of each level distribution (§3.2) but doubles the program time. QLC's milliseconds of program time are one reason SSDs write first to an SLC cache (23-07).

### Solution 23-06.6

MLC: (a) $6.4/3$ = **2.13** V; (b) $2.133/(2 \times 0.07)$ = **15.2**.

TLC: (c) $6.4/7$ = **0.914** V; (d) $0.9143/0.14$ = **6.53**; (e) $\tfrac{2 \times 7}{8 \times 3} Q(6.53)$ = **1.91** × 10⁻¹¹.

QLC: (f) $6.4/15$ = **0.427** V; (g) $0.4267/0.14$ = **3.05**; (h) $\tfrac{2 \times 15}{16 \times 4} Q(3.05)$ = **5.41** × 10⁻⁴.

(i) Setting $\tfrac{30}{64} Q(k) = 2 \times 10^{-3}$ gives $Q(k) = 4.27 \times 10^{-3}$, so $k$ = **2.63**.

(j) $\sigma = d/2k = 0.4267/(2 \times 2.630)$ = **0.0811** V.

QLC tolerates σ growing from 0.07 to 0.0811 V, about 16%, before its raw error rate roughly quadruples to 2 × 10⁻³. Small changes in distribution width move error rates by large factors.

### Solution 23-06.7

(a) Order the levels from erased upward as 11, 10, 00, 01. Adjacent codes differ in one bit: 11 → 10 flips the second bit, 10 → 00 the first and 00 → 01 the second. A misread into an adjacent level therefore flips one of the two bits. A natural binary order (00, 01, 10, 11) would flip both bits on the 01 → 10 boundary.

(b) $(2 + 3 + 2)/3$ = **2.33** references per page read. The middle page is slowest to read, with 3 references.

### Solution 23-06.8

(a) $1024\ \text{Gb}/50\ \text{mm}^2$ = **20.5** Gb/mm².

(b) $20.48/(286 \times 3)$ = **0.0239** Gb/mm² per layer-bit.

(c) $1/(0.02387 \times 10^9\ \text{mm}^{-2}) = 4.19 \times 10^{-8}$ mm² = **0.0419** µm².

(d) $37.6/(3 \times 0.02387)$ = **525** layers. Kioxia reaches 37.6 Gb/mm² with 332 layers by storing 4 bits per cell and packing strings 18.6% more densely than this die (0.02831 against 0.02387 per layer-bit).

### Solution 23-06.9

(a) $400 \times 40\ \text{nm}$ = **16.0** µm.

(b) $16\ \mu\text{m}/100\ \text{nm}$ = **160**; (c) $160/3$ = **53.3**.

(d) $160/70$ = **2.29**, so (e) **3** decks. Two decks would leave each etch at an aspect ratio of 80, above the limit.

### Solution 23-06.10

(a) $AF = \exp[(1.0/8.617 \times 10^{-5})(1/298.15 - 1/398.15)] = \exp(9.776)$ = **1.76** × 10⁴.

(b) $10 \times 8760\ \text{h}/17{,}600$ = **4.98** h.

(c) With 0.6 eV, $AF = \exp(5.87)$ = **353**.

(d) The 4.98 h bake represents $4.977 \times 352.6$ h at 25 °C, which is **0.200** years.

If the plan's activation energy is too high, a bake that "proves" ten years proves only about 2.4 months. This is why qualification measures activation energies for each mechanism rather than assuming one (§3.6).

### Solution 23-06.11

(a) $3.84 \times 365 \times 5$ = **7008** TB.

(b) $7008 \times 3/3.84$ = **5475** cycles. Equivalently, 1 DWPD × 1,825 days × 3.

(c) $1500/(3 \times 365 \times 5)$ = **0.274** DWPD, whatever the capacity.

A drive's DWPD rating is just cycles divided by write amplification and days. Capacity cancels, which is why a larger drive is no more "durable" per drive write.

### Solution 23-06.12

(a) $6 \times 16{,}384/400\ \mu\text{s}$ = **246** MB/s; (b) $6 \times 16{,}384/2\ \text{ms}$ = **49.2** MB/s.

(c) $12{,}000/245.8$ = 48.8, so **49** dies; (d) $12{,}000/49.15$ = 244.1, so **245** dies.

(e) $6 \times 16{,}384/60\ \mu\text{s}$ = **1.64** GB/s.

A drive with too few QLC dies cannot reach its rated write speed without an SLC cache. Once the cache fills, the write rate falls to the QLC figure.

### Solution 23-06.13

(a) $d = 6/15 = 0.4$ V, so $k = 0.4/(2 \times 0.09)$ = **2.22**; (b) $\tfrac{30}{64} Q(2.222)$ = **6.16** × 10⁻³. This exceeds 5 × 10⁻³, so QLC fails at end of life.

(c) $(6/7)/0.18$ = **4.76**; (d) $\tfrac{14}{24} Q(4.762)$ = **5.59** × 10⁻⁷, far inside the limit.

(e) Setting $\tfrac{30}{64} Q(k) = 5 \times 10^{-3}$ gives $k = 2.30$, so $\sigma_{max} = 0.4/(2 \times 2.302)$ = **0.0869** V; (f) **2.30**.

The design choices are: hold σ below 0.0869 V at end of life (smaller program steps, better cells), reduce the rated P/E cycles, strengthen the ECC, or ship TLC.

### Solution 23-06.14

(a) $6 \times 16{,}384/2.5\ \text{ms}$ = **39.3** MB/s; (b) $39.32/4800$ = **0.819** %.

(c) $4800/39.32$ = 122.1, so **123** dies. No channel carries that many; an SSD instead spreads writes over many channels and dies, and accepts that writes, not the interface, set its sustained write speed.

(d) $30/(400 \times 3)$ = **0.025** Gb/mm² per layer-bit; (e) $1 - 0.025/0.02831$ = **11.7** % lower.

The quoted 4.8 Gb/s is the per-pin interface speed: it says how fast data crosses the pins, not how fast the die writes. The 400-layer TLC die is less dense per layer than the 332-layer die: more layers do not mean better lateral design.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 23-06.1a | shift per electron | 8.01 | mV |
| 23-06.1a1 | shift per electron, 4 s.f. | 8.011 | mV |
| 23-06.1b | electrons for 2 V | 250 | |
| 23-06.1c | TLC spacing | 0.8 | V |
| 23-06.1d | electrons per level | 99.9 | |
| 23-06.2a | coupling ratio | 0.6 | |
| 23-06.2a1 | coupling ratio in percent | 60 | % |
| 23-06.2b | uncharged threshold | 1.5 | V |
| 23-06.2c | threshold shift | 1.42 | V |
| 23-06.2c1 | threshold shift, 4 s.f. | 1.424 | V |
| 23-06.2d | new threshold | 2.92 | V |
| 23-06.3a | oxide field | 15 | MV/cm |
| 23-06.3a1 | oxide field in V/m | 1.5e9 | V/m |
| 23-06.3b0 | prefactor A E² | 2.81e12 | A/m² |
| 23-06.3b00 | exponent B/E | 15.53 | |
| 23-06.3b | current density | 5.05e5 | A/m² |
| 23-06.3b1 | current density, 4 s.f. | 5.047e5 | A/m² |
| 23-06.3c0 | area | 1.6e-15 | m² |
| 23-06.3c | current | 0.808 | nA |
| 23-06.3c1 | current, 4 s.f. | 0.8076 | nA |
| 23-06.3d | time for 50 electrons | 9.92 | ns |
| 23-06.3e0 | B in MV/cm | 233 | MV/cm |
| 23-06.3e | current-density ratio | 14.5 | |
| 23-06.3e1 | field rise | 15 | % |
| 23-06.4b | electrons per pulse | 30.0 | |
| 23-06.5a | pulses, 0.2 V step | 40 | |
| 23-06.5b | time, 0.2 V step | 1.00 | ms |
| 23-06.5c | pulses, 0.1 V step | 80 | |
| 23-06.5d | time, 0.1 V step | 2.00 | ms |
| 23-06.6a | MLC spacing | 2.13 | V |
| 23-06.6a1 | MLC spacing, 4 s.f. | 2.133 | V |
| 23-06.6b | MLC margin | 15.2 | |
| 23-06.6c | TLC spacing | 0.914 | V |
| 23-06.6c1 | TLC spacing, 4 s.f. | 0.9143 | V |
| 23-06.6d | TLC margin | 6.53 | |
| 23-06.6e | TLC RBER | 1.91e-11 | |
| 23-06.6f | QLC spacing | 0.427 | V |
| 23-06.6f1 | QLC spacing, 4 s.f. | 0.4267 | V |
| 23-06.6g | QLC margin | 3.05 | |
| 23-06.6h | QLC RBER | 5.41e-4 | |
| 23-06.6i0 | target Q | 4.27e-3 | |
| 23-06.6i | margin for 2e-3 | 2.63 | |
| 23-06.6i1 | margin for 2e-3, 4 s.f. | 2.630 | |
| 23-06.6j | sigma for 2e-3 | 0.0811 | V |
| 23-06.6k | sigma growth tolerated | 16 | % |
| 23-06.6k1 | RBER increase factor | 4 | |
| 23-06.7b | references per page read | 2.33 | |
| 23-06.8a | areal density | 20.5 | Gb/mm² |
| 23-06.8a1 | areal density, 4 s.f. | 20.48 | Gb/mm² |
| 23-06.8b | density per layer-bit | 0.0239 | Gb/mm² |
| 23-06.8b1 | density per layer-bit, 4 s.f. | 0.02387 | Gb/mm² |
| 23-06.8c0 | area per string in mm² | 4.19e-8 | mm² |
| 23-06.8c | area per string | 0.0419 | µm² |
| 23-06.8d | layers to match 37.6 | 525 | |
| 23-06.8e | Kioxia lateral advantage | 18.6 | % |
| 23-06.8e1 | Kioxia density per layer-bit | 0.02831 | Gb/mm² |
| 23-06.9a | stack height | 16.0 | µm |
| 23-06.9b | single-etch aspect ratio | 160 | |
| 23-06.9c | per-deck aspect ratio, 3 decks | 53.3 | |
| 23-06.9d | ratio to the limit | 2.29 | |
| 23-06.9e | decks needed | 3 | |
| 23-06.9f | per-deck aspect ratio, 2 decks | 80 | |
| 23-06.10a0 | exponent, 1.0 eV | 9.776 | |
| 23-06.10a | acceleration factor, 1.0 eV | 1.76e4 | |
| 23-06.10a1 | acceleration factor, 1.0 eV, rounded | 17600 | |
| 23-06.10b | bake hours | 4.98 | h |
| 23-06.10b1 | bake hours, 4 s.f. | 4.977 | h |
| 23-06.10c0 | exponent, 0.6 eV | 5.87 | |
| 23-06.10c | acceleration factor, 0.6 eV | 353 | |
| 23-06.10c1 | acceleration factor, 0.6 eV, 4 s.f. | 352.6 | |
| 23-06.10d | years represented | 0.200 | years |
| 23-06.10e | months represented | 2.4 | months |
| 23-06.11a | rated host writes | 7008 | TB |
| 23-06.11b | P/E cycles | 5475 | |
| 23-06.11b0 | days in 5 years | 1825 | |
| 23-06.11c | QLC DWPD | 0.274 | |
| 23-06.12a | TLC die write throughput | 246 | MB/s |
| 23-06.12a1 | TLC throughput, 4 s.f. | 245.8 | MB/s |
| 23-06.12b | QLC die write throughput | 49.2 | MB/s |
| 23-06.12b1 | QLC throughput, 4 s.f. | 49.15 | MB/s |
| 23-06.12c0 | TLC dies, unrounded | 48.8 | |
| 23-06.12c | TLC dies | 49 | |
| 23-06.12d0 | QLC dies, unrounded | 244.1 | |
| 23-06.12d | QLC dies | 245 | |
| 23-06.12e | SLC-mode throughput | 1.64 | GB/s |
| 23-06.13a | QLC margin | 2.22 | |
| 23-06.13a1 | QLC margin, 4 s.f. | 2.222 | |
| 23-06.13b | QLC RBER | 6.16e-3 | |
| 23-06.13c | TLC margin | 4.76 | |
| 23-06.13c1 | TLC margin, 4 s.f. | 4.762 | |
| 23-06.13d | TLC RBER | 5.59e-7 | |
| 23-06.13e | largest sigma | 0.0869 | V |
| 23-06.13f | margin at the limit | 2.30 | |
| 23-06.13f1 | margin at the limit, 4 s.f. | 2.302 | |
| 23-06.14a | sustained write throughput | 39.3 | MB/s |
| 23-06.14a1 | sustained write throughput, 4 s.f. | 39.32 | MB/s |
| 23-06.14b | share of interface | 0.819 | % |
| 23-06.14c0 | dies, unrounded | 122.1 | |
| 23-06.14c | dies per channel | 123 | |
| 23-06.14d | density per layer-bit | 0.025 | Gb/mm² |
| 23-06.14e | shortfall | 11.7 | % |
