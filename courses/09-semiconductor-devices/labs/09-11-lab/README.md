# Lab 09-11 · CMOS and Scaling

**Chapter:** [09-11](../../chapters/09-11-cmos-and-scaling.md) · **Notebook:** [09-11-cmos-scaling.ipynb](09-11-cmos-scaling.ipynb) · **Netlist:** [inverter.cir](inverter.cir) · **Time:** about 2 hours

## Objective

1. Compute the CMOS inverter transfer curve and its gain for several width ratios, with square-law and velocity-saturated transistors, and find the noise margins.
2. Simulate a ring oscillator transition by transition and recover $T = 2N\tau_d$.
3. Build a scaling calculator and compare constant-field, constant-voltage and partial voltage scaling.
4. Plot 50 years of microprocessor clock frequency and power and locate the end of frequency scaling.
5. Confirm the switching threshold in ngspice with level-1 transistors.

## Background

Chapter sections 3.1–3.7 and Examples 09-11.1 to 09-11.7. The inverter of Parts 1 and 5: $V_{DD}$ = 1.0 V, $V_{TN} = |V_{TP}|$ = 0.3 V, $\mu_n/\mu_p$ = 2. Part 1 also uses the short-channel transistors of 09-10 Problem 4 and 09-11 Problem 12. Part 4 uses K. Rupp's *Microprocessor Trend Data* ([repository](https://github.com/karlrupp/microprocessor-trend-data)), licensed CC-BY 4.0 and copied unchanged into [data/](data/) with attribution headers. The dataset compiles published processor specifications; it is a convenient secondary source, not a primary one. You need Python with NumPy, SciPy and Matplotlib, and optionally ngspice (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [09-11-cmos-scaling.ipynb](09-11-cmos-scaling.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s, which compare with the chapter's examples and the answer key below |
| [inverter.cir](inverter.cir) | ngspice level-1 CMOS inverters with $W_p = W_n$ and $W_p = 2W_n$; DC sweep for $V_M$ | `* EXPECT` lines tied to Example 09-11.1 and the key below (run by `tools/run_spice.py`) |
| [data/rupp_frequency_mhz.dat](data/rupp_frequency_mhz.dat), [data/rupp_power_w.dat](data/rupp_power_w.dat) | Clock frequency and typical power by year, 1971–2021 | Part 4 |

## Procedure

1. **Transfer curves (Part 1).** *Predict first:* with square-law devices, does doubling the PMOS width move $V_M$ by more or less than 50 mV? Then sweep $W_p/W_n$ and find the noise margins of the symmetric inverter.
2. **Ring oscillator (Part 2).** *Predict first:* with 101 stages, is the period 101 or 202 stage delays? Then run the transition-by-transition simulation.
3. **Scaling calculator (Part 3, the chapter's guided exercise).** *Predict first:* with the supply held at 1.2 V over five 0.7× nodes and frequency rising as $1/\text{delay}$, by what factor does power density grow? Then compute it and compare constant-field and partial scaling.
4. **Fifty years of processors (Part 4).** *Predict first:* in which five-year window does the median clock frequency stop rising? Then compute the medians.
5. **ngspice (optional).** Run `ngspice -b inverter.cir` and compare with Example 09-11.1.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | $V_M$, equal widths and $W_p = 2W_n$; noise margins | 0.4657 V and 0.500 V; 0.450 V each (Example 09-11.1) |
| 2 | 101-stage ring period | 852 ps (Example 09-11.2) |
| 3 | Power-density growth over five constant-voltage nodes | see the answer key |
| 4 | Median clock by five-year window; maximum clock; median power | see the answer key |
| 5 | ngspice $V_M$ | 0.4657 V and 0.500 V |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 09-11.a | V_M with W_p = 2 W_n | 0.500 | V |
| Lab 09-11.b | power-density growth, five constant-V nodes | 35.4 | — |
| Lab 09-11.c | median clock, 2000–2004 | 1811 | MHz |
| Lab 09-11.d | median clock, 2005–2009 | 2642 | MHz |
| Lab 09-11.e | median clock, 2010–2014 | 2800 | MHz |
| Lab 09-11.f | highest clock in the dataset | 4656 | MHz |
| Lab 09-11.g | median power, 2000–2004 | 74.0 | W |
| Lab 09-11.h | median power, 2015–2021 | 205 | W |

## Discussion questions

1. Why does the noise margin of the symmetric inverter equal 45% of the supply, not 50%?
2. Why must a ring oscillator have an odd number of stages?
3. Why did the median clock frequency stop rising after 2005, while median power kept rising?
4. What does the scaling calculator say about a technology that scales voltage by only 0.9 per node?

<details><summary>Answers to the discussion questions</summary>

1. Between $V_{IL}$ = 0.45 V and $V_{IH}$ = 0.55 V the gain magnitude exceeds 1, so that 0.1 V band is the uncertain region. Each margin is the distance from a rail to the nearer edge of that band: 0.45 V. A steeper transfer curve (higher transconductance and output resistance) narrows the band and raises the margins toward $V_{DD}/2$.
2. With an odd number of inversions around the loop, no consistent static state exists, so the circuit keeps switching. With an even number, the states alternate consistently around the ring and the circuit settles into one of two stable states (Hu's point about a 92-stage ring).
3. The medians are **1811** MHz for 2000–2004, **2642** MHz for 2005–2009 and **2800** MHz for 2010–2014: the rise stalls after 2005, and the fastest part in the set (**4656** MHz) dates from 2007. The IRDS dates the power limit to 2004 (chapter §3.6). Median typical power keeps rising, from **74.0** W in 2000–2004 to **205** W in 2015–2021. Do not read too much into that rise: the 2015–2021 set has only 16 parts, from 28 W mobile chips to 500 W servers, so the median mostly reflects which parts the dataset includes. Power per core, or per area, is the fairer trend.
4. Power density grows by $(0.9/0.7)^2$ = 1.65 per node instead of 2.04: better than constant voltage, but still unsustainable over many nodes. Only full voltage scaling keeps it constant, and the threshold voltage cannot follow (§3.6). Over five constant-voltage nodes the growth is **35.4**×.

</details>

## Optional extension

Add short-circuit current to the delay model of Part 2: give each transition an input ramp of finite slope, let both transistors conduct while the input lies between $V_{TN}$ and $V_{DD} - |V_{TP}|$, and integrate the current that flows from supply to ground. How does the short-circuit energy compare with $CV_{DD}^2$ as the input edge slows?
