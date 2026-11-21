# Problems 18-06 · Analog Interfaces: ADC, DAC and PWM

Chapter: [18-06](../chapters/18-06-adc-dac-pwm.md) · Worked solutions: [18-06 solutions](../solutions/18-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Ideal ADCs round to the nearest code; LSB $= V_{REF}/2^N$. Unless stated, the ADC's input has $R_{sw}$ = 0.5 kΩ and $C_{sh}$ = 3.3 pF, settles to half an LSB, and has a minimum sampling time of 62.5 ns. "Settling to half an LSB" means $t_s \ge (R_s + R_{sw})C_{sh}\ln 2^{N+1}$. Problems marked *(lab)* can be checked with `labs/18-06-lab/mcuanalog.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 18-06.1 [A]

**Codes and steps.** A 10-bit ADC uses a 2.5 V reference. (a) Find the LSB. (b) What code does 1.8 V give, and what voltage does code 512 represent? (c) What is the largest quantization error of an ideal converter, and its SQNR for a full-scale sine?

### Problem 18-06.2 [A]

**Reading a data sheet.** Raspberry Pi's RP2040 data sheet gives its ADC a typical SINAD of 54.0 dB and SNR of 61.5 dB ([R-307]). (a) Convert the SINAD to ENOB. (b) What ENOB would the SNR alone suggest? (c) What does the gap say about where the converter's errors come from?

### Problem 18-06.3 [A]

**An error budget.** A 12-bit ADC with a 3.3 V reference has offset ±2 LSB, gain error ±3 LSB and INL ±2 LSB; the reference itself is ±0.5%. (a) Express the reference tolerance in LSB at full scale. (b) What is the worst-case total error in LSB and in millivolts? (c) What is the root-sum-square total, and which term dominates? (d) What would a two-point calibration remove?

### Problem 18-06.4 [A]

**Throughput.** A SAR ADC needs its sampling time plus 14 cycles of a 40 MHz ADC clock per conversion. (a) How long is the conversion phase? (b) What is the highest rate at the 62.5 ns minimum sampling time? (c) What rate remains with the 312 ns a 10 kΩ source needs?

### Problem 18-06.5 [B]

**A battery divider.** A 4.2 V Li-ion cell is measured through a 1 MΩ/1 MΩ divider by a 12-bit ADC with a 3.3 V reference. (a) What current does the divider draw? (b) What sampling time would 12-bit settling need without a capacitor? (c) The pin's leakage current can be up to ±50 nA. What error does that cause, in millivolts, LSB and percent of the reading? (d) A 100 nF capacitor is added at the pin, and the ADC samples it 10 times a second after a channel at 0 V. What is the recovery time constant, and roughly what DC error does the S/H cause? (e) Which error matters, and how would you fix it?

### Problem 18-06.6 [B]

**The previous channel.** *(lab)* An input at 0.5 V with a 4.7 kΩ source and 47 nF at the pin is sampled at 200 kHz, each time after a channel at 3.3 V. (a) What is the charge-sharing step? (b) Estimate the DC error with the average-current model, and find it exactly with the recursion of §3.2; express it in LSB of a 12-bit, 3.3 V ADC. Is the reading high or low? (c) What is the exact error at 50 kHz? (d) A colleague proposes converting the channel twice per scan and discarding the first result. Does that help here? Would it help without the external capacitor?

### Problem 18-06.7 [B]

**Supply from a calibrated reference.** During production, an MCU's internal reference was converted at exactly $V_{DD}$ = 3.000 V and gave code 1652 (12 bits, $V_{DD}$ as reference); the value is stored in a factory register. (a) In the field the same conversion gives 1502. What is $V_{DD}$? (b) Another channel reads 2000 at the same moment. What voltage is that? (c) By how much does one code of the reference conversion change the computed $V_{DD}$? (d) Why does the factory value make the result independent of the reference's own tolerance?

### Problem 18-06.8 [B]

**Averaging by design.** A 12-bit ADC runs at 1 Msps. (a) How many samples must be averaged for 14-bit resolution, and at what output rate? (b) What word length does the sum of 16 samples need, and of 256? (c) The ADC's own noise is only 0.1 LSB rms. How much uncorrelated noise (dither) must be added to reach 0.5 LSB rms in total? (d) Why might the 14-bit result still be no more accurate than the 12-bit one?

### Problem 18-06.9 [B]

**A DAC sine generator.** A 12-bit DAC updated at 1 Msps by a timer and DMA makes a 50 kHz sine of 3.3 V peak to peak. (a) What is the zero-order-hold droop at 50 kHz? (b) What is the first image's frequency and level relative to the tone? (c) To push that image 74 dB below the tone, how much more attenuation is needed there, and would a second- or a third-order low-pass at 100 kHz do (use $20n\log_{10}(f/f_c)$ for an $n$th-order filter far above its corner)? (d) What slew rate does the sine need, against the DAC's 5.5 V/µs? (e) How many bytes per second must the DMA move for 16-bit DAC words?

### Problem 18-06.10 [B]

**A 12-bit PWM DAC.** An 80 MHz timer makes a 12-bit PWM from 3.3 V. (a) What is its frequency and period? (b) What single-RC time constant keeps the worst-case ripple within one LSB, and what are the bandwidth and the settling time to half an LSB? (c) What bandwidth results if 4 LSB of ripple are acceptable? (d) Explain why a second RC stage (buffered) is a better route to a fast 12-bit PWM DAC than a slower single stage.

### Problem 18-06.11 [C]

**A duty-cycled thermistor.** *(lab)* A wearable measures skin temperature once a second with a 10 kΩ resistor and a 10 kΩ (at 25 °C) thermistor powered from a GPIO pin instead of $V_{DD}$, with 100 nF at the ADC pin and $V_{DD}$ = 3.3 V as the reference. The GPIO's output resistance is about 50 Ω. (a) What would the divider draw if powered permanently? (b) After the GPIO goes high, what is the pin's time constant and its 12-bit settling time (the capacitor starts at 0 V)? (c) Estimate the charge per measurement (the divider current during settling plus the charge stored in the capacitor) and the average current at one measurement per second. (d) The GPIO's drop breaks the ratiometric cancellation. How many codes, and how many kelvin (at 45.5 codes/K), does it cost at 25 °C? (e) What would you change if the result is still not good enough?

### Problem 18-06.12 [C]

**A four-channel scan.** An ADC scans four channels whose sources have 50 Ω, 5 kΩ, 20 kΩ and 100 kΩ resistance, each conversion needing 350 ns after its sampling time. (a) Find each channel's required sampling time (at least 62.5 ns). (b) What scan rate is possible if each channel has its own sampling time? (c) What if, as on some ADCs, all channels must share one sampling-time setting? (d) A designer instead puts 100 nF on the 100 kΩ channel and uses 62.5 ns for it. Find the new scan rate and, with the 20 kΩ channel at 1.0 V and the 100 kΩ channel at 2.0 V, the DC error the S/H then causes. (e) Recommend a fix.

---

## Objective coverage

| Learning objective (chapter 18-06) | Problems |
|---|---|
| 1. ADC specifications | 1, 2, 3 |
| 2. Sampling time and source resistance | 4, 5, 12 |
| 3. External capacitors and multiplexing | 5, 6, 12 |
| 4. References and ratiometric measurement | 3, 7, 11 |
| 5. Averaging and decimation | 8 |
| 6. DAC and PWM outputs | 9, 10 |
