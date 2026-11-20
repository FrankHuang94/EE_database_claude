<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 11 · Signals and Systems

The mathematics of signals and linear time-invariant systems in continuous and discrete time: convolution, Fourier series and transforms, Laplace and z-transforms, and sampling. This is the language of DSP, communications, control and circuits alike.

| | |
|---|---|
| **Term** | 3 |
| **Study hours** | ≈ 106 |
| **University equivalents** | Signals and Systems (junior); MIT 6.003; Berkeley EE120; Stanford EE102A |
| **Textbook alignment** | Oppenheim & Willsky, *Signals and Systems*; Lathi, *Linear Systems and Signals* |
| **Free courses** | MIT OCW 6.003 Signals and Systems; Berkeley EE16B (frequency-domain content) |
| **Prerequisites** | [02 · Complex Numbers, Differential Equations and Linear Algebra](../02-complex-numbers-des-and-linear-algebra/README.md), [07 · Circuit Analysis II (Transient and AC)](../07-circuit-analysis-2-transient-and-ac/README.md) |
| **FE areas** | Linear Systems, Signal Processing |

## Learning objectives

1. Classify signals and systems (linearity, time invariance, causality, stability) and compute convolutions in continuous and discrete time.
2. Compute Fourier series and Fourier transforms and use their properties to analyze LTI systems in frequency.
3. Use the Laplace and z-transforms, including regions of convergence, to analyze stability and system functions.
4. Apply the sampling theorem, explain aliasing and design anti-aliasing and reconstruction filters.
5. Relate time-domain, frequency-domain and pole-zero descriptions of the same system.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [11-01 · Signals: Classification and Operations](chapters/11-01-signals-classification-and-operations.md) | 8 | 🏁 reviewed | [problems](problems/11-01-problems.md) · [solutions](solutions/11-01-solutions.md) · [lab](labs/11-01-lab/README.md) · [verify](verify/verify_11_01.py) |
| [11-02 · Systems and Their Properties](chapters/11-02-system-properties.md) | 7 | 🏁 reviewed | [problems](problems/11-02-problems.md) · [solutions](solutions/11-02-solutions.md) · [lab](labs/11-02-lab/README.md) · [verify](verify/verify_11_02.py) |
| [11-03 · Convolution](chapters/11-03-convolution.md) | 10 | 🏁 reviewed | [problems](problems/11-03-problems.md) · [solutions](solutions/11-03-solutions.md) · [lab](labs/11-03-lab/README.md) · [verify](verify/verify_11_03.py) |
| [11-04 · LTI Systems and Differential/Difference Equations](chapters/11-04-lti-systems-and-differential-equations.md) | 8 | 🏁 reviewed | [problems](problems/11-04-problems.md) · [solutions](solutions/11-04-solutions.md) · [lab](labs/11-04-lab/README.md) · [verify](verify/verify_11_04.py) |
| [11-05 · Fourier Series](chapters/11-05-fourier-series.md) | 10 | 🏁 reviewed | [problems](problems/11-05-problems.md) · [solutions](solutions/11-05-solutions.md) · [lab](labs/11-05-lab/README.md) · [verify](verify/verify_11_05.py) |
| [11-06 · The Continuous-Time Fourier Transform](chapters/11-06-continuous-time-fourier-transform.md) | 12 | 🏁 reviewed | [problems](problems/11-06-problems.md) · [solutions](solutions/11-06-solutions.md) · [lab](labs/11-06-lab/README.md) · [verify](verify/verify_11_06.py) |
| [11-07 · The Discrete-Time Fourier Transform](chapters/11-07-discrete-time-fourier-transform.md) | 8 | 🏁 reviewed | [problems](problems/11-07-problems.md) · [solutions](solutions/11-07-solutions.md) · [lab](labs/11-07-lab/README.md) · [verify](verify/verify_11_07.py) |
| [11-08 · The Laplace Transform and System Functions](chapters/11-08-laplace-transform-and-system-functions.md) | 10 | 🏁 reviewed | [problems](problems/11-08-problems.md) · [solutions](solutions/11-08-solutions.md) · [lab](labs/11-08-lab/README.md) · [verify](verify/verify_11_08.py) |
| [11-09 · The z-Transform](chapters/11-09-z-transform.md) | 10 | 🏁 reviewed | [problems](problems/11-09-problems.md) · [solutions](solutions/11-09-solutions.md) · [lab](labs/11-09-lab/README.md) · [verify](verify/verify_11_09.py) |
| [11-10 · Sampling, Aliasing and Reconstruction](chapters/11-10-sampling-aliasing-reconstruction.md) | 10 | 🏁 reviewed | [problems](problems/11-10-problems.md) · [solutions](solutions/11-10-solutions.md) · [lab](labs/11-10-lab/README.md) · [verify](verify/verify_11_10.py) |
| [11-11 · Modulation and Filtering Applications](chapters/11-11-modulation-and-filtering-applications.md) | 7 | 🏁 reviewed | [problems](problems/11-11-problems.md) · [solutions](solutions/11-11-solutions.md) · [lab](labs/11-11-lab/README.md) · [verify](verify/verify_11_11.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/11-signals-and-systems.csv) · [Equation sheet](../../reference/equation-sheets/11-signals-and-systems.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 11 is planned at about 106 hours: the chapters' own estimates add to 100, plus review and the exam. It is the course where circuits become systems. Courses 06 and 07 analyzed specific networks; this one asks what any linear, time-invariant system does, and answers in three equivalent languages: the impulse response (time), the frequency response (frequency) and the poles and zeros (the complex plane). Every later course in DSP, communications, control and mixed-signal design speaks all three.

The eleven chapters fall into four blocks:

- **Signals, systems and convolution (11-01 to 11-04).** Classifying signals and operating on them; the system properties (linearity, time invariance, causality, stability, invertibility) and how to test them; convolution as the complete description of an LTI system; and the differential and difference equations behind real circuits and digital filters, with biquads and complex exponentials as eigenfunctions.
- **Fourier analysis (11-05 to 11-07).** Fourier series for periodic signals (harmonics, Gibbs, THD), the Fourier transform for aperiodic ones (pairs, properties, bandwidth and rise time), and the DTFT for sequences (periodicity in ω, linear-phase FIR filters, windows and resolution).
- **Transforms with poles and zeros (11-08 and 11-09).** The bilateral Laplace and z-transforms with their regions of convergence; causality and stability read from the ROC; feedback moving poles; geometric evaluation of frequency responses; all-pass and minimum-phase systems; the biquad stability triangle; and the maps from s to z (sampling and the bilinear transform).
- **Sampling and communication (11-10 and 11-11).** The sampling theorem, aliasing of tones and noise, anti-aliasing and reconstruction, oversampling, jitter and band-pass sampling; then modulation, mixers and images, filter families and channel capacity.

Work at least the [A] and [B] problems of every chapter (152 problems in all). Every lab has a notebook that runs top to bottom; 11-08's lab adds an ngspice netlist whose pole–zero and AC analyses confirm the RLC example. Most verify scripts recompute the chapters' numbers by a different route from the text (numerical integration, simulation, root finding), so a mismatch in your own work usually means a wrong method, not a rounding difference.

**What to master cold.** The equation sheet collects the relations; these are the ideas behind them:

- an LTI system is completely described by its impulse response, and convolution is how it acts (11-03);
- complex exponentials pass through LTI systems unchanged in shape, scaled by $H(s)$, $H(j\omega)$ or $H(e^{j\omega})$, which is why frequency-domain analysis works at all (11-04);
- smoothness controls harmonic decay, sharp edges need bandwidth, and narrow in time means wide in frequency (11-05, 11-06);
- DT frequency lives on a circle; symmetric FIR filters have exactly linear phase; truncation costs ripple and observation time sets resolution (11-07);
- an algebraic transform without its ROC is incomplete; causal and stable means poles in the left half-plane or inside the unit circle; feedback moves poles; a pole's distance from the axis or circle is both its bandwidth and its decay rate (11-08, 11-09);
- sampling copies spectra, aliasing is irreversible, and oversampling moves hard filtering into the digital domain (11-10);
- modulation is multiplication, images must be filtered before mixing, and capacity grows linearly with bandwidth but only logarithmically with SNR (11-11).

The [equation sheet](../../reference/equation-sheets/11-signals-and-systems.md) collects them.

**Assessment.** The [course final exam](exam/README.md) has 14 questions and takes 210 minutes. It allows a calculator and the equation sheet, but not Python or a simulator. Aim for at least 70%. Questions 1 to 12 follow the chapters; Question 13 asks for three short derivations; Question 14 is a diligence question built around a wearable-ECG start-up's sampling claims, graded against a rubric. The course maps onto the FE Electrical and Computer exam's Linear Systems and Signal Processing areas ([R-001](../../reference/research-log.md#r-001--ncees-fe-electrical-and-computer-specification)). The [flashcards](../../flashcards/11-signals-and-systems.csv) (87 cards) are for spaced review alongside the chapters.

**Why this course matters for diligence.** Signal-processing claims hide their assumptions in the frequency domain. This course teaches you to ask:

- what bandwidth, sample rate and observation time a claimed measurement needs (resolution is $1/T_{obs}$, not the FFT size; a detector cannot be fast and fine at once);
- what protects a sampled system from aliasing, and whether the "digital filter fixes it" claim is physically possible (it is not, once a signal has folded);
- where a filter's or loop's poles are, how close to instability, and how long it rings after a disturbance;
- whether an equalizer's or filter's headline number (boost, steepness, latency) is quoted at the conditions that matter, and what it costs in noise, delay or word length;
- how far a link runs from its Shannon capacity, and what limits it.

The Marketing vs Reality sections practice this on "high-resolution FFT analysis", "linear-phase" and "unconditionally stable" filters, "up to 20 dB of equalization", "24-bit" converters, "no anti-aliasing filter needed", "brick-wall filtering" and "gigabit wireless".

**Perishable content.** The mathematics is timeless. The dated facts are data-sheet specifications, library documentation, a standards task force's tools and regulatory and filing data, logged as [R-184](../../reference/research-log.md#r-184--signal-acquisition-data-sheets) to [R-190](../../reference/research-log.md#r-190--sampling-and-anti-aliasing-in-converter-data-sheets), with earlier entries [R-117](../../reference/research-log.md#r-117--ldo-stability-and-output-capacitor-esr), [R-118](../../reference/research-log.md#r-118--pole-zero-analysis-and-s-domain-models-in-ngspice), [R-127](../../reference/research-log.md#r-127--bodes-gainphase-work) and [R-134](../../reference/research-log.md#r-134--rf-filters-and-bands) reused. Converter and codec parts are revised and replaced, and the 802.3ck values come from a draft configuration rather than the published standard; check those entries once a year, and treat each as an example of its class rather than a recommendation.
