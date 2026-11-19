# Problems 08-07 · Registers, Counters and Shift Registers

Chapter: [08-07](../chapters/08-07-registers-counters-shift-registers.md) · Worked solutions: [08-07 solutions](../solutions/08-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** register contents are written most significant bit first ($Q_{n-1} \ldots Q_0$) and quoted as unsigned integers. Fibonacci LFSRs have stages $Q_1 \ldots Q_n$ shifting from $Q_1$ toward $Q_n$; the polynomial $x^n + x^k + 1$ means $Q_1^{\text{next}} = Q_n \oplus Q_k$, and the output is $Q_n$.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 08-07.1 [A]

**Deserializing a byte.** The bits 1, 0, 1, 1, 0, 0, 1, 0 arrive in that order, most significant bit first, at an 8-bit SIPO register that shifts left (each new bit enters at $Q_0$). What word, as an unsigned integer, does the register hold after 8 clocks?

### Problem 08-07.2 [A]

**Serializing a byte.** A PISO register sends the byte 5A₁₆ least significant bit first. (a) List the 8 transmitted bits in order. (b) How many are 1? (c) How many transitions (changes between consecutive bits) does the stream contain?

### Problem 08-07.3 [A]

**Clock counters.** (a) How many flip-flops does a modulo-60 counter (seconds) need, and how many of its states are unused? (b) The same for a modulo-24 counter (hours).

### Problem 08-07.4 [B]

**Counting down.** (a) A 4-bit down counter holds 0010. What does it hold after 5 clock edges? (b) State the toggle condition for bit $i$ of a down counter. (c) How many bits toggle going from 1000 to 0111?

### Problem 08-07.5 [B]

**How fast can a counter count?** An 8-bit synchronous counter has flip-flops with $t_{pcq}$ = 60 ps and $t_{\text{setup}}$ = 40 ps, two-input AND gates of 25 ps and XOR gates of 30 ps. (a) If the toggle conditions are built as a chain of two-input ANDs, how many ANDs lie on the path to $T_7$, and what is $f_{\max}$? (b) If instead $T_7$ is computed by a balanced tree of two-input ANDs, how many levels is that, and what is $f_{\max}$?

### Problem 08-07.6 [B]

**A ripple clock divider.** A 10-stage ripple counter divides a 100 MHz clock. (a) What frequency comes out of the last stage? (b) With $t_{cq}$ = 0.5 ns per stage, how long after an input edge does the last stage change in the worst case? (c) Why is that delay harmless for a clock divider but harmful for a counter whose value is read by logic?

### Problem 08-07.7 [B]

**Divide by ten with a Johnson counter.** (a) How many flip-flops does a Johnson counter need for 10 states, and how many of the $2^n$ states are unused? (b) What is the duty cycle of any one of its outputs? (c) How many two-input AND gates decode all 10 states?

### Problem 08-07.8 [B]

**Ring counter traps.** A 4-bit ring counter (rotate right) is accidentally loaded with 1100. (a) List its states until it repeats. (b) Rotations partition the 16 possible states into cycles; how many cycles are there? (c) How would you make the counter return to the one-hot cycle?

### Problem 08-07.9 [B]

**A 3-bit LFSR.** For $x^3 + x^2 + 1$, step the LFSR from $Q_1Q_2Q_3$ = 100 (that is, $Q_1$ = 1). (a) What is its period? (b) How many 1s appear at the output $Q_3$ in one period? (c) Is $x^3 + x + 1$ also maximal length?

### Problem 08-07.10 [B]

**Testing taps.** (a) What is the period of the 5-bit LFSR with polynomial $x^5 + x^3 + 1$? (b) Into which cycle lengths do the 31 nonzero states of $x^5 + x^4 + 1$ fall? (c) Factor $x^5 + x^4 + 1$ to explain (b).

### Problem 08-07.11 [B]

**Properties of an m-sequence.** For a maximal-length 5-bit LFSR, find: (a) the numbers of 1s and 0s per period; (b) the total number of runs per period, and how many have length 1; (c) the longest run of 1s; (d) the number of positions in which the sequence agrees with a copy of itself shifted by any nonzero amount.

### Problem 08-07.12 [C]

**How good is "no errors"?** A 25.78125 Gb/s link runs PRBS31 for 10 minutes with zero bit errors. (a) How many bits were checked? (b) What 95% upper bound on the bit-error rate does that support (use the rule of three, $3/N$)? (c) How long must it run to support a bound of $10^{-15}$?

### Problem 08-07.13 [C]

**A CRC is an LFSR.** Compute the CRC of 08-01's Example 08-01.7 (message 1101, generator $x^3 + x + 1$) by clocking the message, followed by three 0s, into a 3-bit shift register that XORs the generator into it whenever a 1 falls off the top. (a) How many clock cycles does it take? (b) What remainder is left?

### Problem 08-07.14 [C]

**Counter switching power.** (a) How many flip-flop toggles per count does a free-running 16-bit binary counter make on average? (b) A Gray-code counter? (c) If each toggle costs 5 fJ and the counter runs at 100 MHz, what is the switching power of each?

### Problem 08-07.15 [C]

**The cost of a universal shift register.** A 32-bit universal shift register uses a 4:1 multiplexer per bit (36 transistors each, as NAND-NAND logic from Example 08-04.1) in front of a 24-transistor flip-flop. (a) How many transistors per bit, and in total? (b) What fraction of the total is the multiplexing?

### Problem 08-07.16 [B]

**A parameterized up/down counter in Verilog.** Write `updown #(parameter integer W = 4)` with inputs `clk`, `rst`, `en`, `load`, `up` and `d[W-1:0]` and output `q[W-1:0]`: synchronous reset has priority, then load, then counting up or down when enabled, wrapping modulo $2^W$. Write a self-checking testbench that instantiates it at $W$ = 4 and $W$ = 7, applies 3000 random cycles of the control inputs, and compares both counters each cycle with a behavioral model. (a) After how many up-counts does the 4-bit counter wrap from its reset value? (b) From $q$ = 0, what does one down-count give at $W$ = 7? (c) Swap the priority of load and enable in the design and confirm that the testbench catches it.

---

## Objective coverage

| Learning objective (chapter 08-07) | Problems |
|---|---|
| 1. Registers and shift registers | 1, 2, 15 |
| 2. Synchronous, modulo-$N$ and ripple counters | 3, 4, 5, 6, 14, 16 |
| 3. Ring and Johnson counters | 7, 8 |
| 4. LFSRs and PRBS | 9, 10, 11, 12, 13 |
| 5. Counter timing and switching costs | 5, 6, 14 |
