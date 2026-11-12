# Solutions 00-01 · The Map of Electrical Engineering

Problems: [00-01 problems](../problems/00-01-problems.md) · Chapter: [00-01](../chapters/00-01-map-of-electrical-engineering.md)

All numbers are in the answer key and recomputed by [verify_00_01.py](../verify/verify_00_01.py).

---

## Solutions

### Solution 00-01.1

Other reasonable answers are fine.

(a) **Laptop charger:** power electronics ([22-04](../../22-power-electronics-and-energy-conversion/chapters/22-04-isolated-converters.md)) and control of the converter loop ([22-07](../../22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md)).
(b) **5G radio:** RF ([21-07](../../21-rf-and-microwave-engineering/chapters/21-07-power-amplifiers.md)) and communications and DSP ([17-10](../../17-communication-systems/chapters/17-10-ofdm.md)).
(c) **AI accelerator:** computer architecture ([14-14](../../14-computer-organization-and-architecture/chapters/14-14-ai-accelerators.md)) and digital VLSI ([19-06](../../19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md)), plus memory ([23-05](../../23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md)).
(d) **EV traction inverter:** power electronics with wide-bandgap devices ([22-06](../../22-power-electronics-and-energy-conversion/chapters/22-06-converter-losses-and-wide-bandgap.md)) and motor control ([22-11](../../22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md)).
(e) **Hearing aid:** low-power analog and mixed-signal ([20-08](../../20-analog-and-mixed-signal-ic-design/chapters/20-08-sigma-delta-converters.md)) and DSP ([16-09](../../16-digital-signal-processing/chapters/16-09-multirate-dsp.md)), plus ultra-low-power embedded design ([18-09](../../18-embedded-systems-and-microcontrollers/chapters/18-09-ultra-low-power-design.md)).

### Solution 00-01.2

Energy $= 0.300\text{ Ah} \times 3.85\text{ V} = 1.155$ Wh $= 1.155 \times 3600 = 4158$ J. Over 48 hours, average power $= 1.155/48 = 0.0241$ W $= 24.1$ mW. That is about 40 times less than the phone in Example 00-01.1 draws, which shows why wearable SoCs are designed around always-on, ultra-low-power domains.

### Solution 00-01.3

$P = 9 \times 2.22 = 19.98$ W, about 20 W. Over 30 minutes (1800 s): $19.98 \times 1800 = 35\,960$ J $= 35.96$ kJ $= 9.99$ Wh. That is enough to charge most of a 15 Wh phone battery, ignoring losses.

### Solution 00-01.4

One port: $15\times10^{-12} \times 400\times10^9 = 6.00$ W. 64 ports: $384$ W. A large switch has dozens to hundreds of high-speed ports, and a datacenter has thousands of switches, so interface energy per bit directly drives facility power and cooling. That is the motivation for lower-power optics such as linear-drive and co-packaged optics ([24-09](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-09-lpo-and-cpo.md)).

### Solution 00-01.5

(a) $kT\ln 2 = 1.381\times10^{-23} \times 77 \times 0.6931 = 7.37\times10^{-22}$ J.
(b) $0.1\times10^{-15}/2.87\times10^{-21} = 3.48\times10^4$, still tens of thousands of times above the limit.

### Solution 00-01.6

SNR $= 10^{2.5} = 316.2$.
(a) $80\times10^6 \times \log_2(317.2) = 80\times10^6 \times 8.309 = 664.8$ Mb/s.
(b) Doubling the bandwidth: $160\times10^6 \times 8.309 = 1330$ Mb/s, twice (a).
(c) Doubling the SNR to 632.5: $80\times10^6 \times \log_2(633.5) = 80\times10^6 \times 9.307 = 744.6$ Mb/s, only 12% more.
Bandwidth helps far more, which is why spectrum is valuable and channel widths keep growing.

### Solution 00-01.7

(a) $795.6/1.262 = \$630.4$ B in 2024.
(b) $299.5/86.5 = 3.46$.
(c) Logic is driven by AI and datacenter compute, a fast-growing and cyclical investment wave concentrated in a few large customers. Analog serves thousands of industrial, automotive and consumer customers with long-lived products, so it grows more steadily, with its own inventory cycles. The two segments respond to different end markets.

### Solution 00-01.8

(a) NVIDIA: $18.5\times10^9/42\,000 = \$440$k per employee. ADI: $1.766\times10^9/24\,500 = \$72.1$k per employee.
(b) Any two of the following:

- R&D expense includes far more than salaries (compute, EDA licenses, mask sets, prototypes and stock compensation), and the mix differs by business.
- Employee counts include manufacturing and sales staff, in very different proportions (ADI runs its own fabs).
- Advanced-node digital design is far more capital-intensive per engineer than analog.
- Productivity is measured by the products and revenue that R&D produces, not by spend.

### Solution 00-01.9

(a) $0.6/0.75 = 0.80$ h $= 48.0$ minutes.
(b) $0.6/0.5 = 1.2$ h $= 72.0$ minutes.
(c) For example:

- **Digital and VLSI:** lower-voltage, specialized processing blocks and clock and power gating.
- **Display and optics (devices):** more efficient light engines.
- **Power electronics:** more efficient regulators at light load.
- **Embedded systems:** aggressive sleep states and offloading work to the phone.
- **RF:** lower-power radios and duty-cycled links.

### Solution 00-01.10

(a) $0.98 \times 0.96 \times 0.94 \times 0.90 = 0.796$, about **79.6%**.
(b) $1/0.796 = 1.256$ MW drawn from the grid.
(c) $1.256 - 1.000 = 0.256$ MW, about 256 kW lost as heat in conversion, which must also be removed by the cooling system. That is why rack power-delivery architecture is a major engineering and investment topic ([22-10](../../22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md)).

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 00-01.2a | watch battery energy | 1.155 | Wh |
| 00-01.2b | watch battery energy | 4158 | J |
| 00-01.2c | average power for two days | 24.1 | mW |
| 00-01.3a | charger power | 19.98 | W |
| 00-01.3b | energy in 30 min | 35.96 | kJ |
| 00-01.3c | energy in 30 min | 9.99 | Wh |
| 00-01.4a | power per port | 6.00 | W |
| 00-01.4b | power for 64 ports | 384 | W |
| 00-01.5a | Landauer limit at 77 K | 7.37×10^-22 | J |
| 00-01.5b | 0.1 fJ vs 300 K Landauer | 3.48×10^4 | — |
| 00-01.6a | capacity, 80 MHz | 664.8 | Mb/s |
| 00-01.6b | capacity, 160 MHz | 1330 | Mb/s |
| 00-01.6c | capacity, 80 MHz with doubled SNR | 744.6 | Mb/s |
| 00-01.7a | 2024 sales | 630.4 | US$ B |
| 00-01.7b | logic / analog ratio | 3.46 | — |
| 00-01.8a | NVIDIA R&D per employee | 440 | k$ |
| 00-01.8b | ADI R&D per employee | 72.1 | k$ |
| 00-01.9a | run time at 0.75 W | 48.0 | min |
| 00-01.9b | run time at 0.5 W | 72.0 | min |
| 00-01.10a | end-to-end efficiency | 79.6 | % |
| 00-01.10b | facility power for 1 MW at chips | 1.256 | MW |
| 00-01.10c | conversion losses | 256 | kW |
