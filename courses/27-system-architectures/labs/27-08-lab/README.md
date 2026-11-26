# Lab 27-08 · Inference, Airtime and Energy at the Edge

**Objective.** Use small models of an edge node to see how an NPU changes an always-on budget, how LoRa's spreading factor trades range for airtime and battery life, and how much light and storage a node needs to run without a battery.

**Chapter:** [27-08 · Edge AI and IoT](../../chapters/27-08-edge-ai-and-iot.md)

## Background

The lab uses the chapter's models with its assumed parameters:

- §3.1: MAC and memory counts and inference time $\text{MACs}/(muf)$.
- §3.3: LoRa symbol time $2^{SF}/BW$ and the data sheet's time-on-air formula.
- §3.4: battery life with self-discharge, photovoltaic harvest $(E_v/K)A\eta_{pv}\eta_c$ and the supercapacitor $C = 2E/(V_{\max}^2 - V_{\min}^2)$.

## Files

- `edgemodel.py`: the models.
  - Layer MACs and the chapter's keyword spotter; inference time, average power and life.
  - LoRa symbol time, payload symbols, time on air and duty-cycle message counts.
  - Photovoltaic power, capacitor sizing and hash time.
- `27-08-edge-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · A better NPU mapping** (notebook). *Predict* the NPU's latency, energy per inference and coin-cell life in Example 27-08.1 if its utilization rises from 25% to 50%. Then plot coin-cell life against inference rate for the CPU and the NPU.

**Part 2 · Airtime against spreading factor** (notebook). *Predict* the time on air of Example 27-08.3's 20-byte packet at SF9. Then plot time on air and packets per hour (1% duty cycle) against SF from 7 to 12.

**Part 3 · Battery life** (notebook). *Predict* Example 27-08.4's life, with self-discharge, at SF10. Then plot life against reporting interval for SF7, SF10 and SF12.

**Part 4 · Three dark days** (notebook). *Predict* the supercapacitor (4.0 V to 2.2 V) that carries Example 27-08.5's node through 72 hours of darkness. Then plot the harvest margin against illuminance from 100 to 1000 lux.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 27-08.a | NPU latency at 50% | 0.208 | ms |
| Lab 27-08.a1 | NPU energy at 50% | 8.30 | µJ |
| Lab 27-08.a2 | average power | 0.388 | mW |
| Lab 27-08.a3 | coin-cell life | 72.5 | days |
| Lab 27-08.a4 | front-end share | 77 | % |
| Lab 27-08.b | payload symbols at SF9 | 33 | symbols |
| Lab 27-08.b1 | time on air at SF9 | 185 | ms |
| Lab 27-08.c | energy per message at SF10 | 39.2 | mJ |
| Lab 27-08.c1 | daily energy at SF10 | 4.63 | J |
| Lab 27-08.c2 | life at SF10 with self-discharge | 13.3 | years |
| Lab 27-08.d | energy for 72 h | 4.49 | J |
| Lab 27-08.d1 | supercapacitor | 0.805 | F |
| Lab 27-08.d2 | each of two series cells | 1.61 | F |

## Discussion

1. Doubling the NPU's utilization halves its latency to **0.208** ms and its energy to **8.30** µJ, but the life rises only from 59.7 to **72.5** days: at **0.388** mW the front end is now **77**% of the power.
2. At SF9 the packet takes **185** ms, with **33** payload symbols. Each step in SF roughly doubles the airtime; the payload symbol count falls slowly because each symbol carries more bits.
3. At SF10 a message costs **39.2** mJ and the node uses **4.63** J a day, lasting **13.3** years. The life falls steeply between SF7 and SF12, so each gateway that lowers a node's SF buys years.
4. Three dark days need **4.49** J, and a **0.805** F supercapacitor. At 4.0 V that means two series cells of at least **1.61** F each (series halves the capacitance) or a lithium-ion capacitor, plus the parts' leakage, which the model ignores. Long dark spells still cost little for a periodic sensor.

## Optional hardware

With a LoRa development board and a current probe, measure the transmit time and current at SF7 and SF12 and compare with the formula; with a small indoor solar cell and a light meter, measure its power under office light at several distances from the lamp.
