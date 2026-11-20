/* Recursive Fibonacci in C, for comparing compiler output with fib.s. */
int fib(int n) { return n < 2 ? n : fib(n - 1) + fib(n - 2); }
