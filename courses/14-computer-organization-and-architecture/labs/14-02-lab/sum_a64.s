// int sum(int *a, long n): Arm A64, loop tested at the top. x0 = pointer, x1 = count.
sum:
    mov w2, wzr
loop:
    cbz x1, done
    ldr w3, [x0], #4
    add w2, w2, w3
    sub x1, x1, #1
    b loop
done:
    mov w0, w2
    ret
