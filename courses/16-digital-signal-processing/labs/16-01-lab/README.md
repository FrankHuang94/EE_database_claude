# Lab 16-01 · Discrete-Time Systems as Computations

Chapter: [16-01 Discrete-Time Signals and Systems Review](../../chapters/16-01-discrete-time-systems-review.md)

## Objective

See every idea of the review chapter run as code: aliasing as identical sample arrays, convolution as a counted loop of multiply-accumulates, moving averages and exponential averagers as hum and noise filters, the hidden accumulator in a recursive moving sum, and the same moving sum in Verilog with wraparound arithmetic.

## Background

Read §3 of the chapter. `dtsys.py` writes every operation out sample by sample, the way a DSP core or a datapath computes it, so that operation counts are visible; numpy and scipy are used only to cross-check. The Verilog part needs Icarus Verilog (`iverilog`, `vvp`); CI runs the testbench through `tools/run_hdl.py`.

## Files

- [dtsys.py](dtsys.py): `digital_freq`, `apparent_freq`, `dt_period`, `conv_mac`, `df1`, `impulse`, `step`, `poles`, `is_stable`, `ma_gain`, `ema`, `running_sum` and `wrap`.
- [16-01-dt-systems-lab.ipynb](16-01-dt-systems-lab.ipynb): the notebook (Parts 1–6).
- [movsum4.v](movsum4.v): a 4-sample recursive moving sum in 8-bit two's-complement arithmetic.
- [movsum4_tb.v](movsum4_tb.v): its self-checking testbench (Example 16-01.4's sequence, then 2000 samples chosen so that intermediate sums wrap often).

## Procedure

1. **Alias a tone (Part 1).** Sample 7 kHz and 1 kHz cosines at 8 kHz and compare the arrays. Then sweep an input from 0 to 3 kHz at $f_s$ = 1 kHz and plot the apparent frequency. *Predict first:* the shape of that plot.
2. **Convolve and count (Part 2).** Convolve 1000 random samples with a 64-tap filter using `conv_mac`, check against `numpy.convolve`, and record the MAC count.
3. **Remove mains hum (Part 3).** Build a 10 Hz "biosignal" with 50 Hz hum and noise at $f_s$ = 1 kHz, filter it with 20- and 100-point moving averages, and measure what is left of the 10 Hz component and of the hum.
4. **EMA against moving average (Part 4).** Filter a noisy step with an EMA ($\alpha$ = 1/16) and a 31-point moving average. Measure the residual noise after settling and the settling sample. *Predict first:* which filter is quieter, and which settles first?
5. **Break a running sum (Part 5).** Reproduce Example 16-01.4 in wraparound and saturating arithmetic. Then run a float32 recursive moving sum for $10^6$ samples and plot its error against the exact window sum.
6. **Build it in hardware (Part 6).** Run `movsum4_tb.v` and read the number of wraps the testbench exercised. Then change the design to saturate instead of wrap and run it again. One way: compute each sum one bit wider and clamp it back to $W$ bits, replacing the two arithmetic lines with

   ```verilog
   localparam signed [W:0] MAXV = (1 <<< (W-1)) - 1, MINV = -(1 <<< (W-1));
   wire signed [W:0]   wide1 = s + x;                                       // no wrap in W+1 bits
   wire signed [W-1:0] mid   = (wide1 > MAXV) ? MAXV : (wide1 < MINV) ? MINV : wide1[W-1:0];
   wire signed [W:0]   wide2 = mid - d4;
   wire signed [W-1:0] nxt   = (wide2 > MAXV) ? MAXV : (wide2 < MINV) ? MINV : wide2[W-1:0];
   ```

   and registering `s <= nxt;`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | 7 kHz versus 1 kHz at 8 kHz | identical samples; apparent frequency is a triangle wave in $f$, rising to 500 Hz and folding back at multiples of 1 kHz |
| 2 | Direct convolution | matches `numpy.convolve`; 64,000 MACs for 1000 × 64 |
| 3 | Hum filter | N = 20: hum removed, 10 Hz kept at 0.936; N = 100: hum removed, 10 Hz removed too (a null) |
| 4 | EMA against MA | residual noise standard deviation about 0.180σ for both; MA exact at n = 30, EMA within 1% at n = 71 |
| 5 | Running sums | wraparound gives 125 (correct), saturation 102; the float32 error wanders and grows with time, the integer sum stays exact |
| 6 | Verilog | `TEST PASSED`; the saturating variant fails |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 16-01.a | MACs for 1000 samples and 64 taps | 64000 | — |
| Lab 16-01.b | 10 Hz amplitude after the 20-point average | 0.936 | — |
| Lab 16-01.c | residual noise standard deviation per unit input σ, theory for both filters ($\sqrt{1/31}$; simulations scatter by about 1%) | 0.180 | — |
| Lab 16-01.d | apparent frequency of a 1.2 kHz tone at 1 kHz | 200 | Hz |

## Discussion

1. In Part 1, why does the apparent-frequency plot fold back rather than wrap around?
2. In Part 3, why does the 100-point average remove the 10 Hz signal as well as the hum?
3. In Part 4, both filters leave the same residual noise. What, then, decides between them in a product?
4. In Part 5, why does the float32 error grow even though each addition is accurate to about one part in $10^7$?
5. In Part 6, why does the saturating variant fail on inputs whose true 4-sample sums all fit in 8 bits?

### Answers

1. A real tone at $f$ and one at $f_s - f$ give identical samples ($\cos$ is even), so frequencies above $f_s/2$ mirror back down; only complex exponentials, which distinguish positive from negative frequencies, would simply wrap.
2. Its nulls are at multiples of $f_s/N$ = 10 Hz, and the signal sits exactly on the first one. A moving average cannot have nulls at 50 and 60 Hz without also having them at every multiple of 10 Hz.
3. Settling and memory against arithmetic: the moving average settles exactly after $N$ samples and forgets disturbances completely, but stores $N$ samples; the EMA stores one value and costs two additions and a shift, but takes about 4.6 time constants to settle to 1% and never forgets a disturbance completely. Latency targets, RAM, and whether old data must be flushed after a glitch decide.
4. The recursion has a pole at $z = 1$ that never forgets: each roundoff error stays in the accumulator, and independent errors add like a random walk, so the typical error grows like the square root of the number of samples. Large running totals also lose low-order bits, which makes each roundoff bigger.
5. Saturation is not modular: when the intermediate $s + x$ clamps at 127, the excess is lost, and subtracting $x[n-4]$ afterwards cannot recover it. The error then persists in the accumulator. Wraparound loses only multiples of 256, which the later subtraction restores.

## Optional hardware

On any microcontroller board, sample a potentiometer or a microphone with the ADC at 1 kHz, implement the EMA with a shift (`y += (x - y) >> 4`) and a 20-sample moving average with a circular buffer, and stream both to a serial plotter. Touch the input lead to inject mains hum and watch which filter removes it.
