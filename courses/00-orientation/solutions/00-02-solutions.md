# Solutions 00-02 · The Abstraction Stack

Problems: [00-02 problems](../problems/00-02-problems.md) · Chapter: [00-02](../chapters/00-02-the-abstraction-stack.md)

Every number below is in the answer key and is recomputed by [verify_00_02.py](../verify/verify_00_02.py).

---

## Solutions

### Solution 00-02.1

(a) **Lumped circuit.** It hides the electromagnetic fields; only element voltages and currents, obeying KVL and KCL, remain. It fails when the circuit is not small compared with the wavelength (or when line delay is not short compared with edge time): waves and reflections appear.

(b) **Digital abstraction.** It hides continuous voltages, noise and transition behavior; only 0s and 1s remain. It fails when noise exceeds the noise margin, or when a signal is sampled while still changing (a timing violation, which can cause metastability).

(c) **Instruction-set architecture.** It hides the microarchitecture (pipelines, caches, speculation); software sees only architectural state and the instruction semantics. It leaks through timing and power: performance depends on the hidden structure, and side channels (e.g., Spectre-class attacks) can expose data.

(d) **Process design kit.** It hides the fab's process recipes and physics behind device models, design rules and standard cells. It fails when the models are inaccurate (e.g., outside characterized corners, or for new layout styles) and when physical effects are not captured in the rules (aging, layout-dependent effects).

### Solution 00-02.2

Using $\lambda = c/f$:

(a) $2.998\times10^8/50 = 5.996\times10^6$ m $= 5996$ km.
(b) $2.998\times10^8/2.4\times10^9 = 0.1249$ m $= 12.49$ cm.
(c) $2.998\times10^8/77\times10^9 = 3.89\times10^{-3}$ m $= 3.89$ mm. This is why automotive radar antennas fit on a small chip-sized module.
(d) $f = c/\lambda = 2.998\times10^8/500\times10^{-9} = 5.996\times10^{14}$ Hz $= 599.6$ THz.

### Solution 00-02.3

(a) $NM_L = V_{IL} - V_{OL} = 0.35 - 0.1 = 0.25$ V and $NM_H = V_{OH} - V_{IH} = 0.9 - 0.65 = 0.25$ V.

(b) The input thresholds would overlap: some voltages would count as both a valid 0 and a valid 1. A correct specification needs $V_{IL} \le V_{IH}$. In practice, $V_{IL}$ is the *highest* voltage guaranteed to read as 0 and $V_{IH}$ the *lowest* guaranteed to read as 1, and the actual switching threshold lies somewhere between them.

### Solution 00-02.4

(a) $\lambda = 2\times10^8/2\times10^4 = 1.00\times10^4$ m $= 10$ km, so the cable is $1/10\,000 = 1.0\times10^{-4}$ wavelengths: **lumped**.
(b) $\lambda = 1.5\times10^8/16\times10^9 = 9.375$ mm, so the trace is $300/9.375 = 32.0$ wavelengths: **a transmission line**, which must be impedance-controlled and probably equalized.
(c) $\lambda = 1.5\times10^8/10^9 = 0.150$ m, so the trace is $5/150 = 0.0333$ wavelengths: **lumped** (a third of λ/10 at 1 GHz, but faster edges would change that).

### Solution 00-02.5

The allowed one-way delay is $t_r/6 = 100/6 = 16.7$ ps, so the length is $v\cdot t = 1.5\times10^8 \times 16.7\times10^{-12} = 2.50$ mm.
With $t_r/10$: delay 10 ps, length 1.50 mm.
On a board, essentially every trace carrying 100 ps edges is a transmission line.

### Solution 00-02.6

**C driving B:** $NM_L = V_{IL,B} - V_{OL,C} = 0.6 - 0.3 = 0.3$ V and $NM_H = V_{OH,C} - V_{IH,B} = 3.0 - 1.2 = 1.8$ V. This works logically. However, C's 3 V-class output into a 1.8 V input may exceed B's absolute-maximum input voltage, so check the datasheet or add a level shifter or limiting resistor.

**B driving C:** $NM_L = 1.0 - 0.2 = 0.8$ V, but $NM_H = 1.6 - 2.3 = -0.7$ V. This **fails**: B's 1 is not guaranteed to be read as 1 by C. A level shifter is required.

### Solution 00-02.7

$P_{total} \approx Np \le 10^{-12}$ with $N = 10^9$ gives $p \le 10^{-21}$. Need $Q(d/\sigma) \le 10^{-21}$, so $d/\sigma \ge Q^{-1}(10^{-21}) = 9.505$. With $d = 0.5$ V: $\sigma \le 0.5/9.505 = 52.6$ mV.

Interpretation: the noise can be over 5% of the swing per stage, and a billion stages still make essentially no errors. That margin is what lets digital systems scale.

### Solution 00-02.8

SNR after $N$ stages is the single-stage SNR divided by $N$ (the noise power grows N-fold), so the degradation is $10\log_{10}N$ dB.
(a) $10\log_{10}100 = 20.0$ dB.
(b) $10\log_{10}N = 10$ gives $N = 10$ stages.

### Solution 00-02.9

Half a cycle at 5 GHz is $0.5 \times 200$ ps $= 100$ ps, and $1.5\times10^8 \times 100\times10^{-12} = 15.0$ mm. Even at the speed of light in the chip's insulator, a signal cannot cross a 25 mm die in half a cycle, and real on-chip wires are much slower because of their RC delay. Cross-chip communication must be pipelined over multiple cycles.

### Solution 00-02.10

- $\Gamma_s = \frac{25 - 50}{25 + 50} = -0.333$.
- Launched wave: $1 \times \frac{50}{75} = 0.667$ V.
- First arrival at the open end: $2 \times 0.667 = 1.333$ V.
- The reflected wave returns, reflects at the source to $0.667 \times (-0.333) = -0.222$ V, and adds $2 \times (-0.222) = -0.444$ V at the far end: **0.889 V**.
- The next round trip adds $2 \times (-0.222)(-0.333) = +0.148$ V: **1.037 V**.

The ringing is **smaller** than with 10 Ω (overshoot 33% instead of 67%) and dies faster (factor 1/3 per round trip instead of 2/3), because 25 Ω is closer to the line's 50 Ω. At $R_s = Z_0$ ("source termination"), $\Gamma_s = 0$: the far end goes cleanly from 0 to 1 V in one step. That is the principle behind series-terminated high-speed drivers.

### Solution 00-02.11

(a) Each rising bit draws $CV^2$ from the supply, and rewriting the same value draws nothing, so $\Delta E = 32 \times CV^2 = 32 \times 10\times10^{-15} \times 0.8^2 = 2.05\times10^{-13}$ J $= 0.205$ pJ.
(b) $\Delta P = 0.205\text{ pJ} \times 10^8\text{ s}^{-1} = 2.05\times10^{-5}$ W $= 20.5$ µW.
(c) The supply current depends on how many bits change and in which direction. To first order it tracks the **Hamming distance** between successive register values, and therefore the secret data being processed (e.g., key bytes in a cryptographic operation). By recording thousands of power traces and correlating them with hypotheses about the key ("correlation power analysis"), an attacker can recover the key even though each individual difference is tiny. **Countermeasures:** masking (randomizing the data representation), hiding (constant-switching or dual-rail logic so every operation draws the same energy), and adding noise or random delays ([18-11](../../18-embedded-systems-and-microcontrollers/chapters/18-11-hardware-security.md)).

### Solution 00-02.12

(a) At 3 GHz the period is 333.3 ps, so the budget is $(333.3 - 60)/15 = 18.2$, i.e. **18 gate delays**. At 4 GHz the period is 250 ps, so $(250 - 60)/15 = 12.7$, i.e. **12 gate delays**.

(b) $0.005/1.5\times10^8 = 33.3$ ps, equal to $33.3/15 = 2.2$ gate delays, even at the speed of light. Real RC-limited wires are slower still.

(c) As frequency rises, the fixed flip-flop overhead and the wire delays consume a growing fraction of each cycle, leaving fewer gate delays per stage. Deeper pipelining adds more flip-flop overhead and power (each extra pipeline register is clocked every cycle). Power density limits arrived at the same time ([09-11](../../09-semiconductor-devices/chapters/09-11-cmos-and-scaling.md)). Together these made raising the clock frequency an expensive way to gain performance, so the industry turned to parallelism (more cores, accelerators) instead.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 00-02.2a | λ at 50 Hz | 5996 | km |
| 00-02.2b | λ at 2.4 GHz | 12.49 | cm |
| 00-02.2c | λ at 77 GHz | 3.89 | mm |
| 00-02.2d | frequency of 500 nm light | 599.6 | THz |
| 00-02.3a | $NM_L$ | 0.25 | V |
| 00-02.3b | $NM_H$ | 0.25 | V |
| 00-02.4a | audio cable length in wavelengths | 1.0×10^-4 | — |
| 00-02.4b | board trace length in wavelengths | 32.0 | — |
| 00-02.4c | package trace length in wavelengths | 0.0333 | — |
| 00-02.5a | lumped length limit, $t_r/6$ | 2.50 | mm |
| 00-02.5b | lumped length limit, $t_r/10$ | 1.50 | mm |
| 00-02.6a | $NM_L$, C → B | 0.3 | V |
| 00-02.6b | $NM_H$, C → B | 1.8 | V |
| 00-02.6c | $NM_L$, B → C | 0.8 | V |
| 00-02.6d | $NM_H$, B → C | −0.7 | V |
| 00-02.7a | required per-stage error probability | 1×10^-21 | — |
| 00-02.7b | required $d/\sigma$ | 9.505 | — |
| 00-02.7c | maximum per-stage σ | 52.6 | mV |
| 00-02.8a | SNR degradation after 100 stages | 20.0 | dB |
| 00-02.8b | stages for 10 dB degradation | 10 | — |
| 00-02.9 | distance in half a cycle at 5 GHz | 15.0 | mm |
| 00-02.10a | $\Gamma_s$ | −0.333 | — |
| 00-02.10b | far end, first arrival | 1.333 | V |
| 00-02.10c | far end, second arrival | 0.889 | V |
| 00-02.10d | far end, third arrival | 1.037 | V |
| 00-02.10e | launched wave | 0.667 | V |
| 00-02.11a | energy difference | 0.205 | pJ |
| 00-02.11b | power difference at 10⁸ ops/s | 20.5 | µW |
| 00-02.12a | gate delays per cycle at 3 GHz | 18 | — |
| 00-02.12b | gate delays per cycle at 4 GHz | 12 | — |
| 00-02.12c | 5 mm time of flight | 33.3 | ps |
| 00-02.12d | 5 mm time of flight in gate delays | 2.2 | — |
