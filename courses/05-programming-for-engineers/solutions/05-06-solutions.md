# Solutions 05-06 · C Pointers, Arrays and Memory

Problems: [05-06 problems](../problems/05-06-problems.md) · Chapter: [05-06](../chapters/05-06-c-pointers-and-memory.md). Every C block below is compiled with `-Wall -Wextra -Wpedantic -Werror` and the address and undefined-behavior sanitizers, and run, by [verify_05_06.py](../verify/verify_05_06.py), which checks the printed output exactly (or that the expected sanitizer report or compiler warning appears) and recomputes every number in the answer key independently.

---

## Solutions

### Solution 05-06.1

Step by step: `*p = *q + 1` writes $7 + 1 = 8$ into `a` (through `p`). `p = q` re-points `p` at `b`; it changes the pointer, not any `int`. `*p = 0` then writes 0 into `b`.

```c
#include <stdio.h>

int main(void)
{
    int a = 5, b = 7;
    int *p = &a, *q = &b;
    *p = *q + 1;
    p = q;
    *p = 0;
    printf("a = %d, b = %d\n", a, b);
    return 0;
}
```

```text
a = 8, b = 0
```

So $a$ = **8** and $b$ = **0**. The key distinction: assigning to `p` changes where it points; assigning to `*p` changes what is stored there.

### Solution 05-06.2

`p` points at `a[2]`, so `p[k]` is `a[2 + k]`.

```c
#include <stdint.h>
#include <stdio.h>

int main(void)
{
    int16_t a[6] = {10, 20, 30, 40, 50, 60};
    int16_t *p = a + 2;
    printf("%d %d %d %d\n", *p, p[1], *(p - 2), p[3]);
    printf("%td elements, %td bytes\n", (a + 5) - p, (char *)(a + 5) - (char *)p);
    return 0;
}
```

```text
30 40 10 60
3 elements, 6 bytes
```

`*p` = **30**, `p[1]` = **40**, `*(p - 2)` = **10** (`a[0]`), `p[3]` = **60** (`a[5]`, the last element; `p[4]` would be out of bounds). `(a + 5) - p` = **3** elements, which is **6 bytes** because each `int16_t` is 2 bytes. Negative offsets are legal as long as the result stays inside the array.

### Solution 05-06.3

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    char buf[] = "ok";
    const char *s = "ok";
    printf("%zu %zu\n", strlen("VDD=1.8V"), sizeof "VDD=1.8V");
    printf("%zu %zu\n", sizeof buf, sizeof s);
    return 0;
}
```

```text
8 9
3 8
```

`"VDD=1.8V"` has **8** characters and occupies **9** bytes with its terminator. `sizeof buf` is **3**: `buf` is an array initialized with a copy of the literal (2 characters and the zero). `sizeof s` is **8**: `s` is a pointer (to a literal stored elsewhere, read-only), and `sizeof` reports the pointer's size. Same initializer, different objects.

### Solution 05-06.4

```c
#include <stdio.h>

size_t count_above(const int *a, size_t n, int threshold, size_t *first)
{
    size_t count = 0;
    *first = n;                                /* "none found" until one is */
    for (size_t i = 0; i < n; i++) {
        if (a[i] > threshold) {
            if (count == 0) {
                *first = i;
            }
            count++;
        }
    }
    return count;
}

int main(void)
{
    const int data[] = {3, 9, 4, 12, 7, 15};
    size_t n = sizeof data / sizeof data[0], first;
    size_t count = count_above(data, n, 8, &first);
    printf("count %zu, first index %zu\n", count, first);
    count = count_above(data, n, 100, &first);
    printf("count %zu, first index %zu (= n: none)\n", count, first);
    return 0;
}
```

```text
count 3, first index 1
count 0, first index 6 (= n: none)
```

Three elements (9, 12, 15) exceed 8, so the count is **3**, and the first is 9 at index **1**. With threshold 100, the count is 0 and `*first` is $n$ = 6, a value that cannot be a valid index, as the interface promises. (A production version would also check `a` and `first` for `NULL`.)

### Solution 05-06.5

Offsets by hand: `a` at 0; `b` (2-byte alignment) needs an even offset, so 1 padding byte, `b` at 2–3; `c` at 4; `d` (4-byte alignment) needs a multiple of 4, so 3 padding bytes, `d` at 8–11. Size **12** (already a multiple of 4). Reordering largest-first, `d, b, a, c`, gives `d` 0–3, `b` 4–5, `a` 6, `c` 7: size **8**, with no padding at all, which is the minimum, since the fields' sizes add up to $1 + 2 + 1 + 4 = 8$ bytes.

```c
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

struct s { uint8_t a; uint16_t b; uint8_t c; uint32_t d; };
struct t { uint32_t d; uint16_t b; uint8_t a; uint8_t c; };

int main(void)
{
    printf("s: offsets %zu %zu %zu %zu, size %zu\n", offsetof(struct s, a), offsetof(struct s, b),
           offsetof(struct s, c), offsetof(struct s, d), sizeof(struct s));
    printf("t: size %zu\n", sizeof(struct t));
    return 0;
}
```

```text
s: offsets 0 2 4 8, size 12
t: size 8
```

### Solution 05-06.6

```c
// expect: warning
#include <stdio.h>

const char *make_label(int channel)
{
    char label[16];
    snprintf(label, sizeof label, "CH%d", channel);
    return label;                              /* the array dies when the function returns */
}
```

`label` lives in `make_label`'s stack frame, which is released on return; the caller receives the address of dead storage, and the next function call will overwrite it. GCC warns ("function returns address of local variable", `-Wreturn-local-addr`, on by default) and in fact compiles the `return` as a null pointer, so that the bug crashes rather than corrupting silently. Two correct designs:

```c
#include <stdio.h>

/* Design 1: the caller provides the storage and its size. */
int make_label(char *dst, size_t size, int channel)
{
    return snprintf(dst, size, "CH%d", channel);
}

/* Design 2: static storage (simple, but every call overwrites the same buffer and it is not thread-safe). */
const char *make_label_static(int channel)
{
    static char label[16];
    snprintf(label, sizeof label, "CH%d", channel);
    return label;
}

int main(void)
{
    char buf[16];
    make_label(buf, sizeof buf, 3);
    const char *a = make_label_static(1);
    printf("%s %s\n", buf, a);
    const char *b = make_label_static(2);      /* overwrites the buffer a points to */
    printf("%s %s\n", a, b);
    return 0;
}
```

```text
CH3 CH1
CH2 CH2
```

The second line shows the static design's catch: `a` and `b` point to the same buffer, so both now read `CH2`. Caller-provided buffers (design 1) are the standard C idiom.

### Solution 05-06.7

```c
#include <stdio.h>
#include <string.h>

size_t copy_str(char *dst, size_t size, const char *src)
{
    size_t len = strlen(src);
    if (size > 0) {
        size_t n = len < size - 1 ? len : size - 1;   /* leave room for the terminator */
        memcpy(dst, src, n);
        dst[n] = '\0';
    }
    return len;
}

int main(void)
{
    char small[10];
    size_t needed = copy_str(small, sizeof small, "T=23.5C RH=41%");
    printf("\"%s\" (%zu chars), needed %zu, truncated %d\n", small, strlen(small), needed, needed >= sizeof small);
    return 0;
}
```

```text
"T=23.5C R" (9 chars), needed 14, truncated 1
```

The function copies **9** characters plus the terminator and returns **14**, the full length, so the caller can see the truncation (14 ≥ 10) and, if it matters, allocate a buffer of 15 bytes and retry. This is the contract of BSD's `strlcpy`, which C23 does not include but many platforms provide.

### Solution 05-06.8

$1000 \times 64$ = **64,000 bytes** leak: every call loses its only pointer to the buffer when it returns.

```c
// expect: sanitizer
#include <stdlib.h>
#include <string.h>

static int checksum(const unsigned char *data, size_t n)
{
    unsigned char *scratch = malloc(64);       /* allocated on every call ... */
    if (scratch == NULL) return -1;
    memset(scratch, 0, 64);
    int sum = 0;
    for (size_t i = 0; i < n; i++) {
        scratch[i % 64] ^= data[i];
        sum += scratch[i % 64];
    }
    return sum;                                /* ... and never freed */
}

int main(void)
{
    const unsigned char msg[] = "sensor frame";
    int total = 0;
    for (int k = 0; k < 1000; k++) {
        total += checksum(msg, sizeof msg);
    }
    return total < 0;
}
```

```text
ERROR: LeakSanitizer: detected memory leaks
64000 byte(s) leaked in 1000 allocation(s)
```

LeakSanitizer runs when the program exits, finds the 1000 blocks that nothing points to any more, and totals them. The fix is a `free(scratch);` before the `return` (and before every other exit path), or, better here, no heap at all: a 64-byte `unsigned char scratch[64]` on the stack, since its size is fixed and small.

### Solution 05-06.9

By hand: $\sum_{r=0}^{2}\sum_{c=0}^{3}(10r + c) = 4 \times 10 \times (0 + 1 + 2) + 3 \times (0 + 1 + 2 + 3) = 120 + 18$ = **138**.

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    const size_t rows = 3, cols = 4;
    int *m = malloc(rows * cols * sizeof *m);  /* one block, row-major */
    if (m == NULL) return 1;
    for (size_t r = 0; r < rows; r++)
        for (size_t c = 0; c < cols; c++)
            m[r * cols + c] = (int)(10 * r + c);
    long sum = 0;
    for (size_t k = 0; k < rows * cols; k++)
        sum += m[k];
    printf("m[2][3] = %d, sum = %ld\n", m[2 * cols + 3], sum);
    free(m);                                   /* one allocation, one free */
    return 0;
}
```

```text
m[2][3] = 23, sum = 138
```

Element $(r, c)$ is at index $r \times \text{cols} + c$, the same row-major layout NumPy uses by default (05-02). One contiguous block is faster to traverse (cache-friendly, 14) and needs one `free`, whereas an array of separately allocated rows needs `rows + 1` allocations and frees.

### Solution 05-06.10

Simulating both policies, counting the elements copied at each growth (worst case, every `realloc` moves the block):

```c
#include <stdio.h>

static void grow(const char *name, int doubling)
{
    size_t cap = 16, copies = 0;
    int reallocs = 0;
    while (cap < 1000000) {
        copies += cap;                         /* a full buffer is copied when it grows */
        cap = doubling ? 2 * cap : cap + cap / 2;
        reallocs++;
    }
    printf("%s: %d reallocations, %zu copies, final capacity %zu\n", name, reallocs, copies, cap);
}

int main(void)
{
    grow("x2  ", 1);
    grow("x1.5", 0);
    return 0;
}
```

```text
x2  : 16 reallocations, 1048560 copies, final capacity 1048576
x1.5: 28 reallocations, 2695954 copies, final capacity 1347984
```

Doubling: **16** reallocations ($16 \times 2^{16} = 1{,}048{,}576$), **1,048,560** copies, final capacity 1,048,576. Growth by 1.5×: **28** reallocations, **2,695,954** copies, final capacity 1,347,984. In general, with growth factor $g$ the copies sum to a geometric series of about $C_\text{final}/(g - 1)$: about $1 \times$ the final capacity for doubling and $2\times$ for 1.5×. Both keep the *average* cost per append constant; the smaller factor trades more copying for less unused capacity per growth step (at most 50% spare instead of 100%) and, with some allocators, the chance to reuse the space freed by earlier blocks. Which wins here depends on where 1,000,000 falls between capacities: doubling happened to land close to it.

### Solution 05-06.11

(a) **Heap buffer overflow** (a read past the end of a `malloc`ed block, 4 bytes, so likely an `int`): an off-by-one loop bound or a wrong size in `malloc`; fix the bound or allocate `n * sizeof *p`. (b) **Use after free**: memory read or written after `free` (or after `realloc` moved it); fix the ownership so nothing keeps the pointer, set it to `NULL` after freeing. (c) **Double free**: two owners, or an error path that frees and then falls through to a second `free`; give the block one owner. (d) **Use after return**: a pointer to a local variable used after its function returned (ASan detects this when its stack-use-after-return checking is enabled); return data in caller-provided storage. (e) **Leak**: an allocation whose last pointer was lost; free it on every path, or avoid the heap.

```c
// expect: warning
#include <stdlib.h>

int main(void)
{
    int *frame = malloc(16 * sizeof *frame);
    if (frame == NULL) return 1;
    int error = 1;                             /* pretend processing failed */
    if (error) {
        free(frame);                           /* the error path frees ... */
    }
    free(frame);                               /* ... and so does the normal path */
    return 0;
}
```

When both `free` calls are in one function, GCC 12 and later reject this at compile time (`-Wuse-after-free`, part of `-Wall`, sees the second `free` of a freed pointer). When the two frees sit in different functions, the compiler usually cannot see it, and AddressSanitizer reports `attempting double-free` at run time: that is bug 3 in the lab's [`membugs_demo.c`](../labs/05-06-lab/membugs_demo.c).

This shape, an error path that cleans up and then falls into the normal cleanup, is one of the most common real causes; the usual C remedy is a single cleanup section at the end of the function that every path reaches exactly once.

### Solution 05-06.12

Fixed uses: three buffers of $512 \times 2$ = 1024 bytes each, 3072 bytes; main stack 4096; task stacks 3072. Total 10,240 bytes, leaving $16{,}384 - 10{,}240$ = 6144 bytes for records. With the given order (`uint8_t`, `uint32_t`, `uint16_t`) a record is 12 bytes (Example 05-06.4): $6144/12$ = **512** records. Reordered (`uint32_t`, `uint16_t`, `uint8_t`) it is 8 bytes: $6144/8$ = **768** records, 50% more history for the same RAM, from changing one line of code.

```c
#include <stdint.h>
#include <stdio.h>

struct rec_loose { uint8_t id; uint32_t value; uint16_t flags; };
struct rec_tight { uint32_t value; uint16_t flags; uint8_t id; };

int main(void)
{
    const size_t ram = 16 * 1024, fixed = 3 * 512 * sizeof(int16_t) + 4096 + 3 * 1024;
    printf("free for logs: %zu bytes; loose %zu records, tight %zu records\n", ram - fixed,
           (ram - fixed) / sizeof(struct rec_loose), (ram - fixed) / sizeof(struct rec_tight));
    return 0;
}
```

```text
free for logs: 6144 bytes; loose 512 records, tight 768 records
```

In a real budget the linker map file gives the exact static use, and stack depth is measured (for example by filling the stack with a pattern and checking how much was overwritten), because a stack overflow on an MCU without memory protection silently corrupts whatever lies below it.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 05-06.1a | a | 8 | — |
| 05-06.1b | b | 0 | — |
| 05-06.2a | *p | 30 | — |
| 05-06.2b | p[3] | 60 | — |
| 05-06.2c | (a + 5) − p | 3 | — |
| 05-06.2d | byte distance | 6 | bytes |
| 05-06.3a | strlen("VDD=1.8V") | 8 | — |
| 05-06.3b | bytes occupied | 9 | bytes |
| 05-06.3c | sizeof buf | 3 | bytes |
| 05-06.3d | sizeof s | 8 | bytes |
| 05-06.4a | elements above 8 | 3 | — |
| 05-06.4b | index of the first | 1 | — |
| 05-06.5a | sizeof(struct s) | 12 | bytes |
| 05-06.5b | offset of d | 8 | bytes |
| 05-06.5c | minimum size after reordering | 8 | bytes |
| 05-06.7a | characters kept | 9 | — |
| 05-06.7b | return value | 14 | — |
| 05-06.8a | bytes leaked by 1000 calls | 64000 | bytes |
| 05-06.9a | sum of the matrix | 138 | — |
| 05-06.10a | reallocations, doubling | 16 | — |
| 05-06.10b | copies, doubling | 1048560 | — |
| 05-06.10c | reallocations, 1.5× | 28 | — |
| 05-06.10d | copies, 1.5× | 2695954 | — |
| 05-06.12a | records, original order | 512 | — |
| 05-06.12b | records, reordered | 768 | — |
