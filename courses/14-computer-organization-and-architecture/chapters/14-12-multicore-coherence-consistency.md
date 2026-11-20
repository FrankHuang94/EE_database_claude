<!-- status: reviewed -->
# 14-12 · Multicore, Coherence and Memory Consistency

| | |
|---|---|
| **Course** | [14 · Computer Organization and Architecture](../README.md) |
| **University equivalent** | The multiprocessor unit of a computer architecture course: thread-level parallelism, snooping and directory cache coherence (MSI, MESI), coherence misses and false sharing, memory consistency models (SC, TSO, weak ordering), and synchronization primitives (Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*, ch. 5; Patterson & Hennessy, *Computer Organization and Design*, RISC-V Edition, ch. 6; Sorin, Hill & Wood, *A Primer on Memory Consistency and Cache Coherence*) |
| **Prerequisites** | [14-09 Memory Hierarchy and Caches](14-09-memory-hierarchy-and-caches.md), [14-11 I/O, Buses and Interconnect](14-11-io-buses-and-interconnect.md), [14-01 Performance, Power and the Iron Law](14-01-performance-power-iron-law.md) (Amdahl's law) |
| **Estimated study hours** | 8 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Explain why private caches make shared memory incoherent, and state the invariants a coherence protocol maintains.
2. Trace MSI and MESI snooping protocols through a sequence of reads and writes, counting bus transactions and invalidations, and explain what the E state saves.
3. Size a directory, and explain why large systems use directories instead of snooping.
4. Recognize true and false sharing, and remove false sharing by changing data layout.
5. Determine which outcomes of a litmus test are allowed under sequential consistency, TSO and a weaker model, and place fences to restore the intended behaviour.
6. Explain how atomic instructions and test-and-test-and-set locks are built on coherence.

---

## 1. Big picture

Since single-core performance stopped scaling with frequency (14-01), chips have grown by adding cores. A shared-memory multicore lets threads communicate simply by reading and writing the same addresses. But each core has private caches (14-09), so copies of the same address can exist in several places at once. Two problems follow:

- **Coherence:** all cores must agree on the value of each single address. A write by one core must eventually be seen by the others, and they must not keep reading a stale copy forever.
- **Consistency:** the hardware must also say in what order writes to *different* addresses become visible. Store buffers and out-of-order execution (14-08) reorder memory operations, so the answer is not obvious, and it differs between x86, Arm and RISC-V.

Getting these right is what makes locks, queues and every concurrent data structure work. Getting them wrong produces the hardest bugs in computing: failures that appear once in a billion runs, on one machine and not another.

- **Every multicore CPU, GPU and SoC with caches implements a coherence protocol** in hardware.
- **Coherence traffic limits scaling**: shared data that bounces between cores costs a cache miss on every handoff.
- **Memory models are part of the ISA contract**, and porting concurrent code between x86 and Arm or RISC-V exposes their differences.

## 2. Intuition first

**A shared document with local copies.** A team edits a document, but each member works on a printed copy for speed. If one person changes a paragraph, everyone else's printout of that page is now wrong. A **coherence protocol** is a rule like "before you edit a page, everyone else must throw away their copy of it; anyone who wants to read it again must fetch the new version." Many people can hold read-only copies at once, but an editor must hold the only copy. This **single writer or multiple readers** rule is the heart of every invalidation protocol.

**Memory consistency** is a different question: the *order* in which you learn of changes to *different* pages. Suppose a colleague edits page 5 and then puts a note on page 1 saying "page 5 is done." Must you see page 5's new text if you see the note? Under the strictest rule, **sequential consistency**, yes. Under relaxed rules, the note may reach you first, unless your colleague explicitly waits (a **fence**) between the two.

**Where the analogy breaks.** In hardware, "throwing away a copy" happens in nanoseconds by messages on a bus or network. The pages are 64-byte cache blocks, not whole variables, so two people editing *different* words on the same block still fight over it: **false sharing**.

## 3. Theory

### 3.1 Thread-level parallelism and shared memory

A **shared-memory multiprocessor** runs several threads that share one address space. Each core has private L1 (and usually L2) caches and shares an L3 and memory. The speedup available is bounded by Amdahl's law (14-01), and also by the **communication** the threads need: every value one thread produces and another consumes must travel between caches.

### 3.2 The coherence problem and its invariants

Suppose cores 0 and 1 both read $x = 0$ into their caches. Core 0 then writes $x = 1$ into its own cache (write-back, 14-09). Core 1 keeps reading 0 from its copy, possibly forever. A **coherence protocol** prevents this by maintaining, for each block [1]:

- **the single-writer, multiple-reader (SWMR) invariant**: at any moment, either one core may write the block (and no other core may read it), or any number of cores may read it (and none may write);
- **the data-value invariant**: a read returns the value of the most recent write to that block in the order the protocol establishes.

Hardware coherence covers caches, not TLBs. When the operating system changes a page mapping, other cores' TLBs may still hold the old translation, and the OS must invalidate them itself with interprocessor interrupts: a **TLB shootdown** (14-10).

Almost all real protocols are **write-invalidate**: a core that wants to write must first invalidate every other copy. (Write-update protocols, which broadcast each written value, cost too much bandwidth.)

### 3.3 Snooping protocols: MSI and MESI

In a **snooping** protocol, every cache watches (snoops) a shared bus or broadcast network and reacts to other cores' requests. Each cached block has a state:

| State | Meaning | Can read | Can write |
|---|---|---|---|
| **M** (Modified) | the only copy, dirty | yes | yes |
| **E** (Exclusive) | the only copy, clean (MESI only) | yes | yes, silently → M |
| **S** (Shared) | one of possibly several clean copies | yes | no: must upgrade first |
| **I** (Invalid) | not present | no | no |

The bus carries three requests:

- **BusRd**: read a block;
- **BusRdX**: read a block with intent to write, which invalidates every other copy;
- **BusUpgr**: invalidate the other copies of a block the requester already holds in S.

The transitions are:

| Event at core $i$ | Current state | Bus request | New state | Other caches |
|---|---|---|---|---|
| Read | M, E, S | none | unchanged | none |
| Read | I | BusRd | E if no other copy (MESI); otherwise S | an M copy is written back; M and E copies become S |
| Write | M | none | M | none |
| Write | E | none | M | none |
| Write | S | BusUpgr | M | all copies invalidated |
| Write | I | BusRdX | M | an M copy is written back; all copies invalidated |

The **E** state is MESI's improvement over MSI. A core that reads a block nobody else has gets it in E, and a later write upgrades silently, with no bus transaction. Private data that is read and then written, the common case, then costs one bus transaction instead of two (Example 14-12.2).

The coherence protocol adds a fourth C to the three of 14-09: **coherence misses**, which are misses on blocks the core once held but lost to another core's invalidation.

### 3.4 Directories

Snooping needs every request to reach every cache. That works for a bus or a ring with a few to a few dozen cores, but broadcast bandwidth does not scale. A **directory** protocol keeps, for each block, a record of which caches hold it, at the block's **home** node (usually beside the memory or L3 slice that owns it). A requester sends its request to the home; the home forwards invalidations or data requests only to the caches that need them.

- A **full bit-vector** directory stores one presence bit per core plus a few state bits per block. For $N$ cores and $B$-byte blocks, the overhead is about $N / (8B)$ of the data size: 12.5% for 64 cores with 64-byte blocks, but 200% for 1024 cores (Example 14-12.4).
- Large systems therefore use **limited-pointer** directories (a few core IDs per block, falling back to broadcast) or **sparse** directories that track only cached blocks.
- A directory miss can take three network traversals (requester → home → owner → requester), longer than a snoop on a bus, which is the price of scalability.

### 3.5 True and false sharing

A coherence miss is **true sharing** when another core really wrote the data this core needs, as with a shared counter or a work queue. It is **false sharing** when another core wrote a *different* word that happens to lie in the same block. Coherence works on blocks, so the block ping-pongs between the cores although they never share a variable.

The fix for false sharing is layout: give each thread's private data its own block (padding or alignment to the block size). The fix for true sharing is the algorithm: reduce how often threads communicate, for example by keeping per-thread partial sums and combining them at the end.

### 3.6 Memory consistency

Coherence orders the writes to *one* address. A **memory consistency model** specifies the order in which a core's memory operations to *different* addresses may appear to other cores.

**Sequential consistency (SC)** is the simplest model (Lamport, 1979): the result of any execution is as if all cores' operations were executed in some single global order that respects each core's program order. Programmers reason about SC easily. But it forbids optimizations every fast core wants, such as letting a load proceed while an earlier store is still waiting in a **store buffer**.

Small **litmus tests** expose the differences. In **store buffering (SB)**, with $x = y = 0$ initially:

| Thread 0 | Thread 1 |
|---|---|
| `x = 1` | `y = 1` |
| `r1 = y` | `r2 = x` |

Under SC, at least one store comes first in the global order, so $r1 = r2 = 0$ is impossible. On x86 processors it *is* observed. Sewell et al. explain it as "a visible consequence of store buffering": each core's store sits in its own FIFO store buffer while its load reads memory [2, R-219]. Their **x86-TSO** model makes this precise:

- each hardware thread has a FIFO store buffer;
- a load reads its own newest buffered store to that address if there is one, and memory otherwise;
- buffered stores drain to memory in order;
- MFENCE (and LOCK'd instructions) flush the buffer [2, R-219].

TSO thus relaxes one ordering, a store followed by a load to a different address. (A core may also read its own buffered store before other cores can see it, Problem 14-12.7.) Stores stay ordered with each other, so the **message passing (MP)** idiom works: write data, then a flag; a reader that sees the flag then sees the data.

Weaker models relax more. **RISC-V's RVWMO** is "defined in terms of the global memory order, a total ordering of the memory operations produced by all harts", with constraints that let hardware reorder independent memory operations: "memory instructions from another hart may observe the memory instructions from the first hart being executed in a different order" [3, R-218]. Arm's model is similar in spirit. Under such models even MP needs ordering on both sides: a **fence** (or a release store) between the writer's data and flag stores, and a fence (or an acquire load) between the reader's flag and data loads, because these models may also reorder loads (Problem 14-12.8). RISC-V also defines an optional **Ztso** extension for total store ordering, the x86-style model [3, R-218].

The programmer's escape hatch is the **data-race-free** discipline. Programs whose shared accesses are all protected by synchronization (locks, atomics with the right ordering) behave as if sequentially consistent on all these machines. The language memory models of C, C++, Java and Rust are built on that guarantee, and compilers insert the fences each architecture needs.

### 3.7 Synchronization primitives

Locks and lock-free structures need **atomic read-modify-write** operations. RISC-V provides two families [3, R-218]:

- **LR/SC** (load-reserved, store-conditional): LR.W "registers a reservation set", and SC.W "succeeds only if the reservation is still valid", writing zero to its destination on success. A loop of LR, compute and SC implements any atomic update.
- **AMOs** (atomic memory operations: swap, add, AND, OR, min, max) perform the whole update in one instruction, often at the cache or even at the L3, near the data.

Both are built on coherence: to perform an atomic update, a core obtains the block in M and holds it for the duration.

A **spin lock** shows how much the coding matters:

- **Test-and-set (TAS)** spins on an atomic swap. Every attempt is a write, so every spin invalidates the other spinners' copies, and the lock's block ping-pongs across the bus.
- **Test-and-test-and-set (TTAS)** spins on ordinary *reads* until the lock looks free, and only then tries the swap. Spinners hit in their own caches (state S) and generate no traffic until the release invalidates them (Example 14-12.6).

### 3.8 The lab's models

The lab has two models:

- `mesi.py` simulates $N$ cores with private caches on a snooping bus under MSI or MESI. It counts bus requests, invalidations, write-backs and misses by kind, and checks the SWMR and data-value invariants after every operation: each write stores a new version number, and each read must return the newest one.
- `litmus.py` enumerates *every* execution of a litmus test under SC, under TSO (FIFO store buffers, the x86-TSO abstract machine [2]) and under PSO, a store-reordering model in which stores to different addresses may drain out of order. It returns the set of allowed outcomes.

## 4. Worked examples

### Example 14-12.1 · Tracing MESI (tier A)

**Setup.** Two cores share block X, initially in neither cache. Trace MESI through: P0 reads X; P1 reads X; P0 writes X; P1 reads X; P1 writes X; P0 reads X. Give each step's bus request and the states, and count the bus transactions and invalidations.

**Solution.**

| Step | Operation | Bus | P0 | P1 | Notes |
|---|---|---|---|---|---|
| 1 | P0 read | BusRd | E | I | no other copy, so E |
| 2 | P1 read | BusRd | S | S | P0 sees the request and drops to S |
| 3 | P0 write | BusUpgr | M | I | P1's copy invalidated |
| 4 | P1 read | BusRd | S | S | P0 writes back the dirty block and supplies it |
| 5 | P1 write | BusUpgr | I | M | P0's copy invalidated |
| 6 | P0 read | BusRd | S | S | P1 writes back and supplies it |

That is **6** bus transactions (4 BusRd, 2 BusUpgr), **2** invalidations and **2** write-backs. Steps 4 and 6 are **coherence misses**: blocks once held, then lost to invalidation.

**Units check.** Counts of transactions.

**Sanity check.** At every step at most one cache is in M or E, and never alongside an S copy: the SWMR invariant holds (the simulator checks it after each step).

### Example 14-12.2 · What the E state saves (tier B)

**Setup.** A core reads and then writes each of 100 private blocks that no other core touches. Count the bus transactions under MSI and MESI.

**Solution.** Under MSI each read miss brings the block in S, and the write then needs a BusUpgr: $100 + 100$ = **200** transactions. Under MESI the read gets E, because no one else has the block, and the write upgrades silently: **100** transactions, half as many.

**Units check.** Transactions per block: 2 against 1.

**Sanity check.** Most data in real programs is private, so the E state pays for its extra state bit many times over.

### Example 14-12.3 · False sharing (tier B)

**Setup.** Two threads each increment their own counter 1000 times (a load and a store per increment), interleaved one operation at a time. Count the MESI bus transactions when the two counters are adjacent 4-byte words in one 64-byte block, and when they are 64 bytes apart.

**Solution.**

- **Same block:** each round of four operations (P0 load, P1 load, P0 store, P1 store) causes a BusRd (P0's copy was invalidated by P1's last store), a BusUpgr (P0's store invalidates P1) and a BusRdX (P1's store misses and invalidates P0). That is 3 per round, plus P1's first read: **3001** transactions, with **2000** invalidations.
- **Separate blocks:** each core misses once and keeps its block in E, then M: **2** transactions.

**Units check.** Transactions.

**Sanity check.** The threads never touch each other's counter. The 1500-fold difference is caused purely by the 64-byte coherence granularity. Padding each counter to its own block removes it.

### Example 14-12.4 · Sizing a directory (tier B)

**Setup.** A full bit-vector directory stores one presence bit per core and 2 state bits per 64-byte block. Find the overhead relative to the data for 64 cores and for 1024 cores. How many bits would a limited-pointer entry with 4 pointers need for 1024 cores?

**Solution.**

- **64 cores:** $(64 + 2) / 512$ = **12.9**% of the data bits.
- **1024 cores:** $(1024 + 2) / 512$ = **200.4**%: twice the data it describes.
- **Limited pointers:** 4 pointers of $\log_2 1024 = 10$ bits plus 2 state bits = **42** bits per block, 8.2% overhead. The cost appears when more than 4 cores share a block, and the directory must fall back to broadcast or a coarser record.

**Units check.** Bits per bit of data.

**Sanity check.** The presence vector grows linearly with the core count while the block stays 512 bits, so full bit vectors stop scaling somewhere in the hundreds of cores.

### Example 14-12.5 · Store buffering under SC and TSO (tier B)

**Setup.** For the SB litmus test of §3.6, list the allowed outcomes $(r1, r2)$ under SC and under TSO, and with a fence between each thread's store and load.

**Solution.** Under SC the 6 interleavings of four operations give **3** outcomes: (0, 1), (1, 0) and (1, 1). Some store always precedes both loads, so (0, 0) is impossible. Under TSO both stores can wait in the store buffers while both loads read memory, so (0, 0) is also allowed: **4** outcomes. A fence (MFENCE on x86, `fence w,r` on RISC-V) forces each store to drain before the load: back to **3** outcomes, the SC set.

**Units check.** Outcomes are pairs of register values.

**Sanity check.** The lab's enumerator explores every interleaving and every possible store-buffer drain and finds exactly these sets. Under TSO the message-passing test still forbids $r1 = 1, r2 = 0$; only the weaker PSO model allows it (Problem 14-12.8).

### Example 14-12.6 · Spinning on a lock (tier C)

**Setup.** Core 0 holds a lock. Cores 1–3 each spin 100 times, taking turns round-robin. Core 0 then releases the lock, and each waiter makes one attempt, in order, even after another waiter has taken the lock (a simplification: real code would re-test first). Count the MESI bus transactions with test-and-set and with test-and-test-and-set spinning.

**Solution.**

- **Test-and-set:** every spin is an atomic swap, a write. Each one misses (the previous spinner holds the block in M) and issues a BusRdX that invalidates the last writer. That is 300 spins plus the acquire, the release and 3 attempts: **305** transactions.
- **Test-and-test-and-set:** the first spin read by each waiter brings the block in S, and the other 99 hit locally. The traffic is the acquire, 3 initial reads, the release (a BusUpgr that invalidates 3 copies), 3 re-reads and 3 attempts: **11** transactions.

**Units check.** Transactions.

**Sanity check.** TTAS cuts the transactions from 305 to 11 and the invalidations from **304** to **6**: 3 at the release and 1 at each attempt. Under heavy contention, real locks add exponential backoff or queue-based designs, so that each waiter spins on its own block.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 14-12.1a | bus transactions | 6 | — |
| Ex 14-12.1b | invalidations | 2 | — |
| Ex 14-12.1c | write-backs | 2 | — |
| Ex 14-12.1d | coherence misses | 2 | — |
| Ex 14-12.2a | bus transactions, MSI | 200 | — |
| Ex 14-12.2b | bus transactions, MESI | 100 | — |
| Ex 14-12.3a | bus transactions, same block | 3001 | — |
| Ex 14-12.3b | invalidations, same block | 2000 | — |
| Ex 14-12.3c | bus transactions, separate blocks | 2 | — |
| Ex 14-12.4a | directory overhead, 64 cores | 12.9 | % |
| Ex 14-12.4b | directory overhead, 1024 cores | 200.4 | % |
| Ex 14-12.4c | limited-pointer entry | 42 | bits |
| Ex 14-12.5a | interleavings | 6 | — |
| Ex 14-12.5b | outcomes, SC | 3 | — |
| Ex 14-12.5c | outcomes, TSO | 4 | — |
| Ex 14-12.5d | outcomes, TSO with fences | 3 | — |
| Ex 14-12.6a | bus transactions, test-and-set | 305 | — |
| Ex 14-12.6b | bus transactions, test-and-test-and-set | 11 | — |
| Ex 14-12.6c | invalidations, test-and-set | 304 | — |
| Ex 14-12.6d | invalidations, test-and-test-and-set | 6 | — |

## 5. Simulate it

The lab, [labs/14-12-lab](../labs/14-12-lab/README.md), provides `mesi.py` and `litmus.py`. In the notebook you:

1. **Replay Example 14-12.1** step by step under MSI and MESI.
2. **Measure false sharing** for two to eight threads, with counters packed and padded.
3. **Compare spin locks** as the number of waiters grows.
4. **Enumerate litmus tests** (SB, MP, with and without fences) under SC, TSO and PSO.

**Guided exercise (predict, then run).** **Before Part 4,** predict whether TSO allows the message-passing outcome "flag seen, data not seen" (r1 = 1, r2 = 0). (No: TSO keeps stores in order, so data reaches memory before the flag. PSO allows it. In the lab's PSO model, which reorders only stores, a fence between the two stores forbids it again; on RVWMO or Arm the reader would also need a fence between its two loads.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| MESI's E state (and further states such as O or F) | Fewer bus transactions for private data; cache-to-cache transfers | State bits, protocol complexity and verification | CPU and fabric architects |
| Snooping against directory | Latency and simplicity (snooping) against scalability (directory) | Broadcast bandwidth; directory storage and three-hop misses | SoC architect |
| Block size | Spatial locality | More false sharing | CPU architect |
| Stronger memory model (TSO) | Easier programming and porting | Fewer reordering optimizations, larger store-buffer checks | ISA architect |
| Weaker model (RVWMO, Arm) | Hardware freedom and efficiency | Fences in software; subtle bugs | ISA architect, compiler writers |
| Lock design (TTAS, backoff, queues) | Coherence traffic under contention | Code complexity, fairness tuning | Systems software engineers |
| Padding shared structures | Removes false sharing | Memory footprint | Software engineers |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Coherence granularity | one cache block, typically 64 bytes | §3.5 |
| MESI read-then-write of private data | 1 bus transaction (MSI: 2) | Example 14-12.2 |
| Full-map directory overhead | about $N/(8B)$ of data: 12.5% at 64 cores, 64 B blocks | Example 14-12.4 |
| SB litmus test | SC: 3 outcomes; TSO: 4 (adds 0, 0) | [2, R-219] |
| x86 | TSO-like: stores ordered, a store may be overtaken by a later load | [2, R-219] |
| RISC-V | RVWMO by default; optional Ztso | [3, R-218] |

## 8. Common mistakes

- **Confusing coherence with consistency.** Coherence is about one address; consistency is about the order of accesses to different addresses.
- **Assuming the hardware runs your program in order.** Under TSO and weaker models, other cores may observe your stores and loads reordered.
- **Using `volatile` for synchronization.** It prevents compiler optimizations but adds no hardware fences; use atomics and locks.
- **Ignoring false sharing.** Per-thread counters packed into an array can make a parallel program slower than its serial version.
- **Spinning with atomic writes.** Test-and-set spinning floods the interconnect; spin on reads (TTAS), back off, or use queue locks.
- **Testing concurrency on x86 only.** Code that works under TSO can fail on Arm or RISC-V, whose models allow more reordering.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Formal memory models.** RISC-V specifies RVWMO formally, with an optional Ztso extension [3, R-218]. x86 behaviour is captured by the x86-TSO model of Sewell et al. [2, R-219] **[Established]**.
- **Directories everywhere.** Server processors with tens to hundreds of cores use directory or snoop-filter structures rather than pure broadcast **[Industry estimate]** (textbook practice; vendors rarely publish details).
- **Coherent interconnects beyond the chip.** CXL (14-11, [R-217](../../../reference/research-log.md#r-217--amba-axi-issue-l-and-cxl-40)) extends cache coherence to accelerators and attached memory.

### Why it matters commercially

- **Scaling software to many cores** is limited as much by coherence traffic (shared locks, counters, false sharing) as by Amdahl's serial fraction.
- **Porting from x86 to Arm or RISC-V** in data centres and phones exposes latent memory-ordering bugs. The weaker models are a real migration cost, which is one motivation for RISC-V's Ztso option.

### Marketing vs Reality

- **"Linear scaling with cores."** *Reality:* true only for workloads with little sharing. *Sanity check:* ask for the scaling curve on a workload with shared state, and where it flattens.
- **"Coherent accelerator attach."** *Reality:* coherence makes sharing correct, not fast; fine-grained sharing across a link costs a link round trip per handoff. *Sanity check:* ask how often data actually moves between host and device caches.

### Questions for engineering leaders

1. **"Where does coherence traffic limit your scaling?"**
   *Strong:* measured coherence misses or HITM-style counters per structure, and the fixes made. *Evasive:* "we use lock-free code".
2. **"How do you validate memory ordering on weakly ordered targets?"**
   *Strong:* litmus testing, model checking against the formal model, and stress tests on hardware. *Evasive:* "it passes on x86".
3. **"Snooping, directory or hybrid, and why at your core count?"**
   *Strong:* the trade-off in latency, bandwidth and storage, with numbers. *Evasive:* a product name.
4. **"How does your protocol behave under contention for one line?"**
   *Strong:* measured handoff latency and fairness. *Evasive:* only uncontended latency.

## 10. Concept check

**Q1.** What two invariants does a coherence protocol maintain?

<details><summary>Answer</summary>

Single-writer/multiple-reader: at any time one core may write a block, or any number may read it, never both. Data-value: every read returns the most recent write in the protocol's order.

</details>

**Q2.** What does MESI's E state buy over MSI?

<details><summary>Answer</summary>

A core that reads a block nobody else holds gets it in E and can later write it without a bus transaction, so private read-then-write data costs one transaction instead of two.

</details>

**Q3.** Why do large systems use directories?

<details><summary>Answer</summary>

Snooping broadcasts every request to every cache, which does not scale in bandwidth. A directory sends requests only to the caches that hold the block, at the cost of directory storage and extra network hops.

</details>

**Q4.** What is false sharing, and how is it fixed?

<details><summary>Answer</summary>

Coherence misses caused by different cores writing different words in the same block. It is fixed by layout: padding or aligning each core's data to its own block.

</details>

**Q5.** Why does TSO allow r1 = r2 = 0 in the SB test?

<details><summary>Answer</summary>

Each core's store waits in its store buffer while its later load reads memory, so both loads can complete before either store becomes visible. No interleaving under SC allows that.

</details>

**Q6.** Why is test-and-test-and-set better than test-and-set?

<details><summary>Answer</summary>

Spinning on reads keeps the lock in each waiter's cache in S and generates no traffic until the release; spinning on atomic swaps writes the block on every attempt and invalidates every other waiter each time.

</details>

Now work the [problem set](../problems/14-12-problems.md).

## 11. Key terms

[Cache coherence](../../../reference/glossary.md#cache-coherence) · [MESI protocol](../../../reference/glossary.md#mesi-protocol) · [Snooping](../../../reference/glossary.md#snooping) · [Directory protocol](../../../reference/glossary.md#directory-protocol) · [Coherence miss](../../../reference/glossary.md#coherence-miss) · [False sharing](../../../reference/glossary.md#false-sharing) · [Memory consistency model](../../../reference/glossary.md#memory-consistency-model) · [Sequential consistency](../../../reference/glossary.md#sequential-consistency) · [Total store ordering (TSO)](../../../reference/glossary.md#total-store-ordering-tso) · [Store buffer](../../../reference/glossary.md#store-buffer) · [Fence](../../../reference/glossary.md#fence) · [Litmus test](../../../reference/glossary.md#litmus-test) · [Load-reserved/store-conditional (LR/SC)](../../../reference/glossary.md#load-reserved-store-conditional-lr-sc) · [Spin lock](../../../reference/glossary.md#spin-lock)

## 12. Connections

- **Builds on:** caches and write-back ([14-09](14-09-memory-hierarchy-and-caches.md)); buses and networks-on-chip ([14-11](14-11-io-buses-and-interconnect.md)); out-of-order execution and store buffers ([14-08](14-08-out-of-order-and-superscalar.md)); Amdahl's law ([14-01](14-01-performance-power-iron-law.md)).
- **Next:** [14-13 GPUs and SIMT](14-13-gpus-and-simt.md), which takes thread-level parallelism to thousands of threads with a much weaker coherence model.
- **Related:** TLB shootdowns, which coherence does not cover ([14-10](14-10-virtual-memory.md), §3.2 here).
- **Used later:** CXL coherence ([24-05](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-05-pcie-cxl-ethernet.md)).

## 13. Further study

- D. J. Sorin, M. D. Hill and D. A. Wood, *A Primer on Memory Consistency and Cache Coherence*, Synthesis Lectures on Computer Architecture (2nd ed., with V. Nagarajan, 2020).
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, ch. 5 (thread-level parallelism).
- L. Lamport, "How to Make a Multiprocessor Computer That Correctly Executes Multiprocess Programs," *IEEE Transactions on Computers* C-28(9), 1979.
- S. V. Adve and K. Gharachorloo, "Shared Memory Consistency Models: A Tutorial," *IEEE Computer* 29(12), 1996.

## 14. Sources

1. Sorin, Hill and Wood, *A Primer on Memory Consistency and Cache Coherence* (the SWMR and data-value invariants; textbook).
2. P. Sewell, S. Sarkar, S. Owens, F. Zappa Nardelli and M. O. Myreen, "x86-TSO: A Rigorous and Usable Programmer's Model for x86 Multiprocessors," *Communications of the ACM* 53(7), 2010. [R-219](../../../reference/research-log.md#r-219--x86-tso-sewell-et-al-cacm-2010)
3. RISC-V International, *The RISC-V Instruction Set Manual, Volume I: Unprivileged ISA*, manual set 20260120: the RVWMO, Ztso and A-extension chapters. [R-218](../../../reference/research-log.md#r-218--risc-v-rvwmo-ztso-and-atomics)

Every count and outcome set in the examples is recomputed by the verify script with the lab's simulator (which checks the coherence invariants at every step) and the exhaustive litmus enumerator, and cross-checked by independent reasoning.
