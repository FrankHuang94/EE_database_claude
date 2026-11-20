// The same function with the loop rotated.
sum:
    mov w2, wzr
    cbz x1, done
loop:
    ldr w3, [x0], #4
    add w2, w2, w3
    sub x1, x1, #1
    cbnz x1, loop
done:
    mov w0, w2
    ret
