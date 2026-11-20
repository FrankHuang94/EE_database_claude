# int sum(int *a, long n): x86-64 (AT&T syntax: source, destination), loop tested at the top.
# rdi = pointer, rsi = count.
sum:
    xorl %eax, %eax
loop:
    testq %rsi, %rsi
    je done
    addl (%rdi), %eax
    addq $4, %rdi
    decq %rsi
    jmp loop
done:
    ret
