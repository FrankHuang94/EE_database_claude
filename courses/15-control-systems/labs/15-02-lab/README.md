# Lab 15-02 · Transfer Functions and Block Diagrams

Chapter: [15-02 Transfer Functions and Block Diagrams](../../chapters/15-02-transfer-functions-and-block-diagrams.md)

## Objective

Turn models into transfer functions, connect them with block-diagram algebra, and check every reduction two independent ways. You will convert a state-space motor model into transfer functions, close a two-loop system in Python and in ngspice, test Mason's gain formula against a direct solve of the node equations, and watch a PLL loop filter's resistor set both the damping and a zero that matters.

## Background

Read §3 of the chapter. The lab's `blocks.py` keeps every operation visible. `feedback` forms $G/(1 + GH)$ over a common denominator so that no pole–zero pair is cancelled silently (§3.2). `tf_from_ss` uses the matrix determinant lemma, $\det(sI - A + BC) = \det(sI - A)\,[1 + C(sI - A)^{-1}B]$, so the numerator is the difference of two characteristic polynomials. `mason` enumerates forward paths, loops and sets of mutually non-touching loops; `solve_graph` solves $(I - M)\mathbf{x} = \mathbf{b}r$ directly, as an independent check.

## Files

- [blocks.py](blocks.py): `TF` (with `*` for series and `+` for parallel), `feedback`, `tf_from_ss`, `forward_paths`, `loops`, `mason`, `solve_graph` and `second_order_specs`.
- [15-02-blocks-lab.ipynb](15-02-blocks-lab.ipynb): the notebook (Parts 1–4).
- [two_loop.cir](two_loop.cir): Example 15-02.3's two-loop system built from ideal transconductors, capacitors and a resistor. Node voltages are the signals.

## Procedure

1. **State space to transfer function (Part 1).** Convert Example 15-02.2's motor model to $\Omega/V$ and to $I/V$ with `tf_from_ss`. *Predict first:* do the two share poles? Where is the zero of $I/V$?
2. **Two loops (Part 2).** Build Example 15-02.3 with `feedback` twice, simulate its step response and find the peak and the 2% settling time. Remove the inner loop and repeat. Run `two_loop.cir` in ngspice and compare its overshoot and peak time. *Predict first:* the overshoot without the inner loop.
3. **Mason (Part 3).** Apply `mason` to Example 15-02.5's graph. List its loops and non-touching pairs, and compare with `solve_graph`. Then generate random graphs and compare the two methods on each.
4. **PLL loop filter (Part 4).** For Example 15-02.6's PLL, sweep $R$ over 2.5, 5 and 10 kΩ. Record $\zeta$ and the overshoot of the divided phase after a reference phase step. *Predict first:* at $R$ = 10 kΩ, where $\zeta > 1$, is there any overshoot?

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Poles of $\Omega/V$ and $I/V$ | the same, −65.1 and −1935.4 s⁻¹; $I/V$ has a zero at $-B/J$ = −0.5 s⁻¹ |
| 2 | Two-loop step response | peak 1.018 at 1.006 s, final 0.833, 2% settling at 2.42 s; ngspice agrees |
| 2 | Without the inner loop | 60.5% overshoot, and a DC gain of 1 instead of 0.833 |
| 3 | Example 15-02.5's graph | 4 loops, 1 non-touching pair, $T$ = 7.302 both ways; random graphs agree to rounding |
| 4 | PLL sweep | $\zeta$ = 0.395, 0.791, 1.581; overshoot 36.7%, 18.2%, 6.97% |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 15-02.a | zero of I/V | −0.5 | 1/s |
| Lab 15-02.b | DC gain of I/V | 3.97 | mA/V |
| Lab 15-02.c | two-loop peak | 1.018 | — |
| Lab 15-02.d | two-loop 2% settling time | 2.42 | s |
| Lab 15-02.e | DC gain without the inner loop | 1 | — |
| Lab 15-02.f | loops in Example 15-02.5's graph | 4 | — |
| Lab 15-02.g | non-touching loop pairs | 1 | — |
| Lab 15-02.h | ζ at R = 2.5 kΩ | 0.395 | — |
| Lab 15-02.i | ζ at R = 10 kΩ | 1.581 | — |
| Lab 15-02.j | overshoot at R = 2.5 kΩ | 36.7 | % |
| Lab 15-02.k | overshoot at R = 5 kΩ | 18.2 | % |
| Lab 15-02.l | overshoot at R = 10 kΩ | 6.97 | % |

## Discussion

1. Why do $\Omega/V$ and $I/V$ share their poles, and what does the zero of $I/V$ at $-B/J$ mean physically?
2. Removing the inner velocity loop raises the DC gain from 0.833 to 1 but raises the overshoot from 22% to 60%. Why does the DC gain change?
3. A student's hand calculation of Example 15-02.5 gives 8.68. What did they most likely miss?
4. At $R$ = 10 kΩ the PLL's closed-loop poles are real ($\zeta > 1$), yet the step response overshoots by 7%. How can an overdamped system overshoot?

### Answers

1. Poles are eigenvalues of $A$, which belong to the motor, not to the chosen output. The zero of $I/V$ is where $Js + B = 0$: at DC ($s \to 0$) only friction loads the motor, so with $B$ small the steady current is small (**3.97** mA/V, set by $B/(RB + K^2)$). The current is large only while the rotor accelerates. Physically, at $s = -B/J$ the mechanical branch absorbs no current: a motor decelerating freely at that rate needs no torque.
2. With the inner loop, the plant $1/s$ becomes $1/(s + 2)$: the integrator becomes a lag of DC gain 0.5, and the outer loop's DC gain $L_0$ = 10 × 0.5 = 5 gives $T(0)$ = 5/6 = 0.833. Without it the plant integrates, the loop gain is infinite at DC, and $T(0)$ = 1 exactly. The inner loop buys damping at the cost of DC accuracy; 15-04 and 15-08 show how integral action recovers both.
3. The non-touching pair $L_1L_2$ in $\Delta$: without it $\Delta$ = 5.3 and $T$ = 46/5.3 = 8.68.
4. The closed loop has a zero at $-1/(RC)$. The response is the zero-free (overdamped) response plus $RC$ times its derivative, and that derivative term pushes the output past its final value early on. Real poles guarantee no overshoot only when there are no zeros.

## Optional hardware

An op-amp, two capacitors and a few resistors can build Example 15-02.3's loop as an analogue computer: two integrators (with summing inputs) and a summing amplifier for the error. Scale time by choosing $RC$ = 1 ms, so that the step response peaks near 1 ms, and watch it on an oscilloscope while switching the inner loop's resistor in and out.
