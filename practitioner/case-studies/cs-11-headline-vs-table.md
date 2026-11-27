# CS-11 · The Headline and the Table: Choosing a PPG Front End

| | |
|---|---|
| **Decision** | Select an optical heart-rate front end for a week-long wearable from its data sheet |
| **Source of the case** | This curriculum's [Capstone C3](../../capstones/C3-wearable-sensor-node/reference/design-report.md), using TI's public AFE4404 and CC2340R5 data sheets |
| **Domain** | [Embedded and low-power systems](../playbooks/embedded.md), [analog](../playbooks/analog-mixed-signal.md) |
| **Sources** | [R-311], [R-702] in the [research log](../../reference/research-log.md) |

## What the data sheet says

**The feature list.** The AFE4404 promises "Average Current Less Than 200 μA for PPG Signal Acquisition", without conditions [R-702].

**The electrical table.** It gives 300 µA on the receiver supply in dynamic power-down, at a 100 Hz pulse repetition frequency with the receiver active for 10% of the period, at 3 V. The table adds 20 µA on the interface supply and 5 µA on the LED driver supply. The receiver supply must be between 2.0 and 3.6 V [R-702] **[Established as data-sheet values]**.

**The radio SoC's table.** It specifies its currents at VDDS = 3.0 V with its internal DC/DC on [R-702].

## What happened in the design

- **The first budget.** The reference design's first budget put the front end on a 1.8 V rail and the SoC currents on the same rail. It appeared to meet the 7-day target on a 60 mAh cell.
- **Reading the conditions.** The front end cannot run at 1.8 V, and the SoC's currents apply at 3.0 V.
- **The corrected budget.** With both corrected, the life fell to 5.31 days against a 7-day requirement. The front end's receiver and interface alone exceed the 7-day current allowance ([C3 §3.4](../../capstones/C3-wearable-sensor-node/reference/design-report.md)).
- **The headline doesn't save it either.** At the feature list's 200 µA, the design still reaches only 6.97 days.

## The engineering behind it

- **A current means nothing without its voltage.** Through a switching (buck) regulator, a load's draw from the battery depends on the power it takes, at the voltage it is specified at, divided by the regulator efficiency; through a linear regulator, the battery supplies the load current itself, whatever the rail voltage ([22-01](../../courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md)). Moving a load to a lower rail helps only if the part works there and its current does not rise.
- **Dynamic power-down helps less than its name suggests.** The receiver's "power-down" current is a large fraction of its always-on current. Fitting a straight line between the table's two rows suggests a high floor (an inference shown in C3 §3.4). Lowering the pulse rate therefore helps less than intuition suggests.
- **In an optical wearable, the optics dominate.** The radio was about 1.5% of the budget and the optical chain about 91% (C3 §3.2).

## What a diligence team should ask a wearable or sensor company

1. At what voltage and conditions are your component currents specified? Do your products run at those conditions?
2. What fraction of your battery budget is each block? Where was it measured, and on which firmware?
3. What did your power budget predict before the first board, and what did the board measure?

## Lessons that transfer

- **Read the electrical table, not the feature list.** Check its conditions against the product's.
- **A design that fails its requirement honestly is worth more than one closed by assumption.** C3 ends in a change request, not in a tuned number. Look for that habit in a team's own reports ([28-07](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-07-evaluating-engineering-teams.md)).
