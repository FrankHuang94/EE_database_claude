# Solutions 23-07 · SSD Controllers and Storage Systems

Problems: [23-07 problems](../problems/23-07-problems.md) · Chapter: [23-07](../chapters/23-07-ssd-controllers.md)

Every number is recomputed by [verify_23_07.py](../verify/verify_23_07.py).

---

## Solutions

### Solution 23-07.1

(a) $16 \times 10^9 \times 4 \times (128/130)/8$ = **7.88** GB/s.

(b) $32 \times 10^9 \times 2 \times (128/130)/8$ = **7.88** GB/s. Two PCIe 5.0 lanes match four PCIe 4.0 lanes.

(c) $64 \times 10^9 \times 8/8$ = **64** GB/s, before flit overhead.

### Solution 23-07.2

(a) $3.84 \times 10^{12}/4096 \times 4$ = **3.75** GB.

(b) $122.88 \times 10^{12}/16{,}384$ = **7.5** × 10⁹ entries; (c) $\log_2(7.5 \times 10^9)$ = 32.8, so **33** bits.

(d) $7.5 \times 10^9 \times 5$ = **37.5** GB. Even with 16 KiB units, a 122.88 TB drive needs more than 32 bits per entry, and its table is larger than a 30 TB drive's at 4 KiB (Example 23-07.2).

### Solution 23-07.3

(a) $\alpha$ = 1.1: $u$ = **0.824**, $A$ = **5.68**.

(b) $\alpha$ = 1.2: $u$ = **0.686**, $A$ = **3.19**.

(c) $S_f = 0.1/1.1$ = **9.09** %; (d) $0.2/1.2$ = **16.7** %.

Doubling the over-provisioning from 10% to 20% cuts the work of garbage collection from 4.68 to 2.19 extra writes per host write.

### Solution 23-07.4

(a) Cleaning a victim frees its $(1 - u)$ invalid fraction for new host data and rewrites its $u$ valid fraction. Per block reclaimed, the host gains $(1 - u)N_p$ pages of writes while the flash absorbs $N_p$ page writes (the host's plus the copies). So $A = N_p/((1 - u)N_p) = 1/(1 - u)$.

(b) Under FIFO, a page's block is cleaned after the log has written all $T$ physical pages once. A fraction $(1 - u)$ of those are host writes, each of which overwrites the page's LBA with probability $1/U$. The page survives with probability $(1 - 1/U)^{(1 - u)T} \approx e^{-(1 - u)T/U} = e^{-\alpha(1 - u)}$, and the victim's valid fraction equals this survival probability.

(c) $u$ = **0.417**, $A = 1/(1 - u)$ = **1.72**. Check: $e^{-1.5 \times 0.5828} = e^{-0.8742}$ = 0.4172. ✓

### Solution 23-07.5

(a) The live data is 80% of the user capacity, so $\alpha_{eff} = 1.07/0.8$ = **1.34**.

(b) $A$ = **2.18**; (c) a full drive has $A$ = **7.82**, so TRIM cuts the write amplification by a factor of **3.58**.

Free space the host has trimmed acts exactly like extra over-provisioning. That is why the same drive behaves so differently when empty and full.

### Solution 23-07.6

(a) $33.0/30.72 - 1$ = **7.42** %; (b) $A$ = **7.41**.

(c) $33.0 \times 1000/7.412$ = **4452** TB; (d) $4452/(30.72 \times 1825)$ = **0.0794** DWPD.

(e) Read-modify-write multiplies the NAND writes by $16/4 = 4$, giving $0.0794/4$ = **0.0199** DWPD.

Under worst-case small random writes, a capacity QLC drive offers well under 0.1 DWPD. Such drives are rated for, and should be used with, large or sequential writes.

### Solution 23-07.7

(a) $15 \times 60$ = **900** bits; (b) $16{,}384 + 900$ = **17284** bits.

(c) $17{,}284 \times 2 \times 10^{-3}$ = **34.6**; (d) $P_{fail} = P(X > 60)$ = **3.00** × 10⁻⁵.

(e) Solving $P(X > 60) = 10^{-15}$ gives $p$ = **1.03** × 10⁻³; (f) mean **17.8** errors.

The code reaches $10^{-15}$ only with the mean error count at under a third of $t$. The binomial tail is wide enough that a large margin is needed.

### Solution 23-07.8

(a) $16/17$ = **0.941**.

(b) Solving $1 - H(p) = 0.941$ gives $p$ = **0.681** %.

(c) $1 - H(0.005)$ = **0.955**.

With less spare area, the hard-decision limit falls from 1.48% (Example 23-07.6) to 0.68%. Spare area and soft reads are the two levers.

### Solution 23-07.9

(a) $32/80\ \mu\text{s}$ = **400000** IOPS; (b) $1/80\ \mu\text{s}$ = **12500** IOPS.

(c) $2 \times 10^6 \times 120\ \mu\text{s}$ = **240** commands.

### Solution 23-07.10

(a) $4096/2.4 \times 10^9$ = **1.71** µs.

(b) $2.4 \times 10^9/4096$ = **5.86** × 10⁵ IOPS per channel; (c) $\times 8$ = **4.69** million IOPS.

(d) $32 \times 4/60\ \mu\text{s}$ = **2.13** million IOPS.

(e) The dies limit the drive: it can read at most 2.13 million random 4 KiB blocks per second, under half of what the channels could carry.

### Solution 23-07.11

(a) $15 \times 0.040/0.88$ = **0.682** J.

(b) $C = 2 \times 0.6818/(28^2 - 10^2) = 1.364/684$ = **1.99** mF.

(c) $\tfrac{1}{2} \times 1.994 \times 10^{-3} \times 10^2$ = **0.0997** J; (d) $10^2/28^2$ = **12.8** %.

Most of the stored energy is usable because the converter runs down to 10 V. A converter that needed 20 V would strand $20^2/28^2$, about half.

### Solution 23-07.12

(a) $200/6$ = **33.3** s; (b) $100/1.5$ = **66.7** s.

(c) $300/100$ = **3.00** GB/s.

(d) A TLC cell run as SLC holds one bit instead of three, so 200 GB of SLC cache occupies cells that hold **600** GB in TLC mode.

The drive's "6 GB/s" holds for two thirds of the data but only a third of the time.

### Solution 23-07.13

(a) $DWPD = \dfrac{T N_{PE}/A}{U \times 1825} = \dfrac{\alpha \times 3000}{A(\alpha) \times 1825}$.

(b) Setting this to 3 and solving numerically gives $\alpha$ = **2.18**; (c) $A$ = **1.19**; (d) $OP$ = **118** %.

(e) $8.8/2.176$ = **4.04** TB.

Under worst-case uniform random writes, 3 DWPD from 3,000-cycle TLC would need more flash hidden than shown. Real 3 DWPD drives rely on rating workloads with lower write amplification than the uniform worst case, on flash rated for more cycles, and on firmware that separates hot and cold data.

### Solution 23-07.14

(a) $0.5 \times 10^9 \times 5 \times 365 \times 86{,}400$ = **78.8** PB.

(b) $\times 2$ = **158** PB.

(c) $157.7\ \text{PB}/130\ \text{TB}$ = **1213** cycles.

(d) Yes: running flat out for five years consumes about 1,200 of the 1,500 rated cycles. The claim follows from the drive's size and its limited random-write speed, not from unusually durable cells.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 23-07.1a | PCIe 4.0 x4 bandwidth | 7.88 | GB/s |
| 23-07.1b | PCIe 5.0 x2 bandwidth | 7.88 | GB/s |
| 23-07.1c | PCIe 6.0 x8 raw rate | 64 | GB/s |
| 23-07.2a | mapping table, 3.84 TB | 3.75 | GB |
| 23-07.2b | entries, 122.88 TB at 16 KiB | 7.5e9 | |
| 23-07.2c0 | address bits, unrounded | 32.8 | |
| 23-07.2c | address bits | 33 | |
| 23-07.2d | table with 5-byte entries | 37.5 | GB |
| 23-07.3a0 | valid fraction, 10% OP | 0.824 | |
| 23-07.3a | write amplification, 10% OP | 5.68 | |
| 23-07.3b0 | valid fraction, 20% OP | 0.686 | |
| 23-07.3b | write amplification, 20% OP | 3.19 | |
| 23-07.3c | spare factor, 10% OP | 9.09 | % |
| 23-07.3d | spare factor, 20% OP | 16.7 | % |
| 23-07.3e | extra writes, 10% OP | 4.68 | |
| 23-07.3f | extra writes, 20% OP | 2.19 | |
| 23-07.4c0 | valid fraction at alpha 1.5 | 0.417 | |
| 23-07.4c | write amplification at alpha 1.5 | 1.72 | |
| 23-07.4c1 | 1 - u | 0.5828 | |
| 23-07.4c2 | exponent | 0.8742 | |
| 23-07.4c3 | check value | 0.4172 | |
| 23-07.5a | effective alpha | 1.34 | |
| 23-07.5b | write amplification with TRIM | 2.18 | |
| 23-07.5c | write amplification, full | 7.82 | |
| 23-07.5d | improvement factor | 3.58 | |
| 23-07.6a | over-provisioning | 7.42 | % |
| 23-07.6b | write amplification | 7.41 | |
| 23-07.6b1 | write amplification, 4 s.f. | 7.412 | |
| 23-07.6c | host TBW | 4452 | TB |
| 23-07.6d | DWPD | 0.0794 | |
| 23-07.6e | DWPD with 16 KiB units | 0.0199 | |
| 23-07.7a | parity bits | 900 | |
| 23-07.7b | codeword length | 17284 | |
| 23-07.7c | mean errors at 2e-3 | 34.6 | |
| 23-07.7d | failure probability at 2e-3 | 3.00e-5 | |
| 23-07.7e | raw error rate for 1e-15 | 1.03e-3 | |
| 23-07.7f | mean errors at that rate | 17.8 | |
| 23-07.8a | code rate | 0.941 | |
| 23-07.8b | hard-decision limit | 0.681 | % |
| 23-07.8c | capacity at 0.5% | 0.955 | |
| 23-07.8d | limit from Example 23-07.6 | 1.48 | % |
| 23-07.8e | limit, 2 s.f. | 0.68 | % |
| 23-07.9a | IOPS at QD 32 | 400000 | |
| 23-07.9b | IOPS at QD 1 | 12500 | |
| 23-07.9c | commands for 2 M IOPS | 240 | |
| 23-07.10a | 4 KiB transfer time | 1.71 | µs |
| 23-07.10b | channel-limited IOPS, one channel | 5.86e5 | |
| 23-07.10c | channel-limited IOPS, eight channels | 4.69e6 | |
| 23-07.10d | die-limited IOPS | 2.13e6 | |
| 23-07.11a | energy from the bank | 0.682 | J |
| 23-07.11a1 | energy, 4 s.f. | 0.6818 | J |
| 23-07.11a2 | doubled energy | 1.364 | J |
| 23-07.11b0 | voltage-squared difference | 684 | V² |
| 23-07.11b | capacitance | 1.99 | mF |
| 23-07.11b1 | capacitance, 4 s.f. | 1.994 | mF |
| 23-07.11c | energy left at 10 V | 0.0997 | J |
| 23-07.11d | fraction left | 12.8 | % |
| 23-07.11e | fraction stranded at 20 V | 0.5 | |
| 23-07.12a | time to fill the cache | 33.3 | s |
| 23-07.12b | time for the next 100 GB | 66.7 | s |
| 23-07.12c | average rate | 3.00 | GB/s |
| 23-07.12c0 | total time | 100 | s |
| 23-07.12d | TLC capacity occupied | 600 | GB |
| 23-07.13b | required alpha | 2.18 | |
| 23-07.13b1 | required alpha, 4 s.f. | 2.176 | |
| 23-07.13c | write amplification | 1.19 | |
| 23-07.13d | over-provisioning | 118 | % |
| 23-07.13e | user capacity | 4.04 | TB |
| 23-07.14a | host writes in 5 years | 78.8 | PB |
| 23-07.14b | NAND writes | 158 | PB |
| 23-07.14b1 | NAND writes, 4 s.f. | 157.7 | PB |
| 23-07.14c | P/E cycles consumed | 1213 | |
| 23-07.14d | cycles consumed, rounded | 1.2e3 | |
