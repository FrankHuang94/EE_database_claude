# int sum(int *a, int n): RV32I, loop tested at the top. a0 = pointer, a1 = count.
sum:
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
