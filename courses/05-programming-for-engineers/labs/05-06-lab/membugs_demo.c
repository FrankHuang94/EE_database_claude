/* membugs_demo.c - five deliberate memory bugs for Lab 05-06, one per function.
 * It compiles cleanly: the bugs hide across function boundaries, as real ones do. The helpers are
 * marked noinline (a GCC/Clang extension) so that the compiler cannot see through them; in a
 * single file it otherwise can, and GCC's -Wuse-after-free would catch bug 2 at compile time.
 * Build with ASan and run one bug at a time:
 *   cc -std=c17 -g -O1 -fsanitize=address -fno-omit-frame-pointer membugs_demo.c -o membugs
 *   ./membugs 1        (1 to 5; for 5, older toolchains need ASAN_OPTIONS=detect_stack_use_after_return=1) */
#include <stdio.h>
#include <stdlib.h>

/* 1: off-by-one heap write. */
int bug_off_by_one(size_t n)
{
    int *a = malloc(n * sizeof *a);
    if (a == NULL) return -1;
    for (size_t i = 0; i <= n; i++) {          /* <= writes a[n], one past the end */
        a[i] = (int)i;
    }
    int first = a[0];
    free(a);
    return first;
}

/* 2: use after free, through a helper that frees. */
__attribute__((noinline)) void release(int *p) { free(p); }

int bug_use_after_free(void)
{
    int *a = malloc(4 * sizeof *a);
    if (a == NULL) return -1;
    a[0] = 7;
    release(a);
    return a[0];                               /* reads freed memory */
}

/* 3: double free, from an error path that cleans up and falls through. */
int bug_double_free(int fail)
{
    int *a = malloc(4 * sizeof *a);
    if (a == NULL) return -1;
    if (fail) {
        release(a);
    }
    release(a);
    return 0;
}

/* 4: leak: the only pointer to each block is lost when the function returns. */
int bug_leak(int calls)
{
    int total = 0;
    for (int k = 0; k < calls; k++) {
        int *scratch = calloc(16, sizeof *scratch);
        if (scratch == NULL) return -1;
        total += scratch[0];
    }
    return total;
}

/* 5: dangling stack pointer: the address of a local escapes through an out-parameter. */
__attribute__((noinline)) void remember(int **out, int *where) { *out = where; }

void bug_store_local(int **out)
{
    int reading = 1234;
    remember(out, &reading);                   /* reading dies when this function returns */
}

int main(int argc, char **argv)
{
    int which = argc > 1 ? atoi(argv[1]) : 0;
    int *dangling = NULL;
    switch (which) {
    case 1: printf("%d\n", bug_off_by_one(8)); break;
    case 2: printf("%d\n", bug_use_after_free()); break;
    case 3: printf("%d\n", bug_double_free(1)); break;
    case 4: printf("%d\n", bug_leak(100)); break;
    case 5: bug_store_local(&dangling); printf("%d\n", *dangling); break;
    default: printf("usage: %s N   (N = 1..5 selects a bug)\n", argv[0]); break;
    }
    return 0;
}
