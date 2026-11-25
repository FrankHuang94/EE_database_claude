# Problems 23-04 · DRAM Interfaces: DDR, LPDDR and GDDR

Chapter: [23-04](../chapters/23-04-dram-interfaces.md) · Worked solutions: [23-04 solutions](../solutions/23-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Bandwidths are peak values, in 10⁹ bytes per second. Take $c$ = 3.00 × 10⁸ m/s. "MT/s" is transfers per second per pin. Values marked "assumed" are illustrative; data-sheet values cite the chapter's sources. Problems marked *(lab)* can be checked with `labs/23-04-lab/ddrio.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 23-04.1 [A]

**Prefetch.** Find the core column rate of (a) DDR5-8800 with a 16n prefetch and (b) DDR4-2400 with an 8n prefetch. (c) A server DDR5 subchannel carries 32 data bits plus 8 check bits (assumed): how many bytes cross it in one BL16 burst? (d) What fraction of the data bits are the check bits?

### Problem 23-04.2 [A]

**Bandwidth.** Find the peak bandwidth of (a) an 8-channel DDR5-5600 socket (64 data bits per channel), (b) a 512-bit LPDDR5X bus at 8533 MT/s and (c) a 384-bit GDDR7 bus at 32 Gb/s per pin. Compare (c) with Micron's claim of more than 1.5 TB/s for such a system (chapter source [6]).

### Problem 23-04.3 [A]

**Bits in flight.** Find (a) the UI at 8800 MT/s and (b) the symbol interval of 28 Gb/s GDDR7, which carries 1.5 bits per PAM3 symbol. With 6.67 ps/mm of trace delay, how far does a signal travel in one interval at (c) 8800 MT/s and (d) 28 Gb/s?

### Problem 23-04.4 [B]

**DDR4 POD settings.** *(lab)* A DDR4 line at $V_{DDQ}$ = 1.2 V uses a 48 Ω driver and 60 Ω termination (both available settings in chapter source [2]). Find (a) the low level, (b) the swing, (c) the current and (d) the power while a 0 is driven. At 3200 MT/s find (e) the energy of one 0 and (f) the average termination energy per bit for random data.

### Problem 23-04.5 [B]

**DBI on biased data.** *(lab)* A workload's bits are 0 with probability 0.7, independently. Find the expected number of low wires per byte (a) without DBI and (b) with DDR4's DBI rule, and (c) the saving.

### Problem 23-04.6 [B]

**A lower I/O supply.** Micron's LPDDR5X offers $V_{DDQ}$ = 0.45 V as well as 0.5 V (chapter source [4]). At equal resistances, find (a) the ratio of termination power at 0.45 V to that at 0.5 V and (b) the saving. (c) Find the power while a 1 is driven at 0.45 V with 40 Ω driver and termination.

### Problem 23-04.7 [B]

**Reflections.** *(lab)* A 1.0 V step from a 40 Ω driver enters a 45 Ω line terminated by 60 Ω of ODT. Find (a) the launched wave, (b) the source and (c) the load reflection coefficients, and the far-end voltage (d) after the first arrival, (e) after the second and (f) at the end.

### Problem 23-04.8 [B]

**Fly-by on a server module.** Nine DRAMs sit 14 mm apart on a fly-by route with an effective permittivity of 4.2 (assumed). Find (a) the delay per millimetre, (b) the clock skew from first to last DRAM and (c) that skew in DDR5-8800 UIs.

### Problem 23-04.9 [B]

**Equalizing the next MRDIMM.** A host bus at 12,800 MT/s sees a first-order channel with τ = 60 ps (assumed). Find (a) the UI, (b) $a = e^{-\text{UI}/\tau}$, (c) $h_0$ and (d) $h_1$, the worst-case eye (e) without equalization, (f) with a one-tap DFE and (g) with a full DFE, and (h) the highest unequalized bit rate.

### Problem 23-04.10 [B]

**GDDR7's symbol rate.** A GDDR7 pin carries 32 Gb/s with PAM3. Find (a) the symbol rate and (b) the Nyquist frequency. (c) What loss slope (dB/GHz, linear in frequency) would make PAM3 beat NRZ at this bit rate? (d) Find the Nyquist frequency of the RTX 5090's 28 Gb/s pins.

### Problem 23-04.11 [B]

**Building 1 TB/s.** An accelerator needs 1 TB/s of peak memory bandwidth. Find the number of (a) DDR5-6400 64-bit channels, (b) LPDDR5X-9600 x16 channels and (c) 32 Gb/s x32 GDDR7 devices needed (round up), and (d, e, f) the data pins each option uses. (g) With 32 Gb GDDR7 devices, what capacity does (c) give? (h) With one 64 GB DIMM per DDR5 channel (assumed), what capacity does (a) give?

### Problem 23-04.12 [C]

**Energy per bit, core plus pins.** A DDR5 x8 device spends 0.1638 nJ to activate a row (Example 23-03.7) and delivers 128 bits per burst. Its pins cost Example 23-04.3's 1.28 pJ/bit. Find the energy per bit (a) of the activation alone for one burst per activation, and the total (b) for one burst per activation and (c) for a fully read 8,192-bit row. With LPDDR5X pins at Example 23-04.4's 0.163 pJ/bit and the same core, find the total (d) for one burst and (e) for a full row. (f) What share of (b) is the core?

### Problem 23-04.13 [B]

**Write-leveling resolution.** A controller's delay line divides one DDR5-6400 clock period into 128 steps (assumed). Find (a) the step size and (b) the trace length it corresponds to at 6.67 ps/mm.

### Problem 23-04.14 [C]

**Why a first-order channel never favours PAM.** For a first-order channel with time constant τ and NRZ bit time $T$, let $x = T/\tau$. Show that the worst-case eye is $1 - 2e^{-x}$ for NRZ, $\tfrac12(1 - e^{-1.5x}) - e^{-1.5x}$ for PAM3 and $\tfrac13(1 - e^{-2x}) - e^{-2x}$ for PAM4 at the same bit rate. Find where each eye closes, and prove that NRZ's eye is at least as large as PAM3's and PAM4's wherever any eye is open. Evaluate all three at 48 Gb/s with τ = 20 ps: (a) NRZ, (b) PAM3, (c) PAM4. (d)–(f) Give the closing values of $x$.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Prefetch, burst and granularity | 1 |
| 2. Bandwidth and pins | 2, 11 |
| 3. Termination energy and DBI | 4, 5, 6, 12 |
| 4. Reflections, flight time and training | 3, 7, 8, 13 |
| 5. ISI, DFE and PAM | 9, 10, 14 |
| 6. Choosing an interface | 11, 12 |
