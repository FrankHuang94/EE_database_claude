<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 18 · Embedded Systems and Microcontrollers

Building products around microcontrollers: MCU architecture (Arm Cortex-M, RISC-V), bare-metal C, interrupts, timers and DMA, serial buses and analog interfaces, RTOS concepts, boot and firmware update, ultra-low-power design, sensors and hardware security.

| | |
|---|---|
| **Term** | 5 |
| **Study hours** | ≈ 83 |
| **University equivalents** | Embedded Systems / Microcontrollers (junior/senior); Berkeley EECS149; UT Austin EE319K |
| **Textbook alignment** | Valvano, *Embedded Systems* series (Cortex-M); Yiu, *The Definitive Guide to Arm Cortex-M3 and Cortex-M4 Processors*; White, *Making Embedded Systems*; Lee & Seshia, *Introduction to Embedded Systems* (free online) |
| **Free courses** | Berkeley EECS149 (Lee & Seshia materials); UT Austin 'Embedded Systems — Shape the World' (edX) |
| **Prerequisites** | [05 · Programming for Engineers](../05-programming-for-engineers/README.md), [08 · Digital Logic Design](../08-digital-logic-design/README.md), [10 · Electronics I (Microelectronic Circuits)](../10-electronics-1/README.md), [14 · Computer Organization and Architecture](../14-computer-organization-and-architecture/README.md) |
| **FE areas** | Computer Systems, Digital Systems, Software Engineering |

## Learning objectives

1. Describe MCU architectures (core, bus matrix, memory map, peripherals) and choose an MCU for a requirement.
2. Write bare-metal C that configures peripherals through registers, with correct use of volatile and interrupts.
3. Use timers, DMA and serial buses (UART, SPI, I²C) and analog interfaces (ADC, DAC, PWM).
4. Explain RTOS scheduling, synchronization and priority inversion.
5. Compute power budgets and battery life for duty-cycled sensor nodes.
6. Explain secure boot, roots of trust, TEEs and side-channel threats.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [18-01 · Microcontroller Architecture](chapters/18-01-microcontroller-architecture.md) | 7 | 🏁 reviewed | [problems](problems/18-01-problems.md) · [solutions](solutions/18-01-solutions.md) · [lab](labs/18-01-lab/README.md) · [verify](verify/verify_18_01.py) |
| [18-02 · Bare-Metal C and the Build Toolchain](chapters/18-02-bare-metal-c-and-toolchain.md) | 8 | 🏁 reviewed | [problems](problems/18-02-problems.md) · [solutions](solutions/18-02-solutions.md) · [lab](labs/18-02-lab/README.md) · [verify](verify/verify_18_02.py) |
| [18-03 · Interrupts, Exceptions and Timers](chapters/18-03-interrupts-exceptions-timers.md) | 8 | 🏁 reviewed | [problems](problems/18-03-problems.md) · [solutions](solutions/18-03-solutions.md) · [lab](labs/18-03-lab/README.md) · [verify](verify/verify_18_03.py) |
| [18-04 · DMA and Data Movement](chapters/18-04-dma-and-data-movement.md) | 5 | 🏁 reviewed | [problems](problems/18-04-problems.md) · [solutions](solutions/18-04-solutions.md) · [lab](labs/18-04-lab/README.md) · [verify](verify/verify_18_04.py) |
| [18-05 · Peripherals and Serial Buses: GPIO, UART, SPI, I²C](chapters/18-05-gpio-uart-spi-i2c.md) | 8 | 🏁 reviewed | [problems](problems/18-05-problems.md) · [solutions](solutions/18-05-solutions.md) · [lab](labs/18-05-lab/README.md) · [verify](verify/verify_18_05.py) |
| [18-06 · Analog Interfaces: ADC, DAC and PWM](chapters/18-06-adc-dac-pwm.md) | 6 | 🏁 reviewed | [problems](problems/18-06-problems.md) · [solutions](solutions/18-06-solutions.md) · [lab](labs/18-06-lab/README.md) · [verify](verify/verify_18_06.py) |
| [18-07 · RTOS Concepts](chapters/18-07-rtos-concepts.md) | 8 | 🏁 reviewed | [problems](problems/18-07-problems.md) · [solutions](solutions/18-07-solutions.md) · [lab](labs/18-07-lab/README.md) · [verify](verify/verify_18_07.py) |
| [18-08 · Boot, Bootloaders and Firmware Update](chapters/18-08-boot-and-firmware-update.md) | 5 | 🏁 reviewed | [problems](problems/18-08-problems.md) · [solutions](solutions/18-08-solutions.md) · [lab](labs/18-08-lab/README.md) · [verify](verify/verify_18_08.py) |
| [18-09 · Ultra-Low-Power Design](chapters/18-09-ultra-low-power-design.md) | 9 | 🏁 reviewed | [problems](problems/18-09-problems.md) · [solutions](solutions/18-09-solutions.md) · [lab](labs/18-09-lab/README.md) · [verify](verify/verify_18_09.py) |
| [18-10 · Sensors: IMU, PPG, MEMS and Audio](chapters/18-10-sensors.md) | 7 | 🏁 reviewed | [problems](problems/18-10-problems.md) · [solutions](solutions/18-10-solutions.md) · [lab](labs/18-10-lab/README.md) · [verify](verify/verify_18_10.py) |
| [18-11 · Hardware Security](chapters/18-11-hardware-security.md) | 7 | 🏁 reviewed | [problems](problems/18-11-problems.md) · [solutions](solutions/18-11-solutions.md) · [lab](labs/18-11-lab/README.md) · [verify](verify/verify_18_11.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/18-embedded-systems-and-microcontrollers.csv) · [Equation sheet](../../reference/equation-sheets/18-embedded-systems-and-microcontrollers.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 18 is planned at about 83 hours: the chapters' own estimates add to 78, plus 5 hours of review and the exam. Course 05 gave you C, Course 08 digital logic, Course 14 the processor, its memory system and interrupts in general, and Courses 16 and 17 sampling, filters and serial links. This course turns them into products: a small processor with its own memory, clocks, peripherals and power budget, running code that must meet deadlines on a battery and survive power cuts, updates and attackers.

The eleven chapters fall into four blocks:

- **The machine and its code (18-01 to 18-03).** The microcontroller's memory map, buses, flash wait states and clocks; the toolchain, linker script and startup code that turn C into an image; and interrupts, priorities, worst-case response times, timers and watchdogs.
- **Moving data and talking to the world (18-04 to 18-06).** DMA with ping-pong and circular buffers, bus contention and cache coherence; GPIO, UART, SPI and I²C from their electrical limits up; ADCs, DACs and PWM, with sampling, references and averaging.
- **Software structure and lifecycle (18-07 to 18-08).** RTOS scheduling (rate-monotonic, EDF, response-time analysis), priority inversion and its protocols, queues and memory; bootloaders, image slots, secure boot and power-fail-safe updates.
- **Product constraints (18-09 to 18-11).** Ultra-low-power design from duty cycles to regulators and coin cells; MEMS inertial sensors, PPG and microphones with their noise budgets and fusion; and hardware security: threat models, roots of trust, side channels, PUFs, fault injection and regulation.

Work at least the [A] and [B] problems of every chapter. The labs are of three kinds, each checked by its chapter's verify script:

- firmware that runs on QEMU's emulated Cortex-M4 (labs 18-02 to 18-05): the startup code and linker symbols, an interrupt and SysTick harness that measures priorities, a lock-free ring buffer between a handler and `main`, and a register-level UART driver; a 16× UART receiver in Verilog, simulated in Icarus, measures the clock-mismatch window (18-05);
- Python models imported by their notebooks: `mcuarch.py` (wait states, fetch simulation, PLL search), `irqtime.py` (response times and a discrete-event interrupt simulator), `dmasim.py`, `mcuanalog.py`, `rtsched.py` (fixed-priority and EDF scheduling with mutex protocols), `bootsim.py` (an exhaustive power-cut campaign over update schemes), `ulp.py`, `sensors.py` and `hwsec.py` (a timing attack, CPA and PUF error correction);
- ngspice netlists for the sample-and-hold and the PWM filter (18-06) and the coin-cell burst (18-09), and host C tests for the ADC arithmetic (18-06) and a constant-time comparison (18-11).

**What to master cold.** The [equation sheet](../../reference/equation-sheets/18-embedded-systems-and-microcontrollers.md) collects the relations; these are the ideas behind them:

- clock speed is not performance: wait states, line width and caches set the CPI, and the clock just below a wait-state boundary can beat the one above it (18-01);
- `volatile` makes accesses happen, not sequences atomic; every read-modify-write shared with an interrupt needs a design decision (18-02);
- worst cases, not averages, decide deadlines: the response-time recurrence, blocking from critical sections and the critical instant (18-03, 18-07);
- buffers trade latency and memory for CPU load and tolerance of service latency, but cannot make processing faster than arrival (18-04);
- every bus has an electrical limit behind its protocol: clock tolerance for UART, round-trip delay for SPI, pull-up and capacitance for I²C (18-05);
- an ADC reading is only as good as its sampling time, source impedance and reference; averaging removes white noise, not errors (18-06);
- priority inversion is bounded only by a protocol; queues overflow at their boundaries (18-07);
- an update scheme is defined by what happens when power fails at every step, and by the flash it costs (18-08);
- battery life is charge per period: radios and boards usually dominate, sleep modes pay only beyond a break-even time, and racing to idle wins at fixed voltage (18-09);
- sensor specifications are noise densities: multiply by √B, and integrate gyroscope noise and bias over time (18-10);
- security is economics: attacker cost per device, side channels measured in traces, keys that must be per device and error-corrected (18-11).

**Assessment.** The [course final exam](exam/README.md) has 14 questions and takes 240 minutes, with a calculator and the equation sheet but no Python, compiler or simulator. Aim for at least 70%. Questions 1 to 12 follow the chapters in order (Questions 3 and 4 both cover 18-03). Question 13 asks for three derivations: the wait-state and CPI model, ADC sampling and charge sharing, and the CPA correlation. Question 14 is a diligence question on a smart-ring platform's battery, update and key claims. The exam's verify script recomputes all 178 answers, checking them against the labs' simulators and an ngspice netlist.
