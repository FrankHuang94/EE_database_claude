# Problems 08-10 · Timing, Metastability and Clock-Domain Crossing

Chapter: [08-10](../chapters/08-10-timing-metastability-cdc.md) · Worked solutions: [08-10 solutions](../solutions/08-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** skew $\delta$ is positive when the capture clock arrives later than the launch clock. MTBF $= e^{S/\tau}/(T_W F_C F_D)$, and a two-flip-flop synchronizer has $S = T_c - t_{pcq} - t_{\text{setup}}$; each additional stage adds the same amount. A year is 365.25 days.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 08-10.1 [A]

**Slack.** Flip-flops have $t_{pcq}$ = 60 ps and $t_{\text{setup}}$ = 40 ps. Two register-to-register paths have logic delays of 520 ps and 480 ps. (a) What is the maximum clock frequency? (b) What is each path's slack at 1.5 GHz?

### Problem 08-10.2 [A]

**Hold.** A short path has $t_{ccq}$ = 30 ps, $t_{cd}$ = 15 ps and $t_{\text{hold}}$ = 25 ps. (a) What is its hold slack with no skew? (b) With the capture clock 30 ps late? (c) Does halving the clock frequency fix (b)?

### Problem 08-10.3 [A]

**The exponential lever.** (a) By what factor does one extra time constant $\tau$ of resolution time multiply the MTBF? (b) How many time constants of extra waiting multiply it by $10^6$?

### Problem 08-10.4 [B]

**A skew and jitter budget.** A path has $t_{pcq}$ = 50 ps, 700 ps of logic and $t_{\text{setup}}$ = 40 ps, and the target clock is 1.25 GHz. (a) What is its setup slack with an ideal clock? (b) With the capture clock 30 ps *early*? (c) With no skew but 25 ps of cycle-to-cycle jitter? (d) What logic delay could the path have with both the early clock and the jitter?

### Problem 08-10.5 [B]

**How far can pipelining go?** A 1200 ps block is pipelined into $k$ equal stages with a register overhead of 100 ps per stage. (a) Find the clock frequency for $k$ = 1, 4 and 12, and the limit as $k \to \infty$. (b) What is the latency for $k$ = 4? (c) What is the smallest $k$ that doubles the throughput of $k = 1$?

### Problem 08-10.6 [B]

**Balancing stages.** A three-stage pipeline has stage logic delays of 500, 300 and 400 ps and 100 ps of register overhead per stage. (a) What is its clock frequency? (b) If retiming balances the logic into three 400 ps stages, what is it?

### Problem 08-10.7 [B]

**A fast clock is hard to synchronize into.** A 2 GHz domain samples an asynchronous signal with $F_D$ = 50 MHz. The flip-flops have $\tau$ = 25 ps, $T_W$ = 30 ps, $t_{pcq}$ = 60 ps and $t_{\text{setup}}$ = 40 ps. (a) What is the MTBF of a two-flip-flop synchronizer? (b) Of three and four flip-flops? (c) How many flip-flops are needed for an MTBF of at least 1000 years?

### Problem 08-10.8 [B]

**How much time to wait?** With $T_W F_C F_D = 4 \times 10^6$ per second and $\tau$ = 20 ps, what resolution time $S$ gives an MTBF of $10^4$ years?

### Problem 08-10.9 [B]

**A 3-bit counter crossing domains.** A 3-bit counter going from 3 to 4 is sampled bit by bit during the transition. (a) With binary coding, how many bits change and how many different values can be seen? (b) What is the largest error? (c) With Gray coding, how many values can be seen?

### Problem 08-10.10 [B]

**A toggle synchronizer's speed limit.** Pulses in a 400 MHz domain cross into a 100 MHz domain through a toggle synchronizer. The destination needs the toggled level to stay stable for at least 2 of its cycles between changes. (a) What is the minimum spacing between source pulses, in nanoseconds and in source cycles? (b) What is the maximum pulse rate?

### Problem 08-10.11 [B]

**A handshake's throughput.** A four-phase handshake moves 32-bit words from a 100 MHz domain to an 80 MHz domain. Each of its four crossings (request rising and falling into the destination, acknowledge rising and falling back into the source) takes up to 3 cycles of the receiving clock. (a) How long does one transfer take in the worst case? (b) What are the transfer rate and the data rate?

### Problem 08-10.12 [C]

**Sizing a FIFO for bursts.** A camera interface writes bursts of 256 words at 250 MHz; the consumer reads continuously at 100 MHz. A new burst starts every 3 µs. (a) How many words does the reader remove during a burst (round down, to be safe)? (b) What minimum depth absorbs a burst, and what power-of-2 depth do you choose, allowing 3 words for synchronizer latency? (c) How wide are the address and pointers? (d) Check that the average write rate is below the read rate.

### Problem 08-10.13 [C]

**From one synchronizer to a fleet.** A chip has 2000 synchronizers, each with an MTBF of $10^9$ years at its worst operating corner. (a) What is the chip's MTBF? (b) With 5 million chips deployed, how many synchronizer failures per year should the fleet expect?

### Problem 08-10.14 [C]

**Measuring τ.** A test chip counts synchronizer failures with the resolution time set to 300 ps and then to 400 ps, for the same duration and data rate. It counts $10^5$ failures at 300 ps and 100 at 400 ps. (a) What is $\tau$? (b) How many failures would the same test count at 900 ps?

### Problem 08-10.15 [C]

**Pipelining a loop.** A multiply-accumulate loop has a 600 ps multiplier feeding a 300 ps adder whose output is registered and fed back to the adder; register overhead is 80 ps. (a) What is the clock frequency without pipelining? (b) Splitting the multiplier into two 300 ps stages, what is it? (c) Why can the adder–register loop not be pipelined the same way?

---

## Objective coverage

| Learning objective (chapter 08-10) | Problems |
|---|---|
| 1. Static timing, slack, critical path | 1, 4 |
| 2. Setup and hold with skew and jitter | 2, 4 |
| 3. Pipelining | 5, 6, 15 |
| 4. Synchronizer MTBF | 3, 7, 8, 13, 14 |
| 5. Clock-domain crossing schemes | 9, 10, 11, 12 |
