# Problems 05-06 · C Pointers, Arrays and Memory

Chapter: [05-06](../chapters/05-06-c-pointers-and-memory.md) · Worked solutions: [05-06 solutions](../solutions/05-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** C17 on a 64-bit system (8-byte pointers) with the usual alignment (each type aligned to its own size), compiled with `-Wall -Wextra -Wpedantic` and tested under `-fsanitize=address,undefined`. Trace each answer by hand first, then confirm it with a program.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 05-06.1 [A]

**Tracing pointers.** After the following statements, what are `a` and `b`?

```c
// fragment
int a = 5, b = 7;
int *p = &a, *q = &b;
*p = *q + 1;
p = q;
*p = 0;
```

### Problem 05-06.2 [A]

**Arrays as pointers.** With `int16_t a[6] = {10, 20, 30, 40, 50, 60};` and `int16_t *p = a + 2;`, evaluate `*p`, `p[1]`, `*(p - 2)`, `p[3]`, `(a + 5) - p`, and the distance in bytes from `p` to `a + 5`.

### Problem 05-06.3 [A]

**String sizes.** Give `strlen` and the number of bytes occupied for the literal `"VDD=1.8V"`. For `char buf[] = "ok";` and `const char *s = "ok";`, what are `sizeof buf` and `sizeof s`, and why do they differ?

### Problem 05-06.4 [B]

**Two results from one function.** Write `size_t count_above(const int *a, size_t n, int threshold, size_t *first)` that returns how many elements exceed `threshold` and stores the index of the first such element in `*first` (or `n` if there is none). Apply it to {3, 9, 4, 12, 7, 15} with threshold 8.

### Problem 05-06.5 [B]

**Struct layout.** For `struct s { uint8_t a; uint16_t b; uint8_t c; uint32_t d; };`, find each field's offset and `sizeof(struct s)`. Then find the smallest size achievable by reordering the fields.

### Problem 05-06.6 [B]

**A dangling pointer.** A function builds a label in a local array and returns a pointer to it. Explain what is wrong, show what the compiler says, and give two correct designs.

### Problem 05-06.7 [B]

**A bounded copy.** Write `size_t copy_str(char *dst, size_t size, const char *src)` that copies as much of `src` as fits into `dst` (always terminating it when `size > 0`) and returns `strlen(src)`, so callers can detect truncation. Test it with a 10-byte buffer and the source `"T=23.5C RH=41%"`.

### Problem 05-06.8 [B]

**A leak, found.** A function allocates a 64-byte scratch buffer on every call and never frees it. How many bytes leak after 1000 calls? Show LeakSanitizer reporting the leak, then fix the function.

### Problem 05-06.9 [B]

**A matrix on the heap.** Allocate a 3 × 4 matrix of `int` as one block in row-major order, set element $(r, c)$ to $10r + c$, compute the sum of all elements, and free it. Derive the sum by hand.

### Problem 05-06.10 [C]

**Growth factors.** A growable buffer starts with capacity 16 and must reach at least 1,000,000 elements. Compare growth by doubling with growth by 1.5× (new capacity = old + old/2, integer division). For each, find the number of reallocations, the worst-case total element copies, and the final capacity.

### Problem 05-06.11 [C]

**Reading sanitizer reports.** For each AddressSanitizer headline, name the bug and the most likely fix: (a) `heap-buffer-overflow ... READ of size 4`; (b) `heap-use-after-free`; (c) `attempting double-free`; (d) `stack-use-after-return`; (e) LeakSanitizer `detected memory leaks`. Then write a program that triggers (c) within one function: what does the compiler say, and what changes when the two frees are in different functions?

### Problem 05-06.12 [C]

**A RAM budget.** A wearable's MCU has 16 KB of RAM. Fixed uses: three sample buffers of 512 `int16_t` each; a 4 KB main stack; three RTOS task stacks of 1 KB each. The rest stores log records, each a `uint8_t` id, a `uint32_t` value and a `uint16_t` flags. How many records fit with the fields in that order, and how many after reordering for minimum size?

---

## Objective coverage

| Learning objective (chapter 05-06) | Problems |
|---|---|
| 1. Addresses, pointers and output parameters | 1, 4, 6 |
| 2. Arrays and pointer arithmetic | 2, 4, 9 |
| 3. Strings and bounded functions | 3, 7 |
| 4. Structs and layout | 5, 12 |
| 5. Storage, allocation and memory bugs | 6, 8, 9, 10, 11 |
