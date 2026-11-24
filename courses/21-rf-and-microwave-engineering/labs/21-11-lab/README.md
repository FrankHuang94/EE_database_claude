# Lab 21-11 · Link Budgets: Ledgers, Margins, Coverage and Satellite Links

Chapter: [21-11 · Link Budgets](../../chapters/21-11-link-budgets.md)

## Objective

- Build a link-budget ledger for a wearable's Bluetooth link and see where each receiver's margin runs out.
- Check the combined shadowing-and-fading margin by drawing a million random links.
- Check Jakes's edge-to-area coverage formula by scattering users over a cell.
- Measure the SNR gain of coherent repetition, the mechanism behind NB-IoT's 164 dB.
- Sweep a satellite-to-phone uplink over elevation angle.

## Background

`linkbudget.py` holds the ledger (`noise_floor_dbm`, `sensitivity_dbm`, `sensitivity_from_rate`, `mapl_db`, `fspl_db`, `range_log_distance`), Shannon's bound (`shannon_ebn0_min_db`), margins (`rayleigh_margin_db`, `lognormal_margin_db`, `outage_shadow_rayleigh`, `combined_margin_db`), coverage (`edge_to_area_coverage`), interference (`noise_rise_db`), satellite links (`cn0_dbhz`, `slant_range_m`) and three seeded Monte Carlo checks (`mc_outage`, `mc_area_coverage`, `mc_repetition_gain_db`). A link budget is arithmetic on random quantities; the lab simulates the randomness rather than a circuit, so it has no ngspice netlist.

## Procedure

1. **The wearable ledger.** *Predict* the received power of the watch-to-phone link of Example 21-11.1 at 10 and 30 m, then plot received power against distance with the 1M, Coded and specification sensitivities (Part 1).
2. **Combined margins.** *Predict* the outage at the 15.03 dB combined margin of Example 21-11.3 (σ = 8 dB), then draw a million shadowing-plus-Rayleigh samples (Part 2).
3. **Area coverage.** *Predict* the area coverage for 75% at the edge (σ = 8 dB, $n$ = 3.5), then scatter a million users over a disc (Part 3).
4. **Repetition.** *Predict* the SNR gain of combining 32 repetitions of a BPSK symbol, then simulate it at −10 dB SNR per copy (Part 4).
5. **Satellite elevation.** *Predict* the uplink CNR of the LEO-600 handheld link of Example 21-11.8 overhead and at 20° elevation, then sweep (Part 5).

## Expected results

- **Part 1.** −73.33 dBm at 10 m and −84.73 dBm at 30 m; the 1M margin falls from 23.2 to 11.8 dB, while a receiver at the specification's −70 dBm already fails at 10 m.
- **Part 2.** The seeded simulation gives **10.0** % outage at 15.03 dB, against 20.03 dB that adding the separate margins would demand.
- **Part 3.** **89.9** % of a million users are covered, matching Jakes's formula.
- **Part 4.** The seeded simulation measures 15.03 dB against the ideal $10\log_{10}32$ = **15.05** dB; another seed gives a value a few hundredths of a dB away.
- **Part 5.** The uplink CNR is **7.81** dB overhead (600 km, 154.03 dB path loss), 2.74 dB at 30° and **0.49** dB at 20° (1392 km): the link closes only for part of each pass.

## Discussion

1. **Why does the simulated outage match the Suzuki integral so closely?** The integral is the exact average of the Rayleigh outage over the lognormal shadowing; the simulation draws from the same two distributions, so only sampling noise (about 0.03 percentage points for a million samples) separates them.
2. **Why is repetition worth exactly $10\log_{10}N$ only with coherent combining?** Coherent addition adds the N signal amplitudes but only the N noise powers; non-coherent (energy) combining also adds noise-on-noise terms and loses part of the gain at low SNR.
3. **Why does a satellite pass give a varying data rate?** The slant range, and with it the path loss, changes by several dB between overhead and low elevation, so the scheduler adapts the rate across the pass.

## Optional hardware

Two Bluetooth development boards and a phone running a received-signal-strength app reproduce Part 1: walk away through an office and log RSSI against distance, then fit the slope (the path-loss exponent) and the scatter (the shadowing σ). Repeat holding the board against your body to measure body loss.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 21-11.a | received power at 10 m | −73.33 | dBm |
| Lab 21-11.b | received power at 30 m | −84.73 | dBm |
| Lab 21-11.c | simulated outage at the combined margin | 10.0 | % |
| Lab 21-11.d | simulated area coverage | 89.9 | % |
| Lab 21-11.e | ideal repetition gain, 32 copies | 15.05 | dB |
| Lab 21-11.f | uplink CNR overhead | 7.81 | dB |
| Lab 21-11.g | uplink CNR at 20° | 0.49 | dB |
