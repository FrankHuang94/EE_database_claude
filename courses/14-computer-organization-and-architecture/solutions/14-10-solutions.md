# Solutions 14-10 · Virtual Memory, TLBs and the OS Interface

Problems: [14-10 problems](../problems/14-10-problems.md) · Chapter: [14-10](../chapters/14-10-virtual-memory.md). Every number below is recomputed by [verify_14_10.py](../verify/verify_14_10.py).

- Walks use the lab's Sv32 walker, cross-checked by an independent decoder.
- TLB counts come from the lab's TLB, checked against closed forms.
- Replacement counts come from two implementations and from the MMU's demand paging.

---

## Solutions

### Solution 14-10.1

VPN[1] = 0x80402ABC >> 22 = 0x201 = **513**. VPN[0] = (0x80402ABC >> 12) & 0x3FF = 0x002 = **2**. The offset is 0xABC = **2748**.

### Solution 14-10.2

(a) $4096 / 8$ = **512** PTEs per page.

(b) Each level indexes 512 entries, so it uses $\log_2 512$ = **9** bits, and $27 / 9$ = **3** levels cover the VPN.

(c) $2^{27}$ PTEs × 8 bytes = **1** GiB per process, which is why no 64-bit system uses flat tables.

### Solution 14-10.3

(a) $64 \times 4$ KiB = **256** KiB.

(b) $2048 \times 4$ KiB = **8** MiB.

(c) $2048 \times 2$ MiB = **4** GiB.

Huge pages raise the reach 512-fold for the same number of entries.

### Solution 14-10.4

(a) A store/AMO page fault: **15**.

(b) An environment call from U-mode: **8**.

(c) An interrupt with code 5 (supervisor timer): bit 31 set, giving **0x8000_0005**.

(d) BASE + 4 × 11 = BASE + **0x2C**.

### Solution 14-10.5

The root table is at 0x8000_0000; its entries for VPN[1] = 0, 2 and 3 are at offsets 0, 8 and 12.

(a) VPN[1] = 2. The PTE 0x1000_0017 is a leaf (R = 1) with PPN 0x40000, a 4 MiB-aligned megapage, readable by user mode. The physical address is 0x40000 × 4096 + (0x0080_1234 & 0x3F_FFFF) = **0x4000_1234**, after **1** PTE read.

(b) VPN[1] = 0 points to the table at 0x8000_1000. The entry for VPN[0] = 5, at 0x8000_1014, is 0: invalid. The result is a load page fault, cause **13**, after 2 reads.

(c) VPN[0] = 6 at 0x8000_1018 holds 0x091A_2813, with flags 0x13 = V, R, U. The page is readable but not writable, so a store raises a store page fault, cause **15**.

(d) VPN[1] = 3 holds 0x1000_0417, a leaf with PPN 0x40001. A megapage's PPN must have its low 10 bits zero, so this is a misaligned superpage: a load page fault, cause **13**.

(e) Same PTE as (c), and a load is allowed. The PPN is 0x091A_2813 >> 10 = 0x2468A, so the physical address is **0x2468_A020**, after **2** reads.

### Solution 14-10.6

(a) $0.02 \times (7 + 0.1 \times 60)$ = **0.26** cycles per access.

(b) Without the second level, every first-level miss walks: $0.02 \times 60$ = **1.2** cycles. The second-level TLB cuts the overhead by 78%.

### Solution 14-10.7

(a) Each level-0 table covers one 4 MiB region (one VPN[1] value):

- the code, 0x0040_0000 to 0x004F_FFFF, lies in region 1;
- the heap, 0x1000_0000 to 0x108F_FFFF, spans regions 0x40, 0x41 and 0x42;
- the stack, 0x7FF0_0000 to 0x7FFF_FFFF, lies in region 0x1FF.

That makes 5 level-0 tables plus the root: **6** pages, or **24** KiB.

(b) The heap needs **3** megapages, mapping 12 MiB, so **3** MiB more than it uses (internal fragmentation). Only the root and the code and stack tables remain: **3** page-table pages.

### Solution 14-10.8

With 1024 entries the TLB holds all 1024 pages that a column touches, so only the first column misses, once per page: **1024** misses. With 1023 entries, each column cycles through 1024 pages, one more than the TLB holds. LRU always evicts the page that will be needed next, so every access misses: **1,048,576**.

A one-entry difference changes the misses 1024-fold. Cyclic access patterns make LRU structures fall off a cliff once the working set exceeds their capacity, the same pathology as Problem 14-09.4.

### Solution 14-10.9

The largest VIPT size is page size × ways:

- with 4 KiB pages: 8-way **32** KiB, 12-way **48** KiB, 16-way **64** KiB;
- with 16 KiB pages, 8-way: **128** KiB.

This is one reason larger base pages appeal to designers of high-performance cores.

### Solution 14-10.10

| Policy | 3 frames | 4 frames |
|---|---|---|
| FIFO | **9** | **10** |
| LRU | **10** | **8** |
| OPT | **7** | **6** |

FIFO gets worse with more memory, which is Belady's anomaly, first described by Belady, Nelson and Shedler in 1969. (This string is a relabelling of the classic textbook example.)

LRU cannot get worse because it is a **stack algorithm**: at every moment, the pages held by an LRU memory of $k$ frames are a subset of those held with $k + 1$ frames. These are the $k$ most recently used pages, and they are always among the $k + 1$ most recent. Any hit with $k$ frames is therefore also a hit with $k + 1$. FIFO's contents depend on arrival order, and have no such inclusion property.

### Solution 14-10.11

A switch every 1 ms at 3 GHz leaves 3,000,000 cycles per time slice.

(a) Refilling 64 entries costs $64 \times 30 = 1920$ cycles: **0.064**% of the time.

(b) Refilling another 2048 entries as well: $(64 + 2048) \times 30 = 63{,}360$ cycles, or **2.112**%.

(c) With ASIDs, entries survive the switch, and a process coming back may find much of its working set still translated. The refill cost falls to the entries actually evicted by other processes, and the larger TLBs become worth having. The estimate also shows why large TLBs make flush-on-switch expensive.

### Solution 14-10.12

| Policy | 9 frames | 10 frames |
|---|---|---|
| FIFO | **100** | **10** |
| LRU | **100** | **10** |
| OPT | **20** | **10** |

With 9 frames, FIFO and LRU fault on every reference, because the page evicted is always the next one needed. OPT evicts the page needed furthest in the future, so after the first pass it faults only about once every nine references.

At 5 ms per fault, LRU spends **0.5** s faulting with 9 frames and **0.05** s with 10. One frame less makes the loop 10 times slower: thrashing is a cliff, not a slope.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 14-10.1a | VPN[1] | 513 | — |
| 14-10.1b | VPN[0] | 2 | — |
| 14-10.1c | offset | 2748 | — |
| 14-10.2a | PTEs per page | 512 | — |
| 14-10.2b | VPN bits per level | 9 | bits |
| 14-10.2c | levels | 3 | — |
| 14-10.2d | flat Sv39 table | 1 | GiB |
| 14-10.3a | reach, 64 × 4 KiB | 256 | KiB |
| 14-10.3b | reach, 2048 × 4 KiB | 8 | MiB |
| 14-10.3c | reach, 2048 × 2 MiB | 4 | GiB |
| 14-10.4a | cause, store page fault | 15 | — |
| 14-10.4b | cause, ecall from U | 8 | — |
| 14-10.4c | cause, supervisor timer interrupt | 0x80000005 | — |
| 14-10.4d | vector offset, machine external | 0x2C | — |
| 14-10.5a | physical address (a) | 0x40001234 | — |
| 14-10.5b | PTE reads (a) | 1 | — |
| 14-10.5c | cause (b) | 13 | — |
| 14-10.5d | cause (c) | 15 | — |
| 14-10.5e | cause (d) | 13 | — |
| 14-10.5f | physical address (e) | 0x2468A020 | — |
| 14-10.5g | PTE reads (e) | 2 | — |
| 14-10.6a | overhead with L2 TLB | 0.26 | cycles |
| 14-10.6b | overhead without | 1.2 | cycles |
| 14-10.7a | page-table pages | 6 | — |
| 14-10.7b | page-table memory | 24 | KiB |
| 14-10.7c | heap megapages | 3 | — |
| 14-10.7d | memory mapped beyond the heap | 3 | MiB |
| 14-10.7e | page-table pages with megapages | 3 | — |
| 14-10.8a | misses, 1024 entries | 1024 | — |
| 14-10.8b | misses, 1023 entries | 1048576 | — |
| 14-10.9a | VIPT limit, 8-way | 32 | KiB |
| 14-10.9b | VIPT limit, 12-way | 48 | KiB |
| 14-10.9c | VIPT limit, 16-way | 64 | KiB |
| 14-10.9d | VIPT limit, 8-way, 16 KiB pages | 128 | KiB |
| 14-10.10a | FIFO, 3 frames | 9 | — |
| 14-10.10b | FIFO, 4 frames | 10 | — |
| 14-10.10c | LRU, 3 frames | 10 | — |
| 14-10.10d | LRU, 4 frames | 8 | — |
| 14-10.10e | OPT, 3 frames | 7 | — |
| 14-10.10f | OPT, 4 frames | 6 | — |
| 14-10.11a | overhead, 64 entries | 0.064 | % |
| 14-10.11b | overhead, with 2048 more | 2.112 | % |
| 14-10.12a | FIFO, 9 frames | 100 | — |
| 14-10.12b | LRU, 9 frames | 100 | — |
| 14-10.12c | OPT, 9 frames | 20 | — |
| 14-10.12d | FIFO, 10 frames | 10 | — |
| 14-10.12e | LRU, 10 frames | 10 | — |
| 14-10.12f | OPT, 10 frames | 10 | — |
| 14-10.12g | time faulting, 9 frames, LRU | 0.5 | s |
| 14-10.12h | time faulting, 10 frames, LRU | 0.05 | s |
