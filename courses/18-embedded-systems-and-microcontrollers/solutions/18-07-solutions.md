# Solutions 18-07 · RTOS Concepts

Problems: [18-07 problem set](../problems/18-07-problems.md) · Chapter: [18-07](../chapters/18-07-rtos-concepts.md). Every number below is recomputed by [verify_18_07.py](../verify/verify_18_07.py).

---

## Solutions

### Solution 18-07.1

(a) By period: 10, 15, 30, then 40 ms, highest priority first.

(b) $U = 2/10 + 3/15 + 5/30 + 4/40$ = **0.667**; the bound is $4(2^{1/4} - 1)$ = **0.757**.

(c) $U$ is below the bound, so the set is RM-schedulable; no further analysis is needed.

### Solution 18-07.2

(a) $1000 \times 4\ \mu\text{s} + 1500 \times 2\ \mu\text{s} = 7$ ms per second = **0.7** %.

(b) $2\ \mu\text{s} \times 64\ \text{MHz}$ = **128** cycles.

(c) Between **4** and **5** ms. The kernel counts tick interrupts, not time: if `delay(5)` is called just before a tick, the first of the five ticks arrives almost at once, so the task waits only a little over 4 tick periods. A delay of $n$ ticks therefore lasts between $n - 1$ and $n$ periods. Ask for one tick more than the minimum you need, or use a hardware timer for precise delays.

### Solution 18-07.3

(a) A **binary semaphore** or a direct-to-task notification given from the interrupt (interrupt-safe call): signalling, no ownership.

(b) A **mutex** (with priority inheritance), or a single flash-owner task fed by a queue: mutual exclusion with an owner.

(c) A **queue** of 32-byte items: it copies the data and transfers ownership, with blocking on full and empty.

(d) A **counting semaphore** initialized to 4: each taker gets one channel, the fifth waits.

(e) **Event flags** (an event group) with "wait for all": one wait for several conditions.

(f) **Deadlock:** A holds X and waits for Y while B holds Y and waits for X, and neither ever proceeds. Fixes: take mutexes in one global order (X before Y) in every task; or use the priority-ceiling protocol; or combine X and Y under one lock. Timeouts on takes turn a hang into a detectable error.

### Solution 18-07.4

(a) $1/5 + 2/8 + 4/20 + 5/40$ = **0.775**.

(b) RM priorities, highest first: task 1 (5), task 2 (8), task 3 (20), task 4 (40). The ceiling of S is task 2's priority. Task 1 is above the ceiling, so 0. Task 2 can wait for task 4's 2 ms section, so **2** ms. Task 3 is below the ceiling and can also be held off by task 4's section, so **2** ms. Task 4 has nothing below it, so 0.

(c) $R_1$ = **1** ms. $R_2 = 2 + 2 + \lceil R/5 \rceil$: $4 \to 5 \to 5$, so **5** ms ≤ 8. $R_3 = 4 + 2 + \lceil R/5\rceil + 2\lceil R/8\rceil$: $6 \to 10 \to 12 \to 13 \to 13$, so **13** ms ≤ 20. $R_4 = 5 + \lceil R/5\rceil + 2\lceil R/8\rceil + 4\lceil R/20\rceil$: $5 \to 12 \to 16 \to 17 \to 19 \to 19$, so **19** ms ≤ 40. All deadlines are met.

(d) Blocking needs a particular phasing: task 4 must already hold S when task 2 (or 3) is released, together with all higher-priority tasks. With synchronous release, task 4 starts last and never holds S at the critical instant, so the simulation reports $R_2$ = **3** and $R_3$ = **8** ms. Analysis covers phasings that a test may never produce.

### Solution 18-07.5

(a) $R_2 = C_2 + 4\lceil R_2/10\rceil \le 14$. If $R_2 \le 10$: $C_2 + 4 \le 10$, so $C_2 \le 6$. If $10 < R_2 \le 14$: $C_2 + 8 \le 14$, again $C_2 \le 6$. So $C_2$ = **6** ms (then $R_2$ = 10 ms).

(b) $U = 4/10 + 6/14$ = **0.8286**, just above the two-task bound $2(\sqrt2 - 1)$ = **0.8284**.

(c) Here $T_2/T_1 = 1.4$, close to the worst ratio $1 + f = \sqrt2$, and $C_1 = T_2 - T_1$ exactly, the worst $C_1$ of the derivation. So $U = (1 + f^2)/(1 + f)$ with $f = 0.4$, a hair above the minimum at $f = 0.414$.

### Solution 18-07.6

(a) $1/3 + 2/5 + 2/8$ = **0.983**.

(b) $R_3 = 2 + \lceil R/3\rceil + 2\lceil R/5\rceil$: $2 \to 5 \to 6 \to 8 \to 9$ > 8. **No**: the third task misses.

(c) **Yes**, because $U \le 1$.

(d) RM misses **20** deadlines (all the third task's) in 10 hyperperiods of 120 ms. EDF misses none, with worst responses of **1**, **4** and **7** ms.

### Solution 18-07.7

(a) L holds S from 0. H arrives at 1, needs S and blocks. M1 arrives at 2 and preempts L; M2 arrives at 3 and preempts M1. M2 runs 3–7, M1 runs 7–11 (it ran 2–3 before), L finishes S at 12, and H runs 12–15. Response **14** ms.

(b) From 1, L runs at H's priority, so neither M can preempt it. L releases S at 3, and H runs 3–6. Response **5** ms.

(c) $B_H$ = L's critical section, 3 ms, so $R_H \le C_H + B_H = 3 + 3$ = **6** ms.

### Solution 18-07.8

(a) 115 200 baud, 8N1, is 11 520 bytes/s: $11\,520 \times 0.012$ = **138.2** bytes.

(b) $\lfloor 138.2 \rfloor + 1$ = **139** slots.

(c) Raise the consumer's priority or shorten what holds it off; use the UART's FIFO with RTS/CTS flow control so the sender pauses; or let DMA write into a ring buffer (18-04) and wake the task by notification, so the CPU never handles individual bytes.

### Solution 18-07.9

(a) $640 + 104 + 32 + 64$ = **840** bytes (call chain, FPU exception frame, R4–R11, S16–S31).

(b) $840 \times 1.25 = 1050$, rounded up to **1056** bytes.

(c) $5 \times 1056$ = **5280** bytes.

(d) On Cortex-M, tasks run on the process stack (PSP) and handlers on the main stack (MSP). Exception entry stacks the frame on the interrupted task's PSP, but the handler's own calls use the MSP, so only the frame lands on the task's stack. The MSP must be sized for the deepest interrupt nesting.

### Solution 18-07.10

(a) The flag can be set just after the loop checked it, so the next check comes a whole iteration later: $0.5 + 8 + 25 + 2$ = **35.5** ms. That is far beyond 5 ms, so the requirement is **not met**.

(b) $R = 0.4 + 1.0 + 0.3$ = **1.7** ms (the task's own time, one display critical section, and interrupts), comfortably within 5 ms.

(c) Checking the flag between the four functions still leaves the 25 ms log write, which fails. The log write must be broken into slices of a few milliseconds (a state machine), or the button action done in the interrupt handler itself if it is short. Both are possible, but they spread timing concerns through the code; this is the point at which an RTOS starts to pay.

### Solution 18-07.11

(a) BLE (7.5) > IMU (10) > PPG (40) > UI (100). $U = 2/7.5 + 1.5/10 + 6/40 + 10/100$ = **0.667**, under the four-task bound **0.757** (which ignores blocking).

(b) The I²C ceiling is IMU's priority. BLE: $B$ = 0, so $R$ = **2.0** ms. IMU: $B$ = 3 ms (PPG's section), so $R = 1.5 + 3 + \lceil R/7.5\rceil \cdot 2$: $4.5 \to 6.5$, giving **6.5** ms ≤ 10. PPG: $B$ = 0, and $R = 6 + 2\lceil R/7.5\rceil + 1.5\lceil R/10\rceil$: $6 \to 9.5 \to 11.5 \to 13$, giving **13.0** ms ≤ 40. UI: **28.5** ms ≤ 100.

(c) Disabling interrupts blocks *every* task, BLE included, for up to 3 ms: $R_{BLE} = 2 + 3$ = **5.0** ms.

(d) With the mutex, BLE responds in 2.0 ms and meets 3 ms. With interrupts disabled, 5.0 ms misses it. A long section with interrupts off is a blocking term for the most urgent work in the system, even work that never touches the shared resource. Keep such sections to microseconds, and use mutexes (or a bus-owner task) for anything longer.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 18-07.1a | utilization | 0.667 | — |
| 18-07.1b | Liu & Layland bound, n = 4 | 0.757 | — |
| 18-07.2a | kernel overhead | 0.7 | % |
| 18-07.2b | cycles per switch | 128 | — |
| 18-07.2c | shortest delay(5) | 4 | ms |
| 18-07.2d | longest delay(5) | 5 | ms |
| 18-07.4a | utilization | 0.775 | — |
| 18-07.4b | blocking, task 2 | 2 | ms |
| 18-07.4c | blocking, task 3 | 2 | ms |
| 18-07.4d | R_1 | 1 | ms |
| 18-07.4e | R_2 | 5 | ms |
| 18-07.4f | R_3 | 13 | ms |
| 18-07.4g | R_4 | 19 | ms |
| 18-07.4h | simulated R_2, synchronous release | 3 | ms |
| 18-07.4i | simulated R_3, synchronous release | 8 | ms |
| 18-07.5a | largest C_2 | 6 | ms |
| 18-07.5b | utilization | 0.8286 | — |
| 18-07.5c | two-task bound | 0.8284 | — |
| 18-07.6a | utilization | 0.983 | — |
| 18-07.6b | RM misses in 10 hyperperiods | 20 | — |
| 18-07.6c | EDF worst response, task 1 | 1 | ms |
| 18-07.6d | EDF worst response, task 2 | 4 | ms |
| 18-07.6e | EDF worst response, task 3 | 7 | ms |
| 18-07.7a | H's response, no protocol | 14 | ms |
| 18-07.7b | H's response, inheritance | 5 | ms |
| 18-07.7c | bound with inheritance | 6 | ms |
| 18-07.8a | bytes in 12 ms | 138.2 | — |
| 18-07.8b | queue slots | 139 | — |
| 18-07.9a | worst-case stack | 840 | bytes |
| 18-07.9b | allocated stack | 1056 | bytes |
| 18-07.9c | five tasks | 5280 | bytes |
| 18-07.10a | superloop worst latency | 35.5 | ms |
| 18-07.10b | RTOS worst response | 1.7 | ms |
| 18-07.11a | utilization | 0.667 | — |
| 18-07.11b | Liu & Layland bound, n = 4 | 0.757 | — |
| 18-07.11c | R_BLE | 2.0 | ms |
| 18-07.11d | R_IMU | 6.5 | ms |
| 18-07.11e | R_PPG | 13.0 | ms |
| 18-07.11f | R_UI | 28.5 | ms |
| 18-07.11g | R_BLE with interrupts disabled | 5.0 | ms |
