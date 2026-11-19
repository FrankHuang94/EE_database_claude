# Solutions 05-08 · Data Structures and Algorithms You Will Need

Problems: [05-08 problems](../problems/05-08-problems.md) · Chapter: [05-08](../chapters/05-08-data-structures-and-algorithms.md). Every Python and C block below is executed by [verify_05_08.py](../verify/verify_05_08.py) (C under `-Werror` and the sanitizers), which checks the printed output exactly and recomputes every number in the answer key independently.

---

## Solutions

### Solution 05-08.1

(a) At iteration $i$ the inner loop runs $i$ times, so the total is $0 + 1 + \cdots + (n-1) = n(n-1)/2$ = **499,500**: $\Theta(n^2)$. (b) $m$ takes the values 1000, 500, 250, 125, 62, 31, 15, 7, 3, 1: **10** iterations, $\lfloor\log_2 n\rfloor + 1$: $\Theta(\log n)$. (c) The inner loop runs for $k = 1, 2, 4, \dots, 512$: 10 times per outer iteration, so $1000 \times 10$ = **10,000**: $\Theta(n\log n)$.

```python
n = 1000
a = sum(1 for i in range(n) for j in range(i))   # fragment (a), counted directly
b, m = 0, n                                       # fragment (b)
while m > 0:
    b, m = b + 1, m // 2
inner, k = 0, 1                                   # fragment (c): inner-loop trips per outer iteration
while k < n:
    inner, k = inner + 1, k * 2
print(a, b, n * inner)
```

```text
499500 10 10000
```

### Solution 05-08.2

(a) A **ring buffer**: $O(1)$ push and pop, no allocation, and safe between one interrupt producer and one consumer without disabling interrupts, provided each side publishes its counter after touching the data, with the atomic ordering of Example 05-08.2. (b) A **min-heap priority queue** keyed by expiry time: $O(1)$ to see the next timer, $O(\log n)$ to insert or remove. (c) A **hash table** keyed by serial number: $O(1)$ average lookup. (d) A **balanced search tree** (or a sorted array if entries arrive in order, which logs usually do): $O(\log n)$ to find the start, then walk forward in order; a hash table cannot answer range queries. (e) A **stack**: undo removes the most recent action first, $O(1)$ per push and pop.

### Solution 05-08.3

```python
def binary_search(a, target):
    lo, hi, compared = 0, len(a) - 1, []
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        compared.append(a[mid])
        if a[mid] == target:
            return mid, compared
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, compared

arr = [3, 8, 15, 21, 29, 37, 44, 52, 60]
for t in (37, 40):
    idx, seen = binary_search(arr, t)
    print(t, idx, seen, len(seen))
```

```text
37 5 [29, 44, 37] 3
40 -1 [29, 44, 37] 3
```

For 37: compare with 29 (middle of 0–8, index 4), then 44 (middle of 5–8, index 6), then 37 (index 5): found in **3** comparisons. For 40: 29, 44, 37, then the range is empty: not found after **3** comparisons. (Each "comparison" here is one three-way test of an element.) The maximum for 9 elements is $\lfloor\log_2 9\rfloor + 1$ = **4**, reached for example when searching for 60.

### Solution 05-08.4

(a) The producer delivers $6 \times 4000$ = 24,000 bytes/s; a 12 ms stall accumulates $24{,}000 \times 0.012$ = **288 bytes**, so the next power of two is **512** slots. (A design margin is wise: 288 fits in 512 with room for jitter in the stall estimate.) (b) A `uint32_t` counter advances 24,000 per second and wraps after $2^{32}/24{,}000$ s = 178,957 s = **49.7 hours**. It does not matter: the buffer only ever uses `head - tail` and `counter & (N - 1)`, both correct modulo $2^{32}$ (Example 05-08.2 tested exactly this). What *would* matter is code that compares counters with `<`, which breaks at the wrap.

### Solution 05-08.5

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct node {
    int value;
    struct node *next;
} node_t;

static int push_front(node_t **head, int value)
{
    node_t *n = malloc(sizeof *n);
    if (n == NULL) return -1;
    n->value = value;
    n->next = *head;                           /* new node points at the old head */
    *head = n;
    return 0;
}

static int reverse(node_t **head)              /* returns the number of next pointers rewritten */
{
    node_t *prev = NULL, *cur = *head;
    int rewrites = 0;
    while (cur != NULL) {
        node_t *next = cur->next;              /* save before overwriting */
        cur->next = prev;
        rewrites++;
        prev = cur;
        cur = next;
    }
    *head = prev;
    return rewrites;
}

static void free_list(node_t *head)
{
    while (head != NULL) {
        node_t *next = head->next;
        free(head);
        head = next;
    }
}

int main(void)
{
    node_t *head = NULL;
    for (int v = 5; v >= 1; v--) {             /* push 5..1 to the front: list reads 1 2 3 4 5 */
        if (push_front(&head, v) != 0) { free_list(head); return 1; }
    }
    int rewrites = reverse(&head);
    printf("reversed:");
    for (node_t *p = head; p != NULL; p = p->next) printf(" %d", p->value);
    printf(" (%d pointers rewritten)\n", rewrites);
    free_list(head);
    return 0;
}
```

```text
reversed: 5 4 3 2 1 (5 pointers rewritten)
```

Reversal walks the list once, pointing each node back at its predecessor: **5** rewrites for 5 nodes, $O(n)$ time and $O(1)$ extra memory. The `next` pointer must be saved before it is overwritten, or the rest of the list is lost (and leaked: LeakSanitizer, which runs on this block, would report it). `free_list` saves `next` before freeing for the same reason.

### Solution 05-08.6

```python
def balanced(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack

for s in ("{[()()]}", "([)]", "((", "a[i] = b(c[j])"):
    print(f"{s!r}: {balanced(s)}")
```

```text
'{[()()]}': True
'([)]': False
'((': False
'a[i] = b(c[j])': True
```

`{[()()]}` and `a[i] = b(c[j])` are balanced; `([)]` fails because `)` arrives while `[` is the most recent unclosed bracket; `((` fails because brackets remain open at the end. A stack fits because brackets nest: the bracket that must close next is always the most recently opened one, exactly last-in-first-out. The check is $O(n)$ time.

### Solution 05-08.7

(a) Set the unsuccessful-search cost to 10: $\tfrac12\left(1 + \frac{1}{(1-\alpha)^2}\right) = 10 \Rightarrow (1-\alpha)^2 = \frac{1}{19} \Rightarrow \alpha = 1 - \frac{1}{\sqrt{19}}$ = **0.771**. (b) $0.7706 \times 1024 = 789.1$, so **789** entries. (c) At that load, a successful search costs $\tfrac12(1 + 1/(1 - 0.7706))$ = **2.68** probes with linear probing, and $1 + \alpha/2$ = **1.39** with separate chaining (which degrades more gently, at the cost of a pointer per entry and scattered memory).

### Solution 05-08.8

```python
def push(h, x):
    h.append(x)
    i = len(h) - 1
    while i > 0 and h[(i - 1) // 2] > h[i]:
        h[(i - 1) // 2], h[i] = h[i], h[(i - 1) // 2]
        i = (i - 1) // 2

def pop(h):
    top, last = h[0], h.pop()
    if h:
        h[0], i = last, 0
        while True:
            l, r, m = 2 * i + 1, 2 * i + 2, i
            if l < len(h) and h[l] < h[m]: m = l
            if r < len(h) and h[r] < h[m]: m = r
            if m == i: break
            h[i], h[m] = h[m], h[i]
            i = m
    return top

h = []
for x in (7, 3, 9, 1, 5):
    push(h, x)
    print("after", x, h)
print("pop", pop(h), h)
```

```text
after 7 [7]
after 3 [3, 7]
after 9 [3, 7, 9]
after 1 [1, 3, 9, 7]
after 5 [1, 3, 9, 7, 5]
pop 1 [3, 5, 9, 7]
```

Inserting 3 sifts it above 7; 9 stays a leaf; 1 enters at index 3, swaps with its parent 7 (index 1) and then with 3 (index 0), reaching the root; 5 enters at index 4, whose parent (index 1) now holds 3, smaller than 5, so it stays. Removing the minimum (1) moves the last element (5) to the root and sifts it down past the smaller child (3), giving `[3, 5, 9, 7]`.

### Solution 05-08.9

(a) For $n = 16 = 2^4$: $T(16) = 2T(8) + 16$, $T(8) = 2T(4) + 8$, $T(4) = 2T(2) + 4$, $T(2) = 2T(1) + 2 = 2$, so $T(4) = 8$, $T(8) = 24$, $T(16)$ = **64** $= 16\log_2 16$. (b) The exact worst case is $16 \times 4 - 2^4 + 1$ = **49**: each merge of $a + b$ elements needs at most $a + b - 1$ comparisons (the last element needs none), and the recurrence with $n - 1$ instead of $n$ gives $n\log_2 n - n + 1$ for powers of two. An input that forces every merge to its maximum interleaves the two halves at every level; it can be built by "unmerging" a sorted list (even positions to the left half, odd to the right, recursively):

```python
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

def worst_case(sorted_vals):
    if len(sorted_vals) <= 1:
        return list(sorted_vals)
    return worst_case(sorted_vals[0::2]) + worst_case(sorted_vals[1::2])

w = worst_case(list(range(16)))
print(w, merge_sort(w)[1], merge_sort(list(range(16)))[1])
```

```text
[0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15] 49 32
```

The constructed input needs exactly **49** comparisons; already-sorted input needs only 32, because each merge stops as soon as one half is exhausted ($n/2$ comparisons per level here).

### Solution 05-08.10

```python
import math

for n in (5, 12, 100):
    exact = math.log2(math.factorial(n))
    stirling = n * math.log2(n) - n * math.log2(math.e)
    print(n, math.ceil(exact), round(exact, 2), round(stirling, 2))
print("merge sort worst, n = 12:", 12 * math.ceil(math.log2(12)) - 2 ** math.ceil(math.log2(12)) + 1)
```

```text
5 7 6.91 4.4
12 29 28.84 25.71
100 525 524.76 520.12
merge sort worst, n = 12: 33
```

(a) The lower bounds are **7** comparisons for 5 elements, **29** for 12 and **525** for 100. A lower bound is not the same as the true minimum: for 5 elements, 7 comparisons can be achieved, so the bound is exact; for 12 elements the true minimum is 30, one more than the bound (Wells, 1965, by exhaustive computer search; Knuth, *The Art of Computer Programming*, vol. 3, §5.3.1); for 100 elements the true minimum is not known. Stirling's two-term estimate is low for small $n$ (4.40 versus 6.91 for $n = 5$) because it omits the $\tfrac12\log_2(2\pi n)$ term, but its relative error shrinks as $n$ grows (520.1 versus 524.8 for $n = 100$, under 1%). (b) Merge sort's worst case for 12 elements is $12 \times 4 - 16 + 1$ = **33** comparisons: 4 more than the bound of 29, and 3 more than the best any algorithm can do. (Optimal sorting networks and merge-insertion sorting come closer for small $n$; for large $n$ merge sort's excess is only a small fraction of $n\log n$.)

### Solution 05-08.11

(a) Counting sort reads each of the $n = 10^6$ codes once to count it and then emits the codes from $k = 4096$ counters: about $n + k$ = **1,004,096** steps, plus $n$ writes. Merge sort needs about $n\log_2 n \approx 2.0\times10^7$ comparisons, roughly 20 times more. (b) $4096 \times 4$ bytes = **16,384 bytes** (16 KB): acceptable on a PC, but more than many small MCUs have free, where 16-bit counters (if no code can occur more than 65,535 times) or a coarser histogram are used. (c) Counting sort, and the median directly from the counts:

```c
#include <stdint.h>
#include <stdio.h>

#define CODES 4096u

int main(void)
{
    const uint16_t samples[] = {2050, 2047, 4095, 0, 2047, 2049, 2050, 2047, 1};
    const unsigned n = sizeof samples / sizeof samples[0];
    static uint32_t count[CODES];              /* static: 16 KB off the stack, zero-initialized */
    for (unsigned i = 0; i < n; i++) count[samples[i]]++;

    uint16_t sorted[sizeof samples / sizeof samples[0]];
    unsigned k = 0;
    for (unsigned code = 0; code < CODES; code++)
        for (uint32_t c = 0; c < count[code]; c++) sorted[k++] = (uint16_t)code;

    unsigned seen = 0, median = 0;
    for (unsigned code = 0; code < CODES; code++) {   /* first code reaching the (n + 1)/2-th sample */
        seen += count[code];
        if (seen >= (n + 1) / 2) { median = code; break; }
    }
    printf("sorted:");
    for (unsigned i = 0; i < n; i++) printf(" %u", (unsigned)sorted[i]);
    printf("; median %u\n", median);
    return 0;
}
```

```text
sorted: 0 1 2047 2047 2047 2049 2050 2050 4095; median 2047
```

The 9 samples sort to `0 1 2047 2047 2047 2049 2050 2050 4095`, and the median, the 5th value, is **2047**: found by walking the counts until 5 samples have been seen, without producing the sorted array at all. Percentiles of ADC data in production test and calibration are computed exactly this way.

### Solution 05-08.12

```python
class TwoStackQueue:
    def __init__(self):
        self.inbox, self.outbox, self.moves = [], [], 0

    def enqueue(self, x):
        self.inbox.append(x)

    def dequeue(self):
        if not self.outbox:
            while self.inbox:                  # reverse the inbox into the outbox
                self.outbox.append(self.inbox.pop())
                self.moves += 1
        return self.outbox.pop()

q = TwoStackQueue()
for x in range(1, 9):
    q.enqueue(x)
first = [q.dequeue() for _ in range(3)]
q.enqueue(9)
rest = [q.dequeue() for _ in range(6)]
print(first, rest, q.moves)
```

```text
[1, 2, 3] [4, 5, 6, 7, 8, 9] 9
```

(a) The first dequeue moves all 8 elements (the outbox is empty); the next two dequeues move nothing; after 9 is enqueued, five more dequeues drain the outbox, and the sixth finds it empty and moves the single element 9. Total: **9** moves for 9 elements, and FIFO order is preserved: `1 2 3`, then `4 … 9`. (b) Each element is pushed onto the inbox once, moved to the outbox at most once, and popped once: at most 3 stack operations per element over its whole life. So any sequence of $m$ operations costs $O(m)$ in total, $O(1)$ amortized per operation, even though a single dequeue may cost $O(n)$. This is the same accounting argument as for the doubling array.

### Solution 05-08.13

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct tnode {
    int key;
    struct tnode *left, *right;
} tnode_t;

static tnode_t *insert(tnode_t *t, int key)
{
    if (t == NULL) {
        tnode_t *n = malloc(sizeof *n);
        if (n == NULL) {
            exit(1);
        }
        n->key = key;
        n->left = n->right = NULL;
        return n;
    }
    if (key < t->key) {
        t->left = insert(t->left, key);
    } else if (key > t->key) {
        t->right = insert(t->right, key);
    }
    return t;
}

static void walk(const tnode_t *t, int order)           /* 0 pre-order, 1 in-order, 2 post-order */
{
    if (t == NULL) return;
    if (order == 0) printf(" %d", t->key);
    walk(t->left, order);
    if (order == 1) printf(" %d", t->key);
    walk(t->right, order);
    if (order == 2) printf(" %d", t->key);
}

static int height(const tnode_t *t)
{
    if (t == NULL) return 0;
    int hl = height(t->left), hr = height(t->right);
    return 1 + (hl > hr ? hl : hr);
}

static int count_range(const tnode_t *t, int lo, int hi)  /* keys in [lo, hi] */
{
    if (t == NULL) return 0;
    if (t->key < lo) return count_range(t->right, lo, hi);   /* whole left subtree is too small */
    if (t->key > hi) return count_range(t->left, lo, hi);    /* whole right subtree is too large */
    return 1 + count_range(t->left, lo, hi) + count_range(t->right, lo, hi);
}

static void free_tree(tnode_t *t)
{
    if (t == NULL) return;
    free_tree(t->left);
    free_tree(t->right);
    free(t);
}

int main(void)
{
    const int keys[] = {8, 3, 10, 1, 6, 14, 4, 7, 13};
    const char *names[] = {"pre-order:", "in-order:", "post-order:"};
    tnode_t *root = NULL;
    for (size_t i = 0; i < sizeof keys / sizeof keys[0]; i++) {
        root = insert(root, keys[i]);
    }
    for (int order = 0; order < 3; order++) {
        printf("%-11s", names[order]);
        walk(root, order);
        printf("\n");
    }
    printf("height %d; keys in [4, 10]: %d\n", height(root), count_range(root, 4, 10));
    free_tree(root);

    tnode_t *chain = NULL;
    for (int k = 1; k <= 14; k++) {
        for (size_t i = 0; i < sizeof keys / sizeof keys[0]; i++) {
            if (keys[i] == k) chain = insert(chain, k);     /* the same keys, in increasing order */
        }
    }
    printf("sorted insertion: height %d\n", height(chain));
    free_tree(chain);
    return 0;
}
```

```text
pre-order:  8 3 1 6 4 7 10 14 13
in-order:   1 3 4 6 7 8 10 13 14
post-order: 1 4 7 6 3 13 14 10 8
height 4; keys in [4, 10]: 5
sorted insertion: height 9
```

(a) The tree has 8 at the root; 3 (with children 1 and 6, and 6 with children 4 and 7) on the left; 10 (with right child 14, whose left child is 13) on the right. The traversals are printed above; in-order gives the keys sorted, as it must for a BST. The height is **4** levels: 8, then 3 and 10, then 1, 6 and 14, then 4, 7 and 13.

(b) `count_range` returns **5** (the keys 4, 6, 7, 8 and 10). It prunes: at a node whose key is below `lo`, every key in its left subtree is smaller still, so only the right subtree is searched, and symmetrically above `hi`. The cost is proportional to the height plus the number of keys found, not to the size of the tree: the range query that hash tables cannot answer.

(c) Inserted in increasing order, each key becomes the right child of the previous one: a chain of height **9**. A recursive in-order traversal descends the whole chain before printing anything, holding one frame per node plus one for the call on the last node's empty child: **10** frames at the deepest point.

(d) $2048/32$ = 64 frames. A tree of height $h$ needs $h + 1$ frames at the deepest point, so the tallest tree is $h$ = **63**. A balanced tree of height 63 could hold $2^{63} - 1$ keys, far more than memory, so balance makes recursion safe; a chain of 64 nodes would already overflow the stack. Firmware therefore either keeps trees balanced (with a provable height bound) or walks them with a loop and an explicit stack array of fixed size.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 05-08.1a | steps, fragment (a) | 499500 | — |
| 05-08.1b | steps, fragment (b) | 10 | — |
| 05-08.1c | steps, fragment (c) | 10000 | — |
| 05-08.3a | comparisons to find 37 | 3 | — |
| 05-08.3b | maximum comparisons for 9 elements | 4 | — |
| 05-08.4a | bytes accumulated during a 12 ms stall | 288 | bytes |
| 05-08.4b | buffer size (power of two) | 512 | bytes |
| 05-08.4c | counter wrap time | 49.7 | h |
| 05-08.5a | pointers rewritten reversing 5 nodes | 5 | — |
| 05-08.7a | load factor for 10-probe misses | 0.771 | — |
| 05-08.7b | entries in 1024 slots | 789 | — |
| 05-08.7c | successful probes, linear probing | 2.68 | — |
| 05-08.7d | successful probes, chaining | 1.39 | — |
| 05-08.9a | T(16) | 64 | — |
| 05-08.9b | merge-sort worst case, n = 16 | 49 | — |
| 05-08.10a | lower bound, n = 5 | 7 | — |
| 05-08.10b | lower bound, n = 12 | 29 | — |
| 05-08.10c | lower bound, n = 100 | 525 | — |
| 05-08.10d | merge-sort worst case, n = 12 | 33 | — |
| 05-08.13a | height of the BST | 4 | levels |
| 05-08.13b | keys in [4, 10] | 5 | — |
| 05-08.13c | height after sorted insertion | 9 | levels |
| 05-08.13d | deepest stack frames, in-order on the chain | 10 | — |
| 05-08.13e | tallest tree walkable in 2 KB at 32 bytes per frame | 63 | levels |
| 05-08.11a | counting-sort steps n + k | 1004096 | — |
| 05-08.11b | counter memory | 16384 | bytes |
| 05-08.11c | median code | 2047 | — |
| 05-08.12a | element moves between stacks | 9 | — |
