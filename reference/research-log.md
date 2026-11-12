# Research Log (perishable facts and their sources)

Every perishable fact used in the curriculum is logged here with its source, the date it was checked, and a confidence note. Chapters cite these entries by ID (e.g., `[R-003]`) in their **Sources** section. When a fact is re-checked, add a new dated line instead of deleting the old one.

Confidence tags follow the curriculum convention: **[Established]** (stable, multiple primary sources), **[Industry estimate]** (credible but approximate or single-source), **[Contested]** (sources disagree, so the range is shown).

| ID | Topic | Checked |
|---|---|---|
| R-001 | NCEES FE Electrical & Computer specification | Nov 2026 |
| R-002 | IEEE 802.11ax/be EVM requirements; 802.11be status | Nov 2026 |
| R-003 | 3GPP NR frequency ranges FR1/FR2 | Nov 2026 |
| R-004 | On-chip wire capacitance and resistance | Nov 2026 |
| R-005 | Synchrophasor (PMU) standards | Nov 2026 |
| R-006 | Power-grid frequencies (50/60 Hz, Japan split) | Nov 2026 |
| R-007 | US 6 GHz unlicensed band | Nov 2026 |
| R-008 | SAR ADC settling requirement | Nov 2026 |
| R-009 | kT/C noise | Nov 2026 |
| R-010 | Rise-time–bandwidth relation | Nov 2026 |
| R-011 | Complex multiplication with three real multiplications | Nov 2026 |
| R-012 | Desktop CPU maximum boost clocks | Nov 2026 |
| R-013 | ABET curriculum minimums; semester-credit workload | Nov 2026 |
| R-014 | Nominal mains voltages (IEC 60038, ANSI C84.1) | Nov 2026 |

---

## R-001 · NCEES FE Electrical and Computer specification

- **Spec in force:** the CBT specification "effective beginning with the July 2020 examinations". It has 110 questions in 17 knowledge areas. Source: [NCEES FE E&C CBT specification (PDF)](https://ncees.org/wp-content/uploads/FE-Electrical-and-Computer-CBT-specs.pdf). NCEES's 2025 outreach deck also describes the spec as "Updated in 2020" ([FEOAT 2025 deck](https://ncees.org/wp-content/uploads/2025/05/FEOAT-PPT-2025.pdf)).
- **Question ranges:** Mathematics 11–17 · Probability & Statistics 4–6 · Ethics & Professional Practice 4–6 · Engineering Economics 5–8 · Properties of Electrical Materials 4–6 · Circuit Analysis 11–17 · Linear Systems 5–8 · Signal Processing 5–8 · Electronics 7–11 · Power Systems 8–12 · Electromagnetics 4–6 · Control Systems 6–9 · Communications 5–8 · Computer Networks 4–6 · Digital Systems 8–12 · Computer Systems 5–8 · Software Engineering 4–6.
- **Appointment:** about 6 h in total, of which 5 h 20 min is exam time. The exam is closed-book with the electronic *NCEES FE Reference Handbook*. Errata confirm version 10.4 was in use from July 2024. Some prep sites say 10.6 applies from July 2026, but this was **not verified on ncees.org**.
- **Newer spec announced?** None found as of Nov 2026. The Nov 2026 NCEES Examinee Guide still describes the FE as 110 questions, year-round.
- **Confidence:** high for most areas. Medium for Linear Systems, Signal Processing, Electronics and Communications, which were confirmed via secondary sources citing the spec. **Open issue:** ncees.org was unreachable from the build environment, so the PDF should be re-checked directly.

## R-002 · IEEE 802.11 EVM requirements

- **802.11ax, 1024-QAM (MCS 10/11):** transmit relative constellation error (EVM) ≤ **−35 dB** [Established]. Some test-equipment notes cite −32 dB depending on amplitude-drift compensation; that footnote is ambiguous. Source: [LitePoint EVM application note (2021)](https://www.litepoint.com/wp-content/uploads/2021/01/EVM-App-Notes-010621-web.pdf).
- **802.11be, 4096-QAM (MCS 12/13):** ≤ **−38 dB** [Established]. Source: [Rohde & Schwarz application note 1EF114](https://cdn.rohde-schwarz.com.cn/pws/dl_downloads/dl_application/application_notes/1ef114/1EF114_1e_802_11be_EVM.pdf), which quotes the TGbe draft (clause 36.3.19.4.1).
- **802.11be:** maximum channel width **320 MHz**, in the 6 GHz band only. The standard was approved by the IEEE SA Board on 26 Sep 2024 and published as **IEEE 802.11be-2024** on 22 Jul 2025. Source: [IEEE SA 802.11be page](https://standards.ieee.org/ieee/802.11be/7516/).

## R-003 · 3GPP NR frequency ranges

- **Ranges:** FR1 = 410–7125 MHz; FR2-1 = 24 250–52 600 MHz; FR2-2 = 52 600–71 000 MHz [Established].
- **Source:** 3GPP TS 38.104 Table 5.1-1, [ETSI TS 138 104 V19.2.0 (2025-10)](https://www.etsi.org/deliver/etsi_ts/138100_138199/138104/19.02.00_60/ts_138104v190200p.pdf). The same values appear in V19.6.0 (2026-09). NTN bands (TS 38.101-5) use different ranges.

## R-004 · On-chip interconnect

- **Wire capacitance:** "Typical dense wires have ~0.2 fF/µm", compared with 1–2 fF/µm for gate capacitance [Established rule of thumb]. Source: D. Harris, *CMOS VLSI Design* 4th ed. lecture slides, [Lecture 14 "Wires"](https://pages.hmc.edu/harris/cmosvlsi/4e/lect/lect14.pdf).
- **Research-stage wire resistance:** imec reported semi-damascene Ru lines at **16 nm metal pitch** with average resistance **as low as 656 Ω/µm**, positioned for local metal at the A7 node and beyond [Industry estimate, research result, not production]. Source: [imec press release, 3 Jun 2025 (IITC 2025)](https://www.imec-int.com/en/press/imec-demonstrates-16nm-pitch-ru-lines-record-low-resistance-obtained-using-semi-damascene). No public Ω/µm figure was found for production M0 layers.

## R-005 · Synchrophasor standards

- **Measurement:** IEC/IEEE 60255-118-1:2018 (supersedes IEEE C37.118.1-2011/1a-2014; a revision was approved Nov 2025). **Data transfer:** IEEE C37.118.2-2024. Sources: [IEEE SA 60255-118-1](https://standards.ieee.org/ieee/60255-118-1/5724/), [IEEE SA C37.118.2](https://standards.ieee.org/ieee/C37.118.2/7077/).
- **Reporting rates (C37.118.1-2011 Table 1):** 50 Hz systems use 10/25/50 frames/s; 60 Hz systems use 10/12/15/20/30/60 frames/s. The 20 frames/s rate in the 2018 edition is **unverified**.

## R-006 · Power-grid frequencies

- **Japan:** eastern Japan runs at 50 Hz and western Japan at 60 Hz, with the boundary near the Fuji River (Shizuoka). The split dates from early generator purchases (German machines for Tokyo, US machines for Osaka) [Established]. Sources: [J-POWER](https://www.jpower.co.jp/english/ir/library/pdf/2011/2011b.pdf); [IEEE Milestone: Sakuma Frequency Converter Station, 1965](https://ethw.org/Milestones:Sakuma_Frequency_Converter_Station,_1965).
- **Other countries:** see [IEC World Plugs](https://www.iec.ch/world-plugs). Most of the Americas use 60 Hz; most of Europe, Africa, Asia and Oceania use 50 Hz.

## R-007 · US 6 GHz unlicensed band

- **Allocation:** FCC 20-51 (adopted 23 Apr 2020) opened **5.925–7.125 GHz** (1200 MHz, U-NII-5 to U-NII-8) for unlicensed use [Established]. Sources: [FCC 20-51](https://docs.fcc.gov/public/attachments/FCC-20-51A1.pdf), [FCC announcement](https://www.fcc.gov/document/fcc-opens-6-ghz-band-wi-fi-and-other-unlicensed-uses-0).
- **Later rules:** very-low-power devices were allowed in 2023 and extended to the whole band in 2025.

## R-008 · SAR ADC settling

- **Requirement:** settling a full-scale step to within ½ LSB of an N-bit converter needs ln(2^(N+1)) = (N+1)·ln 2 time constants, which is 11.78τ for 16 bits [Established]. Sources: [TI SBAA535A](https://www.ti.com/lit/an/sbaa535a/sbaa535a.pdf); A. Walsh, ["Front-End Amplifier and RC Filter Design for a Precision SAR ADC", *Analog Dialogue* 46-12 (2012)](https://www.analog.com/en/resources/analog-dialogue/articles/front-end-amp-and-rc-filter-design.html), which gives N_TC = ln(V_step / ½ LSB).

## R-009 · kT/C noise

- **Formula and value:** v_n,rms = √(kT/C), which gives ≈ 64 µV rms for 1 pF at 300 K (64.4 µV computed) [Established]. Source: UC Berkeley EECS 247 Lecture 9 (Khorramabadi), ["expected 64 µV" for 1 pF](https://hasler.ece.gatech.edu/Courses/ECE3400/Proj4/Berkeley_Switch_Cap_Filters.pdf).

## R-010 · Rise time and bandwidth

- **Relation:** t_r(10–90 %) ≈ 0.35 / BW [Established]. It is exact for a single-pole response (ln 9/(2π) = 0.3497). Higher-order "brick-wall-like" scope responses give 0.4–0.45. Source: [Tektronix, *ABCs of Probes*](https://download.tek.com/document/02_ABCs-of-Probes-Primer.pdf).

## R-011 · Complex multiplication with three real multiplications

- **Method:** (a + jb)(c + jd) can be computed from ac, bd and (a + b)(c + d), so only 3 real multiplications are needed; Winograd proved 3 is optimal [Established]. Source: N. J. Higham, "Stability of a method for multiplying complex matrices with three real matrix multiplications," *SIAM J. Matrix Anal. Appl.* 13(3):681–687, 1992, doi:10.1137/0613043. Higham cites Knuth, *TAOCP* Vol. 2, which attributes the method to P. Ungar (1963). The common "Gauss trick" attribution appears only in secondary sources.

## R-012 · Desktop CPU maximum boost clocks

- **Current flagships, as of Nov 2026:** AMD Ryzen 9 9950X3D up to 5.7 GHz (amd.com); Intel Core Ultra 9 285K max turbo 5.7 GHz (Intel ARK).
- **Highest rated stock boost on sale:** Intel Core i9-14900KS, 6.2 GHz (Intel ARK, launched Mar 2024) [Established].
- **Next generation:** reports of ~7 GHz parts are rumor only [Contested].

## R-013 · ABET curriculum minimums and semester-credit workload

- **ABET minimums:** the ABET *Criteria for Accrediting Engineering Programs* (2025–2026), Criterion 5 (Curriculum), require at least **30 semester credit hours** of college-level mathematics and basic sciences and at least **45 semester credit hours** of engineering topics [Established]. Source: [ABET criteria 2025–2026](https://www.abet.org/accreditation/accreditation-criteria/criteria-for-accrediting-engineering-programs-2025-2026/).
- **Credit-hour workload:** traditionally, one semester credit = one hour of class plus about two hours of outside work per week for about 15 weeks, ≈ 45 hours. Source: e.g., [Washington and Lee credit definition](https://www.wlu.edu/university-registrar/policies-and-procedures/undergraduate-credit-definition), based on the long-standing federal definition in 34 CFR 600.2. That federal definition was amended in 2025 and its current wording was not verified, so this is used only as an approximate convention [Industry estimate].

## R-014 · Nominal mains voltages

- **IEC 60038 (50 Hz systems):** the preferred low-voltage values are 230 V single-phase and 230/400 V three-phase (phase-to-neutral / phase-to-phase), with supply at the connection point expected within ±10%. These replaced the older 220/380 V and 240/415 V systems [Established]. Sources: [IEC 60038 summary (Wikipedia)](https://en.wikipedia.org/wiki/IEC_60038); [VDE preview of IEC 60038 ed. 7.0](https://www.vde-verlag.de/iec-normen/preview-pdf/info_iec60038%7Bed7.0%7Db.pdf).
- **North America (60 Hz):** the nominal residential voltage is 120 V single-phase (120/240 V split-phase service), under ANSI C84.1 [Established]. The ANSI tolerance bands were not verified against the standard text. Source: [IEC 60038 summary (Wikipedia)](https://en.wikipedia.org/wiki/IEC_60038), which also lists the 60 Hz values.
- Checked Nov 2026 via secondary sources; neither standard's text was consulted directly.
