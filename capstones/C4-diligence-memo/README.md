# Capstone C4 · Practitioner: a Technical Diligence Memo on a Public Chip Product

**Brief.** Write the memo an investment committee would read before backing a thesis that depends on one chip product: what it is, whether its headline claims hold, where its advantage really comes from, what could erode it, and what you would ask its management. Use only public information. Show your arithmetic, so a skeptical engineer can check every number.

| | |
|---|---|
| **Prerequisites** | [Course 28](../../courses/28-technical-diligence-and-leadership-fluency/README.md) (the evaluation framework, claim validation, maturity, red flags, questions), with the course that covers your product: [Course 27](../../courses/27-system-architectures/README.md) for system context, and Courses 18 to 25 for the technology |
| **Estimated hours** | About 35 |
| **Tools** | A spreadsheet or Python for the arithmetic; the [research log](../../reference/research-log.md) format for sources |
| **Deliverables** | A memo of 8 to 12 pages, a source log, and a script or workbook that recomputes every derived number |

---

## Choosing the product

Pick a product with enough public technical material to test claims against physics: a data sheet or specification table, at least one independent source, and a competitor with public specifications. These work well with what this curriculum has already logged:

| Product | Good for | Starting points |
|---|---|---|
| NVIDIA GB200 NVL72 (the reference) | Peak against delivered, sparse against dense, scale-up domains, facility power | [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md); R-690, R-460, R-694 |
| AMD Instinct MI355X or Google Ironwood | The same questions from the challenger's side | R-692, R-693 |
| A GaN power-IC supplier's AI-server PSU | Power-density claims, foundry dependence | [22-10](../../courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md); R-423 (server PSUs), R-432 (GaN foundry exit) |
| A low-power BLE SoC or MCU | Data-sheet conditions, headline against operating point | [Capstone C3](../C3-wearable-sensor-node/README.md); R-310, R-702 |

## Rules

1. **Public information only.** Use data sheets, filings, standards, papers, product pages, and named trade press. Nothing confidential about any employer, including your own.
2. **Date and cite everything perishable.** Mark each fact "as of Mon YYYY" and log it with an ID. Tag every claim **[Established]**, **[Industry estimate]** or **[Contested]**, and when sources disagree, show the range and why.
3. **Never invent a number.** If a figure you need is not public, say so and treat it as an assumption to test, labelled as one.
4. **Show the arithmetic.** Every derived number must be reproducible from the cited inputs by your script.
5. **Separate the claim from its operating point.** For every headline claim, record the conditions it was measured under before judging it.

## Memo structure

1. **Bottom line** (half a page): the verdict on each claim, where the advantage lies, the top risks, and a recommendation.
2. **What the product is:** the specification table, with derived per-unit figures.
3. **Claim validation:**
   - internal consistency;
   - conventions (dense or sparse, typical or maximum, conditions);
   - a decomposition of each headline claim into physical ratios;
   - a first-principles model of the claim's operating point.
4. **Competitive position:** like-for-like comparison, stating where the figures are not like-for-like.
5. **Facility, reliability, supply and regulation:** whatever sits outside the chip and could stop deployment.
6. **Roadmap and useful life.**
7. **Scorecard:** the seven dimensions of [28-01](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-01-technology-evaluation-framework.md), with weights, scores, uncertainties, both totals, the variance contributions, and the gates.
8. **Questions for management:** five or six, each with what a strong and an evasive answer would look like.
9. **What would change your view**, up and down.

## Milestones

| # | Milestone | Output | Hours |
|---|---|---|---|
| M1 | **Frame the decision.** Whose thesis depends on this product, and what must be true | Half a page | 2 |
| M2 | **Collect and log sources.** Specifications, claims with their footnotes, competitors, independent data | Source log with IDs and tags | 8 |
| M3 | **Validate the claims.** Consistency, conventions, decomposition, a first-principles model | Script and §3 of the memo | 10 |
| M4 | **Position and risks.** Competitors, facility, reliability, supply, regulation, roadmap | §4 to §6 | 7 |
| M5 | **Score and question.** Scorecard with uncertainty; questions with strong and evasive answers | §7 and §8 | 4 |
| M6 | **Write the bottom line.** Then cut the memo to 12 pages | Final memo | 4 |

## Rubric (100 points)

| Criterion | Points | Full credit |
|---|---|---|
| Sourcing and tagging | 15 | Every perishable fact dated, cited and tagged; disagreements shown as ranges; no invented numbers |
| Claim validation | 30 | Each headline claim separated from its operating point, decomposed into physical ratios, and tested with a model; conventions resolved |
| Competitive and risk analysis | 20 | Like-for-like comparison with its limits stated; facility, reliability, supply and regulation each assessed with numbers where public |
| Scorecard | 10 | Weights fit the decision; uncertainty and gates included; the largest variance contribution identified and acted on |
| Questions for management | 10 | Specific, answerable, each with strong and evasive answers |
| Clarity and reproducibility | 15 | A bottom line a committee can act on; every number reproduced by the script |

## Running the reference

In [reference/](reference/):

```bash
python claims.py
```

`claims.py` holds the logged inputs and the serving model; `tools/run_verify.py C4` checks every number in the memo against it.

**Reference solution:** [memo on the NVIDIA GB200 NVL72](reference/memo.md). Read it only after drafting your own memo, or when you are stuck at a milestone. Choose a different product if you can, and use the reference for its method.
