/* Structures from Example 14-03.6 and Problem 14-03.10; compile for different ABIs and compare. */
#include <stddef.h>
struct A  { char c; int i; short s; double d; };
struct Ar { double d; int i; short s; char c; };
struct P  { char c; long l; };
int layout[] = {
    sizeof(struct A), offsetof(struct A, i), offsetof(struct A, s), offsetof(struct A, d),
    sizeof(struct Ar), sizeof(struct P),
};
