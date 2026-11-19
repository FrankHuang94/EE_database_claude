# Lab 08-02 · Boolean Algebra and Logic Gates

**Chapter:** [08-02](../../chapters/08-02-boolean-algebra-and-gates.md) · **Notebook:** [08-02-boolean-algebra.ipynb](08-02-boolean-algebra.ipynb) · **Time:** about 2 hours

## Objective

1. Prove the theorems of Boolean algebra by perfect induction, with a few lines of code instead of by hand.
2. Generate canonical forms and lookup-table integers from truth tables, and classify all functions of two and three inputs.
3. Check NAND-only and NOR-only circuits exhaustively against their specifications.
4. Simulate CMOS gates as networks of switches, and then as transistors in ngspice.
5. Describe one function three ways in Verilog, and build gates from transistor primitives.

## Background

Chapter sections 3.1 to 3.9 and Examples 08-02.1 to 08-02.7. You need Python with NumPy and Matplotlib, Icarus Verilog, and ngspice (see [SETUP.md](../../../../SETUP.md)). Verilog is taught properly in [08-05](../../chapters/08-05-verilog-and-testbenches.md); here you only read and run it. Three constructs appear: `assign y = …;` (a continuous equation, with `&`, `|`, `^`, `~` for AND, OR, XOR, NOT), gate primitives such as `nand g1 (out, in1, in2);` (output first), and switch primitives `nmos` and `pmos` with the argument order (drain, source, gate).

## Files

| File | What it does | Checks against |
|---|---|---|
| [08-02-boolean-algebra.ipynb](08-02-boolean-algebra.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s and this handout's key |
| [gates.v](gates.v) | Majority three ways (SOP, NAND-NAND, multiplexer), the four-NAND XOR, and NAND2 and OAI21 built from `nmos`/`pmos` switches | `gates_tb.v` |
| [gates_top.v](gates_top.v) | A top level instantiating every module, for lint tools | Lint only |
| [gates_tb.v](gates_tb.v) | Self-checking testbench: every module on every input row, plus De Morgan's theorems | Prints `TEST PASSED` |
| [nand2_cmos.cir](nand2_cmos.cir) | A transistor-level CMOS NAND2 at all four input combinations | This handout's key |

Run from the repository root:

```bash
python tools/run_hdl.py
```

```bash
python tools/run_spice.py 08-02
```

## Procedure

1. **Perfect induction (Part 1).** *Predict first:* how many rows does a proof of the consensus theorem need, and how many for a five-variable identity? The notebook proves every theorem of §3.3 and its dual.
2. **Canonical forms and a census (Part 2).** *Predict first:* of the 256 functions of three inputs, how many are symmetric (unchanged by any permutation of the inputs), how many are self-dual, and how many are monotone? Then let the notebook count them.
3. **Universal gates (Part 3).** Convert SOP expressions to NAND-NAND and POS to NOR-NOR, and check each conversion on every row. Search for the smallest NAND circuit that makes XOR.
4. **Switch networks (Part 4).** Describe a pull-down network as nested series and parallel connections, let the notebook build the dual pull-up network, and confirm that exactly one network conducts in every row.
5. **ngspice (the chapter's guided exercise).** *Predict first:* the NAND2's output voltage for each input pair, and the current drawn from the 1.8 V supply once the output has settled. Then run `nand2_cmos.cir`.
6. **Verilog.** Run the testbench, then break something: swap the series and parallel connections in the `nand2_cmos` pull-up network and watch the testbench catch it. (In a real circuit that mistake gives a short circuit in some states and a floating output in others; in the simulator, look for `x` and `z` values.)

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | proofs | every theorem and its dual pass on all rows; consensus needs 8 rows, a five-variable identity 32 |
| 2 | census of three-input functions | see the key: 16 symmetric, 16 self-dual, 20 monotone |
| 3 | smallest NAND XOR | 4 gates |
| 4 | switch networks | the pull-up network is the series-parallel dual of the pull-down network, and exactly one conducts in each row |
| ngspice | NAND2 | output at a rail in every state; settled supply current essentially zero (see the key) |
| Verilog | testbench | `TEST PASSED` |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 08-02.a | NAND2 output, $AB$ = 00 | 1.8 | V |
| Lab 08-02.b | NAND2 output, $AB$ = 01 | 1.8 | V |
| Lab 08-02.c | NAND2 output, $AB$ = 10 | 1.8 | V |
| Lab 08-02.d | NAND2 output, $AB$ = 11 | 0 | V |
| Lab 08-02.e | settled supply current, any input | 0 | A |
| Lab 08-02.f | symmetric functions of three inputs | 16 | — |
| Lab 08-02.g | self-dual functions of three inputs | 16 | — |
| Lab 08-02.h | monotone functions of three inputs | 20 | — |

**Reading the key.** ngspice reports settled supply currents of a few picoamperes, not exactly zero: the simulator adds tiny conductances (its `gmin`, $10^{-12}$ S) across junctions to help convergence, and $1.8\ \text{V} \times 10^{-12}$ S ≈ 2 pA. The level-1 transistor model has no leakage at all. Real transistors leak, by amounts that depend strongly on the process, the threshold voltage and the temperature ([19-06](../../../19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md)), so a chip with billions of gates draws a measurable leakage current even when idle.

The census numbers follow from simple arguments, which the notebook confirms by brute force:

- a **symmetric** function depends only on how many inputs are 1 (0, 1, 2 or 3), so it is a free choice of output for each of 4 counts: $2^4$ = 16;
- a **self-dual** function satisfies $f(\overline{x}) = \overline{f(x)}$, so the 8 rows split into 4 complementary pairs, and choosing the output of one row in each pair fixes the other: $2^4$ = 16;
- the 20 **monotone** functions (outputs never fall when an input rises) are those built from AND and OR alone, plus the constants. There is no simple formula for this count (the Dedekind numbers), and it grows extremely fast with the number of inputs.

## Discussion questions

1. Why is the settled supply current of a static CMOS gate essentially zero, and where, then, does a CMOS chip's power go?
2. The testbench checks De Morgan's theorem on 1-bit values with `!==`. Why use `!==` rather than `!=` in a self-checking testbench?
3. `maj3_nand` uses a three-input NAND primitive. How many transistors would that gate have in static CMOS, and how many does the whole NAND-NAND majority need?
4. If you build `nand2_cmos` with the pull-up network wired in series instead of in parallel, which input rows produce a floating output, and what does the simulator show there?
5. Why are self-dual functions such as majority and XOR3 important in arithmetic circuits? (Hint: look at a full adder's outputs in [08-04](../../chapters/08-04-combinational-building-blocks.md).)

<details><summary>Answers to the discussion questions</summary>

1. In every settled state exactly one of the two networks conducts, so there is no path from the supply to ground; only leakage flows. Power is spent when outputs switch: each transition charges or discharges the capacitance of the wires and gate inputs it drives, costing energy $CV^2$ per charge–discharge cycle, plus a brief short-circuit current while both networks are partly on. Dynamic power therefore scales with activity, capacitance, $V^2$ and frequency, the $P = \alpha C V^2 f$ of [19-06](../../../19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md).
2. `!=` returns `x` (unknown) if either side contains `x` or `z`, and an `if` treats `x` as false, so a broken circuit producing `x` would pass silently. `!==` compares the four-valued patterns exactly, so `x` or `z` counts as a mismatch.
3. A NAND3 has $2 \times 3$ = 6 transistors; with three NAND2s (12), the NAND-NAND majority has 18. The minimal SOP $AB + BC + AC$ has 6 literals, and two-level NAND logic costs two transistors per first-level literal plus two per second-level input.
4. With the pMOS in series, the pull-up conducts only when $A = B = 0$. For $AB$ = 01 and 10, neither network conducts and the output floats: Icarus shows `z`, and the testbench reports a failure. (Real hardware would hold the previous value briefly on the output capacitance, then drift, a classic intermittent bug.)
5. A full adder's sum is $A \oplus B \oplus C_{in}$ and its carry is the majority of $A$, $B$, $C_{in}$; both are self-dual. Complementing all inputs complements both outputs, which lets designers alternate inverted and non-inverted stages along a carry chain and remove inverters from the critical path.

</details>

## Optional hardware

A breadboard with a 74HC00 (quad NAND2) and 74HC02 (quad NOR2), a 5 V supply, DIP switches and LEDs (with 1 kΩ resistors) lets you build the four-NAND XOR and the NAND-NAND majority and step through their truth tables by hand. A CD4007 (a package of individual CMOS transistor pairs) lets you wire an inverter and a NAND2 from discrete transistors and measure the supply current in each state with a multimeter: it is below the meter's resolution in every settled state, and rises only while the inputs are switching.
