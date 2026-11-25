# Course 23 · Final Exam (Memory and Storage Technology)

**Time limit:** 270 minutes, best taken in two sittings of about 135 minutes: Questions 1–6, then Questions 7–12.
**Allowed:** a scientific calculator and the [Course 23 equation sheet](../../../reference/equation-sheets/23-memory-and-storage-technology.md) printed without its chapter links. No notes, no Python and no simulator.

**Instructions.**

- Answer all 12 questions and show every step.
- Questions 1–10 [B] are worth 8 points each (2 per part), and Questions 11 and 12 [C] 12 each (3 per part): 104 points in total. 73 or more (70%) is a strong pass.
- Give numerical answers to 3–4 significant figures, with units.
- Question 11 asks for derivations: results quoted from the equation sheet earn no credit unless derived. Question 12 is a diligence question, partly graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These follow the chapters.

- Bandwidths and capacities are decimal (1 GB = 10⁹ bytes) unless written GiB or KiB; a year is 365.25 days; $q = 1.602 \times 10^{-19}$ C and $k = 8.617 \times 10^{-5}$ eV/K.
- $Q(x)$ is the Gaussian tail probability. Write-amplification questions use the FIFO model $u = e^{-\alpha(1 - u)}$, $A = 1/(1 - u)$, with $\alpha = 1 + OP$ and OP relative to user capacity; you may solve the fixed point by iteration.
- An MRAM bit flips at $f_0e^{-\Delta}$ with $f_0 = 10^9$ s⁻¹ and $\Delta \propto 1/T$. A multiply-accumulate counts as two operations.

---

**1 [B] · The memory wall.** (23-01)
(a) A GPU may spend 80 W on memory at an all-in 5.5 pJ/bit. What bandwidth does that allow, and what power would 6 TB/s draw at the same energy per bit?
(b) An accelerator has six HBM stacks of 1,024 data bits at 8 Gb/s per pin. Find the bandwidth per stack and in total.
(c) At 6 TB/s and a loaded latency of 500 ns, how much data must be in flight, and how many 64-byte requests is that?
(d) The accelerator computes 3 PFLOPS. Find its ridge point in FLOP/byte. A decode kernel performs 2 FLOP per byte read: what fraction of peak compute can it use?

**2 [B] · SRAM.** (23-02)
(a) A 0.024 µm² bitcell's densest macro reaches 30 Mb/mm² (1 Mb = 10⁶ bits). Find the raw bitcell density and the array efficiency.
(b) A die is 35% SRAM by area. It moves to a node where logic shrinks 1.5 times but SRAM not at all. Find the new die area as a fraction of the old, the SRAM share of the new die and the effective shrink.
(c) How many standard deviations of margin must each cell of a 4 MiB (2²⁵-bit) array have for 99% yield without repair?
(d) A 16 MiB (2²⁷-bit) cache leaks 4 pA per bit at 0.75 V. Find its leakage current and power. In retention at 0.45 V, leakage halves for every 100 mV of supply reduction: find the retention power and how many times lower it is.

**3 [B] · DRAM cells and refresh.** (23-03)
(a) A 6 fF cell stores 1.1 V and shares charge with a 36 fF bitline precharged to 0.55 V. Find the signal.
(b) The worst-case stored signal is 0.45 V above precharge, the sense amplifier needs 70 mV, each cell adds 0.07 fF of bitline capacitance and the fixed part is 3 fF. Find the largest bitline capacitance for a 6 fF cell and the largest number of cells per bitline. What power of two would you choose?
(c) A device has $t_{RFC}$ = 410 ns. Find the refresh overhead at $t_{REFI}$ = 7.8125 µs and at 3.90625 µs.
(d) A weak cell retains data for 0.8 s at 45 °C, and retention halves every 10 °C. Find its retention at 85 °C and 95 °C. Does it pass a 64 ms window at 85 °C, and a 32 ms window at 95 °C?

**4 [B] · DRAM interfaces.** (23-04)
(a) A 16-bit channel uses burst length 16 at 8.0 GT/s. Find the bytes per access and the channel bandwidth.
(b) A pseudo-open-drain driver of 40 Ω pulls low against 48 Ω of termination to $V_{DDQ}$ = 1.1 V. Find the low voltage, the current, the power while low, and the energy per bit at 8 Gb/s if half the bits are low.
(c) A 1 V step from a 30 Ω driver enters a 40 Ω line terminated in 60 Ω. Find both reflection coefficients, the launched voltage, the far-end voltage after the first arrival and after the second, and the final value.
(d) A first-order channel has $\tau$ = 0.8 UI. Find $a = e^{-UI/\tau}$, the main cursor and first post-cursor of a one-UI pulse, the worst-case NRZ eye opening (as a fraction of the swing), and the eye after a one-tap DFE removes the first post-cursor.

**5 [B] · HBM.** (23-05)
(a) Find the bandwidth of a 2,048-bit HBM4 stack at 10 Gb/s, of eight such stacks, and the capacity of a 12-high stack of 24 Gb dies.
(b) A data wire presents 0.8 pF and swings 0.4 V. Find the energy per random bit and the interface power of one stack at full bandwidth.
(c) A 16-high stack's layers each have 0.03 K/W, its base die dissipates 12 W and each core die 1.2 W, with all heat leaving through the top. Find the base die's temperature rise.
(d) Each bonded layer yields 99.5%. Find a 16-high stack's yield and the per-layer yield needed for 90%.

**6 [B] · NAND flash.** (23-06)
(a) A cell's control-gate coupling capacitance is 18 aF. Find the threshold shift per electron, and the spacing and electrons per level of a QLC cell with a 5.8 V window.
(b) ISPP moves cells from −1.8 V to +4.2 V in 0.2 V steps, with 22 µs per pulse-and-verify loop. Find the number of pulses and the program time.
(c) With σ = 0.07 V per level, find the QLC margin $d/2\sigma$ and the raw bit error rate.
(d) With an activation energy of 1.0 eV, find the acceleration factor of a 125 °C bake over 40 °C use, and the bake time equivalent to one year at 40 °C.

**7 [B] · SSD controllers.** (23-07)
(a) Find the mapping table of a 15.36 TB drive with 4 KiB units and 4-byte entries, and with 16 KiB units.
(b) Under random writes, find the victim valid fraction and the write amplification at 12% OP, and the write amplification at 25% OP.
(c) The drive has 17.2 TB of raw TLC rated for 3,000 cycles. Find its OP, the worst-case write amplification, its host TBW and its DWPD over 5 years.
(d) It serves 3.2 million random 4 KiB reads per second at 90 µs average latency. Find the commands in flight, the data rate, and the IOPS at queue depth 1.

**8 [B] · ECC and power-loss protection.** (23-07)
(a) A BCH code over GF(2¹³) corrects 48 errors in 1 KiB of data. Find the parity bits, the codeword length, the mean error count and the failure probability at a raw error rate of 2 × 10⁻³ (you may use a Poisson approximation, but state it).
(b) A page holds 16 KiB of data with 2.5 KiB of spare. Find the code rate, the hard-decision capacity at a 1% raw error rate and the highest raw error rate any hard-decision code at this rate could tolerate.
(c) Power-loss protection must supply 25 W for 30 ms through a 90%-efficient converter, from 36 V down to 12 V. Find the energy drawn from the bank and the capacitance.
(d) Explain in two or three sentences why soft-decision LDPC decoding helps a worn drive, and what it costs.

**9 [B] · Emerging memories.** (23-08)
(a) An MTJ has $R_P$ = 5 kΩ and a TMR of 120%, read at 0.12 V through 2.5 kΩ. Find $R_{AP}$, both read currents and the effective contrast.
(b) A 128 Mb (2²⁷-bit) MRAM array must hold data for 10 years with at most one expected flip. Find the required Δ at operating temperature, and the 25 °C Δ needed to meet it at 105 °C.
(c) A PCM cell conducts with 1.6 kΩ and is reset by 250 µA for 40 ns. Find the power, the thermal resistance that gives a 620 K rise, the RESET energy, and the time to cool from 620 K to 140 K if τ = 1.5 ns.
(d) With a drift exponent of 0.08 from $t_0$ = 1 s, find the drift factor after one year and the time to drift by 1.5×.

**10 [B] · Compute-in-memory.** (23-09)
(a) Inputs (0.5, 1.5, 1) drive three rows at 0.1 V per unit. Signed weights (2, −1), (−1, 3), (1, 1) (one row per input, two outputs) are stored as conductance pairs with 8 µS per unit and $G_{min}$ = 0.5 µS. Find the four column currents and the two differential outputs, and check them against the exact products.
(b) With 3% independent relative device variation, find the compute SNR and the effective bits.
(c) A 256-row array uses 8-bit ADCs at 3 fJ per conversion step, with bit-serial inputs and bit-sliced weights at 4 × 4 bits. Find the ADC energy per MAC and the TOPS/W ceiling.
(d) PIM accelerates 70% of a workload's run time 6×. Find the overall speedup, and the fraction that would have to be accelerated for 2.5×.

**11 [C] · Derivations.** (23-03, 23-06, 23-07, 23-09)
(a) Derive the charge-sharing signal of a DRAM cell of capacitance $C_s$ at $V_{cell}$ on a bitline $C_{BL}$ precharged to $V_{pre}$. Evaluate the transfer ratio and the signal for $C_s$ = 7 fF, $C_{BL}$ = 35 fF, $V_{cell}$ = 1.05 V and $V_{pre}$ = 0.525 V.
(b) Show that if every ISPP pulse ends at the same storage-node voltage, each pulse adds charge $C_{CG}\Delta V_{pgm}$ and raises $V_T$ by $\Delta V_{pgm}$. Evaluate the electrons per pulse for $C_{CG}$ = 18 aF and a 0.25 V step.
(c) Derive $u = e^{-\alpha(1 - u)}$ for FIFO garbage collection under uniform random writes, and $A = 1/(1 - u)$. Solve for $u$ and $A$ at α = 1.2 and check the fixed point.
(d) Derive the compute SNR of an analog dot product of $M$ terms with independent relative errors σ, for zero-mean products and for equal positive products. Evaluate both for σ = 4% and $M$ = 128.

**12 [C] · Diligence: a PIM inference card.** (23-01, 23-09)
A start-up pitches an inference card built from eight LPDDR5X-PIM packages: "Each package delivers 614 GB/s, so the card has 4.9 TB/s. A 70-billion-parameter model in 4-bit weights decodes at 140 tokens per second per user, matching an HBM GPU at a fraction of the memory cost, and with 128 GB we serve long contexts."
(a) Find the card's effective bandwidth, the model's size, the bandwidth-bound tokens per second at batch 1, and the same bound with ordinary LPDDR5X-9600 (76.8 GB/s per 64-bit package).
(b) If PIM accelerates 80% of the baseline run time 8×, find the realistic speedup and tokens per second.
(c) The model has 80 layers and 8 KV heads of dimension 128 with an 8-bit KV cache. Find the KV bytes per token, the cache for one 32,768-token sequence, and how many such sequences fit beside the weights in 128 GB.
(d) Find the batch-1 bound of an 8 TB/s HBM GPU on the same model and its ratio to (b). List four questions you would ask the start-up's chief architect, with what a strong answer contains.
