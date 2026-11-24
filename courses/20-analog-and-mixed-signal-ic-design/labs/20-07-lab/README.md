# Lab 20-07 · Flash Encoders, SAR Switching Energy, Pipeline Redundancy and Interleaving Spurs

Chapter: [20-07 · Nyquist ADCs: Flash, SAR and Pipeline](../../chapters/20-07-nyquist-adcs.md)

## Objective

- See why a ones-counting encoder tolerates thermometer bubbles.
- Compute a SAR DAC's switching energy for every code, for conventional and monotonic switching.
- See which errors a pipeline's redundancy forgives (comparator offsets) and which it does not (residue gain).
- Confirm the MDAC's finite-gain residue in ngspice.
- Simulate the spurs of a two-channel interleaved ADC with offset, gain and skew mismatch.

## Background

`nyq.py` contains `flash_thermometer`, `ones_count` and `first_transition` (flash); `conventional_energy`, `conventional_energy_avg` and `monotonic_energy` (charge bookkeeping on the top plates, energy drawn from $V_{REF}$ in units of $C_uV_{REF}^2$); `sar_convert` (a SAR with arbitrary weights and an optional DAC error on each decision); `pipeline` (1.5-bit stages with comparator offsets and gain errors plus a 2-bit backend) and `mdac_residue`; and `ti_capture` and `power_spectrum` for interleaving. `mdac.cir` is the flip-around MDAC's hold phase with $C_s = C_f$ = 0.5 pF, $C_p$ = 0.1 pF and an OTA of 10 mS with 100 kΩ or 10 kΩ output resistance.

## Procedure

1. **Bubbles.** Encode the thermometer codes 1111000 and 1101000 with both encoders (Part 1).
2. **SAR energy.** Compute the 10-bit conventional (differential) and monotonic energies for all 1024 codes; plot them against code and find the averages, minima and maxima (Part 2).
3. **Pipeline.** Sweep the 10-bit pipeline with comparator offsets uniform in ±0.2 $V_{REF}$ (seed 7), with one offset of 0.3 $V_{REF}$, and with first-stage gains of 0.998, 0.99 and 1.01; count codes and compute DNL. Run `ngspice -b mdac.cir` (Part 3).
4. **Interleaving.** Simulate Example 20-07.7's three mismatches and plot the spectra (Part 4).

## Expected results

- **Part 1.** Both encoders give 4 for 1111000; for 1101000 the ones count gives 3 and the first-transition encoder gives 2.
- **Part 2.** Averages 1363.3 (conventional) and 255.5 (monotonic) $C_uV_{REF}^2$. The conventional energy ranges from **682.7** to **1704.7**, highest for code 0, where every trial fails and each large capacitor is charged and then discharged; the monotonic energy ranges only from **170.7** to **298.2**.
- **Part 3.** Offsets within ±0.2 $V_{REF}$ change no code; 0.3 $V_{REF}$ gives errors up to 26 codes; gain 0.998 gives a worst DNL of −0.255 LSB, 0.99 gives 4 missing interior codes (plus two unreachable codes at each end), and 1.01 a code of nearly double width (DNL **+0.99** LSB). ngspice gives the residues 0.099780 V and 0.097847 V (Example 20-07.5).
- **Part 4.** −61.1 dBc at 500 MHz (offset), −46.1 dBc and −62.3 dBc at 255.62 MHz (gain and skew).

## Discussion

1. **Why is the conventional energy highest for code 0?** Every trial fails, so each capacitor is charged to $V_{REF}$ and then discharged; for large codes most trials succeed and the charge stays where it is.
2. **Why does a gain above 1 widen a code while a gain below 1 removes codes?** A residue that is too large overlaps the next segment's range, so two input ranges map to the same codes; one that is too small leaves a gap that no input reaches (missing codes). The overlap also makes the transfer non-monotonic: just past each decision point the output steps back two to three codes (about 1% of the 256-code backend range), which a code-count DNL shows only as wide codes. Plot the output against the input to see it.
3. **What would an interleaved converter with four channels show?** Spurs at $f_s/4$ and $f_s/2$ for offsets, and images at $f_s/2 - f_{in}$ and $f_s/4 \pm f_{in}$ for gain and skew.

## Optional hardware

A breadboard SAR needs only a comparator, a microcontroller and an R-2R ladder or a DAC: implement the binary search in firmware, slow it down to milliseconds per bit, and watch the DAC output on an oscilloscope converge on the input.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 20-07.a | conventional energy minimum | 682.7 | C_u V² |
| Lab 20-07.b | conventional energy maximum | 1704.7 | C_u V² |
| Lab 20-07.c | monotonic energy minimum | 170.7 | C_u V² |
| Lab 20-07.d | monotonic energy maximum | 298.2 | C_u V² |
| Lab 20-07.e | worst DNL, gain 1.01 | 0.99 | LSB |
