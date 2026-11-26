# Lab 27-03 · A Smartwatch's Energy Ledger

**Objective.** Use small models of a smartwatch to see how the floor sets battery life, where a Bluetooth link's current stops falling with the interval, what the refresh rate costs an always-on display, and when batching on the application processor can match an always-on hub.

**Chapter:** [27-03 · Wearables I: The Smartwatch](../../chapters/27-03-wearables-smartwatch.md)

## Background

§3.2 built the day budget $E_{day} = \sum P_it_i$ and the life $L = 24\ \text{h} \times u\,\eta\,E_b/E_{day}$. §3.3 derived display power $\pi L_vA\,\text{APL}/\eta_v + P_0 + E_ff_r$. §3.4 compared AP batching, $f_sE_s + f_sE_w/N$, with an always-on hub. §3.5 gave the BLE link's average current $I_{sl} + I_{rx}s + Q_{ev}/T$. All parameters are assumed, as in the chapter's examples.

## Files

- `watchmodel.py`: battery energy, daily energy and battery life; OLED emission and display power; pixel hold time; AP batching, hub power and the batch for a power target; BLE air time, event charge and average current; light-load buck and LDO input power and their crossover; power-gating break-even; cell active fraction, terminal voltage and the largest safe current; paging current; solar harvest.
- `27-03-watch-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · The floor and battery life** (notebook). *Predict* the battery life of Example 27-03.1 if the floor drops from 6 to 4 mW with the always-on display still on. Then sweep the floor from 2 to 10 mW and plot life against it.

**Part 2 · Where the BLE current stops falling** (notebook). *Predict* the connection interval at which the link's average current is twice its interval-independent part ($I_{sl} + I_{rx}s$ = 1.86 µA). Then plot average current against interval on log axes.

**Part 3 · Refresh and the always-on display** (notebook). *Predict* the always-on display power of Example 27-03.2 at a 10 Hz refresh. Then plot display power against refresh rate for APL 0.15 and 1.0.

**Part 4 · Batching against the hub** (notebook). *Predict* the smallest batch at which an AP with $E_s = 3$ µJ per sample and $E_w = 0.5$ mJ per wake matches the 0.208 mW hub at 50 Hz. Then plot both powers against the batch size.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 27-03.a | battery life with a 4 mW floor | 37.7 | h |
| Lab 27-03.a1 | life per milliwatt of floor | 1.3 | h/mW |
| Lab 27-03.b | interval at twice the floor current | 0.783 | s |
| Lab 27-03.c | always-on display power at 10 Hz | 8.30 | mW |
| Lab 27-03.d | batch matching the hub, 3 µJ per sample | 429 | samples |
| Lab 27-03.d1 | latency of that batch | 8.58 | s |

## Discussion

1. Cutting the floor from 6 to 4 mW lengthens life from 35.1 to **37.7** h. The floor is paid 24 hours a day, so each milliwatt is worth about **1.3** hours here; the curve of life against floor is a hyperbola, steepest where the floor is smallest.
2. At **0.783** s the event term equals the 1.86 µA that no interval removes. Beyond about a second, lengthening the interval buys little and costs latency; the remaining levers are the sleep current and the sleep clock's accuracy.
3. At 10 Hz the always-on display draws **8.30** mW, against 5.60 mW at 1 Hz and 23.3 mW at 60 Hz. For a dark face the refresh term, not the light, decides the power above a few hertz.
4. With 3 µJ per sample the AP's per-sample floor is 0.15 mW, so it needs a batch of **429** samples (**8.58** s of data) to match the hub: fine for logging, impossible for a wrist raise.

## Optional hardware

None needed. With a USB power meter or a bench supply and a BLE development board, measure the average current of an idle connection at intervals of 30 ms, 100 ms and 1 s, and compare it with the model's $I_{sl} + I_{rx}s + Q_{ev}/T$.
