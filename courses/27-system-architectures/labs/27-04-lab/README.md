# Lab 27-04 · Ears, Glasses and Headsets

**Objective.** Use small models to see how delay limits noise cancellation, what an LE Audio stream costs as its bit rate rises, how much warm surface a pair of glasses needs for a given power, and how much foveated rendering saves.

**Chapter:** [27-04 · Wearables II: Earbuds and Smart Glasses / XR](../../chapters/27-04-wearables-earbuds-and-glasses.md)

## Background

§3.1 gave speaker power from loudness, $P = 10^{(\text{SPL} - S)/10}$ mW. §3.2 derived ANC attenuation $-20\log_{10}|1 - g\,e^{-j2\pi f\tau}|$. §3.3 computed LE Audio frames, packets and radio current. §3.5–3.7 gave the heat a frame sheds, $hA\Delta T$, waveguide display power, foveated shading work and registration error $\omega\tau$. All parameters are assumed, as in the chapter's examples.

## Files

- `headworn.py`: speaker power and class-D efficiency; ANC residual, attenuation and delay budget; LC3 frame size, LE packet air time and stream current; earbud life and case recharges; heat shed by a surface; waveguide display power; registration error, pixel rate, foveated work and stream power.
- `27-04-headworn-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · The ANC delay limit** (notebook). *Predict* the frequency at which a 50 µs delay leaves 10 dB of cancellation. Then plot attenuation against frequency for delays of 20 µs, 50 µs, 100 µs and 1 ms.

**Part 2 · LE Audio bit rate** (notebook). *Predict* the average radio current of the Example 27-04.4 earbud at 192 kb/s in 10 ms frames. Then plot current against bit rate for 7.5 ms and 10 ms frames.

**Part 3 · Warm surface for a budget** (notebook). *Predict* the surface area a pair of glasses needs to shed 0.5 W at 8 K with $h$ = 8 W/m²·K. Then plot sustained power against area for allowed rises of 5, 8 and 10 K.

**Part 4 · Foveation** (notebook). *Predict* the shading work for a 30° fovea in a 100° field with the periphery at a quarter of the linear resolution. Then plot work against fovea size for peripheral scales of 1/4, 1/3 and 1/2.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 27-04.a | frequency of 10 dB at 50 µs | 1.01 | kHz |
| Lab 27-04.b | octets at 192 kb/s, 10 ms | 240 | octets |
| Lab 27-04.b1 | radio current at 192 kb/s | 463 | µA |
| Lab 27-04.c | area for 0.5 W at 8 K | 78.1 | cm² |
| Lab 27-04.d | shading work, 30° fovea, quarter scale | 0.147 | — |

## Discussion

1. A 50 µs delay leaves 10 dB of cancellation at **1.01** kHz and less above; at 1 ms the curve crosses 0 dB at 167 Hz and amplifies noise up to 833 Hz and over most of the band above, with narrow dips near multiples of 1 kHz. Delay, not filter cleverness, sets ANC's bandwidth.
2. At 192 kb/s the 240-octet frames raise the radio current to **463** µA, still well under 2 mW at 3.0 V. Doubling the bit rate does not double the current, because wake-up, turnaround and acknowledgment are fixed per frame.
3. Shedding 0.5 W at an 8 K rise needs **78.1** cm² of warm surface, more than a slim frame offers, which is why glasses keep their sustained power to a few hundred milliwatts.
4. A 30° fovea with a quarter-scale periphery needs **0.147** of the full-resolution work; the saving shrinks as the fovea grows, so eye-tracking accuracy (how small a fovea is safe) sets the gain.

## Optional hardware

None needed. With a pair of ANC earbuds and a tone-generator app, compare how well they cancel a 100 Hz tone and a 2 kHz tone played from a loudspeaker at the same level.
