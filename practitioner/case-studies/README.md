# Case Studies

Real engineering decisions reconstructed from public sources. Each one states the decision, explains the physics and economics behind it with links to the chapters that derive them, records what happened (dated, cited to the [research log](../../reference/research-log.md) and tagged), and lists what a diligence team should have asked. Quotations are from the cited public documents; inferences are labelled as ours.

| Case | Decision | Domain |
|---|---|---|
| [CS-01](cs-01-blackwell-two-die-package.md) | Going past the reticle: a two-die GPU on a bridge-based package, and its 2024 yield respin | Packaging, AI accelerators |
| [CS-02](cs-02-validation-time.md) | Validation time sets the schedule: a server processor's two delays | Digital, reliability |
| [CS-03](cs-03-foundry-exit.md) | When the foundry leaves: GaN production ending at TSMC | Power, manufacturing |
| [CS-04](cs-04-scale-up-domain.md) | How big should one domain be? NVLink-72 against a 9,216-chip ICI pod | AI accelerators, interconnect |
| [CS-05](cs-05-designing-for-failure.md) | Designing for failure at 16,000 GPUs: Llama 3 pre-training | AI accelerators, reliability |
| [CS-06](cs-06-rack-voltage.md) | Changing the rack's voltage: from 54 V to 800 VDC | Power |
| [CS-07](cs-07-modem-build-vs-buy.md) | Build versus buy: Apple's first modems | RF and wireless |
| [CS-08](cs-08-custom-accelerators.md) | Building your own accelerator: the hyperscalers' custom silicon | AI accelerators |
| [CS-09](cs-09-mixed-node-chiplets.md) | Mixed-node chiplets: compute on 3 nm, the rest on 6 nm | Packaging, AI accelerators |
| [CS-10](cs-10-subthreshold-bet.md) | Betting on subthreshold: an MCU platform below threshold voltage | Embedded |
| [CS-11](cs-11-headline-vs-table.md) | The headline and the table: choosing a PPG front end from its data sheet | Embedded, analog |

**Using them.** Read the decision and stop. Write down what you would have asked and which first-principles check you would have run, using the domain's [playbook](../playbooks/README.md). Then read the rest.

All facts are as of the dates stated in each case and in the research log; re-check perishable ones before reusing them.
