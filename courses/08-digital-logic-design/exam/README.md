# Course 08 · Final Exam (Digital Logic Design)

**Time limit:** 240 minutes.
**Allowed:** a scientific calculator, and the [Course 08 equation sheet](../../../reference/equation-sheets/08-digital-logic-design.md) printed without its chapter links. No notes, no Python, no simulator.

**Instructions.**

- Answer all 15 questions and show every step.
- Each [A] is worth 5 points, each [B] 8 (except Question 9, which is longer and carries 10) and each [C] 12: 125 points in total. 88 or more (about 70%) is a strong pass.
- Within a question the lettered parts carry equal weight, unless the question says otherwise.
- Questions 8 and 14 ask for a design with its reasoning. Show the steps, not just the result.
- Give numerical answers to 4 significant figures unless told otherwise, with units.
- Question 15 is a short-answer diligence question, graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These are the conventions of the chapters' problem sets.

- **Numbers.** A subscript gives the base (1011₂, B6₁₆). "8-bit" means two's complement unless a number is called unsigned. A signed Q$m$.$f$ number has $m$ integer bits, including the sign, and $f$ fractional bits.
- **Truth tables.** Rows are numbered by reading the inputs as a binary number, with $A$ the most significant bit. Minterm $m_i$ of $A, B, C, D$ has $i = 8A + 4B + 2C + D$. "Minimal" means fewest product (or sum) terms, then fewest literals.
- **Unit delay.** In the unit-delay model, every gate and every inverter takes 1 unit. Transistor counts are for static CMOS: $2k$ for a $k$-input NAND, NOR or compound gate, 2 for an inverter, and AND or OR as the inverting gate plus an inverter.
- **Timing.** $t_{pcq}$ and $t_{ccq}$ are the clock-to-Q propagation and contamination delays, and $t_{pd}$ and $t_{cd}$ those of the logic. Skew $\delta$ is positive when the capture clock arrives later than the launch clock.
- **MTBF.** MTBF $= e^{S/\tau}/(T_W F_C F_D)$, and a two-flip-flop synchronizer has $S = T_c - t_{pcq} - t_{\text{setup}}$. Each additional stage adds the same amount to $S$.
- **Verilog.** Verilog-2005 semantics. Bit patterns are given as unsigned integers unless the variable is declared `signed`.
- **Sequential machines.** Cycles are numbered from 0, starting in the reset state. The input of cycle $t$ is sampled at the clock edge that ends cycle $t$.

---

**1 [A] · Numbers and codes.**
(a) Write B6₁₆ in binary, and give its value as an unsigned number and as an 8-bit two's-complement number.
(b) Add the 8-bit numbers 5A₁₆ and 3C₁₆. Give the 8-bit result in hexadecimal and as a signed value, and say whether the addition overflowed and how the hardware detects it.
(c) Represent −0.40625 in Q1.7. Give the bit pattern, its hexadecimal value, the format's resolution and its range.
(d) A Hamming(7,4) code word is received as 1100010 (bit positions 1 to 7 from the left, check bits at positions 1, 2 and 4, data bits $d_1$ to $d_4$ at positions 3, 5, 6 and 7). Compute the syndrome, correct the word and give the data bits.

**2 [A] · Boolean algebra and gates.**
(a) Simplify $F = AB + \overline{A}C + BC$ and $G = (A + B)(A + C)$, naming the theorem you use for each.
(b) Use De Morgan's theorem to write the complement of $A + \overline{B}C$ as a product of sums.
(c) Implement $H = AB + CD$ in three ways and count the transistors of each: with two-input AND gates and an OR gate; with two-input NAND gates only; and with a single AND-OR-INVERT (AOI22) gate followed by an inverter.
(d) Give the lookup-table integer (row $i$'s output is bit $i$) of the three-input parity function $A \oplus B \oplus C$ and of the majority function $M(A, B, C)$.

**3 [B] · Minimization and hazards.** $F(A, B, C, D) = \sum m(1, 5, 6, 7, 11, 12, 13, 15)$.
(a) Plot $F$ on a K-map. List all its prime implicants and identify the essential ones.
(b) Find the minimal sum of products and its literal count. Which prime implicant is left out, even though it is the largest group on the map?
(c) Find the minimal product of sums.
(d) Does the minimal sum of products of (b) have static-1 hazards (for single-input changes)? If so, list the input transitions concerned and the term that removes them all.
(e) Minterms 3 and 9 become don't cares. Find the new minimal sum of products and its literal count.

**4 [B] · Combinational building blocks.**
(a) Implement $G(A, B, C) = \sum m(1, 2, 6, 7)$ with one 4:1 multiplexer, using $A$ and $B$ (most significant first) as the select lines. Give the four data inputs, each one of $0$, $1$, $C$ or $\overline{C}$.
(b) Implement the same $G$ with a 3:8 decoder and one OR gate.
(c) A 4-bit adder/subtracter computes $A - B$ as $A + \overline{B} + 1$. Compute $0101_2 - 0111_2$ and $0110_2 - 1101_2$: give each 4-bit result, its signed value, the carry out and the overflow flag $V = C_4 \oplus C_3$. Interpret both.
(d) A 16-bit ripple-carry adder is built from full adders with $S = A \oplus B \oplus C_{in}$ and $C_{out} = AB + C_{in}(A \oplus B)$, in the unit-delay model. Find the delay to the most significant sum bit and to the carry out, and these times at 20 ps per unit.

**5 [B] · Verilog semantics.** In a testbench:

```verilog
reg        [3:0] a = 4'd9, b = 4'd12, c;
reg        [7:0] p, q;
reg signed [3:0] s = 4'sb1010;
reg signed [7:0] w1, w2, w3;
initial begin
    c  = a + b;
    p  = a + b;
    q  = {a, b};
    w1 = s;
    w2 = s + a;
    w3 = s >>> 1;
end
```

(a) Give the values of `c`, `p` and `q`, and explain why `c` and `p` differ.
(b) Give the values of `w1`, `w2` and `w3`, and explain the value of `w2`.
(c) Registers start with `x = 1`, `y = 0`, `u = 1`, `v = 0`, and these two blocks run on every rising edge:

```verilog
always @(posedge clk) begin x <= y; y <= x; end
always @(posedge clk) begin u = v;  v = u;  end
```

Give `x`, `y`, `u` and `v` after one edge and after two edges. Which block describes hardware a designer would want?

(d) What does this block synthesize to, and why? Correct it.

```verilog
always @(*) begin
    case (sel)
        2'b00: y = a0;
        2'b01: y = a1;
        2'b10: y = a2;
    endcase
end
```

(e) A testbench applies every input combination of a 16-bit adder with carry-in, one per simulated clock cycle, and the simulator runs one million cycles per second. How many combinations are there, and how long does the run take? Would the same approach work for a 32-bit adder?

**6 [B] · Latches, flip-flops and timing.**
(a) A positive-level D latch (transparent while CLK = 1) and a rising-edge D flip-flop both start with $Q = 0$ and see these samples:

| Sample | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CLK | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 |
| D | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 1 |

A rising edge occurs at a sample where CLK goes from 0 to 1, and the flip-flop captures $D$'s value at that sample. Give each output's samples, and count how many times each output changes.

(b) Flip-flops with $t_{pcq}$ = 70 ps, $t_{ccq}$ = 45 ps, $t_{\text{setup}}$ = 55 ps and $t_{\text{hold}}$ = 60 ps share an ideal clock. The longest logic path has $t_{pd}$ = 615 ps, and a separate short path has $t_{cd}$ = 5 ps. Find the minimum period, the maximum frequency, and the short path's hold slack.
(c) Buffers each add 8 ps of contamination delay and 12 ps of propagation delay. How many must be inserted in the short path, what is its new hold slack, and does the maximum frequency change? Why would slowing the clock not have fixed the violation?
(d) The 615 ps logic is split into three pipeline stages of equal delay. Find the new period and frequency, the throughput gain, and the latency compared with the unpipelined design.

**7 [A] · Counters and LFSRs.**
(a) List the states of a 4-bit Johnson counter starting from 0000. How many states does it use, and how many are unused?
(b) A 4-bit Fibonacci LFSR with polynomial $x^4 + x^3 + 1$ has stages $Q_1$ to $Q_4$, shifting from $Q_1$ toward $Q_4$, with $Q_1^{\text{next}} = Q_4 \oplus Q_3$ and output $Q_4$. Starting from $Q_1Q_2Q_3Q_4$ = 1000, list the states until the sequence repeats. Give the period, the first 15 output bits, and the number of ones among them.
(c) With 8 flip-flops, how many states do a binary counter, a ring counter, a Johnson counter and a maximal-length LFSR have?
(d) A 4-bit ripple counter (each stage clocked by the previous stage's output) counts from 0111 to 1000. List the values its outputs pass through, and say why a decoder watching for 0000 could misfire.

**8 [C] · Design a sequence detector.** A serial input $x$ must raise $z$ whenever the last four inputs were 1, 1, 0, 1, with overlapping allowed (1101101 contains two detections). There is a synchronous reset.
(a) Draw the state diagram (or give the state table) of a Moore machine and of a Mealy machine. How many states does each need?
(b) Encode the Mealy machine's states as $A$ = 00 (nothing seen), $B$ = 01 (seen 1), $C$ = 11 (seen 11), $D$ = 10 (seen 110), with state bits $q_1q_0$. Derive minimized next-state and output equations, and count their literals.
(c) The input for cycles 0 to 11 is 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1. In which cycles is the Mealy output 1, and in which the Moore output? Explain the difference.
(d) Write synthesizable Verilog for the Mealy machine in the three-block style. How many flip-flops do the Moore and Mealy machines need with binary encoding and with one-hot encoding?

**9 [B, 10 points] · Arithmetic circuits.** Use the unit-delay model of 08-09 for adders: two-input gates 1 unit, a prefix operator 2 units on its generate output, carry-in folded into bit 0's generate.
(a) For 64-bit adders, give the ripple-carry delay, and the number of prefix operators and levels of Kogge–Stone, Sklansky and Brent–Kung networks. An arrival-time simulation gives slowest sum bits at 14, 16 and 24 units respectively: find each speed-up over ripple carry. Which would you choose for a low-power microcontroller's address adder, and which for a server core's critical ALU, and why?
(b) For a 16 × 16 unsigned Dadda multiplier, give the number of full adders, half adders and the width of the final adder.
(c) Multiply 0.75 by −0.5 in Q1.15. Give both operands and the product as integers, the product's format, and the Q1.15 result as an integer. Which single product of two Q1.15 numbers cannot be represented in Q1.15, and what should the hardware do with it?
(d) A filter accumulates 64 products in the full-precision format of (c). How wide must the accumulator be to be safe from overflow?
(e) How many 2:1 multiplexers, in how many levels, does a 32-bit logarithmic barrel shifter need?

**10 [B] · Skew, jitter and useful skew.** Three flip-flops R1 → R2 → R3 form two paths. All flip-flops have $t_{pcq}$ = 50 ps, $t_{\text{setup}}$ = 40 ps, $t_{ccq}$ = 30 ps and $t_{\text{hold}}$ = 35 ps. Path R1 → R2 has $t_{pd}$ = 560 ps and $t_{cd}$ = 30 ps; path R2 → R3 has $t_{pd}$ = 520 ps. R1 and R3 are clocked at the same instant.
(a) With no skew, find the minimum period, the maximum frequency and the hold slack of R1 → R2.
(b) A designer delays R2's clock by 60 ps to help the slow path R1 → R2. Find the period each path now requires, the new maximum frequency, and the hold slack of R1 → R2. Was it a good idea?
(c) Find the delay of R2's clock that minimizes the period. Give the period, the frequency and the hold slack of R1 → R2.
(d) With that skew, the clock also has 25 ps of cycle-to-cycle jitter. What is the minimum period? Does jitter affect the hold check here?

**11 [B] · Memories and lookup tables.**
(a) A 128 K × 32 SRAM is built as a square array. How many bits does it hold and how many address bits does it need? How many rows and columns, and how many words per row? How are the address bits split between the row decoder and the column multiplexers?
(b) How many bits does a ROM need to multiply two unsigned 4-bit numbers? Two unsigned 8-bit numbers?
(c) How many 4-input LUTs, in how many levels, implement a 12-input AND? How many 6-input LUTs?
(d) A register file has 32 registers of 64 bits and 4 read ports, each built as a multiplexer tree. How many two-input multiplexers do the read ports need in all?

**12 [B] · Reading an FPGA report.** A design is placed and routed on an iCE40 UP5K (5280 logic cells, 30 block RAMs, 8 DSP blocks, 39 user I/O in the package used). Its report shows 1584 logic cells, 6 block RAMs, 2 DSP blocks and 21 I/O used, and a critical path of clock-to-Q 1.39 ns, logic 8.62 ns, routing 13.47 ns and setup 0.82 ns. The design must run from the 48 MHz internal oscillator.
(a) Give each resource's utilization.
(b) Find the critical path's total delay, the maximum frequency and the slack at 48 MHz. What fraction of the path is routing?
(c) A placement-seed sweep typically improves this kind of path by a few percent. Would a 3% gain be enough? Instead, the path is pipelined into two stages with equal logic and routing, each paying the clock-to-Q and setup overhead. Find the new frequency and slack.
(d) The report was produced with the tool's default 12 MHz constraint, and every path "passed". Explain why that says nothing about operation at 48 MHz, and what to change.

**13 [C] · A multiply-accumulate unit for always-on audio.** A keyword-spotting network in a wearable computes dot products of 8-bit signed weights and 8-bit signed activations, 256 terms per dot product. One inference needs 2.5 million multiply-accumulates (MACs), and the device runs 10 inferences per second. Use the 45 nm energy estimates of 08-09: an 8-bit multiply costs 0.2 pJ, a 32-bit add 0.1 pJ (take this for the accumulator add), a 64-bit read from a 32 KB SRAM 20 pJ, and a 64-bit DRAM access 1.3 nJ (the low end of the range).
(a) How wide must the product and the accumulator be? Find the largest positive and most negative possible dot products, and show that one fewer accumulator bit would not do.
(b) Find the arithmetic energy per MAC, per inference, and the average arithmetic power.
(c) Each weight is used once per inference and read from the 32 KB SRAM, eight weights per 64-bit read (activations stay in registers). Find the weight-fetch energy per inference, its power, and the ratio to the arithmetic. Repeat for weights read from DRAM. What does this say about where the energy goes?
(d) In the MAC, the multiplier takes 1.1 ns, the accumulator adder 0.6 ns, and the register overhead ($t_{pcq} + t_{\text{setup}}$) is 0.1 ns. Find the maximum clock frequency without pipelining and with a register between the multiplier and the adder. With one MAC unit, what clock frequency does the application need? Should the unit be pipelined? What should the designer do with the spare timing margin instead?

**14 [C] · Designing a clock-domain crossing.** A sensor front end writes 16-bit samples at 100 MHz, one per cycle, in bursts of 256 samples. A processor in an unrelated 75 MHz domain reads one sample per cycle whenever the FIFO between them is not empty. The FIFO uses Gray-coded pointers passed through synchronizers. Each part carries 3 points.
(a) Give the 4-bit binary and Gray codes of 7 and 8. How many bits change in each code from 7 to 8? Explain why a binary pointer must not be passed through a bank of synchronizers.
(b) Treat the data flows as continuous. The reader sees the first sample 3 read cycles after it is written, then reads continuously. Find the burst's duration, the number of samples read during the burst, and the peak occupancy. What depth would you choose, and why a power of two? What is the shortest interval between burst starts that the reader can sustain?
(c) For the depth you chose, how wide are the pointers, and why one bit wider than the address? How many synchronizer flip-flops do the two pointer crossings use, with two stages each?
(d) The same FIFO is reused in a chip whose read clock is 1.25 GHz. The flip-flops have $\tau$ = 25 ps, $T_W$ = 20 ps, $t_{pcq}$ = 50 ps and $t_{\text{setup}}$ = 30 ps. During a burst the write pointer changes 100 million times per second, and Gray coding means one bit changes each time, so take $F_D = 10^8$ s⁻¹ for the whole bank. Find the write-pointer synchronizer bank's MTBF with two stages and with three. Which would you ship?

**15 [B] · Diligence: four claims.** For each claim, say in two or three sentences what is wrong or missing, and give the one question you would ask.
(a) "Our edge AI chip delivers 100 TOPS."
(b) "Our design closed timing at 2 GHz."
(c) "Our synchronizers make metastability failures impossible."
(d) "Each device generates its unique key from a 32-bit LFSR seeded at power-up."
