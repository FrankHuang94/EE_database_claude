# Course 18 · Final Exam (Embedded Systems and Microcontrollers)

**Time limit:** 240 minutes.
**Allowed:** a scientific calculator (one that handles hexadecimal helps), and the [Course 18 equation sheet](../../../reference/equation-sheets/18-embedded-systems-and-microcontrollers.md) printed without its chapter links. No notes, no Python, no compiler or simulator.

**Instructions.**

- Answer all 14 questions and show every step.
- Question 1 [A] is worth 8 points (2 per part), each [B] 8 (2 per part), and Questions 13 and 14 [C] 12 each (Question 13: 4 per part; Question 14: 3 per part): 120 points in total. 84 or more (70%) is a strong pass.
- Give numerical answers to 3–4 significant figures, with units, and addresses and register values in hexadecimal.
- Question 13 asks for derivations; Question 14 is a diligence question, partly graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These are the conventions of the chapters' problem sets.

- KiB = 1024 bytes; kB = 1000 bytes. A month is 30 days.
- Flash wait states follow $(1 + \text{WS})/f \ge t_{acc}$. The first-order fetch model is $\text{CPI} \approx \max\big(1, (1 + \text{WS})s/L\big) + b\,m\,\text{WS}$, with branch targets at the start of a line; "no cache" means $m$ = 1.
- Cortex-M priorities: a smaller value is more urgent; implemented priority bits are the most significant bits of the priority byte.
- Response times follow the fixed-priority recurrence, with all requests released together at the start of the longest blocking section.
- UART frames are 8N1 (10 bits per byte). In an I²C transaction, START, repeated START and STOP each count as one clock period, and every byte takes 9 (8 data bits and an acknowledge). Rise times are measured from 30% to 70% of the supply.
- ADC codes are rounded to the nearest integer; an ideal $N$-bit ADC has SQNR $6.02N + 1.76$ dB.
- RTOS tasks are periodic with deadlines equal to their periods; times are in milliseconds unless stated.
- CPA leakage is the Hamming weight of the attacked value plus Gaussian noise of standard deviation σ, and $N \approx (z/\rho)^2$ traces are needed for a margin of $z$ standard deviations. PUF cells flip independently, and keys use a repetition code of odd length with majority decoding.

---

**1 [A] · The microcontroller.** (18-01)
(a) A GPIO port's registers start at 0x4002 0C00, and its output data register is at offset 0x14. Give the register's address and the Cortex-M region it lies in. The part has 192 KiB of SRAM starting at 0x2000 0000: what is the last SRAM address?
(b) The flash has an access time of 40 ns. How many wait states are needed at 48 MHz and at 120 MHz? What is the highest clock that allows 2 wait states?
(c) At 120 MHz, code is all 16-bit instructions with 0.10 taken branches per instruction, there is no cache, and the flash reads 64-bit lines. Find the CPI and the instruction rate. Repeat for 128-bit lines, and explain the difference.
(d) A workload needs 400 CoreMark. On a Cortex-M33 (4.10 CoreMark/MHz with zero-wait-state memory) whose cache recovers all but 4% of the clock, what clock is needed?

**2 [B] · From source to running image.** (18-02)
A build reports `text` = 41 872, `data` = 2 316 and `bss` = 14 622 bytes. The MCU has 512 KiB of flash and 96 KiB of SRAM at 0x2000 0000; the linker script places `.data`, then `.bss`, then a 4 KiB heap at the bottom of SRAM, and a 6 KiB stack at the top.
(a) How much flash and SRAM does the firmware use, in bytes and as percentages?
(b) Sections start 4-byte aligned. Find `_edata`, `_ebss`, the bottom of the stack and the free SRAM between the heap and the stack.
(c) A control register reads 0x0001 52C7. Its 3-bit MODE field occupies bits [6:4]. Give the mask, the register with MODE cleared, and the value that sets MODE = 5 without changing any other bit. An interrupt handler that clears bit 0 of the same register (by its own read-modify-write) runs between main's read and main's write. What value ends up in the register, and what should it have been?
(d) The startup code copies `.data` at 7 cycles per word and zeroes `.bss` at 4 cycles per word, on a 16 MHz reset clock. How many cycles and how long before `main`?

**3 [B] · Interrupt priorities and response times.** (18-03)
(a) A Cortex-M part implements 3 priority bits, split by PRIGROUP into 2 bits of group priority and 1 of subpriority. How many preemption levels and subpriorities are there? Write the priority byte for group 1, subpriority 1. While a handler with that byte runs, do requests with 0x40 and with 0x20 preempt it?
(b) Three interrupts, most urgent first: A ($C$ = 4 µs, period 40 µs, deadline 15 µs), B ($C$ = 12 µs, minimum spacing 100 µs) and C ($C$ = 25 µs, period 500 µs). Main code masks all interrupts (PRIMASK) for at most 6 µs. Find the utilization and each worst-case response time.
(c) What is the longest PRIMASK section A's deadline tolerates? A new driver lengthens it to 14 µs: find the three response times again.
(d) How can the 14 µs critical section stay, with A's deadline met? What is A's response time then?

**4 [B] · Timers and the watchdog.** (18-03)
(a) A timer clocked at 72 MHz makes edge-aligned 25 kHz PWM with the finest resolution. Give PSC and ARR, the resolution in bits, and the compare value for 62.5% duty.
(b) What are the auto-reload value and the resolution in center-aligned mode at the same frequency?
(c) The same 16-bit timer measures a signal's period with input capture. Choose the prescaler for 1 µs ticks. Two consecutive captures read 0xFE70 and 0x0A28: find the period, the frequency and the resolution of the measurement.
(d) An independent watchdog runs from an RC oscillator of nominally 32 kHz, guaranteed between 17 and 47 kHz, with a prescaler of 32 and a reload of 2000. Find the nominal, shortest and longest timeouts. The main loop's worst kick-to-kick time is 1.5 s: is that safe? Find the smallest reload that is, and the longest timeout it gives.

**5 [B] · Moving data.** (18-04)
(a) A 48 MHz MCU records 16 kHz mono audio. With one interrupt per sample at 50 cycles, what is the CPU load? With DMA blocks of 160 samples and a 300-cycle block handler, how many interrupts per second, what load, and how long is each block?
(b) An ADC delivers 500 kS/s by DMA into ping-pong buffers. Processing a block of $N$ samples takes $30\ \mu\text{s} + 1.2\ \mu\text{s} \times N$, and other interrupts can delay its start by up to 40 µs. Find the smallest safe $N$ and the power of two you would use, its memory (16-bit samples) and the worst latency from a sample's arrival to the end of its processing.
(c) Repeat (b) with three buffers. Give both conditions on $N$, say which binds, and show why 32 samples fails.
(d) A UART at 460 800 baud receives into a circular DMA buffer; the consumer runs at least every 8 ms. How many bytes can arrive between services, and what power-of-two ring size do you choose? In a 512-byte ring the DMA's remaining count reads 100 and the consumer's tail is 450: where is the head, and how many bytes are unread?

**6 [B] · Serial buses.** (18-05)
(a) A UART with 16× oversampling runs from 48 MHz. For 230 400 baud, find the ideal divisor, the achieved rate with an integer divisor and its error. For 921 600 baud, find the integer divisor's error, then the divisor and rate with a fractional divisor in sixteenths.
(b) An SPI controller samples MISO half an SCK period after the edge on which the target changes it. Its SCK output delay is 3 ns, the trace delay 1.5 ns each way, the target's clock-to-output 12 ns and the controller's input setup 4 ns. What is the highest SCK? And with a 2.5 ns level translator in each direction?
(c) A 2.5 V I²C bus in fast mode (300 ns rise time, 3 mA sink at 0.4 V) has 250 pF of capacitance. Find the allowed pull-up range, and the rise time with 1.0 kΩ.
(d) At 400 kHz, an MCU reads a 3-axis 16-bit accelerometer (6 data bytes) with START, address + W, register, repeated START, address + R, the data and STOP. How many clock periods and how long does it take? What fraction of the periods carries data, and how many such reads fit in a second?

**7 [B] · Analog interfaces.** (18-06)
(a) A 14-bit ADC has a 2.5 V reference. Find the LSB, the code for 1.000 V and the ideal SQNR. The data sheet's SINAD is 78.0 dB: what ENOB is that?
(b) Its sample-and-hold has $R_{sw}$ = 1 kΩ and $C_{sh}$ = 5 pF. To settle to half an LSB, how many time constants are needed? What sampling time does a 2 kΩ source need, and what is the largest source resistance at a 100 ns sampling time?
(c) It converts at 1 MS/s with 1.2 LSB rms of white noise. Averaging 64 samples: what noise, how many extra bits and what output rate?
(d) A 48 MHz timer makes a 0–3.3 V PWM with an 8-bit period, filtered by one RC. Find the PWM frequency, the time constant that keeps the worst-case ripple within one LSB, the filter's bandwidth and the settling time to half an LSB.

**8 [B] · An RTOS.** (18-07)
(a) A kernel ticks at 1 kHz with a 2 µs tick handler and performs 800 context switches a second at 1.5 µs each. What fraction of the CPU does it use?
(b) Three tasks have $(C, T)$ = (2, 6), (3, 10) and (4, 20) ms under rate-monotonic priorities. Compute $U$, the Liu & Layland bound and the hyperbolic product. What do the tests conclude? Find the exact worst-case response times.
(c) One-shot jobs (times in ms): L (low priority) starts at 0, runs 1, holds mutex S for 3, then runs 1. H (high) arrives at 2, runs 1, needs S for 1, then runs 1. M (medium) arrives at 3 and computes for 6 without S. Find H's response time with no protocol, with priority inheritance and with an immediate priority ceiling. What blocking bound and response-time bound does the analysis give H?
(d) A sensor task queues a 16-byte record every 4 ms to a logger that a flash write can stall for up to 30 ms. How many slots and how many bytes of storage does the queue need? And if the stall can reach 32 ms?

**9 [B] · Boot and firmware update.** (18-08)
(a) The MCU has 512 KiB of flash and a 48 KiB bootloader. Find the largest image for a single slot, for two slots, and for a swap through a 16 KiB scratch area.
(b) A 200 KiB image is installed in 8 KiB sectors. Erasing a sector takes 30 ms, and programming takes 50 µs per 16-byte flash word. Find the number of sectors, the time to copy one sector, the overwrite and swap-through-scratch installation times, and how many updates a one-sector scratch area survives at 10 000 erase cycles.
(c) Secure boot hashes the 200 KiB image with software SHA-256 at 20 cycles per byte and verifies one signature in 3 million cycles, on a 96 MHz core. How long does it take? And with a hash engine at one byte per cycle?
(d) A single-slot design downloads the image over Bluetooth at 40 kB/s directly over the running image. How long is the device unbootable if power fails? With 3 power interruptions per device per month (a Poisson process), what fraction of a 2-million-device fleet is bricked per update, and how many devices?

**10 [B] · Ultra-low power.** (18-09)
(a) A node sleeps at 2 µA and wakes every 2 s to measure (1.5 mA for 4 ms) and advertise over Bluetooth LE (5 mA for 2.5 ms). Find the average current, the life of a 225 mAh coin cell in days (ignoring self-discharge), and the radio's share of the charge.
(b) The MCU's sleep mode draws 0.6 mA, stop 4 µA and standby 0.3 µA. Leaving stop costs an extra 150 nC; leaving standby costs 6 µC more than leaving stop. Above what idle times is stop better than sleep, and standby better than stop? Which mode suits the node of (a)?
(c) A task of 2 million cycles runs once a second on an MCU drawing $50\ \mu\text{A/MHz} \times f + 300\ \mu\text{A}$ when active and 1.5 µA asleep, at a fixed voltage. Compare the charge per second at 16 and 64 MHz.
(d) A coin cell (3.0 V open circuit, 60 Ω internal resistance when cold) supplies a 10 mA, 3 ms radio burst; the brown-out threshold is 2.5 V. What is the droop without a capacitor, and what happens? What capacitance keeps the droop to 0.3 V, and what is the droop with 100 µF?

**11 [B] · Sensors.** (18-10)
(a) An accelerometer has 90 µg/√Hz of noise density in a 100 Hz bandwidth (treat it as brick-wall). Find its rms noise and the tilt noise near level. What is the tilt noise of the average of 400 samples (2 s at 200 Hz, assumed independent)?
(b) A gyroscope has 0.005 °/s/√Hz of rate noise density and an uncalibrated bias of 0.2 °/s. Find its angle random walk, and the angle noise and the bias drift after 100 s of integration.
(c) A complementary filter runs at 200 Hz with α = 0.99. Find its time constant, the steady-state tilt error the 0.2 °/s bias causes, and the factor by which it reduces the accelerometer's white tilt noise.
(d) A ring's PPG sensor gives 2 µA of DC photocurrent with a 0.5% perfusion index in an 8 Hz bandwidth. What is the shot-noise-limited SNR of the pulse? The LED is pulsed at 15 mA for 80 µs, 50 times a second: what average current does it draw?

**12 [B] · Hardware security.** (18-11)
(a) A debug-unlock code has 24 random bits. How long does an attacker need on average at 200 tries a second? And if every wrong try forces a 1 s delay?
(b) A 6-byte token is checked with an early-exit comparison, and the attacker averages 100 timings per guess. How many queries does a byte-by-byte attack need at most, counting the last byte's accept/reject tries?
(c) For a CPA with $z$ = 4, find the correlation and the traces needed at σ = 6, and the traces at σ = 12.
(d) SRAM PUF cells flip with probability 0.08. What repetition length keeps a 128-bit key's failure probability below $10^{-6}$, how many cells does it use, and what is the failure probability at that length?

**13 [C] · Three derivations.** (18-01, 18-06, 18-11)
(a) Derive the number of flash wait states from the access time $t_{acc}$ and the clock $f$, and the first-order CPI model, explaining each term. For $t_{acc}$ = 40 ns, 128-bit lines, 16-bit instructions, 0.10 taken branches per instruction and no cache, compare the instruction rates at 75 and 80 MHz, and explain why the faster clock is slower.
(b) An $N$-bit ADC with reference $V_{REF}$ samples through $R_s + R_{sw}$ onto $C_{sh}$. Derive the sampling time needed to settle to half an LSB, and the external capacitor needed to keep the charge-sharing step under half an LSB when the S/H arrives from 0 V. Then show that at a sampling rate $f$ the S/H loads the source like a resistor $1/(fC_{sh})$. For the ADC of Question 7 ($C_{sh}$ = 5 pF, 14 bits, 2.5 V), find the minimum external capacitor; with 220 nF at the pin of a 10 kΩ source at 2.5 V, sampled at 50 kHz alternately with a 0 V channel, estimate the DC error in millivolts and in LSB.
(c) The device leaks $\text{HW}(v) + n$, where $v$ is a uniformly random byte and $n$ is Gaussian noise of variance σ². Derive the correlation between the leakage and the right key's predicted Hamming weight, and the number of traces for a margin of $z$. Show that $N \to z^2\sigma^2/2$ at high noise. Evaluate both at σ = 10, $z$ = 4, and explain why a fresh random mask, $\text{HW}(v \oplus m)$, defeats this attack.

**14 [C] · Diligence: a smart-ring platform.** (18-08 to 18-11)
A start-up pitches an MCU platform for smart rings to your company, with three claims: "a full week of continuous heart-rate monitoring on an 18 mAh battery", "secure firmware updates in under 3 seconds", and "unclonable device keys from an SRAM fingerprint, with no error correction needed because 97% of our cells are stable". Its data sheet gives: PPG LED pulses of 12 mA for 60 µs at 25 Hz; the analog front end 25 µA continuously; the MCU 35 µA on average; the Bluetooth connection 40 µA on average; 85% of the battery's rated capacity usable over temperature and ageing; a 448 KiB firmware image; a measured Bluetooth throughput of 60 kB/s.
(a) Compute the average current and the battery life. What average current would a week need?
(b) How long does a full image take to download? What must be true for the 3-second claim to hold, and what does it imply about the update architecture? Name two risks to probe.
(c) Treat "97% stable" as a 3% flip probability per cell. How often would a raw 128-bit key read back correctly? What repetition length and how many cells reach $10^{-6}$ key failure?
(d) Write four questions for the chief technology officer, each with what a strong and an evasive answer would sound like.
