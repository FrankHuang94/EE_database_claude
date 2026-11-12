# Lab 00-01 · Calculators for the Map of EE

**Chapter:** [00-01](../../chapters/00-01-map-of-electrical-engineering.md) · **Notebook:** [00-01-calculators.ipynb](00-01-calculators.ipynb) · **Time:** about 30 minutes

## Objective

Build four small calculators you will reuse throughout the curriculum and in diligence work:

1. battery and energy conversions;
2. energy per bit for interconnects;
3. Shannon capacity versus bandwidth and SNR;
4. a dated market-by-segment chart that you can update.

## Background

From the chapter:

- **Battery energy:** energy (Wh) = capacity (Ah) × voltage (V).
- **Interconnect power:** $P = E_b R_b$.
- **Shannon capacity:** $C = B\log_2(1 + \text{SNR})$, with SNR as a power ratio, $\text{SNR} = 10^{\text{dB}/10}$.

## Procedure

1. Run all cells.
2. Use the battery calculator on two devices you own. The capacity and voltage are usually printed on the battery or in the specifications.
3. **Predict, then run:** at 20 dB SNR, does an 80 MHz channel beat a 20 MHz channel at 40 dB SNR? Write your answer, then run the Shannon cell.
4. Open the market cell and read how to update it when WSTS publishes new data (check the date in [R-016](../../../../reference/research-log.md#r-016--global-semiconductor-market-wsts--sia)).

## Expected results

| Exercise | Expected |
|---|---|
| 80 MHz at 20 dB | 532.7 Mb/s |
| 20 MHz at 40 dB | 265.8 Mb/s, so the wider channel wins by about 2×, despite 100× lower SNR |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 00-01.1 | capacity, 80 MHz at 20 dB | 532.7 | Mb/s |
| Lab 00-01.2 | capacity, 20 MHz at 40 dB | 265.8 | Mb/s |

## Discussion questions

1. Why does capacity grow only logarithmically with SNR but linearly with bandwidth?
2. A colleague quotes "chip market growth of 90% in 2026". What questions do you ask before using that number?

## Optional hardware version

None needed. If you have a USB power meter (an inexpensive inline USB-C meter), measure how much energy your phone draws during a full charge and compare it with the battery's rated Wh. The difference is charging loss.
