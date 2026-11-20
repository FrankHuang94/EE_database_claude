# The same function with the loop rotated; decq sets the zero flag, so no separate test is needed.
sum:
    xorl %eax, %eax
    testq %rsi, %rsi
    je done
loop:
    addl (%rdi), %eax
    addq $4, %rdi
    decq %rsi
    jne loop
done:
    ret
