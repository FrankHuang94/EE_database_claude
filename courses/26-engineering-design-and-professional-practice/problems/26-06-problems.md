# Problems 26-06 · Engineering Team Structures and Sizing

Chapter: [26-06](../chapters/26-06-team-structures-and-sizing.md) · Worked solutions: [26-06 solutions](../solutions/26-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Flat-team output $O(n) = n[1 - c(n - 1)]$; hierarchical output $km[1 - c(m - 1)][1 - c_x(k - 1)]$ for $k$ teams of $m$ engineers, each team with a lead who does not count toward output.
- Coordination costs, wages, loads and ramp times are assumed.

---

## Problems

### Problem 26-06.1 [A]

**Channels.** (a) Find the pairwise channels for flat teams of 8, 25 and 200. (b) The 200 engineers are organized as 8 teams of 25 (each including its lead), and the 8 leads coordinate among themselves. How many channels now, and by what factor fewer than flat?

### Problem 26-06.2 [A]

**Which structure?** Recommend a functional, program or matrix organization (or a platform team) for each case, with one reason: (a) a startup building its first chip; (b) a company running six SoC programs that share a CPU cluster, interconnect and physical-design flow; (c) a large company whose program teams have each built their own, incompatible verification environments; (d) a company with one flagship product line and a stable roadmap.

### Problem 26-06.3 [B]

**A flat team's limit.** With a coordination cost $c$ = 0.04 per colleague: (a) find the most productive flat team and its output; (b) find the size at which output falls to zero; (c) find the output of a 20-person flat team.

### Problem 26-06.4 [B]

**Another hierarchy.** Compare Example 26-06.2's 90-person hierarchy (51.8 FTE) with 12 teams of 6 engineers plus a lead each (84 people), with $c$ = 0.03 and a cross-team cost $c_x$ = 0.015 per other team. Find (a) each member's productive fraction, (b) a team's output, (c) the cross-team factor, (d) the total output and the output per head.

### Problem 26-06.5 [B]

**Brooks's law again.** A team of 8 ($c$ = 0.02) has 60 person-months of work left. (a) How long without help? (b) How long if 4 engineers join now, each unproductive for 2 months and taking half of an experienced engineer's time meanwhile? (c) Below how much remaining work would adding them lengthen the project?

### Problem 26-06.6 [B]

**Layers for 1,500 engineers.** Find the managers at each level, the number of layers and the total number of managers for spans of 7 and 10, and compare with $N/(s - 1)$.

### Problem 26-06.7 [B]

**Physical-design staffing.** Physical design needs 20, 30, 50, 60, 60, 50, 30 and 20 engineers in eight quarters. Employees cost $80,000 a quarter and contractors $100,000. Find (a) the newsvendor base, (b) the cost with that base, (c) the cost with a base of 30, (d) the cost with only employees (staffed for the peak), and (e) with only contractors.

### Problem 26-06.8 [B]

**Keep the team or outsource the work?** An in-house DFT team costs $150,000 a month whether busy or not; a design-services firm charges $200,000 per month of work. Over 18 months the expected work is 14 months. (a) Compare the costs. (b) Find the break-even utilization and the number of work-months below which outsourcing is cheaper.

### Problem 26-06.9 [C]

**Conway's law in a chip.** An SoC has a CPU cluster, a GPU, a neural engine, a memory controller and an I/O subsystem. Two teams share ownership of the cache-coherent interconnect, and the memory controller's physical design is done by a team in another time zone. (a) Where would you expect integration bugs, and why? (b) Propose an organizational change and an architectural change that would each reduce the risk.

### Problem 26-06.10 [B]

**A 2 nm design-cost estimate.** IBS, as cited in Arm's 2023 prospectus, put the cost of designing a 2 nm chip at about $725 M [R-019]. If 75% of the cost is engineering labor at a loaded $350,000 per engineer-year over 3 years, find the engineer-years and the average headcount.

### Problem 26-06.11 [C]

**A verification staffing ramp.** Verification needs 600 person-months over a 30-month program, with headcount rising linearly from 0 to a peak at month 18 and falling linearly to 0 at month 30. (a) Find the peak headcount. (b) Find the hiring rate needed to reach the peak by month 18. (c) Why is reaching that peak from employees alone risky?

### Problem 26-06.12 [A]

**Two bosses.** List two advantages and two disadvantages of a matrix organization for a chip company, and one practice that reduces the disadvantages.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Disciplines and staffing profiles | 11 |
| 2. Communication overhead and team size | 1, 3, 4 |
| 3. Brooks's law | 5 |
| 4. Organization structures and layers | 2, 6, 9, 12 |
| 5. Employees, contractors and design services | 7, 8, 10 |
