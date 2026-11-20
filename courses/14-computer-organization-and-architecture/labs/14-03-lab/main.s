# A minimal program: compute fib(10) and stop (Example 14-03.5).
    .text
    .globl _start
_start:
    li   a0, 10
    call fib
    ebreak
