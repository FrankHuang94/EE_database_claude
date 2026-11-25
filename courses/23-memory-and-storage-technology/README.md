<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 23 · Memory and Storage Technology

The technologies that hold data: SRAM, DRAM and its interfaces (DDR, LPDDR, GDDR), HBM in depth, NAND flash and SSD controllers, emerging memories, compute-in-memory, and the memory wall that shapes AI system design.

| | |
|---|---|
| **Term** | 6 |
| **Study hours** | ≈ 53 |
| **University equivalents** | Memory Systems / Semiconductor Memory (senior elective) |
| **Textbook alignment** | Jacob, Ng & Wang, *Memory Systems: Cache, DRAM, Disk*; Weste & Harris, *CMOS VLSI Design* (SRAM/DRAM chapters); JEDEC standards (public summaries) for DDR/LPDDR/HBM |
| **Free courses** | ETH Zürich Computer Architecture lectures (Mutlu) — memory systems lectures |
| **Prerequisites** | [14 · Computer Organization and Architecture](../14-computer-organization-and-architecture/README.md), [19 · Digital VLSI Design](../19-digital-vlsi-design/README.md) |
| **FE areas** | Computer Systems, Properties of Electrical Materials |
| **Deeper** | Companion repo(s): LLM inference engineering |

## Learning objectives

1. Quantify the memory wall with bandwidth, latency and energy-per-bit numbers.
2. Explain DRAM cell, array and refresh operation and the DDR/LPDDR/GDDR/HBM interface tradeoffs.
3. Explain HBM architecture (stacking, TSVs, base die, interposer) and its cost and supply constraints.
4. Explain NAND flash cells, 3D NAND scaling and SSD controller functions.
5. Evaluate emerging memories and compute-in-memory claims against their physics.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [23-01 · The Memory Hierarchy and the Memory Wall](chapters/23-01-memory-hierarchy-and-memory-wall.md) | 4 | 🏁 reviewed | [problems](problems/23-01-problems.md) · [solutions](solutions/23-01-solutions.md) · [lab](labs/23-01-lab/README.md) · [verify](verify/verify_23_01.py) |
| [23-02 · SRAM Technology](chapters/23-02-sram-technology.md) | 4 | 🏁 reviewed | [problems](problems/23-02-problems.md) · [solutions](solutions/23-02-solutions.md) · [lab](labs/23-02-lab/README.md) · [verify](verify/verify_23_02.py) |
| [23-03 · DRAM Cells, Arrays and Refresh](chapters/23-03-dram-cells-arrays-refresh.md) | 7 | 🏁 reviewed | [problems](problems/23-03-problems.md) · [solutions](solutions/23-03-solutions.md) · [lab](labs/23-03-lab/README.md) · [verify](verify/verify_23_03.py) |
| [23-04 · DRAM Interfaces: DDR, LPDDR and GDDR](chapters/23-04-dram-interfaces.md) | 6 | 🏁 reviewed | [problems](problems/23-04-problems.md) · [solutions](solutions/23-04-solutions.md) · [lab](labs/23-04-lab/README.md) · [verify](verify/verify_23_04.py) |
| [23-05 · HBM in Depth](chapters/23-05-hbm-in-depth.md) | 7 | 🏁 reviewed | [problems](problems/23-05-problems.md) · [solutions](solutions/23-05-solutions.md) · [lab](labs/23-05-lab/README.md) · [verify](verify/verify_23_05.py) |
| [23-06 · NAND Flash and 3D NAND](chapters/23-06-nand-flash-and-3d-nand.md) | 7 | 🏁 reviewed | [problems](problems/23-06-problems.md) · [solutions](solutions/23-06-solutions.md) · [lab](labs/23-06-lab/README.md) · [verify](verify/verify_23_06.py) |
| [23-07 · SSD Controllers and Storage Systems](chapters/23-07-ssd-controllers.md) | 5 | 🏁 reviewed | [problems](problems/23-07-problems.md) · [solutions](solutions/23-07-solutions.md) · [lab](labs/23-07-lab/README.md) · [verify](verify/verify_23_07.py) |
| [23-08 · Emerging Memories: MRAM, ReRAM, PCM, FeRAM](chapters/23-08-emerging-memories.md) | 5 | 🏁 reviewed | [problems](problems/23-08-problems.md) · [solutions](solutions/23-08-solutions.md) · [lab](labs/23-08-lab/README.md) · [verify](verify/verify_23_08.py) |
| [23-09 · Compute-in-Memory and Near-Memory Computing](chapters/23-09-compute-in-memory.md) | 5 | 🏁 reviewed | [problems](problems/23-09-problems.md) · [solutions](solutions/23-09-solutions.md) · [lab](labs/23-09-lab/README.md) · [verify](verify/verify_23_09.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/23-memory-and-storage-technology.csv) · [Equation sheet](../../reference/equation-sheets/23-memory-and-storage-technology.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 23 is planned at about 53 hours: the chapters' own estimates add to 50, plus about 3 hours of review; allow a further 4.5 hours for the exam. Course 14 gave you caches and the memory hierarchy as an architect sees them; Course 19 the CMOS circuits inside them; Course 09 the transistor and its leakage; Course 04 tunneling and dielectrics; Course 13 transmission lines and reflections; Course 20 data converters and matching; Course 03 Gaussian tails; and Course 17 coding and capacity. This course opens the boxes: how each memory stores a bit, what it costs to move one, and why AI systems are now designed around memory rather than arithmetic.

The nine chapters fall into four blocks:

- **The memory wall (23-01).** Energy per bit as the real limit on bandwidth, Little's law, the roofline and why long-context LLM decoding is memory-bound.
- **Volatile memories (23-02 to 23-05).** SRAM's stalled bitcell, sigma margins and assists; the DRAM cell, sense amplifier, timing, refresh and row hammer; DDR, LPDDR and GDDR interfaces, termination, reflections, equalization and PAM; HBM's width, interposer, TSVs, heat, yield and packaging.
- **Storage (23-06 and 23-07).** Flash physics, ISPP, multi-level error rates, 3D NAND and retention; the SSD controller's FTL, write amplification, ECC, queues and power-loss protection.
- **Beyond (23-08 and 23-09).** MRAM, PCM, ReRAM and FeRAM, and where they win; compute-in-memory and processing-in-memory, and how to test their claims.

Work at least the [A] and [B] problems of every chapter. The labs are of two kinds, both run in CI (the verify scripts, `run_spice.py` for the netlists' EXPECT lines, and `run_notebooks.py` for the notebooks):

- ngspice netlists: a long on-chip wire's charging energy (23-01), SRAM read and write assists (23-02), DRAM charge sharing, writes and a latch read (23-03), termination, reflections and channel cursors (23-04), an HBM stack's thermal ladder and an interposer link (23-05), ISPP with a Fowler–Nordheim source (23-06), a PCM cell's thermal pulses (23-08) and a resistive crossbar (23-09);
- Python models imported by their notebooks: `memwall.py`, `sramtech.py`, `dramtech.py`, `ddrio.py`, `hbm.py`, `nand.py`, `ssd.py` (with a page-mapped FTL simulator), `emem.py` and `cim.py`.

**What to master cold.** The [equation sheet](../../reference/equation-sheets/23-memory-and-storage-technology.md) collects the relations; these are the ideas behind them:

- moving a bit costs far more than computing on it; energy per bit, not pin count, caps bandwidth; bandwidth times latency is the data that must be in flight; below the ridge point, faster arithmetic changes nothing (23-01);
- SRAM is limited by variation: large arrays need about 6σ of margin, assists trade one failure for another, and the bitcell has stopped shrinking with logic (23-02);
- a DRAM read is charge sharing amplified by a latch; bitline length is set by the signal; the boosted wordline exists because NMOS passes only $V_{WL} - V_{TH}$; refresh and row hammer grow as cells shrink (23-03);
- an interface is a transmission line: termination costs static current, reflections and ISI shrink the eye, DFE removes post-cursors, and PAM pays an eye penalty for a lower symbol rate (23-04);
- HBM is wide and slow over short unterminated wires; heat and yield, not bandwidth, limit stack height; packaging capacity limits supply (23-05);
- a flash cell stores tens of electrons per level; ISPP steps the threshold exactly; each extra bit per cell costs orders of magnitude of raw error rate; retention is thermally activated (23-06);
- an SSD is a remapping machine: over-provisioning buys write amplification and endurance, ECC fails over a cliff and cannot beat capacity, and IOPS are queue depth over latency (23-07);
- emerging memories trade stability, write energy, endurance and density differently; their market is embedded, not NAND's (23-08);
- analog compute is limited by device variation and ADCs, PIM by Amdahl's law, and every TOPS/W figure by its precision, utilization and boundary (23-09).

**After this course.** Course 24 moves the same bits between chips: SerDes, PCIe and CXL, and silicon photonics. Course 27 returns to whole systems, where the memory hierarchy of 23-01 decides an accelerator's real throughput.
