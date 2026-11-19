# Problems 08-05 · Introduction to Verilog/SystemVerilog and Testbenches

Chapter: [08-05](../chapters/08-05-verilog-and-testbenches.md) · Worked solutions: [08-05 solutions](../solutions/08-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** Verilog-2005 semantics as simulated by Icarus Verilog; "the result" of an expression means its value after assignment to the stated destination. Answers that are bit patterns are given as unsigned integers unless the variable is declared `signed`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 08-05.1 [A]

**Widths.** With `wire [7:0] a = 8'd200, b = 8'd100;`, find (a) `a + b` assigned to an 8-bit wire; (b) `a + b` assigned to a 9-bit wire; (c) `a - b` in 8 bits; (d) `b - a` in 8 bits. Interpret (d) as a signed number.

### Problem 08-05.2 [A]

**Literals.** Give the decimal value of (a) `4'hA`, (b) `6'b101_011`, (c) `12'h0F0`. (d) How many bits wide is the unsized literal `'hFF`, and is it signed?

### Problem 08-05.3 [A]

**Operators.** With `wire [7:0] a = 8'b1010_0110;`, evaluate (a) the AND-, OR- and XOR-reductions of `a`; (b) `{2{a[3:0]}}`; (c) `a[7:4]`; (d) `a << 3` in 8 bits.

### Problem 08-05.4 [B]

**Signed arithmetic.** `reg signed [3:0] p = 4'sb1010;` (a) What is $p$ as a signed number? (b) Evaluate `p >>> 2` and `p >> 2`. (c) Evaluate `p + 4'sd7` in 4 bits. (d) What 8-bit pattern results from assigning `p` to a `reg signed [7:0]`, as an unsigned number? (e) Are `p < 4'd0` and `p < 0` true?

### Problem 08-05.5 [B]

**Four-valued logic.** (a) Evaluate `1'bx | 1'b0`, `1'bz & 1'b0`, `~1'bz`. (b) Evaluate `4'b10x1 == 4'b10x1` and `4'b10x1 === 4'b10x1`. (c) Of the 16 combinations of two four-valued inputs, how many give a definite result for OR, for NAND and for XNOR?

### Problem 08-05.6 [B]

**Spot the latches.** How many outputs become latches in the following?

```verilog
always @(*) begin                  // block 1
    if (s) y1 = a; else y1 = b;
end
always @(*) begin                  // block 2
    case (sel)                     // sel is 2 bits
        2'd0: y2 = a;
        2'd1: y2 = b;
        2'd2: y2 = c;
    endcase
end
always @(*) begin                  // block 3
    y3 = 1'b0;
    if (en) begin y3 = a; y4 = b; end
end
```

### Problem 08-05.7 [B]

**Statement order with blocking assignments.** A four-stage shift register is written with blocking assignments in *reverse* order: `q4 = q3; q3 = q2; q2 = q1; q1 = d;`. (a) After how many clock edges does a single 1 at `d` reach `q4`? (b) Same question with the statements in forward order. (c) Why is the reverse-order version still poor practice?

### Problem 08-05.8 [B]

**Rotating three registers.** `a`, `b`, `c` start at 1, 2, 3. (a) What are they after one clock edge of `a <= b; b <= c; c <= a;`, and after three edges? (b) What are they after one edge of the blocking version `a = b; b = c; c = a;`?

### Problem 08-05.9 [B]

**A clock and a counter in a testbench.** `always #5 clk = ~clk;` with `clk` starting at 0 and `` `timescale 1ns/1ps ``. (a) What is the clock frequency? (b) How many rising edges occur in the first 1 µs? (c) An 8-bit counter, reset to 0 before the first edge, increments on every rising edge. What does it read after 1000 edges?

### Problem 08-05.10 [B]

**Another sensitivity-list bug.** `always @(a or b) y = (a & b) | c;` starts at $(a, b, c) = (0, 0, 0)$ with `y` = 0. The inputs then change one at a time: $c \to 1$, $a \to 1$, $c \to 0$, $b \to 1$. After how many of these four steps does the simulated `y` differ from the hardware?

### Problem 08-05.11 [B]

**Planning a random test.** A 4-bit ALU has two 4-bit operands and a 3-bit opcode. (a) How many vectors does exhaustive testing take? (b) What fraction do that many random vectors cover, on average? (c) How many random vectors give an expected coverage of at least 99%?

### Problem 08-05.12 [C]

**The coupon collector.** (a) For $M = 1024$ possible inputs, compute the expected number of random vectors needed to see every input at least once, and its ratio to $M$. (b) Derive the formula, and explain why the last few inputs take most of the time.

### Problem 08-05.13 [C]

**A race.** Two blocks, `always @(posedge clk) x = y;` and `always @(posedge clk) y = x;`, start with `x` = 0, `y` = 1. (a) After one edge, what are the possible results, depending on which block the simulator runs first? How many are there? (b) What happens with non-blocking assignments instead?

### Problem 08-05.14 [C]

**Generated hardware.** A parameterized adder uses `generate for (i = 0; i < W; i = i + 1)` to instantiate a full adder per bit, each full adder being the five gates of 08-04 §3.5. (a) For `W = 32`, how many full adders and how many gates are generated? (b) In what sense does the loop "run", and when?

### Problem 08-05.15 [C]

**Checking an assertion by hand.** The SystemVerilog assertion `assert property (@(posedge clk) req |-> ##[1:3] ack);` requires that whenever `req` is 1 at a clock edge, `ack` is 1 at some edge 1 to 3 cycles later. Over cycles 0 to 10, `req` is 1 at cycles 1, 4 and 7, and `ack` is 1 at cycles 3 and 8. (a) How many of the three requests pass, and how many fail? (b) Which one fails, and what bug might it reveal?

### Problem 08-05.16 [B]

**Writing a self-checking testbench.** A module `add4(a, b, cin, s, cout)` adds two 4-bit numbers and a carry-in. Write a testbench that applies every input combination, compares `{cout, s}` with `a + b + cin` using `!==`, counts the errors and prints `TEST PASSED` or `TEST FAILED`. (a) How many combinations does it apply? (b) Why must the expected value be computed into a 5-bit variable? (c) Build `add4` from four full adders, run your testbench, then break the carry logic of one full adder and confirm the testbench fails.

---

## Objective coverage

| Learning objective (chapter 08-05) | Problems |
|---|---|
| 1. Modules, assignments, synthesized hardware, latches | 6, 14 |
| 2. Simulation semantics, blocking and non-blocking | 7, 8, 10, 13 |
| 3. Widths, signedness, four-valued logic | 1, 2, 3, 4, 5 |
| 4. Testbenches and coverage | 9, 11, 12, 15, 16 |
| 5. Tools and SystemVerilog | 9, 15 |
