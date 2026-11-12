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
| R-015 | Lithography exposure field (reticle limit) | Nov 2026 |
| R-016 | Global semiconductor market (WSTS/SIA) | Nov 2026 |
| R-017 | R&D intensity of major chip companies (10-Ks) | Nov 2026 |
| R-018 | Functional verification study (Wilson Research Group / Siemens EDA) | Nov 2026 |
| R-019 | Advanced-node design and mask cost estimates | Nov 2026 |
| R-020 | Fab cycle time and mask/EUV layer counts | Nov 2026 |
| R-021 | Learning-science evidence (testing, spacing, interleaving) | Nov 2026 |
| R-022 | FE Electrical & Computer pass rates | Nov 2026 |
| R-023 | US semiconductor workforce (SIA/Oxford Economics) | Nov 2026 |

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

## R-015 · Lithography exposure field (the "reticle limit")

- **Standard scanners (DUV and 0.33-NA EUV):** the maximum exposure field is **26 mm × 33 mm ≈ 858 mm²**, which caps the size of a single die printed in one exposure [Established].
- **High-NA EUV (0.55 NA):** anamorphic 4×/8× optics halve the field to **26 mm × 16.5 mm ≈ 429 mm²**. Larger dies must be stitched from two exposures or split into chiplets. Larger (6 × 12 inch) masks are being pursued by ASML and chipmakers to restore the full field [Established for the field size; mask transition timing is an industry plan].
- **Largest single dies:** NVIDIA's GH100 (H100) die is widely reported at about 814 mm² with about 80 billion transistors on TSMC 4N, close to the field limit; its predecessor GA100 was about 826 mm² [Industry estimate: from NVIDIA's Hopper launch materials as reproduced by trade press; the primary whitepaper was not fetched from the build environment]. Sources: [TechPowerUp GH100 database](https://www.techpowerup.com/gpu-specs/nvidia-gh100.g1011); [Notebookcheck, H100 launch](https://www.notebookcheck.net/Nvidia-unveils-H100-Hopper-compute-GPU-and-Grace-superchip-architectures.609352.0.html).
- **Sources:** [IEEE Spectrum, "This Machine Could Keep Moore's Law on Track"](https://spectrum.ieee.org/high-na-euv); [Tom's Hardware on 6×12-inch High-NA photomasks](https://www.tomshardware.com/tech-industry/semiconductors/tsmc-samsung-and-intel-shore-up-support-with-asml-to-deploy-larger-high-na-euv-photomasks-6-12-inch-photomask-transition-may-take-years-despite-unified-effort). Checked Nov 2026.

## R-016 · Global semiconductor market (WSTS / SIA)

**2025 actuals.** WSTS reported US\$795.6 B, +26.2% (Q4 release, 6 Mar 2026). SIA reported \$791.7 B, +25.6% (6 Feb 2026, on a different measurement basis) [Established]. Sources: [WSTS 2025 release](https://www.wsts.org/76/103/Global-Semiconductor-Market-grows-26-in-2025-to-796B); [SIA release](https://www.semiconductors.org/global-annual-semiconductor-sales-increase-25-6-to-791-7-billion-in-2025/).

**2025 by segment (WSTS, US\$ B; segments tie to the total).**

| Segment | 2025 sales (US\$ B) | Share |
|---|---|---|
| Logic | 299.5 | 37.6% |
| Memory | 230.0 | 28.9% |
| Analog | 86.5 | 10.9% |
| Micro | 84.9 | 10.7% |
| Optoelectronics | 43.0 | 5.4% |
| Discretes | 30.7 | 3.9% |
| Sensors | 20.9 | 2.6% |

**Forecasts.** The WSTS Spring 2026 forecast (2 Jun 2026) put 2026 at \$1,511 B (+89.9%, driven by memory at +249%) and 2027 at \$1,914 B [Industry estimate]. An August 2026 Q2 update reported first-half 2026 at \$702 B (+102% YoY). Its re-run model implied about \$1,655 B for 2026, but WSTS states these are not new forecast values. The Autumn 2026 forecast is due in December 2026. Sources: [WSTS Spring 2026](https://www.wsts.org/76/103/Global-Semiconductor-Market-Surges-Beyond-15T-2026); [WSTS Q2 2026](https://www.wsts.org/76/Global-Semiconductor-Market-records-exceptional-growth-in-Q2-2026).

**Logic growth and revisions.** SIA's 2026 State of the U.S. Semiconductor Industry report (Jul 2026) gives logic at \$299.5 B, +38.8% year on year, consistent with the segment table above and with the 2024 logic value of \$215.8 B in the WSTS Autumn 2025 forecast table. SIA's preliminary release of 6 Feb 2026 gave logic +39.9% (\$301.9 B) and memory +34.8% (\$223.1 B). Sources: [SIA 2026 State of the Industry](https://www.semiconductors.org/wp-content/uploads/2026/07/SIA_2026_State-of-the-Semiconductor-Industry.pdf); [SIA release, 6 Feb 2026](https://www.semiconductors.org/global-annual-semiconductor-sales-increase-25-6-to-791-7-billion-in-2025/); [WSTS Autumn 2025 forecast (JEITA mirror)](https://www.jeita.or.jp/japanese/stat/wsts/docs/20251202WSTS.pdf). Checked Nov 2026.

**Caveat.** Segment rows and growth rates come via secondary reproductions of the WSTS table and search-result excerpts of the SIA documents, because the WSTS, SIA and JEITA sites were unreachable from the build environment. Treat segment-level figures as **[Industry estimate]** until checked against the primary PDFs.

## R-017 · R&D intensity (latest fiscal-year 10-K / annual reports)

R&D % = R&D ÷ revenue.

| Company | Fiscal year | Revenue (US\$ B) | R&D (US\$ B) | R&D % | Notes |
|---|---|---|---|---|---|
| NVIDIA | FY2026 | 215.9 | 18.5 | 8.6% | ~42,000 employees, ~31,000 in R&D |
| AMD | FY2025 | 34.6 | 8.1 | 23.4% | |
| Intel | FY2025 | 52.9 | 13.8 | 26.1% | |
| Qualcomm | FY2026 | 43.1 | 10.2 | 23.7% | FY2025: 20.4% |
| Broadcom | FY2025 | 63.9 | 11.0 | 17.2% | ~33,000 employees; ~57% R&D, per secondary sources |
| Texas Instruments | FY2025 | 17.7 | 2.08 | 11.8% | |
| Analog Devices | FY2025 | 11.0 | 1.77 | 16.0% | ~24,500 employees; ~13,000 in engineering roles |

[Established] for revenue and R&D; [Industry estimate] for headcount splits. Sources: SEC 10-K filings ([NVIDIA](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm), [AMD](https://www.sec.gov/Archives/edgar/data/2488/000000248826000018/amd-20251227.htm), [Intel](https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm), [Qualcomm](https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000128/qcom-20260927.htm), [Broadcom](https://www.sec.gov/Archives/edgar/data/1730168/000173016825000121/avgo-20251102.htm), [ADI](https://www.sec.gov/Archives/edgar/data/6281/000000628125000153/adi-20251101.htm)); [TI annual report](https://investor.ti.com/static-files/fc9d9346-cf77-40db-902a-e9961e9c5736).

## R-018 · Functional verification study (Wilson Research Group / Siemens EDA)

- **IC/ASIC first-silicon success:** 5% in the 2026 study (released 8 Sep 2026; the recruitment method changed, which limits comparison) and 14% in 2024. It was about 30–33% from 2010–2020 and 24% in 2022 [Established as reported by the study].
- **Share of project time in verification:** 49% (IC/ASIC, 2026); earlier studies 53–57%.
- **Schedule:** about 75% of IC/ASIC projects were behind schedule (2024 and 2026).
- **Verification vs design engineers:** about a 1:1 mean peak headcount ratio (2022 study), with verification headcount growing faster (6.2% vs 2.7% CAGR, 2007–2022).
- **Respins:** "logic or functional flaws" are the #1 cause of respins. Exact 2024 and 2026 percentages are UNVERIFIED.
- **Sources:** [Siemens 2026 study blog](https://blogs.sw.siemens.com/verificationhorizons/2026/09/08/the-2026-functional-verification-study/); [2024 report PDF](https://static.sw.cdn.siemens.com/siemens-disw-assets/public/1NyfMZJ3nuPhMGQCGFDITG/en-US/ic-asic-functional-verification-trend-report-wp-86424-d3.pdf); [SemiEngineering, "First-Time Silicon Success Plummets"](https://semiengineering.com/first-time-silicon-success-plummets/); [2022 study, part 8](https://blogs.sw.siemens.com/verificationhorizons/2022/12/12/part-8-the-2022-wilson-research-group-functional-verification-study/).

## R-019 · Advanced-node design and mask cost estimates [Contested]

- **IBS design-cost estimates** (from-scratch designs with no IP reuse):
  - c. 2021: 28 nm ≈ \$40 M, 7 nm ≈ \$217 M, 5 nm ≈ \$416 M, 3 nm up to ≈ \$590 M.
  - Arm's 2023 F-1 prospectus, citing IBS (Jul 2022): 7 nm ≈ \$249 M, 2 nm ≈ \$725 M, of which software, verification and IP qualification are about 71%.
  - Earlier 2018 estimates were higher, e.g. 5 nm ≈ \$542 M.
- **Critique:** industry critics (SemiAnalysis, 2022, second-hand) argue IBS figures run 50–66% above typical real-world costs.
- **Mask sets:** reported at roughly \$10–30 M at 3 nm, from secondary sources only (UNVERIFIED).
- **Source:** [Arm F-1](https://www.sec.gov/Archives/edgar/data/1973239/000119312523216983/d393891df1.htm).

## R-020 · Fab cycle time and mask/EUV layer counts

- **Days per mask layer:** fabs average about 1–1.5 days per mask layer (best about 0.8). 28 nm used about 40–50 mask layers and 7 nm about 80–85 (SemiEngineering, ["Battling Fab Cycle Times"](https://semiengineering.com/battling-fab-cycle-times), 2017) [Industry estimate].
- **Wafer cycle time:** about 12 weeks on average and 14–20 weeks for advanced processes, across 400–1,400 process steps ([BCG × SIA, Apr 2021](https://www.semiconductors.org/wp-content/uploads/2021/05/BCG-x-SIA-Strengthening-the-Global-Semiconductor-Value-Chain-April-2021_1.pdf)) [Industry estimate].
- **EUV layers (secondary reports):** about 14 at TSMC N5 and about 19–25 at N3 variants. Total mask counts at N3/N2 are UNVERIFIED.

## R-021 · Learning-science evidence

- **Testing effect:** Roediger & Karpicke (2006), "Test-enhanced learning: Taking memory tests improves long-term retention," *Psychological Science* 17(3), 249–255. Restudy wins at 5 minutes, but testing wins at 2 days and 1 week. One-week recall in Experiment 2 was 61% (STTT) vs 40% (SSSS) [Established].
- **Spacing effect:** Cepeda, Pashler, Vul, Wixted & Rohrer (2006), "Distributed practice in verbal recall tasks: A review and quantitative synthesis," *Psychological Bulletin* 132(3), 354–380. Across 839 assessments, spaced practice beats massed practice, and the optimal gap grows with the retention interval [Established].
- **Interleaving:** Rohrer & Taylor (2007), "The shuffling of mathematics problems improves learning," *Instructional Science* 35, 481–498. One week later, mixed practice scored 63% vs blocked 20%, despite worse performance during practice (60% vs 89%) [Established].
- **Technique review:** Dunlosky, Rawson, Marsh, Nathan & Willingham (2013), *Psychological Science in the Public Interest* 14(1), 4–58. **High utility:** practice testing and distributed practice. **Moderate:** elaborative interrogation, self-explanation and interleaved practice. **Low:** summarization, highlighting, keyword mnemonic, imagery and rereading [Established].

## R-022 · FE Electrical & Computer pass rates

- **First-time takers from ABET programs within 12 months of graduation:** 70% (Jan–Jun 2026 cohort; NCEES table updated July 2026, n = 1,782) and 64% (Jul–Dec 2025 cohort, via PPI).
- **All first-time takers, calendar 2024:** 62% ([NCEES 2025 Engineering Forum presentation](https://ncees.org/wp-content/uploads/2025/08/2025-Engineering-Forum-Presentation_FINAL.pdf)) [Established].
- **Caveat:** non-ABET and self-study candidates are outside the 70% population.

## R-023 · US semiconductor workforce

- **Headline figures:** SIA / Oxford Economics, *Chipping Away* (25 Jul 2023): about 345,000 US semiconductor workers in early 2023, projected to about 460,000 by 2030. About 67,000 of the new jobs are at risk of going unfilled: roughly 39% technicians, 41% engineers and 20% computer scientists [Industry estimate].
- **Source:** [report PDF](https://www.semiconductors.org/wp-content/uploads/2023/07/SIA_July2023_ChippingAway_website.pdf).

## R-024 · EDA market concentration

- **Big-3 vendors:** Synopsys (including Ansys since 2025), Cadence and Siemens EDA dominate commercial EDA. Estimates of their combined share range from about 60–65% (market-research reports covering EDA tools only) to over 85% (SemiAnalysis, May 2026, on a revenue basis that includes IP, emulation hardware and simulation software) **[Contested: depends on market definition]**.
- **Approximate CY2025 revenues (SemiAnalysis estimates):** Synopsys about \$8 B including Ansys; Cadence about \$5.3 B; Siemens EDA about \$2.2–2.5 B **[Industry estimate]**.
- **Sources:** [SemiAnalysis, "EDA Market Primer"](https://newsletter.semianalysis.com/p/eda-market-primer) (paywalled; figures from its public summary); [MarketResearch.com EDA global report summary](https://marketresearch.com/Prof-Research-v4036/Electronic-Design-Automation-EDA-Global-39562423). Checked Nov 2026.

## R-025 · Op-amp slew rate and bandwidth (TI LM358)

- **LM358 / LM358A:** typical slew rate 0.3 V/µs and gain–bandwidth 0.7 MHz. **LM358B / LM358BA:** 0.5 V/µs and 1.2 MHz (revision history of the TI datasheet) **[Established]**.
- **Source:** [TI LM358 datasheet](https://www.ti.com/product/LM358/datasheet) (electrical characteristics and revision history, via TI's document viewer). Checked Nov 2026.

## R-026 · AI accelerator power ratings

- **NVIDIA HGX B200:** 1,000 W per GPU (SXM6, 180 GB), per Lenovo's server product guide and SemiAnalysis. **Full-specification B200:** reported at up to 1,200 W (trade press). The lower HGX rating is attributed to air-cooling limits in some reports **[Industry estimate: OEM and analyst documents rather than NVIDIA's own datasheet]**.
- **Sources:** [Lenovo Press LP2226, ThinkSystem NVIDIA HGX B200 product guide](https://lenovopress.lenovo.com/LP2226); [SemiAnalysis InferenceX, NVIDIA B200](https://inferencex.semianalysis.com/chips/b200); [TweakTown on the 1,200 W full-spec B200](https://www.tweaktown.com/news/97059/). Checked Nov 2026.

## R-027 · Subthreshold and near-threshold operation

- **Minimum-energy point.** In subthreshold CMOS, energy per operation has a minimum at a supply of a few hundred millivolts, where falling switching energy (∝ V²) is balanced by rising leakage energy (leakage acts over a longer, exponentially slower cycle). See B. H. Calhoun, A. Wang and A. Chandrakasan, "Modeling and sizing for minimum energy operation in subthreshold circuits," *IEEE JSSC*, vol. 40, no. 9, pp. 1778–1786, 2005 **[Established]**.
- **Commercial use.** Ambiq's SPOT (Subthreshold Power Optimized Technology) platform runs digital logic below 0.5 V. Its first Apollo MCUs (Cortex-M4F, 24 MHz, launched 2015) were quoted by the company at 30 µA/MHz active and about 100 nA standby, with claims of 5–10× lower energy than competing MCUs **[vendor claim; treat comparisons as Contested]**. Later generations add a higher-frequency "turboSPOT" mode.
- **Sources:** [Ambiq SPOT platform page](https://www.ambiq.com/spot); [Electronic Design, "Q&A: Salas on the SPOT in Low-Power Design"](https://www.electronicdesign.com/technologies/power/article/21800639/qa-salas-on-the-spot-in-low-power-design); [eeNews Europe, Apollo launch (2015)](https://www.eenewseurope.com/en/arm-mcu-built-in-sub-threshold-technology-for-10-fold-power-reduction/). Checked Nov 2026.
