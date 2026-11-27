# Capstone C3 · Embedded and System Design: a Wearable Sensor Node

**Brief.** Design, on paper and in simulation, a skin-worn patch that measures heart rate (photoplethysmography, PPG) and activity (an accelerometer) continuously, and reports to a phone over Bluetooth LE once a second. It must last a week on a small rechargeable cell. Choose the parts, budget the power and the radio link, model the battery life, design the firmware, and say what would break first.

| | |
|---|---|
| **Prerequisites** | [Course 18](../../courses/18-embedded-systems-and-microcontrollers/README.md) (embedded systems), [Course 21](../../courses/21-rf-and-microwave-engineering/README.md) (link budgets), [Course 22](../../courses/22-power-electronics-and-energy-conversion/README.md) (power and batteries); [27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md) is the closest worked system |
| **Estimated hours** | About 35 |
| **Tools** | Python with numpy (budget model and simulation); a C compiler (firmware modules with host tests); no hardware required |
| **Deliverables** | Requirements, power budget, part selection, BLE link budget, battery-life model, firmware architecture with one tested module, risk list |

---

## Requirements

| # | Requirement | Verification |
|---|---|---|
| R1 | PPG sampled continuously at 25 Hz; accelerometer at 25 Hz | Design review |
| R2 | One notification per second to the phone (heart rate, steps, battery, flags); every PPG sample reflected in a notification sent within 2 s of the sample | Firmware timing analysis |
| R3 | At least 7 days of continuous operation on a 60 mAh lithium-polymer cell, using at most 80% of its capacity | Budget and simulation |
| R4 | Uplink margin of at least 10 dB at 5 m to a phone whose receiver reaches −90 dBm, through 10 dB of body loss with a −10 dBi tag antenna | Link budget |
| R5 | No PPG samples lost while the processing task runs once a second; any loss is counted and reported | Firmware test |
| R6 | A charging path and a storage (ship) mode | Part selection |

The −90 dBm phone, the 10 dB body loss and the −10 dBi antenna are this brief's assumptions; your report should test how much the conclusions depend on them. Use only public data-sheet values, cite each one, and mark every assumption as an assumption.

## Milestones

| # | Milestone | Output | Hours |
|---|---|---|---|
| M1 | **Requirements and architecture.** Refine the table; draw the block diagram; decide what runs where | One page and a diagram | 4 |
| M2 | **Part selection.** Compare at least three radio SoCs and justify the sensors and PMIC, with cited values | Comparison table | 6 |
| M3 | **Power budget and battery life.** Every load at the supply voltage its data sheet specifies, with its duty cycle; the life; a sensitivity study that finds what dominates. If the budget does not close, quantify the gap and propose the smallest change, with its cost | Budget model (script), sensitivity table | 8 |
| M4 | **Link budget.** Both directions, with margins, and the range at the required margin | Link table | 4 |
| M5 | **Firmware architecture.** States, interrupts, task timing, buffering; implement and test one module on the host | Diagram, module, host test | 8 |
| M6 | **Report and risks.** Results against every requirement; the five largest risks with mitigations | Report of 8 to 12 pages | 5 |

## Rubric (100 points)

| Criterion | Points | Full credit |
|---|---|---|
| Requirements and architecture | 10 | Every requirement testable; partitioning justified |
| Part selection | 15 | Cited values, compared on the quantities that matter for this product, not on headline figures |
| Power budget | 25 | Every load and duty cycle; regulator efficiency included; the dominant term identified; sensitivity study; an honest verdict against R3, with a change request if it fails |
| Link budget | 15 | Both directions; assumptions stated; range at margin |
| Firmware | 20 | States, interrupts and buffering consistent with the budget; a module with a self-checking test |
| Report and risks | 15 | Results against every requirement; risks ranked, each with a mitigation and a test |

## Running the reference

In [reference/](reference/):

```bash
python budget.py
```

```bash
python energy_sim.py
```

`budget.py` prints the power budget, battery life and link margins; `energy_sim.py` checks them event by event and through a discharge. The firmware test, [reference/firmware/fw_test.c](reference/firmware/fw_test.c), runs in `tools/run_c.py`; the report's numbers are checked by `tools/run_verify.py C3`.

**Reference solution:** [design report](reference/design-report.md). Open it only after your own design is complete, or when you are stuck at a milestone.
