# Problems 18-08 · Boot, Bootloaders and Firmware Update

Chapter: [18-08](../chapters/18-08-boot-and-firmware-update.md) · Worked solutions: [18-08 solutions](../solutions/18-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** KiB = 1024 bytes, MiB = 1024 KiB; download rates in kB/s use 1000 bytes. A sector copy is one erase plus one programming of the sector. Power interruptions form a Poisson process; a month is 30 days. Problems marked *(lab)* can be checked with `labs/18-08-lab/bootsim.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 18-08.1 [A]

**Jumping to the application.** An application is linked at 0x0001 0000 in a Cortex-M's flash. (a) Where are its initial stack pointer and its reset vector? (b) The reset-vector word reads 0x0001 02C9. At what address does the reset handler start, and why is the stored value odd? (c) List, in order, what the bootloader must do before branching to it.

### Problem 18-08.2 [A]

**Budgets.** A 512 KiB part has a 32 KiB bootloader. Find the largest image for (a) two slots, (b) two slots and a 16 KiB scratch area, (c) a single internal slot with downloads going to external flash, (d) two slots each ending in a 4 KiB trailer sector for status.

### Problem 18-08.3 [A]

**Integrity against authenticity.** (a) If random corruption hits an image, with what probability does a CRC-32 fail to notice it? (b) Why does a CRC not stop an attacker, while a signed SHA-256 hash does? (c) Why is a CRC still useful inside an update system?

### Problem 18-08.4 [B]

**Another part's installation.** A 256 KiB image is stored in 2 KiB sectors; a sector erase takes 25 ms and programming takes 16 µs per 4-byte word. The flash endures 10 000 erase cycles. (a) How long does one sector copy take? (b) How long does an overwrite installation take, and a swap through one scratch sector? (c) After how many updates does the scratch sector wear out? (d) The scratch area is enlarged to eight sectors used in rotation. How many updates now?

### Problem 18-08.5 [B]

**Boot-time verification.** A 512 KiB image is hashed at 30 cycles per byte and its signature checked in 3 million cycles on a 100 MHz core. (a) How long does verification add to each boot? (b) Some designs verify only when installing, not at every boot. What do they gain and what do they give up?

### Problem 18-08.6 [B]

**A risky fleet.** 200 000 devices receive a 1 MiB update over Bluetooth at 20 kB/s into their only slot, with no recovery path (nothing can receive a new image if the download is cut). (a) How long is each device vulnerable? (b) With four power interruptions a month per device, how many devices are expected to brick per update from power loss? (c) If 3% of downloads are interrupted by the link and each brick costs $80, what do the link-drop bricks cost per update, and what is the total with the power-loss bricks of (b)? (d) How would you present the case to a product owner, comparing this design with a single slot behind a DFU-capable bootloader and with two slots?

### Problem 18-08.7 [B]

**Fuses for anti-rollback.** A device has 64 fuse bits for its security counter. (a) How long do they last if the counter is raised for six security releases a year? (b) The product must be supported for 12 years. What are the options?

### Problem 18-08.8 [B]

**Update energy.** The 1 MiB download of Problem 18-08.6 keeps the radio at 10 mA from 3.6 V. (a) What energy does it use? (b) A delta update is 12% of the image. How long does it take to download? (c) Name two costs of delta updates.

### Problem 18-08.9 [C]

**When will two slots stop fitting?** A wearable's MCU has 1024 KiB of flash and a 48 KiB bootloader. Its image is 400 KiB and grows 15% a year. (a) What is the largest two-slot image, and after how many years does the image outgrow it? (b) If downloads go to an external flash instead, how long does a single internal slot last? (c) What else should the decision consider?

### Problem 18-08.10 [C]

**Power cuts by hand.** *(lab)* An overwrite update of a three-sector image is performed as: erase and write each of the three secondary sectors (the download), write the status "pending", then for each sector erase and write the primary sector and record progress, then clear the status. (a) How many flash operations is that? (b) For a power cut during each operation, does the next boot run the old or the new image? Count each. (c) The same update done in place (status, then erase and write each primary sector, then status) has how many operations, and how many cuts brick it? (d) Why does a swap of the same image need more operations than an overwrite, and what does it buy?

---

## Objective coverage

| Learning objective (chapter 18-08) | Problems |
|---|---|
| 1. The boot sequence | 1 |
| 2. Flash layouts and largest images | 2, 9 |
| 3. Installation time, wear and verification cost | 4, 5 |
| 4. Power-loss safety | 6, 10 |
| 5. Authentication and anti-rollback | 3, 5, 7 |
| 6. Business risk | 6, 8, 9 |
