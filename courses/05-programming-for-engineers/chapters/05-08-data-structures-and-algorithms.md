<!-- status: reviewed -->
# 05-08 · Data Structures and Algorithms You Will Need

| | |
|---|---|
| **Course** | [05 · Programming for Engineers](../README.md) |
| **University equivalent** | A first data-structures and algorithms course, as taken by EE/CE majors (Cormen, Leiserson, Rivest and Stein, *Introduction to Algorithms*, 4th ed., ch. 1–4, 6–8, 10–12; Sedgewick and Wayne, *Algorithms*, 4th ed., ch. 1–3) |
| **Prerequisites** | [05-06 C Pointers, Arrays and Memory](05-06-c-pointers-and-memory.md), [05-07 Bit Manipulation](05-07-bit-manipulation.md); [01-08 Sequences and Series](../../01-calculus-for-engineers/chapters/01-08-sequences-series-and-taylor.md) for the sums |
| **Estimated study hours** | 12 |
| **Last verified** | 2026-11-19 |

**Learning objectives.** After this chapter you can:

1. State and apply Big-O notation, derive the cost of simple algorithms by counting operations, and distinguish worst-case, average and amortized cost.
2. Implement and use the core linear structures (dynamic array, ring buffer, linked list, stack and queue) and choose among them for a given access pattern.
3. Explain how hash tables work (hashing, collisions, load factor, resizing) and predict their probe counts.
4. Describe binary search trees, heaps (priority queues) and tries, and their operation costs, and write recursive functions that build and walk a tree.
5. Derive the costs of binary search, insertion sort and merge sort, explain the $n\log n$ lower bound for comparison sorting, and choose a search or sort method for a situation.

## 1. Big picture

An algorithm is a precise recipe; a data structure is a way of organizing data so that the recipe's steps are cheap. The choice between them often matters more than the processor: looking up one of a million items takes 20 comparisons with binary search and 500,000 on average with a linear scan; sorting a million items takes about $2\times10^7$ comparisons with a good algorithm and $5\times10^{11}$ with a naive one, the difference between 20 milliseconds and 8 minutes. Engineers meet these choices everywhere, and the FE exam's Software Engineering area tests them explicitly (algorithms: sorting, searching, complexity, Big-O; data structures: lists, trees, vectors, structures, arrays; [R-001](../../../reference/research-log.md#r-001--ncees-fe-electrical-and-computer-specification)).

- **Firmware:** ring buffers carry bytes from a UART interrupt or a DMA engine to the main loop; fixed-size pools replace the heap (05-06).
- **Operating systems and schedulers:** priority queues pick the next task or timer; balanced trees and hash tables index processes, pages and files.
- **Networking:** switches and routers look up flows in hash tables and route by longest-prefix match in trie-like structures, at billions of lookups per second in hardware. **Deeper:** see companion repo *Datacenter Networking*.
- **EDA and AI software:** placement, routing and timing analysis are graph algorithms over millions of cells; inference servers schedule requests with queues and heaps.

## 2. Intuition first

**Big-O is about growth, not speed.** If a method takes time proportional to $n$, doubling the data doubles the time; if it takes time proportional to $n^2$, doubling the data quadruples it. For small $n$ anything works; for large $n$ the growth rate dominates every constant factor. Big-O notation keeps only the growth rate.

**Everyday data structures.**

- A **phone book** is a sorted array: you find a name by opening the middle and halving the search each time (binary search).
- A **stack of plates** is a stack: last in, first out.
- A **checkout line** is a queue: first in, first out. A **circular conveyor** with fixed slots is a ring buffer.
- A **coat check** is a hash table: the attendant turns your coat into a ticket number (the hash) that says exactly which hook to use, so retrieval takes the same short time however many coats there are, unless two coats were assigned the same hook (a collision).
- A **hospital triage queue** is a priority queue: the most urgent patient goes next, whatever their arrival order.

**A finance analogy, and its limits.** An exchange's order book keeps bids and offers so that the best price is always available instantly and new orders slot into place quickly: a pair of priority queues (or sorted trees) keyed by price, with first-in-first-out queues at each price level. *Where it breaks:* an order book has a specific, bounded structure (a few thousand active price levels) that real implementations exploit with arrays indexed by price; general data structures assume nothing about the keys, which is their strength and their cost.

## 3. Theory

### 3.1 Measuring cost: Big-O

**Definition.** For cost functions $f(n)$ and $g(n)$ of the input size $n$, we write $f(n) = O(g(n))$ if there are constants $c > 0$ and $n_0$ such that $f(n) \le c\,g(n)$ for all $n \ge n_0$: eventually, $f$ grows no faster than a constant multiple of $g$. Big-O is an upper bound; $\Theta(g)$ means bounded above *and* below by constant multiples of $g$ (the exact growth rate), and $\Omega(g)$ means bounded below.

**Counting operations.** To find an algorithm's cost, count the basic steps (comparisons, memory accesses, arithmetic) as a function of $n$, then keep the dominant term and drop constant factors. A loop over $n$ items is $O(n)$; two nested loops over $n$ items are $O(n^2)$; halving the problem at each step gives $O(\log n)$, because after $k$ halvings $n/2^k$ items remain, which reaches 1 when $k = \log_2 n$.

| Class | Name | Example | $n = 10^6$ at $10^9$ steps/s |
|---|---|---|---|
| $O(1)$ | constant | array index, hash lookup (average) | 1 ns |
| $O(\log n)$ | logarithmic | binary search | 20 ns |
| $O(n)$ | linear | scanning a list | 1 ms |
| $O(n\log n)$ | linearithmic | merge sort | 20 ms |
| $O(n^2)$ | quadratic | insertion sort, all pairs | 17 minutes |
| $O(2^n)$ | exponential | trying all subsets | far beyond the age of the universe |

**Worst case, average case, amortized.** The **worst case** bounds every input; the **average case** assumes a distribution of inputs (often "random"); the **amortized** cost averages over a *sequence* of operations, where rare expensive steps are paid for by many cheap ones. The doubling buffer of Example 05-06.5 is the standard example: one append occasionally copies everything, but $n$ appends cost $O(n)$ in total, so each is $O(1)$ amortized.

> **Math refresher — the sums behind the costs.** An arithmetic series $1 + 2 + \cdots + n = n(n+1)/2$ is $\Theta(n^2)$: it is why a loop that does $i$ steps at iteration $i$ is quadratic. A geometric series $1 + 2 + 4 + \cdots + 2^k = 2^{k+1} - 1 < 2 \cdot 2^k$ is dominated by its last term: it is why doubling is cheap. And $\log_2 n$ answers "how many times can I halve $n$?"; changing the base only multiplies it by a constant ($\log_2 n = \ln n/\ln 2$), so Big-O writes simply $\log n$ (01-08).

**Constants still matter in practice.** Big-O hides constant factors and memory effects. An $O(n)$ scan of a contiguous array can beat an $O(\log n)$ tree search for small $n$, because the array streams through the cache while the tree chases pointers to scattered addresses (14 explains caches). Use Big-O to rule out approaches that cannot scale; measure to choose among the rest.

### 3.2 Arrays and dynamic arrays

An array stores elements contiguously, so element $i$ is found by arithmetic: $O(1)$ access (05-06). Inserting or deleting in the middle shifts every later element: $O(n)$. A **dynamic array** (C's growable buffer, Python's `list`, C++'s `std::vector`) adds amortized $O(1)$ append by geometric growth. Arrays are the default choice: compact, cache-friendly and simple. Choose something else only when an access pattern demands it.

### 3.3 Ring buffers

A **ring buffer** (circular buffer) is a fixed-size array used as a queue: a **producer** writes at the head, a **consumer** reads at the tail, and both indices wrap around to the start of the array. It never allocates memory and both operations are $O(1)$, which is why it carries data between an interrupt handler (or a DMA engine) and the main loop in nearly every embedded system.

An elegant implementation uses two **free-running unsigned counters** and a power-of-two capacity $N$:

- slot for a counter value $c$: `c & (N - 1)` (05-07's cheap modulo);
- number of stored items: `head - tail`, which is correct even after the counters wrap past $2^{32}$, by unsigned modular arithmetic (05-05);
- empty when `head == tail`; full when `head - tail == N`.

This distinguishes "full" from "empty" without wasting a slot or keeping a separate count, and with a single producer and a single consumer each counter is written by only one side, which is the basis of **lock-free** interrupt-to-main-loop queues: neither side ever waits for the other or disables interrupts. Lock-free is not care-free, though. Three conditions must hold, and a ring buffer that ignores them works in every test and fails in the field:

1. **Publish last.** The producer writes the byte *and then* advances `head`; the consumer reads the byte *and then* advances `tail`. Advancing first would let the other side use a slot that is not yet ready.
2. **Stop the compiler (and the hardware) from reordering or caching.** With ordinary variables the compiler may keep `head` in a register inside the main loop's polling loop and never see the interrupt's update, or move the data write after the `head` update, because a single-threaded program could not tell the difference. `volatile` stops the caching but does not order the non-volatile data write. The portable fix is C11's `<stdatomic.h>`: store each counter with **release** ordering (everything written before it is visible first) and load the other side's counter with **acquire** ordering (Example 05-08.2). On multi-core chips this ordering is also enforced in the hardware.
3. **Read and write each counter in one indivisible access.** A 32-bit counter on an 8- or 16-bit microcontroller is read in two or four pieces, and an interrupt between the pieces produces a torn value. There, use counters no wider than the machine word (8-bit counters allow up to 128 slots; cast `(uint8_t)(head - tail)`, because of 05-05's integer promotion), or disable the interrupt briefly around the main loop's access.

Course 18 treats interrupt-safe design in depth. When the buffer is full the producer must choose a policy: drop the new item, overwrite the oldest, or block. Example 05-08.2 implements drop-newest and counts drops, because silent data loss is the classic ring-buffer bug.

### 3.4 Linked lists

A **linked list** stores each element in a separate **node** that also holds a pointer to the next node (and, in a doubly linked list, the previous one):

```c
// fragment
typedef struct node {
    int value;
    struct node *next;          /* NULL at the end of the list */
} node_t;
```

Given a pointer to a node, inserting or removing next to it is $O(1)$: rewire two pointers, move no data. Finding an element, or the $i$th element, is $O(n)$: follow the chain. Linked lists suit queues of variable length and structures where elements must be unlinked from the middle quickly (an operating system's list of waiting tasks, for example; kernels often use **intrusive** lists, where the link pointers live inside the elements themselves, so no separate allocation is needed). Their weaknesses are a pointer of overhead per element, one allocation per node (05-06's heap concerns), and poor cache behavior because consecutive nodes may lie far apart in memory. For most sequences that are mainly appended to and scanned, a dynamic array is faster in practice.

### 3.5 Stacks and queues

A **stack** supports `push` (add on top) and `pop` (remove from the top): last in, first out (LIFO). The processor's call stack (05-06) is one; others evaluate expressions, implement undo, and drive depth-first search. A **queue** supports `enqueue` at the back and `dequeue` at the front: first in, first out (FIFO); it buffers work between producers and consumers and drives breadth-first search. Both are $O(1)$ per operation when implemented with an array (stack: grow at the end; queue: a ring buffer) or a linked list. They are **abstract data types**: defined by their operations, implementable in several ways.

### 3.6 Hash tables

A **hash table** stores key–value pairs in an array of $m$ slots and computes each key's slot from the key itself with a **hash function** $h$: slot $= h(\text{key}) \bmod m$. A good hash function spreads keys evenly, so lookups, insertions and deletions take $O(1)$ time on average, independent of the number of entries $n$. Python's `dict` and `set` are hash tables; so are the flow tables of network switches and the symbol tables of compilers.

**Hash functions.** For strings, a simple, widely used choice is **FNV-1a**: start from a fixed 32-bit "offset basis" (2,166,136,261), and for each byte XOR it in and multiply by the "FNV prime" (16,777,619), modulo $2^{32}$. Multiplication by an odd constant mixes each input bit into many output bits (05-07's bit operations at work). Hash tables need speed and spread, not cryptographic strength; for tables exposed to attackers, who could choose keys that all collide, languages use randomized (keyed) hash functions.

**Collisions are inevitable.** By the birthday argument (05-04), with $m$ slots a collision becomes likely after only about $\sqrt{m}$ keys. Two standard remedies:

- **Separate chaining:** each slot holds a linked list of the entries that hash there.
- **Open addressing with linear probing:** an entry that finds its slot taken goes to the next free slot (wrapping around); a lookup probes from the home slot until it finds the key or an empty slot.

**Load factor.** The load factor $\alpha = n/m$ controls performance. Assuming a well-mixing hash, the classic results (Knuth) are:

| Scheme | Successful search (average probes) | Unsuccessful search |
|---|---|---|
| Separate chaining | $1 + \alpha/2$ | $\alpha$ |
| Linear probing | $\tfrac12\left(1 + \dfrac{1}{1-\alpha}\right)$ | $\tfrac12\left(1 + \dfrac{1}{(1-\alpha)^2}\right)$ |

Conventions differ between texts, so state which one you use. Here the chaining figures count **key comparisons** (an unsuccessful search compares the key with every element of its chain, $\alpha$ on average; some texts add 1 for reaching the slot), while the linear-probing figures count **slots examined**, including the empty slot that ends an unsuccessful search. For linear probing at $\alpha = 0.75$: 2.5 probes for a successful search and 8.5 for an unsuccessful one; at $\alpha = 0.9$: 5.5 and 50.5. Linear probing degrades sharply as the table fills, because occupied slots clump into runs ("primary clustering"). So tables **resize**: when $\alpha$ passes a threshold (often 0.5 to 0.75 for open addressing), allocate a table twice as large and reinsert everything, which is amortized $O(1)$ per insertion by the same geometric argument as the dynamic array. Linear probing remains popular despite clustering because consecutive probes hit the same cache lines.

### 3.7 Trees, heaps and tries

A **binary search tree** (BST) stores keys in nodes with left and right children such that every key in a node's left subtree is smaller than the node's key and every key in its right subtree is larger. Search, insertion and deletion follow one path from the root: $O(h)$ for a tree of height $h$. A tree built from random insertions has $h = O(\log n)$, but inserting already-sorted keys produces a chain with $h = n$, so practical libraries use **self-balancing** trees (red-black trees, AVL trees, or B-trees with many keys per node for disks and databases) that guarantee $h = O(\log n)$. Unlike hash tables, trees keep keys in order, so they also answer "next larger key" and range queries efficiently.

A **binary heap** is a complete binary tree stored in an array, with each parent no larger than its children (a **min-heap**). Its root is the minimum. For the node at array index $i$ (counting from 0), the children are at $2i + 1$ and $2i + 2$ and the parent at $\lfloor (i - 1)/2 \rfloor$, so no pointers are needed. Insertion appends at the end and "sifts up" by swapping with the parent while smaller; removing the minimum moves the last element to the root and "sifts down". Each is $O(\log n)$, because the tree's height is $\lfloor \log_2 n \rfloor$. A heap implements a **priority queue**: timers in an operating system, events in a simulator, requests in a scheduler (Example 05-08.4).

A **trie** (prefix tree) branches on successive characters or bits of the key rather than on comparisons; a lookup costs time proportional to the key's length, not to the number of keys. Binary tries keyed on address bits are the conceptual basis of **longest-prefix-match** routing lookups, in which a router finds the most specific route covering an IP address (production routers use compressed tries in software or TCAM hardware).

### 3.8 Searching and sorting

**Linear search** checks items one by one: $n$ comparisons in the worst case, about $n/2$ on average for a present key. **Binary search** on a sorted array compares the target with the middle element and discards half. Here a **comparison** means one three-way test of the target against an element (less, equal or greater), as in the code of Problem 05-08.3; code that tests `==` and `<` separately can make two per step. If $m$ candidates remain, one comparison either finds the key or leaves at most $\lfloor m/2 \rfloor$, so after $k$ comparisons at most $\lfloor n/2^k \rfloor$ remain. The search must have ended once that number reaches 0, which happens when $2^k > n$, that is at $k = \lfloor\log_2 n\rfloor + 1$. So binary search needs at most $\lfloor\log_2 n\rfloor + 1$ comparisons: 20 for a million items, 30 for a billion. The catch is that the array must be sorted, and keeping it sorted costs $O(n)$ per insertion.

**Insertion sort** builds a sorted prefix one element at a time, shifting larger elements right to make room. Each element moves past every larger element before it, so the work equals the number of **inversions** (out-of-order pairs) plus about $n$. A random permutation has $\binom n2/2 = n(n-1)/4$ inversions on average, so insertion sort is $\Theta(n^2)$ on average and in the worst case, but $O(n)$ on input that is already nearly sorted, and very fast for small $n$, which is why real sorting libraries switch to it for short runs.

**Merge sort** splits the array in half, sorts each half recursively, and merges the two sorted halves in one linear pass. Merging two sorted lists of total length $n$ takes at most $n - 1$ comparisons: each comparison sends one element to the output, and the last element needs none. So the worst-case comparison count satisfies $T(n) = 2T(n/2) + (n - 1)$; replacing $n - 1$ by $n$ gives a slightly larger, simpler **recurrence** that bounds it from above:

$$
T(n) \le 2\,T(n/2) + n, \qquad T(1) = 0.
$$

Unrolling the bound for $n = 2^k$: level $j$ of the recursion has $2^j$ subproblems of size $n/2^j$, whose merges cost $n$ in total; there are $k = \log_2 n$ levels; so $T(n) \le n\log_2 n$. (Solving the exact recurrence gives $n\log_2 n - n + 1$ for $n = 2^k$, the worst-case formula of Problem 05-08.9; even the best case, $\tfrac12 n\log_2 n$, has the same growth.) Merge sort is $\Theta(n\log n)$ in every case. It needs $O(n)$ extra memory for merging and is **stable**: equal keys keep their original order, which matters when sorting records by one field after another.

**Quicksort** partitions around a pivot element and recurses on both sides: $O(n\log n)$ on average and in place, but $O(n^2)$ in the worst case if the pivots are consistently bad, which randomized pivot choice makes vanishingly unlikely. **Heapsort** builds a heap and repeatedly removes the maximum: $O(n\log n)$ worst case, in place, not stable. Library sorts combine these ideas (Python's `sorted` is an adaptive, stable merge sort that exploits already-sorted runs).

**No comparison sort can beat $n\log n$.** A comparison sort must distinguish all $n!$ possible orderings of its input, and each comparison has two outcomes, so after $k$ comparisons it can distinguish at most $2^k$ cases. It therefore needs $k \ge \log_2(n!)$ comparisons in the worst case. By Stirling's approximation, $\ln n! \approx n\ln n - n$, so

$$
\log_2(n!) \approx n\log_2 n - n\log_2 e \approx n\log_2 n - 1.44\,n = \Omega(n\log n).
$$

Merge sort is therefore optimal up to lower-order terms. Sorts that do not compare keys, such as **counting sort** and **radix sort**, escape the bound by exploiting the keys' structure (small integers, fixed-width bit patterns): $O(n + k)$ for $n$ keys drawn from $k$ values. Sorting 12-bit ADC codes needs only an array of 4096 counters.

### 3.9 Recursion, and walking a tree

A function is **recursive** when it calls itself on a smaller version of its own problem. Every recursive function has two parts: a **base case** small enough to answer directly (an empty list, an empty tree, an array of one element) and a **recursive step** that reduces the problem and combines the answers. Merge sort is one: sort each half, then merge. The way to read, and to write, a recursive function is the way mathematical induction works: check the base case; then *assume* that the recursive call returns the right answer for the smaller input, and check that the step combines it correctly. If both hold, the function is correct for every size, without tracing the calls one by one.

Trees are where recursion is most natural, because a tree is itself defined recursively: a binary tree is either empty, or a node with a left and a right subtree, each a binary tree. Insertion into a BST, the standard **traversals** (orders of visiting every node), the height, and freeing the tree are each a few lines:

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct tnode {
    int key;
    struct tnode *left, *right;
} tnode_t;

static tnode_t *insert(tnode_t *t, int key)          /* returns the (possibly new) subtree root */
{
    if (t == NULL) {                                    /* base case: an empty tree */
        tnode_t *n = malloc(sizeof *n);
        if (n == NULL) {
            exit(1);
        }
        n->key = key;
        n->left = n->right = NULL;
        return n;
    }
    if (key < t->key) {
        t->left = insert(t->left, key);                 /* smaller problem: one subtree */
    } else if (key > t->key) {
        t->right = insert(t->right, key);
    }
    return t;                                           /* duplicates are ignored */
}

static void in_order(const tnode_t *t)                  /* left subtree, node, right subtree */
{
    if (t == NULL) return;
    in_order(t->left);
    printf(" %d", t->key);
    in_order(t->right);
}

static void pre_order(const tnode_t *t)                 /* node first: copies, serializes */
{
    if (t == NULL) return;
    printf(" %d", t->key);
    pre_order(t->left);
    pre_order(t->right);
}

static int height(const tnode_t *t)                     /* levels on the longest root-to-leaf path */
{
    if (t == NULL) return 0;
    int hl = height(t->left), hr = height(t->right);
    return 1 + (hl > hr ? hl : hr);
}

static void free_tree(tnode_t *t)                       /* post-order: children before their parent */
{
    if (t == NULL) return;
    free_tree(t->left);
    free_tree(t->right);
    free(t);
}

int main(void)
{
    const int keys[] = {50, 30, 70, 20, 40, 60, 80};
    tnode_t *root = NULL;
    for (size_t i = 0; i < sizeof keys / sizeof keys[0]; i++) {
        root = insert(root, keys[i]);
    }
    printf("in-order:");
    in_order(root);
    printf("\npre-order:");
    pre_order(root);
    printf("\nheight %d\n", height(root));
    free_tree(root);

    tnode_t *chain = NULL;
    for (int k = 1; k <= 7; k++) {
        chain = insert(chain, 10 * k);                  /* sorted input */
    }
    printf("same keys inserted in sorted order: height %d\n", height(chain));
    free_tree(chain);
    return 0;
}
```

```text
in-order: 20 30 40 50 60 70 80
pre-order: 50 30 20 40 70 60 80
height 3
same keys inserted in sorted order: height 7
```

- **In-order** (left subtree, node, right subtree) visits a BST's keys in sorted order, which is how a tree lists its contents in order in $O(n)$.
- **Pre-order** (node first) visits each parent before its children: the order in which to copy or serialize a tree, so that inserting the keys in that order rebuilds the same shape.
- **Post-order** (children first) visits each node after both its subtrees, which is exactly what `free_tree` needs: freeing a parent first would lose the only pointers to its children.

The second tree makes §3.7's warning concrete: the same seven keys inserted in sorted order produce a chain of height 7 instead of 3, and every operation on it costs $O(n)$.

**The cost of recursion is stack.** Each call that has not yet returned holds a stack frame (05-06) with its parameters, locals and return address, so memory grows with the recursion depth: about $\log_2 n$ frames for a balanced tree, but $n$ for a chain or for recursion along a linked list. A desktop thread's megabytes of stack survive depths of tens of thousands; a microcontroller with a few kilobytes may manage only a few dozen frames, and overflowing it corrupts memory silently. This is why safety-critical C forbids recursion outright (MISRA C Rule 17.2, "Functions shall not call themselves, either directly or indirectly", Required in the 2012 and 2023 editions, [R-092](../../../reference/research-log.md#r-092--c-language-standards-coding-standards-and-embedded-usage)), and why firmware rewrites recursion as loops, with an explicit stack of fixed size where one is needed. Recursion along a list converts to a loop easily (Problem 05-08.5's in-place reverse is one); recursion on a tree is bounded by the tree's height, which a balanced tree keeps at $O(\log n)$ (Problem 05-08.13).

## 4. Worked examples

### Example 05-08.1 · What scaling means in seconds

**Setup.** A test system holds $n = 10^6$ device records and executes about $10^9$ simple operations per second. Estimate (a) linear versus binary search for one record, (b) sorting with an $O(n\log n)$ method versus a quadratic one (about $n^2/2$ steps), and (c) what happens to each time if the data grow to $10^7$ records.

**Solution.** (a) Linear search: on average $n/2 = 500{,}000$ comparisons, about 0.5 ms; binary search: at most $\lfloor\log_2 10^6\rfloor + 1 = 19 + 1$ = **20** comparisons, about 20 ns. (b) $n\log_2 n = 10^6 \times 19.93 = 1.99\times10^7$ steps, about **0.020 s**; $n^2/2 = 5\times10^{11}$ steps, about 500 s, **8.3 minutes**. (c) At $10^7$ records: binary search needs 24 comparisons (+4, because $\log_2 10 = 3.3$); linear search ×10; $n\log n$ sorting grows by $10 \times 23.25/19.93 = 11.7$×, to about 0.23 s; the quadratic sort grows 100-fold, to about 14 hours.

```python
import math

for n in (10**6, 10**7):
    print(f"n = {n:>8}: binary {math.floor(math.log2(n)) + 1} comparisons, linear avg {n // 2}, "
          f"n log n sort {n * math.log2(n) / 1e9:.3f} s, quadratic sort {n * n / 2 / 1e9 / 60:.1f} min")
```

```text
n =  1000000: binary 20 comparisons, linear avg 500000, n log n sort 0.020 s, quadratic sort 8.3 min
n = 10000000: binary 24 comparisons, linear avg 5000000, n log n sort 0.233 s, quadratic sort 833.3 min
```

**Units check.** Steps divided by steps per second gives seconds ✓.

**Sanity check.** $2^{20} = 1{,}048{,}576 > 10^6$, so 20 halvings suffice ✓.

### Example 05-08.2 · A UART ring buffer that counts what it loses

**Setup.** A UART interrupt pushes received bytes into an 8-slot ring buffer; the main loop pops them. Bytes `A` to `J` (10 bytes) arrive before the main loop runs; it then pops 3 bytes, two more bytes `K` and `L` arrive, and it drains the rest. With a drop-newest policy, which bytes are lost and what does the main loop receive?

**Solution.** The buffer holds `A`–`H`; `I` and `J` find it full and are **dropped** (2 drops). Popping 3 removes `A B C`; `K` and `L` fit in the freed slots; draining yields `D E F G H K L`, **7** bytes.

```c
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>

#define RB_SIZE 8u                                     /* must be a power of two */
_Static_assert((RB_SIZE & (RB_SIZE - 1u)) == 0, "RB_SIZE must be a power of two");

typedef struct {
    uint8_t data[RB_SIZE];
    _Atomic uint32_t head;                             /* written only by the producer */
    _Atomic uint32_t tail;                             /* written only by the consumer */
    uint32_t dropped;                                  /* written only by the producer */
} ringbuf_t;

static int rb_push(ringbuf_t *rb, uint8_t byte)        /* called by the producer (the ISR) */
{
    uint32_t head = atomic_load_explicit(&rb->head, memory_order_relaxed);
    uint32_t tail = atomic_load_explicit(&rb->tail, memory_order_acquire);
    if (head - tail == RB_SIZE) {                      /* full */
        rb->dropped++;
        return -1;
    }
    rb->data[head & (RB_SIZE - 1u)] = byte;            /* 1. write the byte ... */
    atomic_store_explicit(&rb->head, head + 1u, memory_order_release);   /* 2. ... then publish it */
    return 0;
}

static int rb_pop(ringbuf_t *rb, uint8_t *byte)        /* called by the consumer (the main loop) */
{
    uint32_t tail = atomic_load_explicit(&rb->tail, memory_order_relaxed);
    uint32_t head = atomic_load_explicit(&rb->head, memory_order_acquire);
    if (head == tail) {                                /* empty */
        return -1;
    }
    *byte = rb->data[tail & (RB_SIZE - 1u)];           /* 1. read the byte ... */
    atomic_store_explicit(&rb->tail, tail + 1u, memory_order_release);   /* 2. ... then free the slot */
    return 0;
}

int main(void)
{
    ringbuf_t rb = {{0}, 0, 0, 0};
    uint8_t b;
    for (char c = 'A'; c <= 'J'; c++) rb_push(&rb, (uint8_t)c);
    printf("stored %u, dropped %u; popped:", (unsigned)(rb.head - rb.tail), (unsigned)rb.dropped);
    for (int i = 0; i < 3 && rb_pop(&rb, &b) == 0; i++) printf(" %c", b);
    rb_push(&rb, 'K');
    rb_push(&rb, 'L');
    printf("; drained:");
    while (rb_pop(&rb, &b) == 0) printf(" %c", b);
    printf("\n");

    ringbuf_t wrap = {{0}, 4294967290u, 4294967290u, 0};   /* counters about to wrap past 2^32 */
    for (int i = 0; i < 8; i++) rb_push(&wrap, (uint8_t)i);
    printf("near wrap: head %u, tail %u, count %u\n", (unsigned)wrap.head, (unsigned)wrap.tail,
           (unsigned)(wrap.head - wrap.tail));
    return 0;
}
```

```text
stored 8, dropped 2; popped: A B C; drained: D E F G H K L
near wrap: head 2, tail 4294967290, count 8
```

The counters are C11 atomics, written only by their owner: each side loads its own counter with relaxed ordering (nobody else writes it), loads the other side's with acquire ordering, and publishes its update with release ordering *after* touching the data, the three conditions of §3.3. On a single-core microcontroller these compile to ordinary loads and stores plus compiler barriers, so the safety costs essentially nothing.

The second test starts the counters just below $2^{32}$: after 8 pushes `head` has wrapped to 2 while `tail` is still 4,294,967,290, and `head - tail` is still exactly **8** (full), because unsigned subtraction is arithmetic modulo $2^{32}$. The `dropped` counter matters more than it looks: a buffer that silently discards data under load is a classic field failure. A designer sizes the buffer from the worst-case gap between consumer runs: at 115,200 baud a UART delivers about 11,520 bytes per second (10 bits per byte), so a main loop that can stall for 5 ms needs at least 58 slots, and the next power of two, 64.

**Sanity check.** $8 - 3 + 2 = 7$ bytes drained ✓.

### Example 05-08.3 · Placing six keys in a hash table

**Setup.** Six peripheral names, `adc`, `gpio`, `i2c`, `spi`, `uart` and `timer`, are inserted, in that order, into a linear-probing table of 8 slots using FNV-1a (32-bit) modulo 8. (a) Where does each land, and how many probes does each insertion take? (b) Compare the average successful-search cost with the formula. (c) What do the formulas predict at this load factor for an unsuccessful search?

**Solution.**

```c
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static uint32_t fnv1a(const char *s)
{
    uint32_t h = 2166136261u;                          /* FNV offset basis */
    for (; *s; s++) {
        h ^= (uint8_t)*s;
        h *= 16777619u;                                /* FNV prime; wraps modulo 2^32 */
    }
    return h;
}

int main(void)
{
    const char *keys[] = {"adc", "gpio", "i2c", "spi", "uart", "timer"};
    const char *slot[8] = {NULL};
    int total = 0;
    for (int k = 0; k < 6; k++) {
        uint32_t home = fnv1a(keys[k]) & 7u, i = home;
        int probes = 1;
        while (slot[i] != NULL) {                      /* linear probing */
            i = (i + 1) & 7u;
            probes++;
        }
        slot[i] = keys[k];
        total += probes;
        printf("%-5s home %u -> slot %u (%d probe%s)\n", keys[k], (unsigned)home, (unsigned)i, probes, probes > 1 ? "s" : "");
    }
    printf("average probes to find a stored key: %.2f\n", total / 6.0);
    return 0;
}
```

```text
adc   home 1 -> slot 1 (1 probe)
gpio  home 2 -> slot 2 (1 probe)
i2c   home 3 -> slot 3 (1 probe)
spi   home 5 -> slot 5 (1 probe)
uart  home 5 -> slot 6 (2 probes)
timer home 2 -> slot 4 (3 probes)
average probes to find a stored key: 1.50
```

(a) `spi` and `uart` share home slot 5, so `uart` moves to 6 (2 probes); `gpio` and `timer` share slot 2, and `timer` must pass the occupied slot 3 (`i2c`) to reach 4 (3 probes). (b) A later search for a key retraces its insertion probes, so the average successful search costs $9/6$ = **1.50** probes. The formula $\tfrac12(1 + 1/(1-\alpha))$ at $\alpha = 6/8 = 0.75$ predicts 2.5; this small table did better than average, since the formula describes the expected value over random keys, in large tables. (c) For an unsuccessful search the formula predicts $\tfrac12(1 + 1/0.25^2)$ = **8.5** probes; here a missing key with home slot 1 would find slots 1 to 6 all occupied and stop at empty slot 7: 7 probes, counting the empty slot as the formula does. This is why open-addressing tables resize before they are three-quarters full.

**Sanity check.** Two collisions among 6 keys in 8 slots is unsurprising: the birthday bound puts the first collision near $\sqrt{8} \approx 3$ keys ✓.

### Example 05-08.4 · A deadline scheduler with a binary heap

**Setup.** Tasks with deadlines 40, 10, 30, 5, 20, 50 and 15 ms are inserted into a min-heap. Show the array after all insertions and the order in which tasks are removed. How many comparisons can one insertion or removal need for $n = 10^6$ tasks?

**Solution.**

```c
#include <stdio.h>

#define CAP 16
static int heap[CAP];
static int n = 0;

static void swap(int *a, int *b) { int t = *a; *a = *b; *b = t; }

static void heap_push(int key)
{
    int i = n++;
    heap[i] = key;
    while (i > 0 && heap[(i - 1) / 2] > heap[i]) {        /* sift up */
        swap(&heap[(i - 1) / 2], &heap[i]);
        i = (i - 1) / 2;
    }
}

static int heap_pop(void)
{
    int top = heap[0];
    heap[0] = heap[--n];
    for (int i = 0;;) {                                   /* sift down */
        int l = 2 * i + 1, r = l + 1, m = i;
        if (l < n && heap[l] < heap[m]) m = l;
        if (r < n && heap[r] < heap[m]) m = r;
        if (m == i) break;
        swap(&heap[i], &heap[m]);
        i = m;
    }
    return top;
}

int main(void)
{
    const int deadlines[] = {40, 10, 30, 5, 20, 50, 15};
    for (int k = 0; k < 7; k++) heap_push(deadlines[k]);
    printf("array:");
    for (int k = 0; k < n; k++) printf(" %d", heap[k]);
    printf("\norder:");
    while (n > 0) printf(" %d", heap_pop());
    printf("\n");
    return 0;
}
```

```text
array: 5 10 15 40 20 50 30
order: 5 10 15 20 30 40 50
```

The array is `5 10 15 40 20 50 30`: index 0 holds the minimum; the children of index 1 (10) are at indices 3 and 4 (40 and 20), both larger, as the heap property requires. Note that the array is *not* sorted: a heap guarantees only parent ≤ child, which is weaker and cheaper to maintain. Removal yields the deadlines in increasing order, `5 10 15 20 30 40 50`: earliest deadline first. (This is also heapsort.) For $n = 10^6$ the heap has height $\lfloor\log_2 10^6\rfloor$ = **19**, so an insertion needs at most 19 comparisons and a removal at most $2 \times 19 = 38$ (two per level, to find the smaller child and compare with it).

**Sanity check.** Seven elements fill a complete tree of height 2: levels of 1, 2 and 4 nodes ✓.

### Example 05-08.5 · Counting the comparisons of two sorts

**Setup.** Sort the same 1000 random integers with insertion sort and with merge sort, counting comparisons. Compare with $n(n-1)/4$, with $n\log_2 n$, and with the lower bound $\log_2(n!)$.

**Solution.**

```python
import math
import random

def insertion_sort(a):
    a, comparisons = list(a), 0
    for i in range(1, len(a)):
        x, j = a[i], i - 1
        while j >= 0:
            comparisons += 1
            if a[j] <= x:
                break
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x
    return a, comparisons

def merge_sort(a):
    if len(a) <= 1:
        return list(a), 0
    left, cl = merge_sort(a[:len(a) // 2])
    right, cr = merge_sort(a[len(a) // 2:])
    merged, i, j, c = [], 0, 0, cl + cr
    while i < len(left) and j < len(right):
        c += 1
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    return merged + left[i:] + right[j:], c

random.seed(42)
data = [random.randrange(1_000_000) for _ in range(1000)]
s1, c1 = insertion_sort(data)
s2, c2 = merge_sort(data)
n = len(data)
print(s1 == s2 == sorted(data), c1, c2)
print(f"n(n-1)/4 = {n * (n - 1) / 4:.0f}, n log2 n = {n * math.log2(n):.0f}, log2(n!) = {math.log2(math.factorial(n)):.1f}")
```

```text
True 240414 8698
n(n-1)/4 = 249750, n log2 n = 9966, log2(n!) = 8529.4
```

Insertion sort used 240,414 comparisons: this input has 239,421 inversions, and each element whose inner loop stopped at a smaller predecessor added one more comparison (993 of them). Random data have $n(n-1)/4$ = **249,750** inversions on average, with a standard deviation of about 5,300 for $n = 1000$, so this sample sits about two standard deviations below the mean, unremarkable. Merge sort used under nine thousand, below $n\log_2 n$ = 9966 and just above the information-theoretic minimum $\log_2(1000!)$ = **8529.4**: no comparison sort can average fewer than about 8,530 comparisons on 1000 distinct keys. Merge sort's worst case for $n = 1000$ is $n\lceil\log_2 n\rceil - 2^{\lceil\log_2 n\rceil} + 1$ = **8977** comparisons, so on this input it was close to optimal.

**Sanity check.** The ratio of the two counts, about 28, is close to $(n/4)/\log_2 n \approx 250/10 = 25$, as the growth rates predict ✓.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| T 05-08.a | linear probing, successful probes at α = 0.75 | 2.5 | — |
| T 05-08.b | linear probing, unsuccessful probes at α = 0.75 | 8.5 | — |
| T 05-08.c | linear probing, unsuccessful probes at α = 0.9 | 50.5 | — |
| Ex 05-08.1a | binary search comparisons, 10⁶ items | 20 | — |
| Ex 05-08.1b | n log₂ n sort time, 10⁶ items | 0.020 | s |
| Ex 05-08.1c | quadratic sort time, 10⁶ items | 8.3 | min |
| Ex 05-08.1d | binary search comparisons, 10⁷ items | 24 | — |
| Ex 05-08.2a | bytes dropped | 2 | — |
| Ex 05-08.2b | bytes drained after the second burst | 7 | — |
| Ex 05-08.2c | minimum slots for a 5 ms stall at 115,200 baud | 58 | — |
| Ex 05-08.3a | total insertion probes | 9 | — |
| Ex 05-08.3b | average successful-search probes | 1.50 | — |
| Ex 05-08.4a | heap height for 10⁶ tasks | 19 | — |
| Ex 05-08.5a | expected insertion-sort inversions n(n−1)/4 | 249750 | — |
| Ex 05-08.5b | log₂(1000!) | 8529.4 | — |
| Ex 05-08.5c | merge-sort worst case, n = 1000 | 8977 | — |

## 5. Simulate it

Open [labs/05-08-lab/](../labs/05-08-lab/README.md). It has two parts:

1. **A C module with tests** (`ds.c`, run by [`tools/run_c.py`](../../../tools/run_c.py)): a ring buffer with free-running counters, a linear-probing hash table with FNV-1a and automatic resizing, and a binary heap, each checked against simple reference behavior. *Predict first:* how many times does the hash table resize while 1000 keys are inserted into an initial 8 slots with a 0.75 load limit?
2. **A notebook of operation counts** ([05-08-complexity.ipynb](../labs/05-08-lab/05-08-complexity.ipynb)): measure comparisons and probes, not seconds (which vary from machine to machine), as $n$ grows, and fit the growth rates on log-log axes. *Predict first:* what slope does $n\log n$ have on a log-log plot?

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Array versus linked list | Array: cache-friendly, compact, $O(1)$ index | $O(n)$ insertion in the middle | Engineer |
| Hash table versus balanced tree | Hash: $O(1)$ average lookup | No ordering or range queries; worst case $O(n)$; resizing pauses | Engineer / architect |
| Hash-table load factor | Lower: fewer probes | More memory | Library designer |
| Ring-buffer size | Larger: absorbs longer consumer stalls without loss | RAM (scarce on MCUs) and worst-case latency | Firmware engineer, from the timing budget |
| Static pools versus dynamic structures | Static: deterministic, no fragmentation | Fixed capacity, chosen at design time | Firmware architect |
| Sort choice (merge, quick, heap, radix) | Stability, worst-case guarantees, memory, speed on special keys | Each wins on some axis and loses on another | Engineer, often by library default |
| Hardware lookup (TCAM, hash engines) versus software | Line-rate lookups at billions per second | Area, power and cost in silicon | Chip architect |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| $\log_2 10^3$, $10^6$, $10^9$ | about 10, 20, 30 | halvings to search |
| Binary search on $n$ sorted items | $\lfloor\log_2 n\rfloor + 1$ comparisons | |
| Comparison-sort lower bound | $\log_2 n! \approx n\log_2 n - 1.44n$ | merge sort is within lower-order terms |
| Random permutation | $n(n-1)/4$ inversions on average | insertion sort's work |
| Linear probing at α = 0.5 / 0.75 / 0.9 | successful 1.5 / 2.5 / 5.5; unsuccessful 2.5 / 8.5 / 50.5 probes | resize before it fills |
| Heap index arithmetic | children $2i+1$, $2i+2$; parent $\lfloor(i-1)/2\rfloor$ | 0-based |
| UART at 115,200 baud (8N1) | about 11,520 bytes/s | sizing receive buffers |

## 8. Common mistakes

1. **Choosing by Big-O alone for small $n$,** or ignoring Big-O for large $n$. Rule out what cannot scale; measure the rest.
2. **Off-by-one and full/empty confusion in ring buffers.** Use free-running counters or keep a count; never let `head == tail` mean two things.
3. **Silent overflow policies:** a full queue that drops data without counting it.
4. **Letting a hash table fill up,** or using a weak hash on structured keys (all keys landing in a few slots).
5. **Binary search on unsorted data,** or the classic midpoint overflow `(lo + hi) / 2` for huge arrays (use `lo + (hi - lo) / 2`).
6. **Quadratic algorithms hiding in loops:** calling an $O(n)$ operation (`list.insert(0, x)`, `x in list`, string concatenation in a loop) inside an $O(n)$ loop.
7. **Assuming a sort is stable** when it is not (quicksort, heapsort), when sorting records by several fields.
8. **Pointer bugs in linked structures:** losing the rest of a list by overwriting `next` before saving it, and leaks when nodes are removed but not freed (05-06).

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **The fundamentals are stable; the hardware context is not.** The algorithms in this chapter date from the 1950s to the 1970s and remain the standard toolkit **[Established]**. What has changed is the cost model: memory access, not arithmetic, now dominates, so cache-friendly layouts (arrays, open addressing, B-trees with wide nodes) usually beat pointer-heavy ones of the same Big-O. Modern hash-table designs probe several slots at once with SIMD instructions, and sorting libraries are tuned to the memory hierarchy.
- **Data structures in silicon.** Network switches implement hash tables, longest-prefix match and priority scheduling directly in hardware, with TCAMs (memories that compare a key against every stored entry in parallel) and hash engines, because software cannot keep up with terabit line rates. **Deeper:** see companion repo *Datacenter Networking*.
- **The FE exam tests this material directly.** Its Software Engineering area (4–6 of 110 questions) covers algorithms (sorting, searching, complexity, Big-O) and data structures (lists, trees, vectors, structures, arrays) ([R-001](../../../reference/research-log.md#r-001--ncees-fe-electrical-and-computer-specification)) **[Established]**.

### Why it matters commercially

Scalability claims are algorithm claims. "Our EDA tool handles billion-instance designs", "our switch holds a million flows at line rate", "our scheduler supports 100,000 concurrent requests" are statements about data structures and their constants. When a product works in a demo and fails at a customer, a quadratic step that was invisible at small $n$ is a common cause. In diligence, ask how performance scales with the size of the customer's problem, not how fast the demo is, and look for evidence of measured scaling curves. In hardware, the same question appears as table sizes: how many routes, flows, or keys fit on-chip, what happens when they do not, and how lookup time degrades with load.

### Marketing vs Reality

- **"Constant-time lookups."** *Reality:* hash tables are $O(1)$ *on average* at a bounded load factor; the worst case, under adversarial or unlucky keys, is linear, and resizing causes occasional pauses. Ask about the worst case and the load factor.
- **"Scales linearly."** *Reality:* often measured over a narrow range of sizes. Ask for the measured curve over two or three orders of magnitude, on log-log axes.
- **"Billions of lookups per second."** *Reality:* with what table size, key distribution and hit rate? Small tables that fit in cache, or in on-chip memory, are far faster than large ones.
- **"No data loss under load."** *Reality:* every finite buffer overflows at some rate. Ask for the buffer sizing analysis and the drop counters in the field.

### Questions for engineering leaders

1. **"How does your runtime grow with the customer's problem size, and over what range have you measured it?"** *Strong:* a measured scaling curve with its slope, and the size where it breaks. *Evasive:* a single benchmark number.
2. **"What happens when this table or buffer fills up?"** *Strong:* a defined policy (resize, evict, drop with counting, back-pressure) and telemetry. *Evasive:* "It won't fill up."
3. **"Where are your worst-case, not average-case, performance risks?"** *Strong:* specific operations (rehashing, garbage collection, pathological inputs) with mitigations. *Evasive:* "Our average latency is excellent."
4. **"Which parts of the lookup pipeline are in hardware, and what are the table-size limits?"** *Strong:* capacities per table, behavior on overflow, and the software fallback's cost. *Evasive:* "It's all line rate."

## 10. Concept check

1. Define $f(n) = O(g(n))$, and explain why $3n^2 + 100n = O(n^2)$.

   <details><summary>Answer</summary>

   $f = O(g)$ if there are constants $c > 0$ and $n_0$ with $f(n) \le c\,g(n)$ for all $n \ge n_0$. For $n \ge 100$, $100n \le n^2$, so $3n^2 + 100n \le 4n^2$: take $c = 4$, $n_0 = 100$.

   </details>

2. Why does a doubling dynamic array have $O(1)$ amortized append even though some appends copy the whole array?

   <details><summary>Answer</summary>

   Copies happen only at sizes 1, 2, 4, …, so $n$ appends copy at most $1 + 2 + 4 + \cdots < 2n$ elements in total: $O(n)$ for $n$ appends, $O(1)$ each on average over the sequence.

   </details>

3. In a ring buffer with free-running unsigned counters and power-of-two size $N$, how are the slot index, the count, "empty" and "full" computed, and why does wrap-around of the counters not matter?

   <details><summary>Answer</summary>

   Slot `c & (N - 1)`; count `head - tail`; empty when the count is 0; full when it is $N$. Unsigned subtraction is modulo $2^{32}$, so `head - tail` is the true difference as long as it is less than $2^{32}$, which it always is (it never exceeds $N$).

   </details>

4. When is a linked list a better choice than an array, and why are arrays usually faster in practice?

   <details><summary>Answer</summary>

   When elements are frequently inserted or removed in the middle at known positions (given a pointer to the node), or the length varies widely and copying is unacceptable. Arrays are usually faster because their elements are contiguous, so the processor streams them through the cache, while list nodes are scattered and each step is a dependent memory access; lists also pay a pointer and an allocation per element.

   </details>

5. What is the load factor of a hash table, and what happens to linear probing as it approaches 1?

   <details><summary>Answer</summary>

   $\alpha = n/m$, entries per slot. With linear probing, occupied slots form long runs, and the expected probes for an unsuccessful search, $\tfrac12(1 + 1/(1-\alpha)^2)$, blow up: 8.5 at 0.75, 50.5 at 0.9. Tables resize well before then.

   </details>

6. What property does a min-heap guarantee, and why does that make it suitable for a priority queue but not for searching?

   <details><summary>Answer</summary>

   Every parent is no larger than its children, so the minimum is at the root and insertion and removal of the minimum cost $O(\log n)$. Nothing orders siblings or subtrees relative to each other, so finding an arbitrary key may require examining every element.

   </details>

7. Derive the number of comparisons merge sort makes for $n = 2^k$.

   <details><summary>Answer</summary>

   $T(n) = 2T(n/2) + n$ with $T(1) = 0$ (counting $n$ comparisons per merge, an upper bound). Each of the $k = \log_2 n$ levels of recursion does merges totaling $n$, so $T(n) = n\log_2 n$.

   </details>

8. Why can no comparison sort do better than about $n\log_2 n$ comparisons, and how does counting sort avoid the bound?

   <details><summary>Answer</summary>

   It must distinguish all $n!$ orderings, and $k$ binary comparisons distinguish at most $2^k$, so $k \ge \log_2 n! \approx n\log_2 n - 1.44n$. Counting sort never compares keys: it uses each key (a small integer) as an array index to count occurrences, taking $O(n + k)$ for keys in a range of size $k$.

   </details>

Now work the [problem set](../problems/05-08-problems.md).

## 11. Key terms

[Big-O notation](../../../reference/glossary.md#big-o-notation) ·
[Amortized cost](../../../reference/glossary.md#amortized-cost) ·
[Ring buffer](../../../reference/glossary.md#ring-buffer) ·
[Linked list](../../../reference/glossary.md#linked-list) ·
[Stack (data structure)](../../../reference/glossary.md#stack-data-structure) ·
[Queue](../../../reference/glossary.md#queue) ·
[Hash table](../../../reference/glossary.md#hash-table) ·
[Load factor](../../../reference/glossary.md#load-factor) ·
[Binary search tree](../../../reference/glossary.md#binary-search-tree) ·
[Binary heap](../../../reference/glossary.md#binary-heap) ·
[Binary search](../../../reference/glossary.md#binary-search) ·
[Merge sort](../../../reference/glossary.md#merge-sort)

## 12. Connections

- **Builds on:** [05-06](05-06-c-pointers-and-memory.md) (pointers, structs, the heap, growable buffers), [05-07](05-07-bit-manipulation.md) (power-of-two masks, hashing by bit mixing), [05-04](05-04-reproducible-workflows.md) (the birthday bound), [05-01](05-01-python-fundamentals.md) (bisection, Example 05-01.7) and [01-08](../../01-calculus-for-engineers/chapters/01-08-sequences-series-and-taylor.md) (series).
- **Next:** [05-09 Software Engineering Practices](05-09-software-engineering-practices.md), on how teams design, test and maintain the code built from these pieces.
- **Used later:** [14 · Computer Organization and Architecture](../../14-computer-organization-and-architecture/README.md) (caches and why layout matters), [18 · Embedded Systems](../../18-embedded-systems-and-microcontrollers/README.md) (ring buffers, schedulers, real-time constraints), [19 · Digital VLSI Design](../../19-digital-vlsi-design/README.md) (graph algorithms in synthesis and place-and-route) and [23 · Memory and Storage](../../23-memory-and-storage-technology/README.md) (B-trees and flash translation layers).

## 13. Further study

- Cormen, Leiserson, Rivest and Stein, *Introduction to Algorithms*, 4th ed., chapters 1–4 (analysis), 6 (heapsort), 7 (quicksort), 8 (lower bound, counting and radix sort), 10–12 (elementary data structures, hash tables, binary search trees).
- Sedgewick and Wayne, *Algorithms*, 4th ed., chapters 1–3, with the free online course and visualizations at algs4.cs.princeton.edu.
- Knuth, *The Art of Computer Programming*, Vol. 3, *Sorting and Searching*, section 6.4 (hashing and the linear-probing analysis), for the derivations behind the probe formulas.
- Bentley, *Programming Pearls*, 2nd ed.: short, practical essays on choosing algorithms and data structures.

## 14. Sources

1. Cormen, Leiserson, Rivest and Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022.
2. Knuth, *The Art of Computer Programming*, Vol. 3, 2nd ed., Addison-Wesley, 1998 (linear-probing analysis).
3. Sedgewick and Wayne, *Algorithms*, 4th ed., Addison-Wesley, 2011.
4. Fowler, Noll and Vo, FNV hash (IETF draft "The FNV Non-Cryptographic Hash Algorithm"), for the 32-bit offset basis and prime.
5. NCEES, *FE Electrical and Computer CBT specification* (July 2020). [R-001]
