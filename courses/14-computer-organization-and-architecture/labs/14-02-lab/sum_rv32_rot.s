# The same function with the loop rotated: the test moves to the bottom.
sum:
    addi t0, zero, 0
    beq  a1, zero, done
loop:
    lw   t1, 0(a0)
    add  t0, t0, t1
    addi a0, a0, 4
    addi a1, a1, -1
    bne  a1, zero, loop
done:
    addi a0, t0, 0
    jalr zero, 0(ra)
