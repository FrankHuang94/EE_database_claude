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

1. **The "30× inference vs H100" claim is plausible only at the operating point in its footnote, and only if the H100 baseline runs far below its peak.** It is not a general speed-up.
   - Per GPU, the hardware improves memory bandwidth **2.39×** and dense compute **2.5×** at equal precision. Moving from FP8 to FP4 doubles the dense rate and halves the bytes per weight.
   - The footnote's requests carry 32,768 input tokens per 1,024 output tokens, so prefill compute dominates. A first-principles serving model that counts it gives about **4.8×** per GPU, and **5.1×** when the model needs two H100 servers: close to the 5.0× dense-compute ratio with the precision change.
   - The remaining factor of about **6** has to come from the H100 servers being "scaled over InfiniBand" at a 50 ms per-token deadline, which the claim does not quantify.
2. **The chip is not the differentiator. The 72-GPU NVLink domain, sold as merchant hardware, is, but it is not unique.**
   - Per GPU, AMD's MI355X matches the bandwidth (8 TB/s) and the dense FP8 and FP4 rates, and has **1.55×** the memory.
   - Each NVL72 GPU has 900 GB/s each way of NVLink, **18×** a 400 Gb/s network port (50 GB/s each way; one port per GPU is our assumption).
   - Google's Ironwood links 9,216 chips at 0.67× NVLink's per-chip bandwidth, so domain size alone is not a moat. How each topology serves a given collective, and who can buy the capacity, are open diligence questions (§4).
3. **The specification table needs care.** Its FP8 and BF16 rows are sparse figures, printed as single numbers next to an NVFP4 row that shows both. Read as dense, they overstate compute **2×**.
4. **Most of the risk is in the facility and the supply chain, not in the silicon.**
   - **Power and cooling.** A rack draws 120 to 132 kW and needs liquid cooling, with up to 192 kW provisioned.
   - **Reliability.** An H100-like failure rate gives about **7.3** to **8.0** GPU-related interruptions per rack per year. Each one can stall a 72-GPU domain.
   - **Packaging.** It depends on a single packaging route, and the mask was respun for yield in 2024.
   - **Short life.** A one-year product cadence shortens its useful life as the leading platform.
5. **Scorecard:** **4.10** of 5 (arithmetic), **4.04** (geometric). Software and supply carry most of the uncertainty (§7).

**Recommendation.** Underwrite the platform's lead in large-model inference through its successors. Do not underwrite "30×" for any customer: underwrite about 2.5× per GPU at equal precision for long-prompt serving and up to 5× with FP4, and ask for the H100 baseline's delivered utilization. Make facility readiness (power, liquid cooling, the 800 VDC transition) an explicit diligence item for every thesis that depends on deployment volume.

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

**The package.** Each GPU joins two near-reticle dies with a 10 TB/s die-to-die link, about 208 billion transistors in all, on TSMC's custom 4NP process [R-149]. A teardown of the GPU from an HGX B200 system, the same Blackwell package, found eight SK hynix HBM3E stacks on TSMC's CoWoS-L, NVIDIA's first bridge-based 2.5D package [R-586] **[Established for the unit torn down]**.

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

The inputs are manufacturer specifications as of Nov 2026 **[Established as manufacturer specifications]**.

**The ceiling for bandwidth-bound decoding.** Generating each token reads the weights and the KV cache once, so a step is limited by memory bandwidth. Bandwidth gives 2.39×. Halving the bytes per weight (FP4 against FP8) gives a further **2**×. Together that is a ceiling of about **4.78×** for decoding a model that fits in both systems.

To reach 30×, the operating point must supply the remaining **6.28×**.

**A first-principles serving model.** [claims.py](claims.py) models the footnote's operating point in two parts.

- **Decode.** Each step reads all weights $W$ and each sequence's KV cache $K$ once. With batch $B$ in a domain of $G$ GPUs, the step takes $t = (W + BK)/(G\,BW)$. The batch is the largest that meets both the latency limit, $t \le$ 50 ms, and the capacity limit, $W + BK \le G\,C$. At GB200's batch of 13,330 the weight multiplications take **5.18** ms of a **23.3** ms step, so decode is memory-bound, as assumed.
- **Prefill.** Each request's 32,768 input tokens are processed before its first output token, at about $2P$ FLOPs per token for a model of $P$ parameters. Each output token therefore carries $2P \times 32$ FLOPs of prefill. Run at the dense peak $F$, prefill alone caps a GPU at $F/(64P)$ output tokens per second. Attention adds FLOPs at long context; we omit them, which flatters both systems.
- **Together.** With prefill and decode on separate pools of GPUs, each sized to its load (our assumption), the throughput per GPU is $1/(1/D + 1/P_c)$, where $D$ is the decode rate and $P_c$ the prefill cap.

Two hypothetical models show the mechanism. Their sizes are ours; the footnote as logged names no model. Both use FP8 weights on H100 and FP4 on GB200, with 1 GB of FP8 KV cache per 32k-token sequence on both. All rates are output tokens per second per GPU.

| Hypothetical model | Limit | H100 | GB200 NVL72 | Ratio per GPU |
|---|---|---|---|---|
| A: 140 GB of FP8 weights (140 B parameters; fits one 8-GPU server) | Decode alone | **2,617** (batch **500**, capacity-limited) | **7,958** (batch **13,330**, capacity-limited) | **3.04×** |
| | Prefill cap | **223** | **1,116** | 5.0× |
| | Together | **206** | **979** | **4.76×** |
| B: 1 TB of FP8 weights (1 T parameters; needs two H100 servers) | Decode alone | **733** on 16 GPUs, *ignoring the network between them* | **7,701** | **10.5×** |
| | Prefill cap | **31.25** | **156** | 5.0× |
| | Together | **30.0** | **153** | **5.11×** |

**Three readings.**

1. **Prefill dominates.** In model A the prefill pool needs **92**% of the H100s and **88**% of the GB200 GPUs. The per-GPU ratio therefore collapses toward the dense-compute ratio: 5.0× with FP4 against FP8, and **2.53×** at equal precision (GB200 serving model A at FP8 gives **521** tokens/s per GPU).
2. **Decode alone would look different.** Model A's decode ratio, 3.04×, is below the 4.78× ceiling. At a capacity-limited batch the KV cache (13,330 GB) dwarfs the weights (70 GB), so FP4 cuts the bytes read per generated token only from **1.28** GB to **1.005** GB, **1.27×**; and 2.39 × 1.27 ≈ 3.04. Model B's decode ratio passes 10.5× because the H100 needs two servers. Neither ratio survives once prefill is counted.
3. **Neither deadline binds in the model.** Every decode step takes 23–24 ms (**23.9** ms on H100), under the 50 ms limit. Prefilling one request at the dense peak takes **0.573** s on H100 for model A and **2.05** s for model B, against the 5 s first-token limit (**0.0127** and **0.0910** s on GB200). The H100's model-B prefill would miss 5 s at a delivered utilization below **41**%, about what Meta reported for training (38–43% [R-694]).

**Where the rest of 30× must come from.** The model gives about 5× per GPU at the footnote's point, even when the model needs two H100 servers. So 30× needs a further **6.3×** from the H100 side running far below its peak:

- tensor- or pipeline-parallel traffic over InfiniBand on every step, through a 400 Gb/s port: 50 GB/s each way against NVLink's 900 GB/s, **18×** less;
- smaller batches to meet the deadline across servers;
- lower delivered utilization.

None of that is in the model, and the footnote does not disclose the H100 configuration's utilization **[Contested: a plausible mechanism, not measured here]**.

**Verdict on the inference claim: possible at its operating point only if the H100 baseline is far from its peak; not transferable.** For a customer serving long prompts, plan on about **2.5×** per GPU at equal precision and up to **5×** with FP4, after checking accuracy at FP4. For short prompts and decode-heavy work, plan on about **3×** when the model fits an 8-GPU server, and more when it does not. Ask for the H100 baseline's measured utilization (§8, question 1).

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
| Scale-up domain | 72 GPUs, 1.8 TB/s each (both directions) | 7 links of 144 GB/s, **1,008** GB/s in all (direction convention not stated) | 9,216 chips, 1.2 TB/s ICI each (both directions) |
| FP8 FLOPs per byte of HBM | **625** | **625** | **626** |

Sources: [R-460], [R-690], [R-692], [R-693] **[Established as manufacturer specifications; power definitions differ, so the power row is not like-for-like]**.

**Three conclusions.**

1. **The chips have converged.** Compute per byte of bandwidth is essentially identical across all three, and H100 sat at **597**. These are balanced designs aimed at the same workloads. The MI355X carries **1.55×** the memory per GPU, which matters for KV-cache-heavy serving.
2. **Domain size and bandwidth differentiate.**
   - **NVL72:** a 72-GPU domain at 1.8 TB/s per GPU.
   - **MI355X:** seven links, consistent with an eight-GPU fully connected server (our inference from the link count).
   - **Ironwood:** a much larger ICI domain of 9,216 chips, at **0.67** times NVLink's per-chip bandwidth (both figures bidirectional).

   So a large domain alone is not unique to NVIDIA. Three questions the logged sources do not settle decide how much it is worth:

   - **Topology.** NVLink is switched all-to-all within the rack [R-521]; the logged Ironwood source does not describe the ICI topology [R-693]. How many hops a collective takes, and what bisection bandwidth it sees, decide how much of each chip's link bandwidth a given parallelism can use.
   - **Availability.** NVL72 racks are sold by several system makers [R-098]; whether Ironwood capacity is offered outside Google's own cloud is not established here.
   - **Direction convention.** R-692 does not say whether the MI355X's 144 GB/s per link counts one direction or both, so its scale-up figure may be off by 2×.
3. **Capacity in one domain decides what fits.** At 4-bit, 13.4 TB holds the weights of a model of about **26.8** trillion parameters, before the KV cache. An eight-GPU MI355X server holds **4.61** trillion, and an eight-GPU H100 server holds **640** billion at FP8.

**Software.** NVIDIA's CUDA stack and its libraries are the incumbent ecosystem. This memo has no logged metric for its advantage, so it is scored on judgment (§7) with a wide uncertainty ($\sigma$ = 1.0).

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

**[Contested: 120–135 kW for GB200 depending on definition (typical, nominal, operating range); the 140 and 142 kW figures in R-098 are for GB300, and R-098's rack-power lines are search excerpts.]** A rack at this density needs liquid cooling and in-rack power shelves at about 50 V [R-444].

NVIDIA has announced a move to 800 VDC "starting in 2027" for megawatt racks [R-691]. Facilities built today for 54 V distribution therefore face a retrofit decision within one product generation **[Established as announced]**.

### 5.2 Reliability and blast radius

Meta's training run gives the only logged failure data at this scale [R-694]:

- 419 unexpected interruptions in 54 days on up to 16,384 H100s **[Established as reported]**;
- caused by GPUs: 58.7% in the paper's text, about **246**; but **64.0**% (**268**) from its own table, whose faulty-GPU count of 148 does not match its printed percentage **[Contested: internal inconsistency in the source]**.

**Per GPU.** That is **0.102** to **0.111** GPU-related interruptions per GPU-year. "Up to" makes these lower bounds.

**Per rack.** Applied to 72 GPUs, it is **7.3** to **8.0** per rack-year, one every **46** to **50** days. Blackwell's rate may differ, so the H100 rate is an assumption.

**The blast radius.** In an eight-GPU server a fault stalls 8 GPUs. In a 72-GPU NVLink domain, a job spanning the domain stalls 72, **9×** as many GPU-hours per fault for the same recovery time. How spares, checkpoints and domain reconfiguration contain this is the most important operational question for anyone renting or operating these racks (§8, question 4).

### 5.3 Manufacturing and supply

**The 2024 yield problem.** In August 2024 NVIDIA "executed a change to the Blackwell GPU [mask] to improve production yields", with "inventory provisions for low-yielding Blackwell material" and, per the CEO, "no functional changes" [R-646] **[Established: management statements]**. A yield problem on near-reticle dies in a new bridge-based package has already happened once and been fixed. It is the kind of risk that recurs at each generation (28-03).

**Concentration.** The package depends on TSMC's CoWoS-L and on HBM3E supply. The one unit torn down carried SK hynix stacks [R-586] **[Established for that unit; not a supply share]**. This memo has no logged capacity allocations. Packaging and HBM allocation are therefore the largest unknowns, which the scorecard reflects (§7).

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
| Ecosystem and software | 0.20 | 5.0 | 1.0 | Incumbent stack; no logged metric, hence the wide σ |
| Manufacturing and supply | 0.20 | 3.0 | 0.75 | Single packaging route, HBM, facility readiness (§5) |

The totals:

| Quantity | Value |
|---|---|
| Weighted arithmetic score $S$ | **4.10** |
| Weighted geometric score $G$ | **4.04** |
| Standard deviation of $S$ (independent errors) | **0.31** |
| Share of the variance from ecosystem and software | **41.8**% |
| Share of the variance from manufacturing and supply | **23.5**% |
| Share of the variance from the roadmap | **13.2**% |

The geometric score is lower because supply is the weak dimension (28-01 §3.2). Software and supply carry two-thirds of the uncertainty, so diligence effort should go there next:

- **Software first,** because public evidence cannot settle it. Measure it directly: the porting effort for a reference workload on a competitor's accelerator, and the share of the customer's code tied to CUDA-only libraries.
- **Supply next:** packaging and HBM allocations, and facility readiness at the customers that matter to the thesis.

**Gates.** The supply path passes on public evidence (shipping volume, with one yield respin absorbed). IP is unassessed: there is no public evidence either way. Export controls pass for permitted destinations and fail for restricted ones (§5.4).

## 8. Questions for management

Each question comes with the answer that should reassure (strong) and the one that should not (evasive).

**1. Show the throughput-against-interactivity curve, not one point, with the H100 baseline's delivered utilization. At what model size, prompt length and latency does the ratio to H100 fall below 5×?**

- *Strong:* curves for several model sizes and prompt lengths, including models that fit an 8-GPU server, with the baseline's utilization stated.
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
  - a competitor offering a scale-up domain of comparable size and per-chip bandwidth as merchant hardware with software parity (Ironwood already matches the size inside Google);
  - facility constraints capping deployment below demand;
  - a second yield event at the next generation.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| C.bw | bandwidth ratio to H100 | 2.39 | — |
| C.fp8 | dense FP8 ratio to H100 | 2.5 | — |
| C.serveA | per-GPU ratio with prefill, model A | 4.8 | — |
| C.serveB | per-GPU ratio with prefill, model B | 5.1 | — |
| C.resid | factor left to the H100 baseline | 6 | — |
| C.mi355cap | MI355X memory over a GB200 GPU | 1.55 | — |
| C.port | NVLink over a 400 Gb/s port, each way | 18 | — |
| C.sparse | overstatement if sparse rows read as dense | 2 | — |
| C.rackyr | GPU-related interruptions per rack-year, low | 7.3 | — |
| C.rackhi | GPU-related interruptions per rack-year, high | 8.0 | — |
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
| M.port | NVLink over a network port, each way | 18 | — |
| M.gemm | weight-multiplication time per GB200 step, model A | 5.18 | ms |
| M.step | GB200 decode step, model A | 23.3 | ms |
| M.steph | H100 decode step | 23.9 | ms |
| M.hpA | H100 prefill cap, model A | 223 | tokens/s per GPU |
| M.gpA | NVL72 prefill cap, model A | 1116 | tokens/s per GPU |
| M.hcA | H100 with prefill, model A | 206 | tokens/s per GPU |
| M.gcA | NVL72 with prefill, model A | 979 | tokens/s per GPU |
| M.rcA | ratio with prefill, model A | 4.76 | — |
| M.hpB | H100 prefill cap, model B | 31.25 | tokens/s per GPU |
| M.gpB | NVL72 prefill cap, model B | 156 | tokens/s per GPU |
| M.hcB | H100 with prefill, model B | 30.0 | tokens/s per GPU |
| M.gcB | NVL72 with prefill, model B | 153 | tokens/s per GPU |
| M.rcB | ratio with prefill, model B | 5.11 | — |
| M.preh | prefill share of H100 GPUs, model A | 92 | % |
| M.preg | prefill share of GB200 GPUs, model A | 88 | % |
| M.eq | NVL72 at FP8 with prefill, model A | 521 | tokens/s per GPU |
| M.eqr | equal-precision ratio, model A | 2.53 | — |
| M.bph | bytes per token, H100, model A | 1.28 | GB |
| M.bpg | bytes per token, NVL72, model A | 1.005 | GB |
| M.bpr | bytes-per-token ratio | 1.27 | — |
| M.ttA | H100 prefill time per request, model A | 0.573 | s |
| M.ttB | H100 prefill time per request, model B | 2.05 | s |
| M.tgA | NVL72 prefill time per request, model A | 0.0127 | s |
| M.tgB | NVL72 prefill time per request, model B | 0.0910 | s |
| M.mfu | utilization at which H100 model-B prefill reaches 5 s | 41 | % |
| M.res | factor left to the H100 baseline, model A | 6.3 | — |
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
| R.gpu | GPU-related interruptions, text share | 246 | — |
| R.gpuhi | GPU-related interruptions, table counts | 268 | — |
| R.pcthi | GPU share from the table counts | 64.0 | % |
| R.rate | interruptions per GPU-year, low | 0.102 | — |
| R.ratehi | interruptions per GPU-year, high | 0.111 | — |
| R.rack | interruptions per rack-year, low | 7.3 | — |
| R.rackhi | interruptions per rack-year, high | 8.0 | — |
| R.days | days between interruptions per rack, low rate | 50 | days |
| R.dayshi | days between interruptions per rack, high rate | 46 | days |
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
| S.sd | standard deviation of S | 0.31 | — |
| S.sw | software share of variance | 41.8 | % |
| S.sup | supply share of variance | 23.5 | % |
| S.road | roadmap share of variance | 13.2 | % |
