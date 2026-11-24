<!-- status: verified -->
# 19-07 · Sequential Circuits, Timing and Clocking

| | |
|---|---|
| **Course** | [19 · Digital VLSI Design](../README.md) |
| **University equivalent** | The sequencing and clocking chapter of a senior digital-IC course: latch and flip-flop timing parameters, setup and hold constraints with skew and jitter, sequencing overhead and pipelining, latch-based design and time borrowing, metastability and synchronizers, and clock distribution (Weste & Harris, *CMOS VLSI Design*, ch. 10 and 13; Rabaey, Chandrakasan & Nikolić, *Digital Integrated Circuits*, ch. 7 and 10) |
| **Prerequisites** | [08-06](../../08-digital-logic-design/chapters/08-06-latches-and-flip-flops.md) (latches and flip-flops), [08-10](../../08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md) (timing, metastability and clock-domain crossing at the logic level), [19-03](19-03-logic-families.md) (transmission gates), [19-04](19-04-sizing-and-logical-effort.md) (FO4 and buffering), [19-01](19-01-cmos-inverter-static.md) (gain at the switching threshold) |
| **Estimated study hours** | 9 |
| **Last verified** | 2026-11-21 |

**Learning objectives.** After this chapter you can:

1. Define the timing parameters of latches and flip-flops and explain them from their transmission-gate circuits.
2. Derive the setup (maximum-delay) and hold (minimum-delay) constraints with clock skew and jitter, and fix violations.
3. Compute sequencing overhead and the benefit and cost of pipelining, in picoseconds and in FO4 delays.
4. Explain time borrowing in latch-based design and compute how much a path may borrow.
5. Derive the exponential resolution of a metastable latch and compute a synchronizer's mean time between failures.

## 1. Big picture

Combinational logic computes; sequential elements decide *when*. Every synchronous chip divides its work into clock cycles, with registers that capture values on a clock edge and hold them while the next cycle's logic computes. The registers are not free: each one costs part of every cycle (its sequencing overhead), constrains how fast and how slowly signals may arrive (setup and hold), and needs a clock that reaches thousands or millions of them at nearly the same instant. And whenever a signal crosses between unrelated clocks, a register can be caught undecided, a failure that can only be made rare, never impossible.

- **Frequency.** The clock period is the slowest path's logic plus the registers' overhead plus clock uncertainty; designers budget all three in FO4 delays (19-04).
- **Correctness at any frequency.** Hold violations do not depend on the clock period, so they cannot be fixed by slowing the chip down; they must be found in signoff (19-10).
- **Power.** The clock network switches every cycle and is among the largest single consumers of dynamic power (19-06).
- **Reliability.** Clock-domain crossings, in every SoC with more than one clock, depend on synchronizers whose failure rate is set by the physics of a metastable latch.

## 2. Intuition first

A **latch** is a door that stays open while the clock is high: data walks straight through (it is **transparent**) and is frozen in place when the door shuts. A **flip-flop** is two doors in series, opened alternately, like an airlock: only what is at the first door at the instant the clock rises gets through, so the flip-flop samples a single moment.

The **setup time** is how long before the door shuts the data must arrive to be sure of getting through; the **hold time** is how long after it shuts the data must stay put, so that the new value does not slip in under the closing door. The **clock-to-Q delay** is how long it takes the captured value to appear on the far side.

A metastable latch is a ball balanced on a hilltop: two cross-coupled inverters with their outputs exactly at the switching threshold are in equilibrium, and only a nudge decides which valley the ball rolls into. The smaller the nudge, the longer it takes to fall. The analogy is accurate in its key feature: the time to fall grows only logarithmically as the nudge shrinks, which is why waiting a little longer makes failures exponentially rarer.

```text
  D --TG1(clk_b)--+--[inv]--+--TG3(clk)--+--[inv]--+-- Q
                  |         |            |         |
                  +--TG2----+            +--TG4----+
                    (feedback, clk)        (feedback, clk_b)
       master latch (transparent      slave latch (transparent
       while clk is low)               while clk is high)
```

*Figure 1. A transmission-gate master–slave flip-flop (simplified: the feedback loops' inverters are not drawn). While the clock is low the master follows D and the slave holds; at the rising edge the master closes on the value present and the slave passes it to Q.*

## 3. Theory

### 3.1 Timing parameters

A flip-flop is characterized by four parameters, each measured from the clock's active edge:

- **Setup time** $t_{setup}$: D must be stable this long *before* the edge.
- **Hold time** $t_{hold}$: D must stay stable this long *after* the edge.
- **Propagation clock-to-Q** $t_{pcq}$: the latest Q settles after the edge.
- **Contamination clock-to-Q** $t_{ccq}$: the earliest Q starts to change after the edge.

A latch adds the **D-to-Q delay** $t_{pdq}$, the time for data to pass through while it is transparent. In the transmission-gate flip-flop of Figure 1, the setup time is the time for D to propagate through the master's input gate and inverter so that the feedback loop holds the right value when the master closes; the hold time reflects how long the master's input gate takes to turn fully off after the edge, which is why clock skew between the master's two clock phases matters. These parameters are characterized by simulation for every library cell (SkyWater's open flip-flop `dfxtp_1` uses exactly this transmission-gate structure, [R-315]).

### 3.2 The setup and hold constraints

Consider two flip-flops, a launching one (FF1) and a capturing one (FF2), with combinational logic between them whose longest delay is $t_{pd}$ and shortest is $t_{cd}$. Let both receive the same ideal clock of period $T_c$.

**Setup (maximum delay).** Data launched at an edge leaves FF1 by $t_{pcq}$, passes the logic by $t_{pd}$, and must arrive $t_{setup}$ before the *next* edge:

$$
T_c \ge t_{pcq} + t_{pd} + t_{setup} .
$$

The **sequencing overhead** $t_{pcq} + t_{setup}$ is the part of every cycle the registers consume.

**Hold (minimum delay).** The same edge that captures the old data at FF2 launches new data from FF1. That new data must not reach FF2 before FF2's hold time has passed:

$$
t_{ccq} + t_{cd} \ge t_{hold} .
$$

The period does not appear: a hold violation fails at any frequency. Flip-flops are designed so that $t_{ccq} \ge t_{hold}$, making back-to-back registers safe with no logic between them.

**Skew.** Let FF2's clock arrive $\delta$ later than FF1's (the **skew**, positive when the capture clock is late). The capture edge moves later by δ, which helps setup and hurts hold:

$$
T_c \ge t_{pcq} + t_{pd} + t_{setup} - \delta, \qquad t_{ccq} + t_{cd} \ge t_{hold} + \delta .
$$

**Jitter.** The clock period itself varies from cycle to cycle. If successive edges can come $t_{jitter}$ early relative to each other, the setup budget loses $t_{jitter}$; hold involves the *same* edge at both registers and is unaffected by cycle-to-cycle jitter. In design, skew and jitter are combined into a **clock uncertainty** that is subtracted from the setup budget and added to the hold requirement in the worst direction. Unintended skew must be bounded in both directions: positive skew threatens hold, negative skew threatens setup. Some designs intentionally skew clocks ("useful skew") to lend time from a fast stage to a slow one.

**Fixing violations.** A setup violation is fixed by a slower clock, faster logic (19-04 sizing, restructuring) or less overhead. A hold violation is fixed by adding delay to the short path (buffers), never by changing the clock.

### 3.3 Sequencing overhead and pipelining

Divide a block of logic with total delay $t_L$ into $N$ pipeline stages. Each stage carries the full overhead $t_o = t_{pcq} + t_{setup}$ plus uncertainty:

$$
T_c = \frac{t_L}{N} + t_o, \qquad \text{throughput} = \frac{1}{T_c}, \qquad \text{latency} = NT_c = t_L + Nt_o .
$$

Pipelining raises throughput until $t_L/N$ becomes comparable to $t_o$, after which each extra stage adds overhead and latency for little gain: the overhead's share of the cycle, $t_o/T_c$, grows toward 1.

![Throughput and overhead share against the number of pipeline stages for 2000 ps of logic and 60 ps of overhead per stage: throughput rises from 0.485 GHz to 8.2 GHz at 32 stages, below the ideal straight line, while the overhead share rises from 2.9% to 49%](../../../assets/figures/19-07/pipelining.svg)

*Figure 3. Pipelining Example 4's logic. Throughput falls further and further below the ideal line as overhead takes a growing share of each cycle.* In processors, deeper pipelines also lose cycles on branch mispredictions and hazards, so the best depth balances overhead, hazards and power. Expressed in FO4 delays (19-04), sequencing overhead is a few FO4 per cycle, and cycle times of commercial processors are a small number of tens of FO4 (§9).

### 3.4 Latches and time borrowing

Replace each flip-flop with two latches on opposite clock phases (a **two-phase** design), with logic between every pair. A latch does not sample an instant: while transparent, it passes data straight through. So if one half-cycle's logic is slow, its data can arrive after the latch opens and simply pass through, **borrowing** time from the next half-cycle. The constraint moves from each stage to the loop as a whole: around a cycle containing two latches,

$$
T_c \ge t_{L,1} + t_{L,2} + 2t_{pdq},
$$

and a half-cycle path may borrow up to $T_c/2 - t_{setup}$ (for a 50% duty cycle) before data arrives too late at the closing latch. Latch-based design tolerates skew better (a late clock edge just shortens the borrowing window) and balances uneven logic automatically, at the cost of harder timing analysis and two hold constraints per cycle. High-performance custom designs have used it extensively; standard-cell flows mostly use flip-flops.

### 3.5 Metastability and synchronizers

When D changes within the setup–hold window, the latch may close with its internal nodes near the switching threshold. Model the latch's storage loop as two identical inverters, cross-coupled, each node loaded by $C$, both near $V_M$. Near that point each inverter is a transconductance amplifier (19-01 §3.4) with $g_m = g_{mn} + g_{mp}$, and its output current charges the other node. For the difference $\Delta v = v_1 - v_2$,

$$
C\frac{d\Delta v}{dt} = g_m\Delta v \quad\Longrightarrow\quad \Delta v(t) = \Delta v_0\,e^{t/\tau}, \qquad \tau = \frac{C}{g_m} .
$$

The pair is unstable: any initial difference grows exponentially with time constant τ. The time to resolve to a valid level $\Delta V_{valid}$ is $t = \tau\ln(\Delta V_{valid}/\Delta v_0)$; a thousand-fold smaller initial difference costs only $\tau\ln 1000 = 6.9\tau$ more. (With square-law devices and no output conductance, $g_m = 2kV_{ov}$ at the metastable point; the lab's simulated pair matches $\tau = C/g_m$ = 100 ps exactly.)

![Left: node voltages of a cross-coupled inverter pair released from 0.6 V with offsets of 1 mV, 1 microvolt and 1 nV; the outputs cross 0.9 V after 643.9, 1334.6 and 2025 ps. Right: time to reach 0.9 V against the reciprocal of the initial offset on a log axis, a straight line rising 230 ps per decade](../../../assets/figures/19-07/metastability.svg)

*Figure 2. Metastability in the lab's cross-coupled pair. Each thousand-fold smaller initial offset adds the same 690.8 ps ($\tau\ln 1000$).*

**Failure probability.** If data transitions arrive uniformly in time, the probability that a transition lands close enough to the clock edge to leave the latch unresolved after a waiting time $t_r$ is proportional to $e^{-t_r/\tau}$. With $f_{data}$ data transitions per second and a clock at $f_{clk}$, the mean time between failures is

$$
\text{MTBF} = \frac{e^{t_r/\tau}}{T_0\,f_{clk}\,f_{data}},
$$

where $T_0$ is a characterized aperture constant of the flip-flop. Because MTBF grows exponentially in $t_r$, the standard **synchronizer** is two flip-flops in series: the first may go metastable, and it has a full clock cycle (minus overhead) to resolve before the second samples it. Each extra cycle of waiting multiplies the MTBF by $e^{T_c/\tau}$.

### 3.6 Clock distribution

The clock must reach every register with small skew and jitter, every cycle, while driving an enormous capacitance (α = 1, 19-06).

- **Trees.** A balanced H-tree makes every path from the root to a leaf the same length, so nominal skew is zero; mismatched loads, wire widths and process variation create residual skew. Buffers along the tree are sized by the methods of 19-04 and 19-05.
- **Grids and meshes.** A grid shorts the leaves of a tree together, averaging out skew at the cost of more wire capacitance and power; high-performance processors often use a tree driving a grid.
- **Generation.** A phase-locked loop (15-12) multiplies a reference clock to the core frequency; its jitter and the supply noise on clock buffers set the jitter budget.
- **Gating.** Clock gates at the tree's branches stop the clock to idle blocks, the main dynamic-power saving of 19-06.

> **Going deeper — resonant clocking and source-synchronous links.** Because a clock network is a large capacitance switched every cycle, some processors resonate it with on-chip inductors, recovering part of the $CV^2$ energy each cycle. And for long distances or between chips, designs send a clock or strobe alongside the data (source-synchronous) so that skew between data and clock, not absolute delay, matters: the starting point of the high-speed links covered in the companion material on datacenter networking.

## 4. Worked examples

### Example 19-07.1 · Maximum frequency (tier A)

**Setup.** Flip-flops have $t_{pcq}$ = 30 ps and $t_{setup}$ = 20 ps; the longest logic path is 250 ps. (a) Find the minimum period and maximum frequency with an ideal clock. (b) Repeat with 10 ps of jitter and the capture clock arriving 15 ps *early* (δ = −15 ps).

**Solution.** (a) $T_c = 30 + 250 + 20$ = **300** ps, **3.33** GHz.

(b) $T_c = 300 + 10 + 15$ = **325** ps, **3.08** GHz.

**Units check.** All terms in ps.

**Sanity check.** Clock uncertainty of 25 ps costs 8% of the frequency; at higher frequencies the same uncertainty costs a larger share.

### Example 19-07.2 · A hold violation (tier B)

**Setup.** A shift-register path has $t_{ccq}$ = 15 ps, no logic ($t_{cd}$ = 5 ps of wire), $t_{hold}$ = 25 ps, and the capture clock arrives 20 ps late. (a) Is hold met? (b) How much delay must be added? (c) Would halving the clock frequency help?

**Solution.** (a) Slack $= 15 + 5 - (25 + 20)$ = **−25** ps: a violation.

(b) At least **25** ps of buffering on the short path.

(c) No: the period does not appear in the hold constraint. The chip would fail at any frequency.

**Units check.** ps.

**Sanity check.** Without the skew, the slack would be −5 ps; skew turned a marginal path into a clear failure.

### Example 19-07.3 · Skew in both directions (tier B)

**Setup.** A path has $t_{pcq}$ = 30 ps, $t_{pd}$ = 400 ps, $t_{setup}$ = 20 ps, $t_{ccq}$ = 20 ps, $t_{cd}$ = 30 ps and $t_{hold}$ = 15 ps, with a 500 ps clock. What range of skew δ satisfies both constraints?

**Solution.** Setup: $500 \ge 450 - \delta$, so $\delta \ge$ **−50** ps. Hold: $20 + 30 \ge 15 + \delta$, so $\delta \le$ **35** ps. The clock tree must keep this pair's skew within −50 to +35 ps.

**Units check.** ps.

**Sanity check.** The window is asymmetric: this path has 50 ps of setup slack but only 35 ps of hold slack.

### Example 19-07.4 · Pipelining (tier B)

**Setup.** A function's logic takes 2000 ps. Each pipeline stage adds 60 ps of overhead. Find the cycle time, throughput and overhead share for 1, 2, 4, 8 and 16 stages, and the latency for 16.

**Solution.**

| Stages | $T_c$ (ps) | Throughput (GHz) | Overhead share |
|---|---|---|---|
| 1 | **2060** | **0.485** | **2.9** % |
| 2 | **1060** | **0.943** | **5.7** % |
| 4 | **560** | **1.79** | **10.7** % |
| 8 | **310** | **3.23** | **19.4** % |
| 16 | **185** | **5.41** | **32.4** % |

The 16-stage latency is $16 \times 185$ = **2960** ps, 48% longer than the unpipelined logic.

**Units check.** 1/ps = THz; 1/(310 ps) = 3.23 GHz.

**Sanity check.** Going from 8 to 16 stages raises throughput by only 1.68 times, not 2: a third of every cycle is now overhead.

### Example 19-07.5 · Time borrowing (tier B)

**Setup.** A two-phase latch design runs with $T_c$ = 500 ps and 50% duty cycle; latches have $t_{pdq}$ = 25 ps and $t_{setup}$ = 20 ps. (a) What is the most a half-cycle path can borrow? (b) If the two half-cycles' logic is 300 ps and 120 ps, does the cycle work? (c) Could flip-flops with the same overhead per cycle handle the 300 ps half-cycle?

**Solution.** (a) $T_c/2 - t_{setup}$ = **230** ps.

(b) The loop needs $300 + 120 + 2 \times 25$ = **470** ps ≤ 500 ps: it works, with the first half-cycle's logic borrowing into the second.

(c) A flip-flop design that split the logic at the same point into half-cycle stages would need each half to fit in 250 ps with overhead; the 300 ps half would fail. Latches let uneven halves share the cycle.

**Units check.** ps.

**Sanity check.** The borrowing needed is $300 + 25 - 250$ = 75 ps, well within 230 ps.

### Example 19-07.6 · Metastability and synchronizers (tier C)

**Setup.** (a) The lab's cross-coupled inverter pair (10 fF per node, $k$ = 200 µA/V², $V_{DD}$ = 1.2 V, $V_{TH}$ = 0.35 V) starts with offsets of 1 mV and 1 µV. Simulation gives the times for the high node to reach 0.9 V. Check that their difference matches τ = C/g_m. (b) A faster flip-flop has τ = 20 ps and $T_0$ = 20 ps, with a 1 GHz clock and data changing at 100 MHz. Compare the MTBF of a single flip-flop with 0.3 ns to resolve and a two-flip-flop synchronizer with 0.95 ns.

**Solution.** (a) Simulation gives **643.9** ps and **1334.6** ps. $g_m = 2 \times 200\ \mu \times 0.25$ = 100 µS and τ = 10 fF/100 µS = **100** ps, so the difference should be $100 \times \ln 1000$ = **690.8** ps, as observed.

(b) Single: $e^{15}/(20\ \text{ps} \times 1\ \text{GHz} \times 100\ \text{MHz})$ = **1.63** s: a failure every couple of seconds. Synchronizer: $e^{47.5}/(2 \times 10^6\ \text{s}^{-1})$ = **2.1** × 10¹⁴ s, about **6.7** million years.

**Units check.** $T_0f_{clk}f_{data}$ has units of 1/s.

**Sanity check.** The extra 0.65 ns is 32.5 τ, a factor of $e^{32.5} \approx 1.3 \times 10^{14}$ in MTBF.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 19-07.1a | minimum period, ideal clock | 300 | ps |
| Ex 19-07.1b | maximum frequency, ideal clock | 3.33 | GHz |
| Ex 19-07.1c | minimum period with uncertainty | 325 | ps |
| Ex 19-07.1d | maximum frequency with uncertainty | 3.08 | GHz |
| Ex 19-07.1e | frequency cost of uncertainty | 8 | % |
| Ex 19-07.2a | hold slack | -25 | ps |
| Ex 19-07.2b | delay to add | 25 | ps |
| Ex 19-07.2c | hold slack without skew | -5 | ps |
| Ex 19-07.3a | lowest skew allowed | -50 | ps |
| Ex 19-07.3b | highest skew allowed | 35 | ps |
| Ex 19-07.4a | cycle, 1 stage | 2060 | ps |
| Ex 19-07.4b | throughput, 1 stage | 0.485 | GHz |
| Ex 19-07.4c | overhead share, 1 stage | 2.9 | % |
| Ex 19-07.4d | cycle, 2 stages | 1060 | ps |
| Ex 19-07.4e | throughput, 2 stages | 0.943 | GHz |
| Ex 19-07.4f | overhead share, 2 stages | 5.7 | % |
| Ex 19-07.4g | cycle, 4 stages | 560 | ps |
| Ex 19-07.4h | throughput, 4 stages | 1.79 | GHz |
| Ex 19-07.4i | overhead share, 4 stages | 10.7 | % |
| Ex 19-07.4j | cycle, 8 stages | 310 | ps |
| Ex 19-07.4k | throughput, 8 stages | 3.23 | GHz |
| Ex 19-07.4l | overhead share, 8 stages | 19.4 | % |
| Ex 19-07.4m | cycle, 16 stages | 185 | ps |
| Ex 19-07.4n | throughput, 16 stages | 5.41 | GHz |
| Ex 19-07.4o | overhead share, 16 stages | 32.4 | % |
| Ex 19-07.4p | latency, 16 stages | 2960 | ps |
| Ex 19-07.4q | latency increase | 48 | % |
| Ex 19-07.4r | throughput gain, 8 to 16 stages | 1.68 | — |
| Ex 19-07.5a | maximum borrowing | 230 | ps |
| Ex 19-07.5b | loop requirement | 470 | ps |
| Ex 19-07.5c | borrowing needed | 75 | ps |
| Ex 19-07.6a | resolution time, 1 mV offset | 643.9 | ps |
| Ex 19-07.6b | resolution time, 1 uV offset | 1334.6 | ps |
| Ex 19-07.6c | small-signal tau | 100 | ps |
| Ex 19-07.6d | predicted difference | 690.8 | ps |
| Ex 19-07.6e | MTBF, single flip-flop | 1.63 | s |
| Ex 19-07.6f | MTBF, synchronizer | 2.1e14 | s |
| Ex 19-07.6g | MTBF, synchronizer | 6.7 | million years |
| Ex 19-07.6h | extra resolution time in tau | 32.5 | — |
| Ex 19-07.6i | MTBF factor | 1.3e14 | — |
| Txt 19-07.a | Itanium skew as a share of the cycle | 2.2 | % |
| Txt 19-07.b | implied global clock share of core power | 18 | % |
| Txt 19-07.c | SKY130 flip-flop t_pcq + t_setup | 0.373 | ns |
| Txt 19-07.d | the same in FO4 at 65 ps | 5.7 | — |
| Txt 19-07.e | resolution time, 1 nV offset | 2025 | ps |
| Txt 19-07.f | resolution-time slope per decade | 230 | ps |
| Txt 19-07.g | throughput at 32 stages | 8.2 | GHz |
| Txt 19-07.h | overhead share at 32 stages | 49 | % |

## 5. Simulate it

The lab ([labs/19-07-lab](../labs/19-07-lab/README.md)) has two parts:

- **ngspice** ([meta.cir](../labs/19-07-lab/meta.cir)): two cross-coupled inverter pairs released from metastability with offsets of 1 mV and 1 µV.
- **Python** (`timing.py` and the notebook): setup and hold checks with skew, pipelining curves, time borrowing, the metastable pair as coupled ODEs (resolution time against initial offset), and synchronizer MTBF.

**Predict, then run.**

1. Predict the resolution times for offsets of 1 mV and 1 µV given τ = 100 ps; run `ngspice -b meta.cir` and Part 1.
2. Predict how τ changes if each node's capacitance doubles, or if the inverters are twice as wide; check with `resolve_time`.
3. Predict the skew window of Example 3 if $t_{cd}$ falls to 10 ps; run Part 2.
4. Plot throughput and overhead share against pipeline depth for overheads of 30, 60 and 120 ps (Part 3).
5. Predict the MTBF of a three-flip-flop synchronizer in Example 6(b) (Part 4).

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Deeper pipelining | Frequency, throughput | Latency, overhead share, power, hazard penalties | Microarchitect |
| Faster flip-flops (lower $t_{pcq} + t_{setup}$) | Cycle time | Hold risk, area, clock load, power | Library designer |
| Latch-based design | Skew tolerance, time borrowing | Timing-analysis complexity, two hold checks per cycle | Custom circuit team |
| Tighter clock skew (grids, careful trees) | Setup and hold margins | Clock power and wire | Clock design team |
| Synchronizer depth | MTBF (exponentially) | Latency in cycles | SoC integrator |
| Hold buffers | Hold safety | Area, power, possible setup impact | Physical design |

## 7. Numbers to know

| Quantity | Value | Notes |
|---|---|---|
| Setup constraint | $T_c \ge t_{pcq} + t_{pd} + t_{setup} - \delta + t_{jitter}$ | δ = capture − launch clock |
| Hold constraint | $t_{ccq} + t_{cd} \ge t_{hold} + \delta$ | Independent of $T_c$ |
| Pipelined cycle | $t_L/N + t_o$ | Latency $t_L + Nt_o$ |
| Time borrowing | up to $T_c/2 - t_{setup}$ | Two-phase, 50% duty |
| Metastable resolution | $\Delta v = \Delta v_0e^{t/\tau}$, $\tau = C/g_m$ | |
| MTBF | $e^{t_r/\tau}/(T_0f_{clk}f_{data})$ | ×$e^{T_c/\tau}$ per extra stage |

## 8. Common mistakes

- **Fixing hold by slowing the clock.** Hold does not depend on the period.
- **Getting the skew sign wrong.** A late capture clock helps setup and hurts hold; check both directions.
- **Applying cycle-to-cycle jitter to hold.** Hold compares the same edge at two registers.
- **Pipelining without counting overhead.** Each stage adds $t_{pcq} + t_{setup}$ and uncertainty; deep pipelines are mostly overhead.
- **Treating metastability as solvable.** Synchronizers make failures rare, not impossible; specify an MTBF target and compute it.
- **Synchronizing multi-bit values bit by bit.** Bits can resolve differently; use handshakes, gray codes or asynchronous FIFOs for buses.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **How deep should pipelines be? [Established].** Hrishikesh and colleagues (ISCA 2002) concluded that "The Optimal Logic Depth Per Pipeline Stage is 6 to 8 FO4 Inverter Delays", counting a sequencing overhead of 1.8 FO4 at 100 nm: a 1 FO4 latch plus 0.3 FO4 of skew and 0.5 FO4 of jitter ([R-316]). IBM described POWER6 as a "13 FO4 design" ([R-315]). Harris's textbook slides give a buffered latch as "1.5 – 2 FO4 delays" ([R-316]).
- **Skew budgets in shipped processors [Established].** Intel's Itanium (0.18 µm, 800 MHz) projected 110 ps of clock skew without its deskew circuits and 28 ps with them, **2.2** % of its 1.25 ns cycle; the Pentium 4 cut skew from about ±32 ps to ±8 ps with compensation and then "Deliberately skew[ed] clocks for performance", gaining 200 MHz: useful skew in practice ([R-316]). IBM's POWER6 drove a clock grid from local H-trees, and "On-chip clock tuning resulted in up to a 10% frequency improvement" ([R-316]).
- **The clock's share of power [Established].** AMD's Piledriver resonant clock mesh (ISSCC 2012) cut clock distribution power "up to 24%"; its journal paper reports "a peak 25% global clock power reduction at 75°C, which translates to a 4.5% reduction in average application core power" ([R-316]), which implies the global clock was about **18** % of core power.
- **An open library's flip-flop [Established].** SkyWater's `sky130_fd_sc_hd__dfxtp_1` (the transmission-gate flip-flop of §3.1) has, at its typical corner with a fast clock edge and a light load, a clock-to-Q delay of 0.269 ns, a setup time of up to 0.103 ns and negative hold times (−0.029 and −0.047 ns), so D may change slightly before the edge ([R-316]). Its $t_{pcq} + t_{setup}$ of **0.373** ns is about **5.7** FO4 by Harris's rule of thumb for a 130 nm-class process (FO4 ≈ 0.5 ps per nm of feature size), several times the aggressive custom latch above: open, density-oriented libraries are not built for the highest frequencies.

### Why it matters commercially

- **Frequency targets are sequencing budgets.** A product's clock frequency follows from how many FO4 delays fit in a cycle after overhead and clock uncertainty; marketing frequency and microarchitecture are decided together.
- **Hold escapes are expensive.** A hold violation that reaches silicon fails at every frequency and every voltage, usually forcing a re-spin; signoff across corners exists to prevent it.
- **Clock-domain crossings are a classic field-failure source.** Chips with many clocks (every SoC) depend on correct synchronizers; MTBF targets are part of reliability specifications for automotive and infrastructure parts.

### Marketing vs Reality

- **"Higher frequency."** Ask whether it comes from deeper pipelining (more overhead and latency per instruction) or from faster logic; instructions per cycle may fall.
- **"Zero-skew clock tree."** Nominal skew can be zero; variation, temperature gradients and supply noise are not. Ask for the skew and jitter budget at signoff.
- **"Metastability-free."** No synchronous capture of an asynchronous signal is free of metastability; ask for the MTBF calculation and its assumptions.

### Questions for engineering leaders

1. *"What is your cycle time in FO4, and how much of it is sequencing overhead and clock uncertainty?"* Strong: a breakdown. Evasive: only gigahertz.
2. *"How do you close hold timing across corners, and how many hold buffers does the design carry?"* Strong: corner strategy and buffer counts. Evasive: "the tool fixes hold".
3. *"How do you verify clock-domain crossings?"* Strong: structural CDC analysis plus MTBF targets per crossing. Evasive: "we use two flops".
4. *"What fraction of your power is the clock network, and how much does gating save?"* Strong: measured numbers. Evasive: no breakdown.

## 10. Concept check

**Q1.** Why does the hold constraint not depend on the clock period?

<details><summary>Answer</summary>

It compares the same clock edge at two registers: the edge that captures old data at FF2 also launches new data from FF1, and the new data must not arrive before FF2's hold time ends, whatever the period.

</details>

**Q2.** A capture clock arrives 30 ps late. Which constraint gets easier and which harder?

<details><summary>Answer</summary>

Setup gets easier by 30 ps (the capture edge is later); hold gets harder by 30 ps (old data must be held 30 ps longer).

</details>

**Q3.** Why does pipelining give diminishing returns?

<details><summary>Answer</summary>

Each stage carries a fixed overhead; as $t_L/N$ shrinks, the overhead becomes a growing fraction of the cycle, so throughput approaches $1/t_o$ while latency keeps growing.

</details>

**Q4.** What is time borrowing, and why can latches do it but flip-flops cannot?

<details><summary>Answer</summary>

A slow half-cycle's data arriving after a latch opens passes straight through and uses time from the next half-cycle. A flip-flop samples only at its edge, so late data is simply missed.

</details>

**Q5.** Why does waiting a little longer make synchronizer failures exponentially rarer?

<details><summary>Answer</summary>

A metastable pair's imbalance grows as $e^{t/\tau}$, so only initial imbalances smaller than $\Delta V e^{-t/\tau}$ remain unresolved after time $t$; the probability of landing that close to balance falls exponentially with $t$.

</details>

**Q6.** Why can a multi-bit bus not be synchronized by putting a two-flip-flop synchronizer on each bit?

<details><summary>Answer</summary>

Each bit may resolve differently and on different cycles, so the receiver can see a mixture of old and new bits; buses cross domains with handshakes, gray-coded pointers or asynchronous FIFOs.

</details>

Problems: [19-07 problem set](../problems/19-07-problems.md).

## 11. Key terms

[Setup time](../../../reference/glossary.md#setup-time) · [Hold time](../../../reference/glossary.md#hold-time) · [Clock skew](../../../reference/glossary.md#clock-skew) · [Clock jitter](../../../reference/glossary.md#clock-jitter) · [Sequencing overhead](../../../reference/glossary.md#sequencing-overhead) · [Time borrowing](../../../reference/glossary.md#time-borrowing) · [Metastability](../../../reference/glossary.md#metastability) · [Synchronizer](../../../reference/glossary.md#synchronizer)

## 12. Connections

- **Builds on:** [08-06](../../08-digital-logic-design/chapters/08-06-latches-and-flip-flops.md) and [08-10](../../08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md) (flip-flops, timing and synchronizers at the logic level), [19-03](19-03-logic-families.md) (transmission gates), [19-04](19-04-sizing-and-logical-effort.md) (FO4 and buffer trees), [19-01](19-01-cmos-inverter-static.md) (gain at the switching threshold).
- **Next:** [19-08](19-08-sram-design.md) applies cross-coupled inverters as storage and sense amplifiers.
- **Used later:** [19-10](19-10-synthesis-and-sta.md) (static timing analysis automates §3.2 across corners), [19-11](19-11-place-route-signoff.md) (clock-tree synthesis).

## 13. Further study

- Weste & Harris, *CMOS VLSI Design*, 4th ed., ch. 10 (sequential circuit design) and ch. 13 (clocking).
- Rabaey, Chandrakasan & Nikolić, *Digital Integrated Circuits*, 2nd ed., ch. 7 (sequential logic) and ch. 10 (timing issues).
- D. Harris, *Skew-Tolerant Circuit Design*, Morgan Kaufmann, 2001: latches, time borrowing and skew tolerance in depth.
- C. Dike and E. Burton, "Miller and noise effects in a synchronizing flip-flop", *IEEE J. Solid-State Circuits*, 1999: measured metastability.

## 14. Sources

1. Weste & Harris, *CMOS VLSI Design*, 4th ed., Addison-Wesley, 2011, ch. 10 and 13.
2. Rabaey, Chandrakasan & Nikolić, *Digital Integrated Circuits*, 2nd ed., Prentice Hall, 2003, ch. 7 and 10.
3. D. Harris, *Skew-Tolerant Circuit Design*, Morgan Kaufmann, 2001.
4. [R-315] Stolt et al., POWER6 (*JSSC*, 2008); the `sky130_fd_sc_hd` library repository.
5. [R-316] Hrishikesh et al. (ISCA 2002); Harris, *CMOS VLSI Design* lecture slides; I. Young, Stanford EE380 lecture on clock distribution (2005); AMD Piledriver resonant clocking (ISSCC 2012, *JSSC* 2013); IBM POWER6 (*JSSC*, 2008); the `sky130_fd_sc_hd__dfxtp_1` Liberty model.
