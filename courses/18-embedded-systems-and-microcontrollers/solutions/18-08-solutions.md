# Solutions 18-08 · Boot, Bootloaders and Firmware Update

Problems: [18-08 problem set](../problems/18-08-problems.md) · Chapter: [18-08](../chapters/18-08-boot-and-firmware-update.md). Every number below is recomputed by [verify_18_08.py](../verify/verify_18_08.py).

---

## Solutions

### Solution 18-08.1

(a) The vector table starts the image: the initial stack pointer is the word at **0x00010000**, the reset vector the word at **0x00010004**.

(b) **0x000102C8**. Bit 0 of a branch target marks Thumb state; Cortex-M executes only Thumb (Problem 18-02.3), so every vector has it set, and the handler starts at the even address.

(c) Mask interrupts globally; stop SysTick and the timers and peripherals the bootloader used, and clear their NVIC enable and pending bits; if the bootloader used the process stack or an RTOS, return to the main stack in Thread mode (CONTROL.SPSEL = 0); clean and disable the caches if it enabled them; set VTOR to 0x0001 0000; load MSP from the first word; re-enable interrupts as the application expects, and branch to the reset handler. (Armv6-M's Cortex-M0 has no VTOR, so its bootloaders remap memory or copy the vector table to SRAM instead.) The application's startup code then initializes its own `.data` and `.bss` (18-02 §3.5).

### Solution 18-08.2

(a) $(512 - 32)/2$ = **240** KiB.

(b) $(512 - 32 - 16)/2$ = **232** KiB.

(c) $512 - 32$ = **480** KiB.

(d) $240 - 4$ = **236** KiB.

### Solution 18-08.3

(a) A CRC-32 maps corruptions onto $2^{32}$ values, so a random corruption matches the stored CRC with probability $2^{-32}$ = **2.33e-10**. (Short burst errors are always detected.)

(b) Anyone can compute a CRC (or a plain hash) of a modified image and store it alongside. A signature over the hash can only be made with the vendor's private key, so a modified image cannot carry a valid one.

(c) It is cheap and quick for detecting transmission errors chunk by chunk during a download, so a corrupted chunk can be re-requested at once instead of discovering a bad image only at the final signature check.

### Solution 18-08.4

(a) Programming takes $512 \times 16\ \mu\text{s} = 8.192$ ms, so a copy takes $25 + 8.192$ = **33.19** ms.

(b) $128 \times 33.19\ \text{ms}$ = **4.25** s (overwrite); three copies per sector, **12.75** s (swap).

(c) The scratch sector is erased 128 times per update: $10\,000/128$ = **78** updates.

(d) Each scratch sector is then erased 16 times per update: $8 \times 10\,000/128$ = **625** updates.

### Solution 18-08.5

(a) Hash: $524\,288 \times 30/(100 \times 10^6)$ = **157.3** ms; signature **30** ms; total **187.3** ms.

(b) They save the boot time (and energy) on every reset. They give up detecting images modified *in flash* after installation, by a fault, a debug port or an exploit that can write flash. That is acceptable only if flash write protection and debug locks are trustworthy.

### Solution 18-08.6

(a) $1\,048\,576/20\,000$ = **52.4** s.

(b) $1 - e^{-(4/2\,592\,000\ \text{s}) \times 52.4\ \text{s}}$ = **8.09e-5**, so about **16.2** devices of 200 000.

(c) $0.03 \times 200\,000$ = **6000** devices, $6000 \times \$80$ = **\$480 000** per update; with the 16.18 power-loss bricks of (b), $\$480\,000 + 16.18 \times \$80$ = **\$481 294**, the power-loss part being a rounding error.

(d) Put it in expected cost per update and per year: with no recovery path every campaign costs about half a million dollars of returns, plus support and reputation. Then compare the two fixes. A DFU-capable bootloader removes the bricks for the cost of a larger bootloader, at the price of downtime during each update and no rollback (a bad image needs another download). A second slot also removes the bricks, keeps the product working during the download and enables rollback, for the bill-of-materials cost of the extra flash (a bigger part or an external flash) multiplied by volume. The choice turns on whether downtime and rollback are worth that flash.

### Solution 18-08.7

(a) $64/6$ = **10.7** years.

(b) Raise the counter only for releases that must lock out a vulnerability (not every security fix need do so); use a part with more fuses; or keep the counter in a protected monotonic counter of a secure element or replay-protected memory, which supports many more increments. Planning for the support life is part of the design, not an afterthought.

### Solution 18-08.8

(a) $52.4\ \text{s} \times 10\ \text{mA} \times 3.6\ \text{V}$ = **1.89** J.

(b) $0.12 \times 52.4$ = **6.29** s.

(c) The device needs working space and code to apply the patch (and must still be power-safe while doing so), and the server must generate and store a patch for every version still in the field.

### Solution 18-08.9

(a) $(1024 - 48)/2$ = **488** KiB. Solving $400 \times 1.15^t = 488$ gives $t = \ln 1.22/\ln 1.15$ = **1.42** years.

(b) The internal slot can hold $1024 - 48 = 976$ KiB: $t = \ln 2.44/\ln 1.15$ = **6.38** years.

(c) The cost of the external flash and its board area against a larger MCU, security of an image stored outside the chip (it should be encrypted, and verified again after copying), the installation time from external flash, and whether the product's life is longer than either horizon, in which case the code-size growth itself needs managing.

### Solution 18-08.10

(a) Download $3 \times 2 = 6$, status 1, installation $3 \times 3 = 9$, final status 1: **17** operations.

(b) Cuts during the download or the "pending" status write leave the old image running and the update simply not started: **7** cuts boot the **old** image. Cuts during the installation leave a progress record and an intact secondary, so the next boot finishes the copy; a cut during the final status write leaves a complete new image: **10** cuts boot the **new** image. None brick.

(c) $1 + 3 \times 2 + 1$ = **8** operations. Cuts during any of the 6 sector erases and writes leave a half-old, half-new slot with no second copy: **6** brick (the first status write leaves the old image, the last the new one).

(d) A swap moves each sector three times and records progress after each move (36 operations for three sectors in the lab's model, against 17). In exchange, the old image survives in the secondary slot, so an image that fails its health check can be swapped back.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 18-08.1a | initial stack pointer address | 0x00010000 | — |
| 18-08.1b | reset vector address | 0x00010004 | — |
| 18-08.1c | reset handler entry | 0x000102C8 | — |
| 18-08.2a | two slots | 240 | KiB |
| 18-08.2b | two slots and scratch | 232 | KiB |
| 18-08.2c | single internal slot | 480 | KiB |
| 18-08.2d | two slots with trailers | 236 | KiB |
| 18-08.3a | CRC-32 miss probability | 2.33e-10 | — |
| 18-08.4a | sector copy | 33.19 | ms |
| 18-08.4b | overwrite installation | 4.25 | s |
| 18-08.4c | swap installation | 12.75 | s |
| 18-08.4d | updates before scratch wear-out | 78 | — |
| 18-08.4e | with eight scratch sectors | 625 | — |
| 18-08.5a | hash time | 157.3 | ms |
| 18-08.5b | signature time | 30 | ms |
| 18-08.5c | total | 187.3 | ms |
| 18-08.6a | vulnerable window | 52.4 | s |
| 18-08.6b | probability per device | 8.09e-5 | — |
| 18-08.6c | expected bricks from power loss | 16.2 | — |
| 18-08.6d | bricks from link drops | 6000 | — |
| 18-08.6e | cost per update | 480000 | \$ |
| 18-08.6f | total cost per update with power-loss bricks | 481294 | \$ |
| 18-08.7a | fuse life | 10.7 | years |
| 18-08.8a | download energy | 1.89 | J |
| 18-08.8b | delta download time | 6.29 | s |
| 18-08.9a | largest two-slot image | 488 | KiB |
| 18-08.9b | years until it no longer fits | 1.42 | years |
| 18-08.9c | years with external download flash | 6.38 | years |
| 18-08.10a | overwrite operations | 17 | — |
| 18-08.10b | cuts booting the old image | 7 | — |
| 18-08.10c | cuts booting the new image | 10 | — |
| 18-08.10d | in-place operations | 8 | — |
| 18-08.10e | in-place cuts that brick | 6 | — |
| 18-08.10f | swap operations, three sectors | 36 | — |
