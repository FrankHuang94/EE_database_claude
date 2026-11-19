# Problems 05-08 · Data Structures and Algorithms You Will Need

Chapter: [05-08](../chapters/05-08-data-structures-and-algorithms.md) · Worked solutions: [05-08 solutions](../solutions/05-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $\log$ without a base means $\log_2$. Count operations exactly where asked, then state the Big-O class. Solutions use Python or C, whichever is clearer.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 05-08.1 [A]

**Counting steps.** For $n = 1000$, how many times does the innermost statement run in each fragment, and what is each fragment's Big-O class?

```c
// fragment
/* (a) */ for (int i = 0; i < n; i++) for (int j = 0; j < i; j++) work();
/* (b) */ for (int m = n; m > 0; m /= 2) work();
/* (c) */ for (int i = 0; i < n; i++) for (int k = 1; k < n; k *= 2) work();
```

### Problem 05-08.2 [A]

**Choosing a structure.** Name the most suitable data structure, and its key operation's cost, for: (a) bytes from a UART interrupt to the main loop; (b) the next timer to expire among thousands; (c) looking up a device by its 64-bit serial number; (d) listing log entries between two timestamps; (e) an undo history.

### Problem 05-08.3 [A]

**Tracing binary search.** Search for 37 and then for 40 in the sorted array `[3, 8, 15, 21, 29, 37, 44, 52, 60]`, using `mid = lo + (hi - lo) / 2` on the inclusive range `[lo, hi]`. List the elements compared and count the comparisons. What is the maximum for 9 elements?

### Problem 05-08.4 [B]

**Sizing a sensor buffer.** An SPI sensor delivers 6-byte samples at 4 kHz into a ring buffer; the consumer can stall for up to 12 ms. (a) What capacity is needed, rounded up to a power of two? (b) The buffer uses free-running `uint32_t` byte counters. After how long do they wrap, and does it matter?

### Problem 05-08.5 [B]

**A linked list in C.** Write `push_front`, an in-place `reverse` and `free_list` for a singly linked list of `int`. Build the list 1, 2, 3, 4, 5 (in that order of value from head to tail), reverse it, print it, and free it. How many `next` pointers does reversal rewrite?

### Problem 05-08.6 [B]

**A stack at work.** Using a stack, check whether brackets are balanced in `{[()()]}`, `([)]`, `((` and `a[i] = b(c[j])`. Why is a stack the right structure?

### Problem 05-08.7 [B]

**How full may a hash table get?** A linear-probing table has 1024 slots. (a) At what load factor does the expected unsuccessful search reach 10 probes? (b) How many entries is that? (c) What is the expected successful-search cost there, with linear probing and with separate chaining?

### Problem 05-08.8 [B]

**Heap operations by hand.** Insert 7, 3, 9, 1 and 5, in that order, into an empty min-heap stored in an array. Show the array after each insertion, then after one removal of the minimum.

### Problem 05-08.9 [B]

**Merge sort's comparisons.** (a) Solve $T(n) = 2T(n/2) + n$, $T(1) = 0$, for $n = 16$. (b) The exact worst case of merge sort is $n\lceil\log n\rceil - 2^{\lceil\log n\rceil} + 1$ comparisons. Evaluate it for $n = 16$, and find an input of 16 elements that needs that many comparisons with the chapter's implementation.

### Problem 05-08.10 [C]

**The lower bound for small n.** (a) Compute $\lceil\log_2 n!\rceil$ for $n$ = 5, 12 and 100, and compare with Stirling's estimate $n\log_2 n - n\log_2 e$. (b) For $n = 12$, how many comparisons does merge sort need in the worst case, and how far is that from the lower bound?

### Problem 05-08.11 [C]

**Counting sort for ADC codes.** One million 12-bit ADC codes must be sorted (to compute percentiles). (a) Compare the step counts of counting sort and merge sort. (b) How much memory do the counters take with `uint32_t`? (c) Implement counting sort in C for a small array and verify it, and use the counts to find the median without sorting.

### Problem 05-08.12 [C]

**A queue from two stacks.** A queue can be built from an "inbox" stack (for enqueues) and an "outbox" stack (for dequeues): to dequeue, pop from the outbox, first moving every inbox element into it if the outbox is empty. (a) Enqueue 1 to 8, dequeue 3 times, enqueue 9, then dequeue everything. Count element moves between stacks. (b) Show that every operation is $O(1)$ amortized.

### Problem 05-08.13 [B]

**Recursion on a tree.** (a) Insert the keys 8, 3, 10, 1, 6, 14, 4, 7, 13, in that order, into an empty binary search tree. Sketch the tree, and give its pre-order, in-order and post-order traversals and its height (the number of levels). (b) Write a recursive function that counts the keys lying in a range $[lo, hi]$, visiting only subtrees that can contain such keys, and apply it to $[4, 10]$. (c) If the same nine keys arrive in increasing order, what is the tree's height, and how many stack frames does a recursive in-order traversal hold at its deepest (count the call made on an empty child)? (d) A microcontroller has 2 KB of stack free for a traversal whose frames take 32 bytes each. What is the tallest tree it can walk recursively?

---

## Objective coverage

| Learning objective (chapter 05-08) | Problems |
|---|---|
| 1. Big-O and counting operations | 1, 9, 10, 12 |
| 2. Linear structures | 2, 4, 5, 6, 12 |
| 3. Hash tables | 2, 7 |
| 4. Trees, heaps and tries | 2, 8, 13 |
| 5. Searching and sorting | 3, 9, 10, 11 |
