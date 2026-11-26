# Lab 27-06 · Networks, Sensors and Compute in a Car

**Objective.** Use small models of a vehicle's electronics to see how CAN response times explode as a bus fills, how much camera data a central computer must take in, what compute costs in an electric vehicle's range, and how latency turns into stopping distance.

**Chapter:** [27-06 · Automotive E/E Architecture and ADAS Compute](../../chapters/27-06-automotive-ee-architecture.md)

## Background

§3.2 derived the worst-case CAN frame length with bit stuffing and the fixed-priority response-time iteration. §3.3 gave camera data rate $Pfb$. §3.4 sized compute and its range cost $P_c/(P_c + ev)$. §3.5 gave stopping distance $vt + v^2/(2a)$. All parameters are assumed, as in the chapter's examples.

## Files

- `automodel.py`: CAN frame length and time, bus load and response time; camera data rate, TOPS sizing, range loss, reaction and stopping distance; Manhattan wiring for star and zonal layouts; residual FIT, fleet events and update time.
- `27-06-auto-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Filling the bus** (notebook). *Predict* the lowest-priority response time on Example 27-06.1's bus at 125 kb/s if one more 8-byte, 100 ms message is added at the lowest priority. Then plot the lowest-priority response time against bit rate.

**Part 2 · Camera budget** (notebook). *Predict* how many 8-megapixel, 30 frame/s, 12-bit cameras fit within 40 Gb/s of input. Then plot total input rate against camera count and resolution.

**Part 3 · Range in the city** (notebook). *Predict* the range lost to a 500 W computer in slow traffic at 30 km/h and 140 Wh/km. Then plot range loss against speed for 100 W and 500 W.

**Part 4 · Latency and stopping** (notebook). *Predict* the stopping distance at 130 km/h with 0.5 s of latency at 8 m/s². Then plot stopping distance against latency for 50, 100 and 130 km/h.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 27-06.a | bus load with the added message | 96.8 | % |
| Lab 27-06.a1 | lowest-priority response time | 41.0 | ms |
| Lab 27-06.b | cameras within 40 Gb/s (fractional) | 13.9 | — |
| Lab 27-06.b1 | cameras within 40 Gb/s (whole) | 13 | — |
| Lab 27-06.c | range lost at 30 km/h | 10.6 | % |
| Lab 27-06.d | stopping distance with 0.5 s | 99.6 | m |
| Lab 27-06.d1 | extra distance against 100 ms | 14.4 | m |

## Discussion

1. Adding one more low-priority message lifts the load to **96.8**% and its worst-case response to **41.0** ms: near saturation, each new frame lengthens everyone else's worst case.
2. Forty gigabits per second carries **13** such cameras (**13.9** before rounding down), which is why camera count and resolution are negotiated against the central computer's input lanes.
3. In 30 km/h traffic a 500 W computer costs **10.6**% of range: low-speed robotaxi duty is where compute efficiency matters most.
4. Half a second of latency stretches the stopping distance at 130 km/h to **99.6** m, **14.4** m more than with 100 ms.

## Optional hardware

None needed. With a USB-to-CAN adapter and an open-source analyser on a development board, measure frame times at 125 and 500 kb/s and compare with the worst-case formula.
