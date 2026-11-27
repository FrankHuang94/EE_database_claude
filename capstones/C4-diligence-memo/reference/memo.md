# C4 Reference · Technical Diligence Memo: NVIDIA GB200 NVL72

**To:** Investment committee · **From:** Technical diligence · **Date:** 27 Nov 2026 · **Basis:** public information only, as logged in the [research log](../../../reference/research-log.md); every perishable fact is dated "as of Nov 2026"

This is the reference solution to [Capstone C4](../README.md). The arithmetic is in [claims.py](claims.py), and [verify_c4.py](verify_c4.py) recomputes every number below from the logged inputs.

**Tags.** Claims are tagged **[Established]**, **[Industry estimate]** or **[Contested]**, as in [28-02](../../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-02-validating-claims.md). The scorecard follows [28-01](../../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-01-technology-evaluation-framework.md).

**The question.** Several theses in the portfolio depend on whether this rack is, and will stay, the reference platform for serving large models. That holds whether we hold suppliers, customers or competitors of it. This memo asks four things:

- Are its headline claims real?
- Where does its advantage actually come from?
- What could erode it?
- What would we ask management?

---

## 1. Bottom line

1. **The "30× inference vs H100" claim is true only at the operating point stated in its footnote.** It is not a general speed-up.
   - Per GPU, the hardware improves memory bandwidth **2.39×** and dense low-precision compute **2.5×** at equal precision. Moving from FP8 to FP4 adds a further 2× on bandwidth-bound decoding.
   - A first-principles serving model gives about **3.0×** per GPU for a model that fits in one 8-GPU H100 server. The ratio rises past **10.5×** once the model no longer fits.
   - The rest of the 30× comes from H100 servers being "scaled over InfiniBand" at a 50 ms per-token deadline.
2. **The chip is not the moat. The 72-GPU NVLink domain is.**
   - Per GPU, AMD's MI355X matches the bandwidth (8 TB/s) and the dense FP8 and FP4 rates, and has **1.55×** the memory.
   - What no logged competitor matches is 72 GPUs sharing 1.8 TB/s each of NVLink, **36×** a 400 Gb/s network port (one per GPU, our assumption).
3. **The specification table needs care.** Its FP8 and BF16 rows are sparse figures, printed as single numbers next to an NVFP4 row that shows both. Read as dense, they overstate compute **2×**.
4. **Most of the risk is in the facility and the supply chain, not in the silicon.**
   - **Power and cooling.** A rack draws 120 to 132 kW and needs liquid cooling, with up to 192 kW provisioned.
   - **Reliability.** An H100-like failure rate gives about **7.3** GPU-related interruptions per rack per year. Each one can stall a 72-GPU domain.
   - **Packaging.** It depends on a single packaging route, and the mask was respun for yield in 2024.
   - **Short life.** A one-year product cadence shortens its useful life as the leading platform.
5. **Scorecard:** **4.10** of 5 (arithmetic), **4.04** (geometric). Manufacturing and supply contributes the most uncertainty (§7).

**Recommendation.** Underwrite the platform's lead in large-model inference through its successors. Do not underwrite "30×" for any customer whose models fit in an 8-GPU server. Make facility readiness (power, liquid cooling, the 800 VDC transition) an explicit diligence item for every thesis that depends on deployment volume.

## 2. What the product is

All rack figures are from NVIDIA's product page [R-690] **[Established as manufacturer claims]**.

| Item | Rack (72 GPUs, 36 CPUs) | Per GPU (derived) |
|---|---|---|
| HBM3E capacity | 13.4 TB | **186** GB |
| HBM bandwidth | 576 TB/s | **8.00** TB/s |
| NVLink bandwidth | 130 TB/s | **1.81** TB/s (NVIDIA states 1.8) |
| NVFP4 Tensor Core | 1,440 \| 720 PFLOPS | **20** \| **10** PFLOPS |
| FP8/FP6 Tensor Core | 720 PFLOPS | **10** PFLOPS |
| FP16/BF16 Tensor Core | 360 PFLOPS | **5** PFLOPS |
| Grace CPU cores | 2,592 Arm Neoverse V2 | **72** per CPU |

**The package.** Each GPU joins two near-reticle dies with a 10 TB/s die-to-die link, about 208 billion transistors in all, on TSMC's custom 4NP process [R-149]. A teardown found eight HBM3E stacks on TSMC's CoWoS-L, NVIDIA's first bridge-based 2.5D package [R-586] **[Established]**.

**Power.** NVIDIA gives Blackwell's maximum GPU power as "up to 1,200 W" [R-460]; a per-GPU figure for the GB200 rack itself was not found (R-596) **[Contested for GB200]**. The rack is liquid-cooled [R-690].

## 3. Validating the claims

### 3.1 Is the table self-consistent?

Mostly, yes. The rack's capacity and bandwidth divide to per-GPU figures that match the superchip column: 372 GB and 16 TB/s for two GPUs. The 1.81 TB/s of NVLink matches the stated 1.8 TB/s [R-690].

The capacity agrees less well across products: **186** GB per GPU here, 180 GB in the DGX B200 and 192 GB in NVIDIA's own per-GPU table [R-221, R-460] **[Contested: configuration-dependent]**. A buyer sizing models should use the figure for the configuration actually being bought.

### 3.2 Which rows are dense?

The footnote that defines the Tensor Core rows was read on 20 Nov 2026 as "Dense is one-half sparse spec shown" [R-221]. It did not appear in a reading on 26 Nov [R-690]. NVIDIA's per-GPU table settles the question:

- **NVFP4** is 10 dense and 20 sparse [R-460]. That matches the rack's 720 and 1,440 divided by 72, so the NVFP4 row shows both.
- **FP8** is 5 PFLOPS dense per GPU [R-460]. The rack's single 720 PFLOPS divides to 10, so it is the sparse figure.
- **BF16** is printed as 360 PFLOPS for the rack, 5 per GPU: half the FP8 figure, the same ratio as between the dense FP8 and FP4 rates. By the footnote's rule [R-221] it is sparse too, and the dense rate is **2.5** PFLOPS per GPU. That last figure is our halving; the logged per-GPU table gives no BF16 row.

Taken as dense, the FP8 and BF16 rows overstate compute **2×**. Comparing them with a competitor's dense figures is the most common error in reading this table [28-02 §9] **[Established for the arithmetic; Contested for the missing footnote]**.

### 3.3 Decomposing "30× inference vs H100"

The claim: "LLM Inference 30x vs. NVIDIA H100 GPU". The footnote sets the operating point: 50 ms between tokens, 5 s to the first token, 32,768 input and 1,024 output tokens, and "NVIDIA HGX™ H100 scaled over InfiniBand (IB) vs. GB200 NVL72" [R-690] **[Established as a vendor-measured claim]**.

**What the hardware gives per GPU:**

| Ratio, GB200 GPU to H100 | Value | Basis |
|---|---|---|
| HBM bandwidth | **2.39×** | 8.0 against 3.35 TB/s [R-460] |
| HBM capacity | **2.33×** | 186 against 80 GB |
| Dense FP8 | **2.5×** | 5 against 2 PFLOPS [R-460] |
| Dense NVFP4 against H100's dense FP8 | **5.0×** | 10 against 2 PFLOPS: a change of precision as well as of hardware |
| NVLink per GPU | **2.0×** | 1.8 against 0.9 TB/s [R-521] |
| GPUs in one NVLink domain | **9×** | 72 against 8 |
| Maximum GPU power | **1.71×** | 1,200 against 700 W [R-460] |

**The ceiling for bandwidth-bound decoding.** Generating each token reads the weights and the KV cache once, so a step is limited by memory bandwidth. Bandwidth gives 2.39×. Halving the bytes per weight (FP4 against FP8) gives a further **2**×. Together that is a ceiling of about **4.78×** for decoding a model that fits in both systems.

To reach 30×, the operating point must supply the remaining **6.28×**.

**A first-principles serving model.** [claims.py](claims.py) assumes each decode step reads all weights $W$ and each sequence's KV cache $K$ once. With batch $B$ in a domain of $G$ GPUs, the step takes $t = (W + BK)/(G\,BW)$. The batch is the largest that meets both limits:

- the latency limit, $t \le$ 50 ms;
- the capacity limit, $W + BK \le G\,C$.

Two hypothetical models show the mechanism. Their sizes are ours; the footnote as logged names no model. Both use FP8 weights on H100 and FP4 on GB200, with 1 GB of FP8 KV cache per 32k-token sequence on both.

| Hypothetical model | H100 | GB200 NVL72 | Ratio per GPU |
|---|---|---|---|
| A: 140 GB of FP8 weights (fits one 8-GPU server) | **2,617** tokens/s per GPU (batch **500**, capacity-limited) | **7,958** tokens/s per GPU (batch **13,330**) | **3.04×** |
| B: 1 TB of FP8 weights (needs two H100 servers) | **733** tokens/s per GPU on 16 GPUs, *ignoring the network between them* | **7,701** tokens/s per GPU | **10.5×** at least |

**Case A.** When the model fits, the ratio is about 3×, close to the capacity and bandwidth ratios.

**Case B.** When it does not fit, the H100 must split the model across servers. Each GPU's link to the other server is then a network port of about 50 GB/s against 1.8 TB/s of NVLink, **36×** less. The 10.5× already ignores that penalty, which can only widen the gap.

**What this means.** Every pass at the footnote's 50 ms deadline puts the slow link on the critical path. Large models, tight interactivity and long contexts are where the 72-GPU domain pays most, and the claim was measured exactly there.

**Verdict on the inference claim: plausible at its operating point; not transferable.** For a customer whose models fit an 8-GPU server, plan on about **3×** per GPU, and check accuracy at FP4 before counting the precision gain. For frontier-scale models served interactively, an order of magnitude or more is credible.

### 3.4 The energy and training claims

**The energy claim.** NVIDIA claims "Energy Efficiency 25x vs. H100" at the same operating point [R-690]. Thirty times the throughput at 25 times the energy efficiency implies that power per GPU rose only **1.2×**. Yet the GPU's maximum power rose 1.71×, and the GB200 rack spends **1.67** to **1.83** kW per GPU all-in.

The two claims are consistent only if the H100 side carried a large per-GPU overhead: CPUs, network switches, and many more servers at that operating point. That is plausible, but the power counted on each side is not disclosed. **[Contested: definition of power not stated.]**

**The training claim.** NVIDIA claims "LLM Training 4x vs. H100" [R-690]. Dense FP8 gives 2.5×, so the claim needs a further **1.6×** from the system. A shorter communication critical path inside one NVLink domain could supply that, but it is unverified.

For context, Meta's Llama 3 405B training on up to 16,384 H100s reached 38–43% of the BF16 peak [R-694] **[Established]**. Delivered utilization, not peak, is what a buyer should ask about.

## 4. Where the advantage lies: the competitive position

| Per accelerator (as of Nov 2026) | NVIDIA GB200 GPU | AMD MI355X | Google Ironwood |
|---|---|---|---|
| HBM capacity | 186 GB | 288 GB | 192 GB |
| HBM bandwidth | 8.0 TB/s | 8 TB/s | 7.37 TB/s |
| Dense FP8 | 5 PFLOPS | 5 PFLOPS | 4.614 PFLOPS (peak FP8) |
| Dense 4-bit | 10 PFLOPS (NVFP4) | 10.1 PFLOPS (MXFP4; no sparse figure listed) | — |
| Power | up to 1,200 W (GPU) | 1,400 W (typical board power) | about 1.09 kW all-in (pod ÷ chips) |
| Scale-up domain | 72 GPUs, 1.8 TB/s each | 7 links of 144 GB/s, **1,008** GB/s in all | 9,216 chips, 1.2 TB/s ICI each |
| FP8 FLOPs per byte of HBM | **625** | **625** | **626** |

Sources: [R-460], [R-690], [R-692], [R-693] **[Established as manufacturer specifications; power definitions differ, so the power row is not like-for-like]**.

**Three conclusions.**

1. **The chips have converged.** Compute per byte of bandwidth is essentially identical across all three, and H100 sat at **597**. These are balanced designs aimed at the same workloads. The MI355X carries **1.55×** the memory per GPU, which matters for KV-cache-heavy serving.
2. **Domain size and bandwidth differentiate.**
   - **NVL72:** a 72-GPU domain at 1.8 TB/s per GPU.
   - **MI355X:** seven links, consistent with an eight-GPU fully connected server (our inference from the link count).
   - **Ironwood:** a much larger ICI domain of 9,216 chips, at **0.67** times NVLink's per-chip bandwidth (both figures bidirectional).
3. **Capacity in one domain decides what fits.** At 4-bit, 13.4 TB holds the weights of a model of about **26.8** trillion parameters, before the KV cache. An eight-GPU MI355X server holds **4.61** trillion, and an eight-GPU H100 server holds **640** billion at FP8.

**Software.** NVIDIA's CUDA stack and its libraries are the incumbent ecosystem. This memo has no logged metric for its advantage, so it is scored on judgment (§7) with a wide uncertainty.

## 5. Facility, reliability and supply

### 5.1 Power and cooling

| Figure | Value | Source |
|---|---|---|
| Rack power, NVIDIA | about 120 kW | [R-444] |
| Rack power, HPE nominal | 132 kW | [R-098] |
| Busway provisioned (HPE) | about 192 kW, **1.45×** nominal | [R-098] |
| All-in power per GPU | **1.67** to **1.83** kW | derived |
| Above the GPU's own 1,200 W | **0.47** to **0.63** kW per GPU, **39** to **53**% | derived |
| Energy per rack-year at 132 kW | **1,156** MWh | derived |

**[Contested: 120–142 kW depending on definition, R-098.]** A rack at this density needs liquid cooling and in-rack power shelves at about 50 V [R-444].

NVIDIA has announced a move to 800 VDC "starting in 2027" for megawatt racks [R-691]. Facilities built today for 54 V distribution therefore face a retrofit decision within one product generation **[Established as announced]**.

### 5.2 Reliability and blast radius

Meta's training run gives the only logged failure data at this scale [R-694] **[Established as reported]**:

- 419 unexpected interruptions in 54 days on up to 16,384 H100s;
- 58.7% of them caused by GPUs, about **246**.

**Per GPU.** That is at least **0.102** GPU-related interruptions per GPU-year. "Up to" makes this a lower bound.

**Per rack.** Applied to 72 GPUs, it is **7.3** per rack-year, one every **50** days. Blackwell's rate may differ, so the H100 rate is an assumption.

**The blast radius.** In an eight-GPU server a fault stalls 8 GPUs. In a 72-GPU NVLink domain, a job spanning the domain stalls 72, **9×** as many GPU-hours per fault for the same recovery time. How spares, checkpoints and domain reconfiguration contain this is the most important operational question for anyone renting or operating these racks (§8, question 4).

### 5.3 Manufacturing and supply

**The 2024 yield problem.** In August 2024 NVIDIA "executed a change to the Blackwell GPU [mask] to improve production yields", with "inventory provisions for low-yielding Blackwell material" and, per the CEO, "no functional changes" [R-646] **[Established: management statements]**. A yield problem on near-reticle dies in a new bridge-based package has already happened once and been fixed. It is the kind of risk that recurs at each generation (28-03).

**Concentration.** The package depends on TSMC's CoWoS-L and on HBM3E supply; the teardown found SK hynix stacks [R-586]. This memo has no logged capacity allocations. Packaging and HBM allocation are therefore the largest unknowns, which the scorecard reflects (§7).

### 5.4 Export controls

**Total processing performance.** TPP counts 2 × MacTOPS × bit length [R-659]. The dense FP4 rate (10 PFLOPS, **5,000** MacTOPS at 4 bits) gives **40,000**, and dense FP8 gives the same **40,000**. That is **8.3×** the 4,800 threshold of ECCN 3A090.a.1.

**What it means.** Sales into restricted destinations need licenses, so the addressable market is policy-dependent. A thesis built on sales to a restricted destination fails this gate. One question is open: whether a sparse rate counts toward TPP (open issue 80) **[Established for the threshold; not legal advice]**.

## 6. The roadmap and the useful life

| Successor (as of Nov 2026) | Change against GB200 | Source |
|---|---|---|
| GB300 NVL72 (Blackwell Ultra) | Dense FP4 **15** PFLOPS per GPU (1,080 ÷ 72), **1.5×**; HBM 288 GB per GPU, **1.55×** | [R-460, R-690] |
| Vera Rubin NVL72 (projected) | HBM4 at 19.2 TB/s per GPU, **2.4×**; NVFP4 inference 50 PFLOPS sparse, **2.5×** | [R-460, R-040] |

**The cadence.** A new rack generation arrives about every year with roughly 1.5× to 2.5× the per-GPU capability **[Established as published; Rubin figures vendor-projected]**.

**What it means for each kind of holder.**

- **Investors in GB200 capacity** (clouds, neoclouds) face fast economic obsolescence. A rack's competitive pricing power lasts about one generation.
- **Suppliers of NVL72-class components** benefit from the cadence. Their risk is the specification churn: 54 V to 800 VDC power, and HBM3E to HBM4.

## 7. Scorecard

**The decision being scored:** will the GB200 NVL72 class remain the reference platform for large-model inference through 2027? Scores are on the 1–5 scale of 28-01 and are this analyst's judgment, with $\sigma$ wide where the evidence is public statements only.

| Dimension | Weight | Score | σ | Evidence |
|---|---|---|---|---|
| Architecture | 0.20 | 4.5 | 0.5 | Balanced compute and bandwidth; a unique 72-GPU domain (§3–4) |
| Implementation | 0.15 | 4.0 | 0.5 | Shipping; one yield respin (§5.3) |
| IP position | 0.05 | 4.0 | 1.0 | No public evidence either way |
| Team | 0.05 | 4.0 | 1.0 | Annual cadence delivered; no public data on depth |
| Roadmap | 0.15 | 4.0 | 0.75 | Published successors; Rubin figures projected (§6) |
| Ecosystem and software | 0.20 | 5.0 | 0.5 | Incumbent stack; no logged metric |
| Manufacturing and supply | 0.20 | 3.0 | 0.75 | Single packaging route, HBM, facility readiness (§5) |

The totals:

| Quantity | Value |
|---|---|
| Weighted arithmetic score $S$ | **4.10** |
| Weighted geometric score $G$ | **4.04** |
| Standard deviation of $S$ (independent errors) | **0.26** |
| Share of the variance from manufacturing and supply | **34**% |
| Share of the variance from the roadmap | **19**% |

The geometric score is lower because supply is the weak dimension (28-01 §3.2). Supply also dominates the uncertainty, so diligence effort should go there next: packaging and HBM allocations, and facility readiness at the customers that matter to the thesis.

**Gates.** IP and the supply path pass on public evidence. Export controls pass for permitted destinations and fail for restricted ones (§5.4).

## 8. Questions for management

Each question comes with the answer that should reassure (strong) and the one that should not (evasive).

**1. Show the throughput-against-interactivity curve, not one point. At what model size and latency does the ratio to H100 fall below 5×?**

- *Strong:* curves for several model sizes, including ones that fit an 8-GPU server.
- *Evasive:* repeating "30×".

**2. Which rows of the specification table are sparse, and where is the footnote?**

- *Strong:* row-by-row dense and sparse figures.
- *Evasive:* "industry-standard convention".

**3. What power was counted on each side of the 25× efficiency claim?**

- *Strong:* wall power of the whole system, both sides, at the same utilization.
- *Evasive:* GPU power on one side only.

**4. What happens to a job when one GPU in a 72-GPU domain fails, and how long until it runs again?**

- *Strong:* spare GPUs or domain reconfiguration, measured restart times and fleet failure rates.
- *Evasive:* "Blackwell is more reliable" with no rates.

**5. What accuracy do customers keep at NVFP4 against FP8 on their own models?**

- *Strong:* per-model accuracy deltas and where FP4 is not used.
- *Evasive:* only throughput.

**6. What share of announced deployments needed facility work (liquid cooling, 130 kW racks, busways), and how does the 800 VDC transition affect sites built today?**

- *Strong:* a site-readiness breakdown.
- *Evasive:* "our partners handle it".

## 9. What would change this view

- **Upward:** measured fleet failure rates with a small blast radius; published accuracy at FP4 matching FP8; disclosed packaging and HBM allocations covering demand.
- **Downward:**
  - a competitor shipping a scale-up domain of comparable size and per-GPU bandwidth, since that is the actual moat;
  - facility constraints capping deployment below demand;
  - a second yield event at the next generation.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| C.bw | bandwidth ratio to H100 | 2.39 | — |
| C.fp8 | dense FP8 ratio to H100 | 2.5 | — |
| C.serveA | per-GPU ratio, model A | 3.0 | — |
| C.serveB | per-GPU ratio, model B (at least) | 10.5 | — |
| C.mi355cap | MI355X memory over a GB200 GPU | 1.55 | — |
| C.port | NVLink over a 400 Gb/s port | 36 | — |
| C.sparse | overstatement if sparse rows read as dense | 2 | — |
| C.rackyr | GPU-related interruptions per rack-year | 7.3 | — |
| C.S | weighted arithmetic score | 4.10 | — |
| C.G | weighted geometric score | 4.04 | — |
| P.hbm | HBM per GPU | 186 | GB |
| P.bw | HBM bandwidth per GPU | 8.00 | TB/s |
| P.nvl | NVLink per GPU | 1.81 | TB/s |
| P.fp4s | NVFP4 sparse per GPU | 20 | PFLOPS |
| P.fp4d | NVFP4 dense per GPU | 10 | PFLOPS |
| P.fp8 | FP8 table figure per GPU | 10 | PFLOPS |
| P.bf16 | BF16 table figure per GPU | 5 | PFLOPS |
| P.cores | cores per Grace CPU | 72 | — |
| V.cap | HBM per GPU (consistency check) | 186 | GB |
| V.bf16 | dense BF16 per GPU | 2.5 | PFLOPS |
| H.bw | bandwidth ratio | 2.39 | — |
| H.cap | capacity ratio | 2.33 | — |
| H.fp8 | dense FP8 ratio | 2.5 | — |
| H.fp4 | dense NVFP4 over H100 dense FP8 | 5.0 | — |
| H.nvl | NVLink ratio | 2.0 | — |
| H.dom | domain-size ratio | 9 | — |
| H.tgp | GPU power ratio | 1.71 | — |
| H.bytes | weight bytes, FP8 over FP4 | 2 | — |
| H.ceil | decode ceiling at FP4 | 4.78 | — |
| H.resid | factor left to the operating point | 6.28 | — |
| M.hA | H100 throughput, model A | 2617 | tokens/s per GPU |
| M.bA | H100 batch, model A | 500 | — |
| M.gA | NVL72 throughput, model A | 7958 | tokens/s per GPU |
| M.gbA | NVL72 batch, model A | 13330 | — |
| M.rA | ratio, model A | 3.04 | — |
| M.hB | H100 throughput, model B | 733 | tokens/s per GPU |
| M.gB | NVL72 throughput, model B | 7701 | tokens/s per GPU |
| M.rB | ratio, model B | 10.5 | — |
| M.port | NVLink over a network port | 36 | — |
| E.pw | implied per-GPU power ratio | 1.2 | — |
| E.lo | all-in power per GPU, 120 kW | 1.67 | kW |
| E.hi | all-in power per GPU, 132 kW | 1.83 | kW |
| E.train | factor left to the system, training | 1.6 | — |
| K.mi | MI355X scale-up bandwidth | 1008 | GB/s |
| K.rg | FLOPs per byte, GB200 GPU | 625 | FLOP/byte |
| K.rm | FLOPs per byte, MI355X | 625 | FLOP/byte |
| K.ri | FLOPs per byte, Ironwood | 626 | FLOP/byte |
| K.rh | FLOPs per byte, H100 | 597 | FLOP/byte |
| K.cap | MI355X memory ratio | 1.55 | — |
| K.ici | Ironwood ICI over NVLink per chip | 0.67 | — |
| K.fitr | parameters held by one rack at 4-bit | 26.8 | trillion |
| K.fitm | parameters held by eight MI355X at 4-bit | 4.61 | trillion |
| K.fith | parameters held by eight H100 at FP8 | 640 | billion |
| F.prov | provisioned over nominal power | 1.45 | — |
| F.lo | all-in power per GPU, low | 1.67 | kW |
| F.hi | all-in power per GPU, high | 1.83 | kW |
| F.olo | power above the GPU, low | 0.47 | kW |
| F.ohi | power above the GPU, high | 0.63 | kW |
| F.plo | power above the GPU, low | 39 | % |
| F.phi | power above the GPU, high | 53 | % |
| F.mwh | energy per rack-year | 1156 | MWh |
| R.gpu | GPU-related interruptions | 246 | — |
| R.rate | interruptions per GPU-year | 0.102 | — |
| R.rack | interruptions per rack-year | 7.3 | — |
| R.days | days between interruptions per rack | 50 | days |
| R.blast | blast-radius ratio | 9 | — |
| X.mac | MacTOPS at dense FP4 | 5000 | — |
| X.tpp | TPP from dense FP4 | 40000 | — |
| X.tpp8 | TPP from dense FP8 | 40000 | — |
| X.ratio | TPP over the threshold | 8.3 | — |
| D.fp4 | GB300 dense FP4 per GPU | 15 | PFLOPS |
| D.fp4r | GB300 dense FP4 ratio | 1.5 | — |
| D.mem | GB300 memory ratio | 1.55 | — |
| D.bw | Rubin bandwidth ratio | 2.4 | — |
| D.fp4s | Rubin sparse NVFP4 ratio | 2.5 | — |
| S.S | arithmetic score | 4.10 | — |
| S.G | geometric score | 4.04 | — |
| S.sd | standard deviation of S | 0.26 | — |
| S.sup | supply share of variance | 34 | % |
| S.road | roadmap share of variance | 19 | % |
