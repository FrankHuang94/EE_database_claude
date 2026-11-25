# Solutions 24-06 · Die-to-Die Links, Memory PHYs and Scale-Up Fabrics

Problems: [24-06 problems](../problems/24-06-problems.md) · Chapter: [24-06](../chapters/24-06-d2d-memory-phys-scale-up.md)

Every number is recomputed by [verify_24_06.py](../verify/verify_24_06.py).

---

## Solutions

### Solution 24-06.1

(a) $500\ \text{fF} \times 0.6^2$ = **180** fJ.

(b) $180/4$ = **45** fJ.

(c) $45\ \text{fJ} \times 16 \times 10^9$ = **0.72** mW.

(d) $1024 \times 0.72$ mW = **0.74** W.

### Solution 24-06.2

(a) $0.3^2/(4 \times 50 \times 16 \times 10^9)$ = **0.028** pJ/b.

(b) $300\ \text{fF} \times 0.09/4$ = **6.75** fJ = 0.0068 pJ/b, a quarter of (a).

(c) Setting $V^2/(4Rf_b) = CV^2/4$ gives $f_b = 1/RC$ = **66.7** Gb/s. At that rate a bit lasts only one $RC$ time constant, so the wire no longer settles within a bit and cannot be treated as a lumped capacitor: it is a transmission line that would need termination anyway. Below that rate, a short unterminated wire is cheaper.

### Solution 24-06.3

(a) $(1000/25)^2$ = 1,600 bumps/mm², 800 for data: $800 \times 32/8$ = **3,200** GB/s/mm².

(b) 330.6 bumps/mm²: **661** GB/s/mm².

A 2.2× change of pitch is a 4.8× change in density.

### Solution 24-06.4

(a) $10{,}000/25$ = **400** GB/s/mm.

(b) **Yes**: 400 lies inside 165–1,317.

(c) $10{,}000/224$ = **44.6** mm, more than the 25 mm available.

A standard package cannot reach this bandwidth along this edge; an advanced package or a different floor plan is needed.

### Solution 24-06.5

Each module carries $64 \times 64/8$ = 512 GB/s each way, 1,024 GB/s in both: $10{,}000/1024$ = 9.8, so **10** modules. The power is $10\ \text{TB/s} \times 8 \times 0.25$ pJ/b = **20** W, the same as at 32 GT/s: doubling the rate halves the module count but not the bits moved.

### Solution 24-06.6

(a) $C_{tot} = 50 + 100 + 50$ = **200** fF.

(b) $100 \times 200\ \text{fF} + 25 \times (50 + 50)\ \text{fF} = 20 + 2.5$ = **22.5** ps.

(c) $2.2 \times 22.5$ = **49.5** ps.

(d) $1/49.5$ ps = **20.2** GT/s.

The driver's resistance, not the wire's, dominates here; a stronger driver would help more than a better wire.

### Solution 24-06.7

$4 \times 512$ = **2,048** Gb/s = **256** GB/s per millimetre, inside BoW's 2–12+ Tb/s/mm target range.

### Solution 24-06.8

(a) $2 \times 100/8$ = **25** GB/s each way, **50** GB/s in both.

(b) $18 \times 50$ = **900** GB/s.

(c) $8 \times 900$ = **7.2** TB/s.

### Solution 24-06.9

(a) $4 \times 200/8$ = **100** GB/s.

(b) Each port carries 200 GB/s in both directions: $1800/200$ = **9** ports.

(c) $212.5/200 - 1$ = **6.25** %.

### Solution 24-06.10

Die to die: $2 \times 10^{12} \times 8 \times 0.25 \times 10^{-12}$ = **4.0** W. Scale-up: **18.7** W. Scale-out: **4.8** W. Total: **27.5** W.

The scale-up fabric dominates although it carries less than the die-to-die link, because it sits two rungs higher on the energy ladder.

### Solution 24-06.11

(a) $8 \times 2048 \times 8/8$ = **16,384** GB/s, about 16.4 TB/s.

(b) $22 \times 10^{12} \times 8/(8 \times 2048)$ = **10.7** Gb/s per wire; 19.2 TB/s implies **9.4** Gb/s.

Both exceed the JEDEC baseline, so the parts must run faster than 8 Gb/s (or the GPU has more stacks). Diligence should ask which: faster HBM4 bins are a supply question.

### Solution 24-06.12

(a) $10^6$ bonds/mm², half for data at 1 Gb/s: $0.5 \times 10^6 \times 1/8$ = 62,500 GB/s/mm² = **62.5** TB/s/mm².

(b) $10\ \text{TB/s} \times 8 \times 0.01$ pJ/b = **0.8** W.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 24-06.1a | energy per edge | 180 | fJ |
| 24-06.1b | energy per bit | 45 | fJ |
| 24-06.1c | power per wire | 0.72 | mW |
| 24-06.1d | bus power | 0.74 | W |
| 24-06.2a | terminated energy | 0.028 | pJ/b |
| 24-06.2b | unterminated energy | 6.75 | fJ |
| 24-06.2b1 | unterminated energy in pJ | 0.0068 | pJ/b |
| 24-06.2c | equal-energy rate | 66.7 | Gb/s |
| 24-06.3a0 | bumps at 25 um | 1600 | |
| 24-06.3a | density at 25 um | 3200 | GB/s/mm² |
| 24-06.3b0 | bumps at 55 um | 330.6 | |
| 24-06.3b | density at 55 um | 661 | GB/s/mm² |
| 24-06.3c | pitch ratio | 2.2 | |
| 24-06.3c1 | density ratio | 4.8 | |
| 24-06.4a | needed shoreline density | 400 | GB/s/mm |
| 24-06.4c | UCIe-S edge needed | 44.6 | mm |
| 24-06.5a | module both directions | 1024 | GB/s |
| 24-06.5b0 | modules, exact | 9.8 | |
| 24-06.5b | modules | 10 | |
| 24-06.5c | power | 20 | W |
| 24-06.6a | total capacitance | 200 | fF |
| 24-06.6b | Elmore delay | 22.5 | ps |
| 24-06.6c | rise time | 49.5 | ps |
| 24-06.6d | rate | 20.2 | GT/s |
| 24-06.7a | edge density | 2048 | Gb/s |
| 24-06.7b | edge density in bytes | 256 | GB/s |
| 24-06.8a | link each way | 25 | GB/s |
| 24-06.8a1 | link both directions | 50 | GB/s |
| 24-06.8b | per GPU | 900 | GB/s |
| 24-06.8c | 8-GPU node | 7.2 | TB/s |
| 24-06.9a | x4 port each way | 100 | GB/s |
| 24-06.9b | ports to match NVLink 5 | 9 | |
| 24-06.9c | overhead | 6.25 | % |
| 24-06.10a | die-to-die power | 4.0 | W |
| 24-06.10b | scale-up power | 18.7 | W |
| 24-06.10c | scale-out power | 4.8 | W |
| 24-06.10d | total | 27.5 | W |
| 24-06.11a | baseline bandwidth | 16384 | GB/s |
| 24-06.11a1 | baseline in TB/s | 16.4 | TB/s |
| 24-06.11b | rate for 22 TB/s | 10.7 | Gb/s |
| 24-06.11b1 | rate for 19.2 TB/s | 9.4 | Gb/s |
| 24-06.12a | areal density | 62.5 | TB/s/mm² |
| 24-06.12b | power | 0.8 | W |
