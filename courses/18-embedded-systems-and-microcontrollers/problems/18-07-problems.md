# Problems 18-07 · RTOS Concepts

Chapter: [18-07](../chapters/18-07-rtos-concepts.md) · Worked solutions: [18-07 solutions](../solutions/18-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Tasks are periodic with implicit deadlines ($D_i = T_i$) unless stated, run on one core under preemptive fixed priority, and are written $(C_i, T_i)$. Rate-monotonic (RM) priorities give shorter periods higher priority. "Blocking" $B_i$ is the longest time a task can be kept from running by lower-priority work: a critical section on a mutex it needs, and under the ceiling protocol also one on any mutex whose ceiling is at or above its priority (§3.3). Problems marked *(lab)* can be checked with `labs/18-07-lab/rtsched.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 18-07.1 [A]

**A quick test.** Four tasks are (2, 10), (3, 15), (5, 30) and (4, 40) ms. (a) Order them by RM priority. (b) Compute $U$ and the Liu & Layland bound for four tasks. (c) What can you conclude?

### Problem 18-07.2 [A]

**Ticks and switches.** A kernel ticks at 1 kHz with a 4 µs tick handler and makes 1500 context switches a second at 2 µs each. (a) What fraction of the CPU does the kernel take? (b) How many cycles is one switch at 64 MHz? (c) A task calls `delay(5)` (five ticks) at a random moment. Between what limits does the delay actually last, and why?

### Problem 18-07.3 [A]

**Choosing the primitive.** Name the best kernel object for each, and say why: (a) an ADC interrupt tells a processing task that a block is ready; (b) three tasks share one SPI flash; (c) a sensor task hands 32-byte records to a logger task; (d) a pool of four identical DMA channels is shared by any task that needs one; (e) a task must wait until both "GPS fix" and "battery OK" have happened. (f) Task A takes mutex X then mutex Y; task B takes Y then X. What can happen, and what are two fixes?

### Problem 18-07.4 [B]

**Response times with blocking.** *(lab)* Four tasks are (1, 5), (2, 8), (4, 20) and (5, 40) ms under RM priorities. Task 2 (period 8) and task 4 (period 40) share a mutex S under the priority-ceiling protocol: task 2 holds it for its last 1 ms, task 4 for its last 2 ms. (a) Compute $U$. (b) What is each task's blocking term? (c) Compute every response time and check the deadlines. (d) A simulation with all tasks released together reports smaller worst cases for tasks 2 and 3. Why?

### Problem 18-07.5 [B]

**The worst two-task set.** Task 1 is (4, 10) and task 2 has period 14 under RM. (a) Find the largest $C_2$ for which task 2 meets its deadline. (b) What is $U$ then, and how does it compare with the two-task bound? (c) Why is this set close to the worst case of the derivation in §3.2?

### Problem 18-07.6 [B]

**RM or EDF.** *(lab)* Three tasks are (1, 3), (2, 5) and (2, 8) ms. (a) Compute $U$. (b) Is the set RM-schedulable? Show the iteration. (c) Is it EDF-schedulable? (d) Over 10 hyperperiods, how many deadlines does RM miss, and what are the worst EDF response times?

### Problem 18-07.7 [B]

**Two medium tasks.** *(lab)* One-shot jobs (ms): L (lowest priority) starts at 0 and holds mutex S for 3, then runs 1. H (highest) arrives at 1, needs S at once for 1, then runs 2. M1 arrives at 2 and computes 5; M2 (above M1, below H) arrives at 3 and computes 4. Neither M uses S. (a) Find H's response with no protocol, drawing the timeline. (b) With priority inheritance. (c) What is the analytical bound on H's response with inheritance?

### Problem 18-07.8 [B]

**A byte queue.** A UART at 115 200 baud (8N1) delivers bytes continuously through an interrupt into a queue; the consuming task can be held off for up to 12 ms by higher-priority work. (a) How many bytes arrive in 12 ms? (b) How many queue slots are needed? (c) What would you change if the RAM is not available?

### Problem 18-07.9 [B]

**A task's stack.** A task's deepest call chain uses 640 bytes. It uses the FPU, so an interrupt pushes a 26-word frame onto its stack, and the kernel saves R4–R11 and S16–S31 there on a switch. (a) What is the worst-case stack use? (b) With 25% margin, rounded up to a multiple of 8 bytes, what stack would you allocate? (c) What do five such tasks need? (d) Why does an interrupt's own call chain not appear in the task's stack?

### Problem 18-07.10 [C]

**Superloop or RTOS.** A superloop calls: sensor read (0.5 ms), display update (up to 8 ms), log write (up to 25 ms) and communications (up to 2 ms). A button event must be acted on within 5 ms; its interrupt sets a flag that the loop checks once per iteration. (a) What is the worst-case latency, and is the requirement met? (b) In an RTOS design the button is handled by the highest-priority task (0.4 ms), which shares the SPI bus with the display task under a mutex with priority inheritance; the display holds the bus for at most 1 ms at a time. Interrupts take at most 0.3 ms in any 5 ms. What is the worst-case response? (c) What else could fix the superloop without an RTOS, and at what cost?

### Problem 18-07.11 [C]

**A wearable's task set.** *(lab)* Four tasks (ms): BLE servicing (2, 7.5), IMU sampling (1.5, 10), PPG processing (6, 40) and UI (10, 100). IMU and PPG share the I²C bus under a priority-ceiling mutex: IMU holds it for its last 1.2 ms, PPG for its first 3 ms. (a) Assign RM priorities and compute $U$ and the bound. (b) Find each task's blocking and response time. (c) A colleague replaces the mutex by disabling interrupts during each I²C transfer. What happens to BLE's response time? (d) BLE must actually respond within 3 ms of its release (deadline 3 ms, period 7.5 ms). Which design meets it, and what does this say about disabling interrupts?

---

## Objective coverage

| Learning objective (chapter 18-07) | Problems |
|---|---|
| 1. What a kernel adds and costs | 2, 9, 10 |
| 2. RM priorities and utilization bounds | 1, 5, 11 |
| 3. Exact response-time analysis | 4, 6, 10, 11 |
| 4. Fixed priority against EDF | 6 |
| 5. Synchronization and priority inversion | 3, 4, 7, 11 |
| 6. Queues, stacks and deadlock | 3, 8, 9 |
