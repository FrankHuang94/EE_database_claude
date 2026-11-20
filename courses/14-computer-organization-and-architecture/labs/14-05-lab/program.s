# Test program for the single-cycle core (Lab 14-05). Sums a 10-element array with the loop of Lab 14-02,
# computes fib(10) with the recursive function of Example 14-03.4, stores both results, and halts.
    .text
    .globl _start
_start:
    li   sp, 0x4000           # stack at the top of the 16 KiB data memory
    li   a0, 0x2000           # the array
    li   a1, 10
    call sum
    sw   a0, 0x100(zero)      # result 1
    li   a0, 10
    call fib
    sw   a0, 0x104(zero)      # result 2
    ebreak

sum:                          # int sum(int *a, int n), top-tested loop
    addi t0, zero, 0
loop:
    beq  a1, zero, done
    lw   t1, 0(a0)
    add  t0, t0, t1
    addi a0, a0, 4
    addi a1, a1, -1
    jal  zero, loop
done:
    addi a0, t0, 0
    jalr zero, 0(ra)

fib:                          # int fib(int n), recursive
    li   t0, 2
    blt  a0, t0, base
    addi sp, sp, -16
    sw   ra, 12(sp)
    sw   s0, 8(sp)
    sw   s1, 4(sp)
    mv   s0, a0
    addi a0, a0, -1
    call fib
    mv   s1, a0
    addi a0, s0, -2
    call fib
    add  a0, s1, a0
    lw   ra, 12(sp)
    lw   s0, 8(sp)
    lw   s1, 4(sp)
    addi sp, sp, 16
base:
    ret
