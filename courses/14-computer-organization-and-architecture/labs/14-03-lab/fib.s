# Recursive Fibonacci, as in Example 14-03.4.  int fib(int n)
    .text
    .globl fib
fib:
    li   t0, 2
    blt  a0, t0, base     # n < 2: return n
    addi sp, sp, -16
    sw   ra, 12(sp)
    sw   s0, 8(sp)
    sw   s1, 4(sp)
    mv   s0, a0           # keep n
    addi a0, a0, -1
    call fib              # fib(n-1)
    mv   s1, a0           # keep fib(n-1)
    addi a0, s0, -2
    call fib              # fib(n-2)
    add  a0, s1, a0
    lw   ra, 12(sp)
    lw   s0, 8(sp)
    lw   s1, 4(sp)
    addi sp, sp, 16
base:
    ret
