# CS-02 · Validation Time Sets the Schedule: Sapphire Rapids

| | |
|---|---|
| **Decision** | Add platform and product validation time before releasing a complex server processor to production, twice |
| **Company and date** | Intel, July 2021 and June 2022 |
| **Domain** | [Digital logic and CPUs](../playbooks/digital-cpu.md), [packaging and reliability](../playbooks/packaging.md) |
| **Sources** | [R-647] in the [research log](../../reference/research-log.md) |

## What was decided

**July 2021.** Intel said: "Given the breadth of enhancements in Sapphire Rapids, we are incorporating additional validation time prior to the production release." It moved production to the first quarter of 2022, with the ramp in the second.

**June 2022.** Intel said it was "building in more platform and product validation time", so the ramp would come later in the year than first forecast [R-647] **[Established for the statements as reported]**.

The later production steppings carry letter-number names in Intel's specification update (for example E-5 for the largest die) [R-647]. A press report of hundreds of bugs and a dozen steppings was not confirmed by Intel and is not used here.

## The engineering behind it

- **What "more validation" means.** Post-silicon validation finds bugs that pre-silicon verification missed: corner cases at speed, platform interactions, electrical margins ([25-12](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-12-post-silicon-validation.md)).
- **Each fix that needs new silicon costs a stepping.** That means new masks for the affected layers, weeks of fabrication, and repeated validation.
- **Integration multiplies the work.** A product that integrates many new features at once (new cores, accelerators, memory types, interconnects) multiplies the states to validate. Verification effort grows faster than design size ([19-13](../../courses/19-digital-vlsi-design/chapters/19-13-verification-methods.md)).
- **The schedule arithmetic.** Each extra stepping adds a fabrication cycle plus re-validation, and the delay costs gross profit for every month the market window is shortened ([26-05](../../courses/26-engineering-design-and-professional-practice/chapters/26-05-schedule-and-respin-risk.md); [28-09](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-09-business-engineering-translation.md)).

## What a diligence team should have asked

1. What fraction of the validation plan has run, on how many units, at which corners?
2. What is the open-bug trend, by severity, and is it flattening ([28-03](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-03-silicon-maturity-scales.md))?
3. How many more steppings does the plan assume, and what does each cost in time?
4. Which new features could be fused off if they hold up the release?

## Lessons that transfer

- **"Taped out" and "first silicon works" are early levels on the maturity scale.** Production readiness is decided by validation completeness ([28-03](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-03-silicon-maturity-scales.md)).
- **Plan for at least one stepping beyond the base case.** The base rates in [26-05](../../courses/26-engineering-design-and-professional-practice/chapters/26-05-schedule-and-respin-risk.md) say most complex projects need one or more.
