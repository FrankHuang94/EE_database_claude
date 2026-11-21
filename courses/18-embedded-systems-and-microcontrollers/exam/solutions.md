# Course 18 · Final Exam Solutions (Embedded Systems and Microcontrollers)

Exam: [README.md](README.md). Every number below is recomputed by [verify_18_exam.py](../verify/verify_18_exam.py):

- addresses, masks and linker symbols by integer arithmetic, with the read-modify-write race replayed as an explicit interleaving;
- wait states by searching for the smallest whole number of cycles covering the access time; CPIs checked against the 18-01 lab's cycle-level fetch simulator;
- interrupt response times against the 18-03 lab's discrete-event simulation at the critical instant; prescalers and reloads by search;
- buffer sizes against the 18-04 lab's block simulator, which shows overruns just below each bound and none at the chosen sizes;
- rise and settling times by root finding, ADC averaging by Monte Carlo, the multiplexed-input error by the exact charge-sharing recursion, and the PWM ripple from the filter's exact steady state;
- RTOS response times, the three priority-inversion timelines and the queue depth by the 18-07 lab's scheduler and occupancy simulations;
- the coin-cell droop by integrating the circuit equation, confirmed in ngspice by [coin_cell_exam.cir](coin_cell_exam.cir);
- the complementary filter by simulated noise and bias; CPA correlations measured on the 18-11 lab's simulated traces, PUF lengths from the binomial tail, and the timing attack's query count by running the lab's attack.

---

## Solutions

### Solution 1

(a) $0x4002\,0C00 + 0x14$ = **0x40020C14**, in the **peripheral** region (0x4000 0000–0x5FFF FFFF). 192 KiB is $192 \times 1024 = 196\,608$ = 0x3 0000 bytes, so the last SRAM address is $0x2000\,0000 + 0x3\,0000 - 1$ = **0x2002FFFF**.

(b) $\text{WS} = \lceil f\,t_{acc}\rceil - 1$. At 48 MHz, $f\,t_{acc} = 1.92$, so WS = **1**. At 120 MHz, $f\,t_{acc} = 4.8$, so WS = **4**. Two wait states give three cycles, which must cover 40 ns: $f \le 3/40\ \text{ns}$ = **75** MHz.

(c) With 64-bit (8-byte) lines, a line holds only 4 instructions but takes $1 + \text{WS} = 5$ cycles to read, so even straight-line code waits for the flash: the sequential term is $5 \times 2/8 = 1.25$. Each taken branch adds WS = 4 stall cycles: $\text{CPI} = 1.25 + 0.10 \times 4$ = **1.65**, and the rate is $120/1.65$ = **72.7** instructions per µs. With 128-bit lines the line holds 8 instructions, more than the 5 cycles it takes to read, so the prefetch keeps up and the sequential term is 1: $\text{CPI} = 1 + 0.4$ = **1.40**, $120/1.4$ = **85.7** per µs. The wider line removes the sequential stall; only the branch penalty remains, and that needs a cache.

(d) $400/4.10 = 97.56$ MHz at the core's published efficiency, divided by 0.96 for the 4% the cache does not recover: **101.6** MHz.

### Solution 2

(a) Flash holds `text` and the initial values of `.data`: $41\,872 + 2\,316$ = **44 188** bytes, $44\,188/524\,288$ = **8.43** %. SRAM holds `.data`, `.bss`, the heap and the stack: $2\,316 + 14\,622 + 4\,096 + 6\,144$ = **27 178** bytes, $27\,178/98\,304$ = **27.65** %.

(b) $2316$ = 0x90C, already a multiple of 4: `_edata` = **0x2000090C**. `.bss` is 14 622 = 0x391E bytes: $0x2000\,090C + 0x391E = 0x2000\,422A$, aligned up to `_ebss` = **0x2000422C**. The heap ends at $0x2000\,422C + 0x1000 = 0x2000\,522C$. The stack top is $0x2000\,0000 + 96 \times 1024 = 0x2001\,8000$, and its bottom $0x2001\,8000 - 0x1800$ = **0x20016800**. Free SRAM: $0x2001\,6800 - 0x2000\,522C = 0x1\,15D4$ = **71 124** bytes, which is the 98 304 bytes less the 27 178 of (a) and the 2 bytes of alignment padding.

(c) The mask is $(2^3 - 1) \ll 4$ = **0x70**. Clearing the field: $0x152C7 \mathbin{\&} \lnot 0x70$ = **0x00015287** (bits [6:4] of 0xC7 = 1100 0111 were 100). Inserting $5 \ll 4 = 0x50$: **0x000152D7**.

The race: main reads 0x152C7. The handler reads 0x152C7, clears bit 0 and writes 0x152C6. Main then writes the value it computed from its stale copy, **0x000152D7**: bit 0 is set again and the handler's change is lost. The correct result has both changes, **0x000152D6**. The fix must be on main's side, because it is main's write-back of the whole register that destroys the bit: make main's read-modify-write atomic (a critical section that masks the handler, or `LDREX`/`STREX` where the core and the register support exclusive access), or have both contexts change their bits only through set/clear registers, so that neither ever writes back a stale copy.

(d) Words: $\lceil 2316/4\rceil = 579$ to copy and $\lceil 14\,622/4\rceil = 3656$ to zero. Cycles: $579 \times 7 + 3656 \times 4 = 4053 + 14\,624$ = **18 677**, which at 16 MHz is **1.167** ms.

### Solution 3

(a) $2^2$ = **4** preemption levels with $2^1$ = **2** subpriorities each. The implemented bits are 7:5: group 1 = 0b01 in bits 7:6 and subpriority 1 in bit 5 give 0b0110 0000 = **0x60**. A request with 0x40 (0b010…: group 1, subpriority 0) has the same group priority, so it **does not** preempt; it would only be taken first among pending group-1 requests. 0x20 (0b001…: group 0) is more urgent and **preempts**.

(b) $U = 4/40 + 12/100 + 25/500$ = **0.27**. A has nothing above it: $R_A = 4 + 6$ = **10** µs, within its 15 µs deadline. B starts at $12 + 6 = 18$: $18 + \lceil 18/40\rceil \times 4 = 22$, and $\lceil 22/40\rceil = 1$ again: $R_B$ = **22** µs. C starts at $25 + 6 = 31$: $31 + \lceil 31/40\rceil 4 + \lceil 31/100\rceil 12 = 47$; then $31 + \lceil 47/40\rceil 4 + 12 = 51$; then $\lceil 51/40\rceil = 2$ again gives 51: $R_C$ = **51** µs.

(c) $R_A = 4 + B \le 15$ allows **11** µs of blocking. With 14 µs: $R_A = 4 + 14$ = **18** µs, a missed deadline. B: $26 \to 26 + 4 = 30 \to 30$: **30** µs. C: $39 \to 39 + 4 + 12 = 55 \to 39 + 8 + 12 = 59 \to 59$: **59** µs.

(d) Implement the critical section with BASEPRI set at B's priority instead of PRIMASK, so that it masks B and C but never A (provided the section shares no data with A's handler). A then sees no blocking: $R_A$ = **4** µs. B and C keep 30 and 59 µs, which is acceptable if their own deadlines allow it.

### Solution 4

(a) $(PSC + 1)(ARR + 1) = 72 \times 10^6/25 \times 10^3 = 2880$. The finest resolution uses the largest ARR: PSC = 0, ARR = **2879**. Resolution $\log_2 2880$ = **11.49** bits; CCR $= 0.625 \times 2880$ = **1800**.

(b) A center-aligned period is $2 \times ARR$ ticks: ARR = $2880/2$ = **1440**, and the resolution is $\log_2 1440$ = **10.49** bits, one bit less.

(c) $PSC + 1 = 72$, so PSC = **71**. The counter wrapped between the captures: $(0x0A28 - 0xFE70) \bmod 2^{16} = 0x1\,0A28 - 0xFE70 = 0x0BB8$ = **3000** ticks = 3.000 ms, so the frequency is $1/3\ \text{ms}$ = **333.3** Hz. One tick in 3000 is a resolution of **0.033** %.

(d) The timeout is $\text{prescaler} \times \text{reload}/f_{LSI}$: nominal $32 \times 2000/32\,000$ = **2.0** s, shortest $64\,000/47\,000$ = **1.362** s, longest $64\,000/17\,000$ = **3.765** s. A 1.5 s loop is **not** safe: a part whose oscillator runs fast resets while healthy. The reload must satisfy $32R/47\,000 \ge 1.5$ s, so $R \ge 2203.1$: **2204**, whose longest timeout is $32 \times 2204/17\,000$ = **4.149** s. That is the worst-case time a hang lasts before reset; a 25% margin on the loop time would need a larger reload still.

### Solution 5

(a) $16\,000 \times 50/(48 \times 10^6)$ = **1.667** %. With DMA: $16\,000/160$ = **100** interrupts a second, $100 \times 300/(48 \times 10^6)$ = **0.0625** %, and each block lasts $160/16\,000$ = **10** ms.

(b) $bf_s = 1.2 \times 10^{-6} \times 5 \times 10^5 = 0.6 < 1$. $N \ge (a + L)f_s/(1 - bf_s) = 70 \times 10^{-6} \times 5 \times 10^5/0.4$ = **87.5**, so **128** as a power of two. Memory: $2 \times 128 \times 2$ = **512** bytes. Worst latency, for a block's first sample: $128/500\,000 = 256$ µs to fill, then $40 + 30 + 1.2 \times 128 = 223.6$ µs to process: **479.6** µs.

(c) Two conditions. The deadline: the CPU has two block times, so $N \ge 35/(2 - 0.6)$ = **25.0**. The throughput floor: the CPU must also keep up on average, $a + bN \le N/f_s$, so $N \ge af_s/(1 - bf_s) = 15/0.4$ = **37.5**. The floor binds. A block of 32 satisfies the deadline condition, but it takes $30 + 1.2 \times 32$ = **68.4** µs to process while a new one arrives every 64 µs, so the backlog grows without limit. The smallest power of two is **64**: memory $3 \times 64 \times 2$ = **384** bytes, worst latency $128 + 40 + 30 + 76.8$ = **274.8** µs. The third buffer saves memory and 205 µs of latency.

(d) $460\,800/10$ = **46 080** bytes/s; in 8 ms, **368.6** bytes. The ring must exceed that: **512** bytes. Head $= 512 - 100$ = **412**; unread $= (412 - 450) \bmod 512 = 412 + 512 - 450$ = **474** bytes. The head has wrapped past the end of the ring, and the unsigned modular difference handles it.

### Solution 6

(a) $48 \times 10^6/(16 \times 230\,400)$ = **13.02**; the integer 13 gives $48 \times 10^6/208$ = **230 769** baud, an error of **0.160** %, harmless. For 921 600 baud the ideal divisor is **3.255**; the integer 3 gives 1 000 000 baud, **8.51** % fast, far outside the +4.58% limit of a 16× receiver. In sixteenths, $3.255 \times 16 = 52.08 \to 52/16$ = **3.25**, which gives **923 077** baud, again +0.160%.

(b) Half a period must cover the round trip: $3 + 1.5 + 12 + 1.5 + 4 = 22$ ns, so $f \le 1/44\ \text{ns}$ = **22.7** MHz. With translators the round trip is 27 ns: **18.5** MHz.

(c) $R_{p,min} = (2.5 - 0.4)/3\ \text{mA}$ = **700** Ω. The 30–70% rise time of an RC is $\ln(0.7/0.3)R_pC = 0.8473R_pC$, so $R_{p,max} = 300\ \text{ns}/(0.8473 \times 250\ \text{pF})$ = **1416** Ω. With 1.0 kΩ, $t_r = 0.8473 \times 1000 \times 250\ \text{pF}$ = **212** ns.

(d) Nine bytes (address + W, register, address + R and six data bytes) of 9 periods, plus START, repeated START and STOP: $81 + 3$ = **84** periods, $84 \times 2.5\ \mu\text{s}$ = **210** µs. Data: $48/84$ = **57.1** %. At most $1/210\ \mu\text{s}$ = **4762** reads a second, before any processing. Reading several samples per transaction from a FIFO raises the data fraction further.

### Solution 7

(a) $2.5/16\,384$ = **152.6** µV. $1.000/152.6\ \mu\text{V} = 6553.6$, which rounds to code **6554**. SQNR $= 6.02 \times 14 + 1.76$ = **86.04** dB. ENOB $= (78.0 - 1.76)/6.02$ = **12.66** bits.

(b) $e^{-t_s/\tau} \le 2^{-15}$ needs $t_s \ge \tau\ln 2^{15}$ = **10.40** τ. With 2 kΩ, $\tau = 3\ \text{kΩ} \times 5\ \text{pF} = 15$ ns, and $t_s \ge 15 \times 10.40$ = **156** ns. At 100 ns, $R_s + R_{sw} \le 100\ \text{ns}/(5\ \text{pF} \times 10.40) = 1924$ Ω, so $R_{s,max}$ = **924** Ω.

(c) Noise $1.2/\sqrt{64}$ = **0.15** LSB rms; $\tfrac12\log_2 64$ = **3** extra bits; output rate $10^6/64$ = **15.6** kS/s. This holds only if the noise is white and at least about half an LSB rms, so that it dithers the quantizer; 1.2 LSB qualifies.

(d) $48\ \text{MHz}/256$ = **187.5** kHz, $T$ = 5.333 µs. The worst-case ripple (at 50% duty, for $\tau \gg T$) is $V_{DD}T/(4\tau)$; setting it to one LSB, $V_{DD}/256$, gives $\tau \ge 256T/4$ = **341.3** µs. Bandwidth $1/(2\pi\tau)$ = **466** Hz; settling to half an LSB, $\tau\ln 2^9$ = **2.13** ms.

### Solution 8

(a) $1000 \times 2\ \mu\text{s} + 800 \times 1.5\ \mu\text{s} = 3.2$ ms per second = **0.32** %.

(b) $U = 2/6 + 3/10 + 4/20$ = **0.833**, above the bound $3(2^{1/3} - 1)$ = **0.780**; the hyperbolic product $(1.333)(1.3)(1.2)$ = **2.08** exceeds 2. Both tests are **inconclusive**: they are sufficient, not necessary. Exact analysis: $R_A$ = **2** ms. $R_B$: from 3, $3 + \lceil 3/6\rceil 2 = 5$, and again 5: **5** ms. $R_C$: from 4, $4 + 2 + 3 = 9$; $4 + 2\lceil 9/6\rceil + 3 = 11$; $4 + 4 + 3\lceil 11/10\rceil = 14$; $4 + 2\lceil 14/6\rceil + 6 = 16$; $4 + 6 + 6 = 16$: **16** ms ≤ 20. The set is schedulable.

(c) *No protocol:* L runs 0–2 (it locks S at 1); H preempts at 2, runs 2–3, then blocks on S; M arrives at 3 and, outranking L, runs 3–9; L finishes its critical section 9–11; H runs 11–13. Response **11** ms, 6 of them caused by a task that never touches S. *Inheritance:* at 3, L runs at H's priority, finishes S at 5; H runs 5–7: **5** ms. *Ceiling:* L runs at the ceiling from 1 to 4, so H cannot start until 4; H runs 4–7: **5** ms, the blocking moved to its start. The bound: H can be blocked at most once, for L's longest critical section on S, $B_H$ = **3** ms, so $R_H \le C_H + B_H$ = **6** ms, consistent with the 5 ms observed (L had already used 1 ms of its section when H arrived).

(d) Records arriving during a stall wait until it ends, including one at its very start and one at its very end: $\lfloor 30/4\rfloor + 1$ = **8** slots, **128** bytes of storage. With 32 ms: $\lfloor 32/4\rfloor + 1$ = **9**: the off-by-one at the boundary is where queues overflow.

### Solution 9

(a) Single slot: $512 - 48$ = **464** KiB. Two slots: $464/2$ = **232** KiB. Swap through scratch: $(464 - 16)/2$ = **224** KiB.

(b) $200/8$ = **25** sectors. A sector copy is an erase plus $8192/16 = 512$ programs: $30 + 512 \times 0.05$ = **55.6** ms. Overwrite: $25 \times 55.6\ \text{ms}$ = **1.39** s; swap through scratch, three copies per sector: **4.17** s. The scratch sector is erased once per image sector per update: $10\,000/25$ = **400** updates.

(c) Hash: $204\,800 \times 20/(96 \times 10^6)$ = **42.67** ms; signature $3 \times 10^6/(96 \times 10^6)$ = **31.25** ms; total **73.92** ms. With a hash engine the hash takes 2.13 ms and the total is **33.38** ms; the signature then dominates.

(d) $204\,800/40\,000$ = **5.12** s. Power cuts arrive at $\lambda = 3/2\,592\,000$ per second, so the probability of at least one in the window is $1 - e^{-\lambda \times 5.12}$ = **5.93e-6**, or **11.9** devices per update across 2 million. Small, but certain to happen fleet-wide, each a return or a truck roll; a two-slot design, or a bootloader that keeps a recovery path, makes an interrupted download harmless.

### Solution 10

(a) Charge per 2 s period: $1.5\ \text{mA} \times 4\ \text{ms} + 5\ \text{mA} \times 2.5\ \text{ms} = 6 + 12.5 = 18.5\ \mu\text{C}$, plus sleep $2\ \mu\text{A} \times 1.9935\ \text{s} = 3.987\ \mu\text{C}$: 22.49 µC every 2 s, $\bar I$ = **11.24** µA. Life: $225\ \text{mAh}/11.24\ \mu\text{A} = 20\,012$ h = **834** days. The radio's share: $12.5/22.49$ = **55.6** %.

(b) Stop beats sleep when the current saved over the idle time exceeds the wake-up cost: $t > 150\ \text{nC}/(0.6\ \text{mA} - 4\ \mu\text{A})$ = **0.252** ms. Standby beats stop when $t > 6\ \mu\text{C}/(4 - 0.3)\ \mu\text{A}$ = **1.62** s. The node of (a) idles about 1.99 s, just above 1.62 s, so standby wins, by a small margin: if its state is cheap to restore, otherwise stop.

(c) At 16 MHz: active $2 \times 10^6/16 \times 10^6 = 125$ ms at $800 + 300 = 1100\ \mu\text{A}$, 137.5 µC, plus $1.5\ \mu\text{A} \times 0.875$ s: **138.8** µC. At 64 MHz: 31.25 ms at 3500 µA, 109.4 µC, plus sleep: **110.8** µC. Racing to idle saves **20.2** %, all of it in the 300 µA fixed current; the dynamic part, $50\ \mu\text{A/MHz} \times 2 \times 10^6$ cycles = 100 µC, is the same at both clocks.

(d) Without a capacitor the droop is $10\ \text{mA} \times 60\ \Omega$ = **0.60** V: the supply falls to 2.40 V, below the 2.5 V brown-out, and the MCU resets mid-burst. With a capacitor $C$ at the load, the cell and the capacitor form an RC with $\tau = 60C$, and the droop after 3 ms is $0.6(1 - e^{-3\ \text{ms}/\tau})$. Setting it to 0.3 V: $\tau = 3\ \text{ms}/\ln 2 = 4.33$ ms, so $C$ = **72.1** µF. With 100 µF ($\tau$ = 6 ms): $0.6(1 - e^{-0.5})$ = **236** mV, a supply of 2.76 V. Choose 100 µF or more for tolerance, ageing and the cell's higher resistance at end of life.

### Solution 11

(a) $90\ \mu\text{g} \times \sqrt{100}$ = **0.90** mg rms. Near level, tilt $= \arcsin(a/g)$: $\arcsin(0.9 \times 10^{-3})$ = **0.0516** °. Averaging 400 independent samples divides it by 20: **0.00258** °.

(b) The data sheet's density ρ is one-sided, like the accelerometer's in (a), so the rate noise's two-sided level is $\rho^2/2$, and integrating it for a time $t$ gives an angle variance $\rho^2t/2$: $\sigma_\theta = \rho\sqrt{t/2}$. In °/√h that is ARW $= 60\rho/\sqrt2$ = **0.212** °/√h (the common shortcut $60\rho$ overstates it by √2). After 100 s, the angle noise is $0.005\sqrt{50}$ = **0.0354** °, while the bias drifts $0.2 \times 100$ = **20** °: as in 18-10, bias, not noise, limits a gyroscope over minutes.

(c) $\tau = \alpha\,\Delta t/(1 - \alpha) = 0.99 \times 0.005/0.01$ = **0.495** s. The bias error settles at $b\tau = 0.2 \times 0.495$ = **0.099** °. The first-order low-pass $y_n = \alpha y_{n-1} + (1 - \alpha)x_n$ passes $\sqrt{(1 - \alpha)/(1 + \alpha)} = \sqrt{0.01/1.99}$ = **0.0709** of white noise's rms.

(d) SNR $= m^2I/(4qB) = (0.005)^2 \times 2 \times 10^{-6}/(4 \times 1.602 \times 10^{-19} \times 8) = 9.75 \times 10^6$, or **69.9** dB. The LED draws $15\ \text{mA} \times 80\ \mu\text{s} \times 50$ = **60** µA on average, more than the rest of a sleeping ring.

### Solution 12

(a) $(2^{24} + 1)/2/200$ s = 41 943 s = **11.65** hours. With a forced 1 s per wrong try, $(2^{24} + 1)/2$ s = **97.1** days: rate limiting turns a lunchtime attack into a quarter-year one, and exponential lockouts or a hard lock do far better.

(b) Five bytes by timing, at most $256 \times 100$ queries each, plus at most 256 accept/reject tries for the last: $5 \times 256 \times 100 + 256$ = **128 256** queries.

(c) $\rho = \sqrt{2/(2 + 36)}$ = **0.229**, $N = (4/0.229)^2 = 16 \times 38/2$ = **304**. At σ = 12: $16 \times 146/2$ = **1168** traces, 3.84 times more for twice the noise.

(d) The smallest odd $n$ with $1 - (1 - P_{bit})^{128} \le 10^{-6}$, where $P_{bit} = P(\text{more than } n/2 \text{ flips})$, is **27** (at 25 the key fails with probability 1.45e-6), using $128 \times 27$ = **3456** cells, with a key failure probability of **4.1e-7**. Real designs use stronger codes (BCH, Reed–Muller) with helper data, needing far fewer cells.

### Solution 13

(a) *Wait states.* The flash interface is clocked at $f$, so a read takes a whole number of cycles, $1 + \text{WS}$, and must last at least $t_{acc}$: $(1 + \text{WS})/f \ge t_{acc}$. The smallest such WS is $\lceil f\,t_{acc}\rceil - 1$ (at least 0). Each wait state therefore buys a band of clock frequencies $1/t_{acc}$ wide.

*CPI.* Let $s$ be the instruction size, $L$ the line size, $b$ the taken branches per instruction and $m$ the fraction of their targets not already buffered or cached. Sequential code consumes $L/s$ instructions per line, and the flash delivers a line every $1 + \text{WS}$ cycles, so the sequential CPI is $\max(1, (1 + \text{WS})s/L)$: 1 if the prefetch keeps ahead, more if the line is too narrow. A taken branch to an unbuffered target discards the prefetch and waits for a new read, $\text{WS}$ cycles beyond the refill a zero-wait memory would also cost. Adding the two: $\text{CPI} \approx \max(1, (1 + \text{WS})s/L) + b\,m\,\text{WS}$.

At 75 MHz, $f\,t_{acc} = 3.0$ exactly, so WS = 2, CPI $= 1 + 0.1 \times 2 = 1.2$ (a 16-byte line holds 8 instructions, more than 3 cycles' worth), and the rate is $75/1.2$ = **62.5** per µs. At 80 MHz, $f\,t_{acc} = 3.2$, so WS = 3, CPI = 1.3 and the rate is $80/1.3$ = **61.5** per µs. The clock rose 6.7%, but the CPI rose 8.3%: just above a band edge every branch costs one more cycle, so the part delivers more work at the top of a band than at the bottom of the next.

(b) *Settling.* Through $R_s + R_{sw}$ the S/H capacitor approaches the input exponentially with $\tau = (R_s + R_{sw})C_{sh}$; the worst initial error is $V_{REF}$. Half an LSB is $V_{REF}/2^{N+1}$, so $V_{REF}e^{-t_s/\tau} \le V_{REF}/2^{N+1}$ gives $t_s \ge \tau\ln 2^{N+1} = (N + 1)\tau\ln 2$.

*Charge sharing.* With $C_{ext}$ at the pin charged to $V$ and $C_{sh}$ arriving at $V_0$, charge is conserved when they connect: $C_{ext}V + C_{sh}V_0 = (C_{ext} + C_{sh})V'$, so the step is $V - V' = (V - V_0)C_{sh}/(C_{ext} + C_{sh})$. With $|V - V_0| = V_{REF}$, keeping it under $V_{REF}/2^{N+1}$ needs $C_{ext} \ge C_{sh}(2^{N+1} - 1)$.

*Equivalent resistance.* Each sample removes the charge $C_{sh}(V_x - V_0)$ from the pin, $f$ times a second, so the average current is $fC_{sh}(V_x - V_0)$: exactly the current a resistor $1/(fC_{sh})$ to $V_0$ would draw. With $C_{ext}$ large ($R_sC_{ext} \gg 1/f$) the pin voltage is nearly constant and this average is what the source sees, so the pin sits at the divider value $V_s \cdot R_{eq}/(R_s + R_{eq})$.

For 5 pF at 14 bits: $C_{ext} \ge 5\ \text{pF} \times 32\,767$ = **163.8** nF, so 220 nF passes (its step, 0.057 mV, is under the 0.076 mV half LSB). At 50 kHz, $R_{eq} = 1/(5 \times 10^4 \times 5\ \text{pF}) = 4$ MΩ, and the error is $2.5 \times 10\ \text{kΩ}/(10\ \text{kΩ} + 4\ \text{MΩ})$ = **6.23** mV = **40.9** LSB. The exact recursion of 18-06 gives 6.26 mV, the estimate plus the small charge-sharing step. The external capacitor fixes the step, not the DC error: that needs a lower source resistance, a buffer, or a lower sampling rate on this channel.

(c) *Correlation.* A uniform byte's 8 bits are independent fair coins, so $\text{HW}(v)$ is binomial with $n = 8$, $p = 1/2$: mean 4, variance $8 \times \tfrac14 = 2$. For $\ell = \text{HW} + n$ with $n$ independent of HW, $\text{Cov}(\text{HW}, \ell) = \text{Var}(\text{HW}) = 2$ and $\text{Var}(\ell) = 2 + \sigma^2$, so

$$
\rho = \frac{2}{\sqrt{2(2 + \sigma^2)}} = \sqrt{\frac{2}{2 + \sigma^2}} .
$$

*Traces.* For a wrong key the predicted Hamming weights are nearly uncorrelated with the leakage, and the sample correlation of $N$ unrelated pairs has a standard deviation of about $1/\sqrt N$ (03-04). The right key stands out by $z$ standard deviations when $\rho\sqrt N \approx z$, so $N \approx (z/\rho)^2 = z^2(2 + \sigma^2)/2$, which tends to $z^2\sigma^2/2$ when $\sigma^2 \gg 2$: the trace count grows as the noise variance, four times per doubling of σ.

At σ = 10 and $z$ = 4: $\rho = \sqrt{2/102}$ = **0.140**, $N = 16 \times 102/2$ = **816**, against the high-noise limit $16 \times 100/2$ = **800**.

*Masking.* With a fresh uniform mask $m$, $v \oplus m$ is uniform whatever $v$ is, so its Hamming weight is independent of $v$, of the plaintext and of the key. Every key guess then predicts something uncorrelated with the leakage, and no number of traces separates the right key at first order. (A second-order attack, combining two leakage points that involve the same mask, remains possible: masking raises the order of the attack, and its cost.)

### Solution 14

(a) The LED's average current is $12\ \text{mA} \times 60\ \mu\text{s} \times 25$ = **18** µA. Total: $18 + 25 + 35 + 40$ = **118** µA. Usable charge $0.85 \times 18$ mAh = 15.3 mAh lasts $15.3/0.118 = 129.7$ h = **5.40** days. A week needs at most $15.3\ \text{mAh}/168\ \text{h}$ = **91.1** µA, 23% less than the data sheet's own numbers. The claim holds only for the rated capacity at room temperature, or with a lower PPG duty cycle or a lighter radio schedule. *Rubric (3 points):* correct average current (1), life with derating (1), the required current and where it must come from (1).

(b) $458\,752\ \text{B}/60\ \text{kB/s}$ = **7.65** s for a full image, before installation and the secure-boot check. Three seconds at 60 kB/s moves 180 kB, **39.2** % of the image, so the claim implies delta or compressed updates, or a much faster link than the one they measured. Probe: (1) whether "update" includes installation and verification; (2) delta-update dependencies: a patch per installed version, working space and the patching code's own robustness; (3) whether the device keeps a bootable image during the update (two slots or a recovery bootloader) and has anti-rollback. *Rubric:* time (1), the implication (1), two well-chosen risks (1).

(c) A raw 128-bit key reads back correctly with probability $0.97^{128}$ = **0.0203**: it fails 98% of the time. "97% stable" is a per-cell figure, and keys are 128 cells at once. With a repetition code the smallest odd length is **15** (13 gives 4.1e-6), using $128 \times 15$ = **1920** cells; a BCH or Reed–Muller code with helper data does it with far fewer. Error correction is not optional, so the claim shows either a misunderstanding or marketing. *Rubric:* the probability (1), the code length and cells (1), the conclusion (1).

(d) Four questions, with a strong and an evasive answer for each. Any four of comparable depth earn the 3 points.

1. *"Show the battery-life measurement: which firmware, temperature, PPG duty cycle and radio schedule?"* Strong: a current profile from a power analyzer, a breakdown matching (a), and the conditions under which a week holds. Evasive: "typical use", a capacity figure without derating, or a lab number at 25 °C only.
2. *"What happens if power or the link fails halfway through an update?"* Strong: two slots or a recovery bootloader, an image verified before it boots, a confirm-or-revert step, and a power-cut test campaign. Evasive: "our updates are fast, so it doesn't happen".
3. *"How are device keys provisioned, and is any key shared across the fleet?"* Strong: per-device keys from the PUF with error correction and helper data, or injected in a secure facility, plus a certificate chain. Evasive: "keys are hard-coded but protected", or a single shared key (the honeypot of 18-11).
4. *"Which certification and regulatory obligations have you planned for?"* Strong: a target PSA Certified or SESIP level and evaluation lab, and a support and vulnerability-handling plan that meets the EU Cyber Resilience Act's obligations (18-11). Evasive: "the chip vendor is certified, so we are too".

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| X18.1a | output register address | 0x40020C14 | — |
| X18.1b | last SRAM address | 0x2002FFFF | — |
| X18.1c | wait states at 48 MHz | 1 | — |
| X18.1d | wait states at 120 MHz | 4 | — |
| X18.1e | highest clock with 2 wait states | 75 | MHz |
| X18.1f | CPI, 64-bit lines | 1.65 | — |
| X18.1g | instruction rate, 64-bit lines | 72.7 | per µs |
| X18.1h | CPI, 128-bit lines | 1.40 | — |
| X18.1i | instruction rate, 128-bit lines | 85.7 | per µs |
| X18.1j | clock for 400 CoreMark | 101.6 | MHz |
| X18.2a | flash used | 44188 | bytes |
| X18.2b | flash used | 8.43 | % |
| X18.2c | SRAM used | 27178 | bytes |
| X18.2d | SRAM used | 27.65 | % |
| X18.2e | _edata | 0x2000090C | — |
| X18.2f | _ebss | 0x2000422C | — |
| X18.2g | bottom of the stack | 0x20016800 | — |
| X18.2h | free SRAM | 71124 | bytes |
| X18.2i | MODE mask | 0x70 | — |
| X18.2j | register with MODE cleared | 0x00015287 | — |
| X18.2k | register with MODE = 5 | 0x000152D7 | — |
| X18.2l | value after the race | 0x000152D7 | — |
| X18.2m | correct value | 0x000152D6 | — |
| X18.2n | startup cycles | 18677 | — |
| X18.2o | startup time | 1.167 | ms |
| X18.3a | preemption levels | 4 | — |
| X18.3b | subpriorities | 2 | — |
| X18.3c | priority byte, group 1 sub 1 | 0x60 | — |
| X18.3d | utilization | 0.27 | — |
| X18.3e | R_A, 6 µs blocking | 10 | µs |
| X18.3f | R_B, 6 µs blocking | 22 | µs |
| X18.3g | R_C, 6 µs blocking | 51 | µs |
| X18.3h | longest tolerable blocking for A | 11 | µs |
| X18.3i | R_A, 14 µs blocking | 18 | µs |
| X18.3j | R_B, 14 µs blocking | 30 | µs |
| X18.3k | R_C, 14 µs blocking | 59 | µs |
| X18.3l | R_A with BASEPRI | 4 | µs |
| X18.4a | ARR, edge-aligned | 2879 | — |
| X18.4b | resolution, edge-aligned | 11.49 | bits |
| X18.4c | compare value for 62.5% | 1800 | — |
| X18.4d | ARR, center-aligned | 1440 | — |
| X18.4e | resolution, center-aligned | 10.49 | bits |
| X18.4f | prescaler for 1 µs ticks | 71 | — |
| X18.4g | period in ticks | 3000 | — |
| X18.4h | frequency | 333.3 | Hz |
| X18.4i | measurement resolution | 0.033 | % |
| X18.4j | nominal watchdog timeout | 2.0 | s |
| X18.4k | shortest timeout | 1.362 | s |
| X18.4l | longest timeout | 3.765 | s |
| X18.4m | smallest safe reload | 2204 | — |
| X18.4n | longest timeout at that reload | 4.149 | s |
| X18.5a | CPU load, per-sample interrupts | 1.667 | % |
| X18.5b | interrupts per second with DMA | 100 | — |
| X18.5c | CPU load with DMA | 0.0625 | % |
| X18.5d | block duration | 10 | ms |
| X18.5e | smallest block, two buffers | 87.5 | samples |
| X18.5f | chosen block, two buffers | 128 | samples |
| X18.5g | memory, two buffers | 512 | bytes |
| X18.5h | worst latency, two buffers | 479.6 | µs |
| X18.5i | deadline bound, three buffers | 25.0 | samples |
| X18.5j | throughput floor | 37.5 | samples |
| X18.5k | chosen block, three buffers | 64 | samples |
| X18.5l | memory, three buffers | 384 | bytes |
| X18.5m | worst latency, three buffers | 274.8 | µs |
| X18.5n | processing time of a 32-sample block | 68.4 | µs |
| X18.5o | UART byte rate | 46080 | bytes/s |
| X18.5p | bytes per 8 ms | 368.6 | bytes |
| X18.5q | ring size | 512 | bytes |
| X18.5r | head index | 412 | — |
| X18.5s | unread bytes | 474 | bytes |
| X18.6a | ideal divisor, 230 400 baud | 13.02 | — |
| X18.6b | achieved rate, divisor 13 | 230769 | baud |
| X18.6c | error, divisor 13 | 0.160 | % |
| X18.6d | ideal divisor, 921 600 baud | 3.255 | — |
| X18.6e | error, integer divisor 3 | 8.51 | % |
| X18.6f | fractional divisor | 3.25 | — |
| X18.6g | achieved rate, fractional divisor | 923077 | baud |
| X18.6h | highest SCK | 22.7 | MHz |
| X18.6i | highest SCK with translators | 18.5 | MHz |
| X18.6j | minimum pull-up | 700 | Ω |
| X18.6k | maximum pull-up | 1416 | Ω |
| X18.6l | rise time with 1.0 kΩ | 212 | ns |
| X18.6m | clock periods per read | 84 | — |
| X18.6n | transaction time | 210 | µs |
| X18.6o | data fraction | 57.1 | % |
| X18.6p | reads per second | 4762 | — |
| X18.7a | LSB | 152.6 | µV |
| X18.7b | code for 1.000 V | 6554 | — |
| X18.7c | ideal SQNR | 86.04 | dB |
| X18.7d | ENOB | 12.66 | bits |
| X18.7e | time constants for 14-bit settling | 10.40 | — |
| X18.7f | sampling time, 2 kΩ source | 156 | ns |
| X18.7g | largest source at 100 ns | 924 | Ω |
| X18.7h | noise after 64-sample averaging | 0.15 | LSB rms |
| X18.7i | extra bits | 3 | bits |
| X18.7j | output rate | 15.6 | kS/s |
| X18.7k | PWM frequency | 187.5 | kHz |
| X18.7l | filter time constant | 341.3 | µs |
| X18.7m | filter bandwidth | 466 | Hz |
| X18.7n | settling to half an LSB | 2.13 | ms |
| X18.8a | kernel CPU share | 0.32 | % |
| X18.8b | utilization | 0.833 | — |
| X18.8c | Liu & Layland bound, n = 3 | 0.780 | — |
| X18.8d | hyperbolic product | 2.08 | — |
| X18.8e | R_A | 2 | ms |
| X18.8f | R_B | 5 | ms |
| X18.8g | R_C | 16 | ms |
| X18.8h | H's response, no protocol | 11 | ms |
| X18.8i | H's response, inheritance | 5 | ms |
| X18.8j | H's response, ceiling | 5 | ms |
| X18.8k | blocking bound B_H | 3 | ms |
| X18.8l | response-time bound for H | 6 | ms |
| X18.8m | queue slots, 30 ms stall | 8 | — |
| X18.8n | queue storage | 128 | bytes |
| X18.8o | queue slots, 32 ms stall | 9 | — |
| X18.9a | single-slot image | 464 | KiB |
| X18.9b | two-slot image | 232 | KiB |
| X18.9c | swap-with-scratch image | 224 | KiB |
| X18.9d | sectors | 25 | — |
| X18.9e | sector copy time | 55.6 | ms |
| X18.9f | overwrite installation | 1.39 | s |
| X18.9g | swap installation | 4.17 | s |
| X18.9h | updates before scratch wear-out | 400 | — |
| X18.9i | software hash time | 42.67 | ms |
| X18.9j | signature time | 31.25 | ms |
| X18.9k | secure-boot time, software hash | 73.92 | ms |
| X18.9l | secure-boot time, hash engine | 33.38 | ms |
| X18.9m | vulnerable window | 5.12 | s |
| X18.9n | fraction bricked per update | 5.93e-6 | — |
| X18.9o | devices bricked per update | 11.9 | — |
| X18.10a | average current | 11.24 | µA |
| X18.10b | coin-cell life | 834 | days |
| X18.10c | radio share of charge | 55.6 | % |
| X18.10d | stop/sleep break-even | 0.252 | ms |
| X18.10e | standby/stop break-even | 1.62 | s |
| X18.10f | charge per second at 16 MHz | 138.8 | µC |
| X18.10g | charge per second at 64 MHz | 110.8 | µC |
| X18.10h | saving from racing | 20.2 | % |
| X18.10i | droop without capacitor | 0.60 | V |
| X18.10j | capacitance for 0.3 V droop | 72.1 | µF |
| X18.10k | droop with 100 µF | 236 | mV |
| X18.11a | accelerometer rms noise | 0.90 | mg |
| X18.11b | tilt noise | 0.0516 | ° |
| X18.11c | tilt noise of a 400-sample average | 0.00258 | ° |
| X18.11d | angle random walk | 0.212 | °/√h |
| X18.11e | angle noise after 100 s | 0.0354 | ° |
| X18.11f | bias drift after 100 s | 20 | ° |
| X18.11g | complementary-filter time constant | 0.495 | s |
| X18.11h | steady-state bias error | 0.099 | ° |
| X18.11i | white-noise reduction factor | 0.0709 | — |
| X18.11j | PPG shot-noise SNR | 69.9 | dB |
| X18.11k | average LED current | 60 | µA |
| X18.12a | average brute-force time | 11.65 | h |
| X18.12b | with a 1 s delay per try | 97.1 | days |
| X18.12c | timing-attack queries | 128256 | — |
| X18.12d | correlation at σ = 6 | 0.229 | — |
| X18.12e | traces at σ = 6 | 304 | — |
| X18.12f | traces at σ = 12 | 1168 | — |
| X18.12g | repetition length, p = 0.08 | 27 | — |
| X18.12h | PUF cells | 3456 | — |
| X18.12i | key failure at that length | 4.1e-7 | — |
| X18.13a | instruction rate at 75 MHz | 62.5 | per µs |
| X18.13b | instruction rate at 80 MHz | 61.5 | per µs |
| X18.13c | minimum external capacitor | 163.8 | nF |
| X18.13d | DC error estimate | 6.23 | mV |
| X18.13e | DC error estimate | 40.9 | LSB |
| X18.13f | correlation at σ = 10 | 0.140 | — |
| X18.13g | traces at σ = 10, z = 4 | 816 | — |
| X18.13h | high-noise limit | 800 | — |
| X18.14a | average LED current | 18 | µA |
| X18.14b | total average current | 118 | µA |
| X18.14c | battery life | 5.40 | days |
| X18.14d | current needed for a week | 91.1 | µA |
| X18.14e | full-image download time | 7.65 | s |
| X18.14f | fraction of the image in 3 s | 39.2 | % |
| X18.14g | raw 128-bit key correct | 0.0203 | — |
| X18.14h | repetition length, p = 0.03 | 15 | — |
| X18.14i | PUF cells | 1920 | — |
