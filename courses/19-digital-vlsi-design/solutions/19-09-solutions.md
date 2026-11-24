# Solutions 19-09 · Layout, Design Rules and Standard Cells

Problems: [19-09 problem set](../problems/19-09-problems.md) · Chapter: [19-09](../chapters/19-09-layout-and-standard-cells.md). Every number below is recomputed by [verify_19_09.py](../verify/verify_19_09.py).

---

## Solutions

### Solution 19-09.1

A contact is 2λ wide and active must enclose it by 1λ on each side: $2 + 2 \times 1$ = **4**λ, more than the 3λ minimum active width. Contacted regions are therefore wider than the bare transistor, which is one reason transistors are often drawn at the contacted width.

### Solution 19-09.2

Contacted: $2 + 2 \times 3 + 2$ = **10**λ. Uncontacted: unchanged at **5**λ (it involves no contact).

### Solution 19-09.3

With the stack fixed as A-B-C, the pull-down graph is a chain, so only **2** orderings walk it: A-B-C and C-B-A. The pull-up (three parallel PMOS) accepts any order. The designer can gain freedom by reordering the series stack itself: series transistors can be stacked in any order without changing the logic (though the order matters for delay, 19-03 §3.3).

### Solution 19-09.4

**4** of 24; one is A-B-C-D. The pull-down is (A in series with B) in parallel with C and with D, between the output and ground; with n the node between A and B, the walk is out→A→n→B→ground→C→out→D→ground. The pull-up is (A ∥ B) in series with C and then D, from VDD to the output; with m the node after the A–B pair and p the node between C and D, the walk starts at m: m→A→VDD→B→m→C→p→D→out. (Starting at VDD fails: after A and B the walk is back at VDD, which C does not touch.) The valid orderings all keep A and B adjacent and C and D adjacent.

### Solution 19-09.5

**8**, the same as the AOI22, because the OAI22's pull-down network is the AOI22's pull-up and vice versa: the pair of graphs is the same, only swapped between NMOS and PMOS.

### Solution 19-09.6

(a) $500/120$ = **4.17** mm².

(b) $30\,000 \times 20.02\ \mu\text{m}^2$ = **0.601** mm² of cells; at 65%, **0.924** mm²; at 80%, **0.751** mm².

### Solution 19-09.7

(a) Each end needs enclosure, contact and contact-to-gate spacing, $1 + 2 + 2$ = 5λ; three gates are 6λ and two uncontacted gaps 6λ: **22**λ.

(b) Each internal gap becomes contact-to-gate, contact, contact-to-gate, 6λ: $10 + 6 + 12$ = **28**λ.

Leaving the internal nodes uncontacted saves **21** %.

### Solution 19-09.8

(a) $3.0/4.0$ = **75** %. (b) $3.0/0.85$ = **3.53** mm², **11.8** % smaller, at the cost of harder routing.

### Solution 19-09.9

(a) A connected graph has an Euler path if and only if it has zero or two nodes of odd degree (an Euler circuit if zero).

(b) In the AOI22 pull-down, the output and ground each connect to two transistors and each internal node to two: **0** odd-degree nodes. The pull-up is the same, with **0**. With no odd nodes, every Euler path is a closed circuit, which is why the valid orderings of Example 3 return to their starting node.

(c) An all-series network is a chain whose end nodes have degree 1 and internal nodes degree 2: exactly two odd nodes, at the ends, so the only Euler paths run from one end to the other, in either direction: two orderings.

### Solution 19-09.10

(a) Gate area $0.150 \times 0.420$ = **0.063** µm², so the metal may cover $400 \times 0.063$ = **25.2** µm², a line of $25.2/0.14$ = **180** µm of top area.

(b) Counting sidewalls, a line of length $\ell$ and width 0.14 µm exposes $2(\ell + 0.14) \times 0.35$ µm² of sidewall. Setting that to 25.2 µm² gives $\ell + 0.14 = 36$, so $\ell$ = **35.9** µm, five times shorter. Small gates driven over long routes are the usual antenna violations, which is why routers insert diodes and layer jumps.

### Solution 19-09.11

(a) Pull-down: one diffusion strip, gate A then gate B, with the output contact at one end and ground at the other. Pull-up: one strip with VDD contacts at both ends and the output contact in the middle, gates A and B on either side of it; a vertical metal strap joins the two output contacts, and each input's poly stripe crosses both strips.

(b) Each end needs enclosure, contact and contact-to-gate space, $1 + 2 + 2 = 5\lambda$. Pull-down (two gates, one uncontacted gap of 3λ): $2 \times 5 + 2 \times 2 + 3$ = **17** λ. Pull-up (two gates, one contacted gap of $2 + 2 + 2 = 6\lambda$): $2 \times 5 + 2 \times 2 + 6$ = **20** λ. The pull-up's middle contact sets the width.

(c) $17 \times 0.075$ = **1.275** µm and $20 \times 0.075$ = **1.50** µm.

### Solution 19-09.12

(a) **DRC**: a spacing rule is violated. (b) **LVS**: the extracted connectivity has an open that the schematic does not, so the netlists differ. (c) **Parasitic extraction with static timing**: the layout is legal and matches the schematic; only the extracted RC reveals the slower path. (d) **Antenna**: a manufacturing-time charge rule, separate from DRC's geometry. (e) **LVS** with parameter checking compares device sizes, so it flags the width mismatch. (f) **None** of them: every physical check compares the layout with the schematic or with rules, so a wrong schematic passes; only verification (19-13) catches it.

### Solution 19-09.13

(a) $3.7536/2.72$ = **1.38** µm, which is $1.38/0.46$ = **3** sites.

(b) The λ estimate of 1.50 µm (Problem 11) is about **8.7** % wider than the real cell. (c) The real transistors are 0.65 µm (NMOS) and 1.0 µm (PMOS), as in 19-03. Real rules are not multiples of one λ: each layer has its own minimum widths and spacings, contacts can be shared and placed tighter than a scalable rule allows, and library designers spend months compacting each cell, so production cells beat λ-rule estimates.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 19-09.1a | minimum contacted active width | 4 | λ |
| 19-09.2a | contacted pitch with 3λ spacing | 10 | λ |
| 19-09.2b | uncontacted pitch | 5 | λ |
| 19-09.3a | valid NAND3 orderings, fixed stack | 2 | — |
| 19-09.4a | valid AOI211 orderings | 4 | — |
| 19-09.5a | valid OAI22 orderings | 8 | — |
| 19-09.6a | logic area | 4.17 | mm² |
| 19-09.6b | flip-flop cell area | 0.601 | mm² |
| 19-09.6c | flip-flop core area at 65% | 0.924 | mm² |
| 19-09.6d | flip-flop core area at 80% | 0.751 | mm² |
| 19-09.7a | strip length, end contacts only | 22 | λ |
| 19-09.7b | strip length, all nodes contacted | 28 | λ |
| 19-09.7c | saving | 21 | % |
| 19-09.8a | utilization | 75 | % |
| 19-09.8b | core area at 85% | 3.53 | mm² |
| 19-09.8c | reduction | 11.8 | % |
| 19-09.9a | odd nodes, AOI22 pull-down | 0 | — |
| 19-09.9b | odd nodes, AOI22 pull-up | 0 | — |
| 19-09.10a | gate area | 0.063 | µm² |
| 19-09.10b | allowed metal area | 25.2 | µm² |
| 19-09.10c | allowed metal-1 length | 180 | µm |
| 19-09.10d | allowed length with sidewall area | 35.9 | µm |
| 19-09.11a | pull-down strip | 17 | λ |
| 19-09.11b | pull-up strip | 20 | λ |
| 19-09.11c | pull-down strip in µm | 1.275 | µm |
| 19-09.11d | pull-up strip in µm | 1.50 | µm |
| 19-09.13a | nand2_1 width | 1.38 | µm |
| 19-09.13b | nand2_1 width in sites | 3 | — |
| 19-09.13c | λ estimate excess | 8.7 | % |
