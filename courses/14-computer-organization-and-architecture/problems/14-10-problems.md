# Problems 14-10 · Virtual Memory, TLBs and the OS Interface

Chapter: [14-10](../chapters/14-10-virtual-memory.md) · Worked solutions: [14-10 solutions](../solutions/14-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** RISC-V Sv32 unless stated: 4 KiB pages, 4 MiB megapages, two levels of 4-byte PTEs, PTE flags V = 0x01, R = 0x02, W = 0x04, X = 0x08, U = 0x10, G = 0x20, A = 0x40, D = 0x80, PPN in bits 31–10. TLBs are fully associative with LRU replacement unless stated. KiB, MiB and GiB are powers of two.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 14-10.1 [A]

**Splitting.** Give VPN[1], VPN[0] and the page offset of the Sv32 address 0x8040_2ABC, in hexadecimal and decimal.

### Problem 14-10.2 [A]

**Sv39's tables.** Sv39 uses 4 KiB pages and 8-byte PTEs. (a) How many PTEs fit in one page-table page? (b) How many bits of VPN does each level use, and how many levels cover a 27-bit VPN? (c) How large would a flat Sv39 table be?

### Problem 14-10.3 [A]

**Reach.** Find the reach of (a) a 64-entry TLB with 4 KiB pages, (b) a 2048-entry second-level TLB with 4 KiB pages, and (c) the same 2048 entries with 2 MiB pages.

### Problem 14-10.4 [A]

**Cause codes.** On RV32, what value does the cause register hold for (a) a store to a read-only page, (b) an `ecall` from user mode, (c) a supervisor timer interrupt? (d) In vectored mode, where does a machine external interrupt go?

### Problem 14-10.5 [B]

**Walking with faults.** satp.PPN = 0x80000. Physical memory holds:

| Physical address | Value |
|---|---|
| 0x8000_0000 | 0x2000_0401 |
| 0x8000_0008 | 0x1000_0017 |
| 0x8000_000C | 0x1000_0417 |
| 0x8000_1014 | 0x0000_0000 |
| 0x8000_1018 | 0x091A_2813 |

For each user-mode access, give the physical address and number of PTE reads, or the fault and its cause code:

- (a) load from 0x0080_1234;
- (b) load from 0x0000_5010;
- (c) store to 0x0000_6020;
- (d) load from 0x00C0_0000;
- (e) load from 0x0000_6020.

### Problem 14-10.6 [B]

**Two TLB levels.** 2% of accesses miss in the first-level TLB. A second-level TLB answers in 7 cycles and misses on 10% of the lookups it receives. A page walk then costs 60 cycles. (a) What is the average translation overhead per access? (b) What would it be with no second-level TLB?

### Problem 14-10.7 [B]

**Page-table memory.** A process uses 1 MiB of code from 0x0040_0000, 9 MiB of heap from 0x1000_0000, and 1 MiB of stack ending at 0x8000_0000. (a) How many Sv32 page-table pages does it need, and how many KiB? (b) If the heap is mapped with megapages instead, how many megapages does it take, how much memory do they map beyond the 9 MiB, and how many page-table pages remain?

### Problem 14-10.8 [B]

**When does the TLB thrash?** The column traversal of Example 14-10.4 (a 1024 × 1024 integer matrix, 4 KiB pages) is run with fully associative LRU TLBs of 1024 and 1023 entries. Find the TLB misses in each case and explain the cliff.

### Problem 14-10.9 [B]

**VIPT limits.** With 4 KiB pages, what is the largest VIPT L1 cache (with no synonym handling) that is 8-way, 12-way and 16-way? What is the largest 8-way one with 16 KiB pages?

### Problem 14-10.10 [C]

**Belady's anomaly.** A program references the pages 5, 3, 4, 1, 5, 3, 2, 5, 3, 4, 1, 2. Count the page faults with 3 and with 4 frames under FIFO, LRU and OPT. Which policy gets worse with more memory, and why can LRU never do so?

### Problem 14-10.11 [C]

**The cost of a context switch.** A core switches processes every 1 ms at 3 GHz. Without ASIDs, the TLBs are flushed on each switch, and the new process refills every entry with a 30-cycle walk. Estimate the overhead as a percentage of time for (a) a 64-entry TLB alone and (b) a 2048-entry second-level TLB as well. (c) What do ASIDs change?

### Problem 14-10.12 [C]

**Thrashing.** A loop touches 10 pages cyclically, 10 times over (100 references). Count the page faults with 9 and with 10 frames under FIFO, LRU and OPT. At 5 ms per fault, how long does the loop spend faulting with 9 frames under LRU, and with 10?

---

## Objective coverage

| Learning objective (chapter 14-10) | Problems |
|---|---|
| 1. Virtual memory and multilevel page tables | 1, 2, 7 |
| 2. Walking Sv32 page tables | 1, 5 |
| 3. TLB reach and translation cost | 3, 6, 8, 11 |
| 4. Traps and cause codes | 4, 5 |
| 5. Replacement, thrashing and VIPT limits | 9, 10, 12 |
