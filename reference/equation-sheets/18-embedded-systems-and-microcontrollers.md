# Equation Sheet · 18 Embedded Systems and Microcontrollers

The relations to know cold from Course 18, each with its conditions and the chapter that derives it.

Conventions:

- $f$ is a clock frequency, $T$ a period, $C$ a worst-case execution time and $N$ a count (bits, samples, traces or tasks, as each row says);
- KiB = 1024 bytes; noise densities are one-sided, so the rms noise in a bandwidth $B$ is (density) × $\sqrt B$;
- Cortex-M priority values: smaller is more urgent; addresses and register values are hexadecimal.

## Architecture

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Cortex-M map: code from 0x0000 0000, SRAM 0x2000 0000, peripherals 0x4000 0000–0x5FFF FFFF, core registers (NVIC, SysTick, SCB) 0xE000 0000 | Armv7-M/Armv8-M default map; vendors place memories inside the regions | [18-01](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-01-microcontroller-architecture.md) |
| Wait states: $(1 + \text{WS})/f \ge t_{acc}$, so $\text{WS} = \lceil f\,t_{acc}\rceil - 1$; $f_{max}(\text{WS}) = (1 + \text{WS})/t_{acc}$ | Each wait state buys a band $1/t_{acc}$ wide; $t_{acc}$ rises at lower supply | [18-01](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-01-microcontroller-architecture.md) |
| $\text{CPI} \approx \max\big(1, (1 + \text{WS})s/L\big) + b\,m\,\text{WS}$; instruction rate $f/\text{CPI}$ | $s$ instruction bytes, $L$ line bytes, $b$ taken branches per instruction, $m$ fraction of targets missing; targets line-aligned | [18-01](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-01-microcontroller-architecture.md) |
| Required clock = (required CoreMark) ÷ (CoreMark/MHz) ÷ (fraction of the clock delivered) | Published core figures assume zero-wait-state memory | [18-01](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-01-microcontroller-architecture.md) |
| PLL: $f_{SYS} = f_{in}N/(MP)$, $f_{48} = f_{in}N/(MQ)$, with limits on $f_{in}/M$ and on the VCO $f_{in}N/M$ | Exact USB needs an integer $Q$ | [18-01](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-01-microcontroller-architecture.md) |
| Energy per period $E = V(I_0 + kf)\,N\,\text{CPI}/f + VI_{sleep}(T - N\,\text{CPI}/f)$ | Fixed current $I_0$ favors racing; wait states raise CPI; optimum at the top of a wait-state band | [18-01](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-01-microcontroller-architecture.md) |

## Toolchain and startup

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Flash = `text` + `data`; SRAM = `data` + `bss` + stack + heap | `.data` is stored in flash and copied to SRAM | [18-02](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-02-bare-metal-c-and-toolchain.md) |
| Vector table = $(16 + n_{IRQ}) \times 4$ bytes; sections start at $\operatorname{align}_4$ | Armv7-M; code starts after the table | [18-02](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-02-bare-metal-c-and-toolchain.md) |
| Field of width $w$ at bit $p$: mask $M = (2^w - 1) \ll p$; new $= (\text{old} \mathbin{\&} \lnot M) \mathbin{|} ((x \ll p) \mathbin{\&} M)$ | A read-modify-write is not atomic, even on a `volatile` register | [18-02](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-02-bare-metal-c-and-toolchain.md) |
| Startup cycles ≈ (copy cycles/word)$\lceil \text{data}/4\rceil$ + (zero cycles/word)$\lceil \text{bss}/4\rceil$ | Runs on the reset clock unless the clock is raised first | [18-02](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-02-bare-metal-c-and-toolchain.md) |

## Interrupts and timers

| Relation | Conditions / notes | Chapter |
|---|---|---|
| CPU load = event rate × cycles per event / $f_{CPU}$ | Polling, interrupts or DMA compared on the same footing | [18-03](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-03-interrupts-exceptions-timers.md) |
| Priority byte: implemented bits at the top; PRIGROUP splits them into group (preempts) and subpriority (orders pending requests only) | Only a strictly more urgent group preempts | [18-03](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-03-interrupts-exceptions-timers.md) |
| $R_i = C_i + B_i + \sum_{j \in hp(i)}\lceil R_i/T_j\rceil C_j$, iterated from $C_i + B_i$; necessary: $\sum C_j/T_j \le 1$ | Fixed priorities, deadlines within periods; $B_i$ = longest blocking (masked section, non-preemptible lower handler) | [18-03](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-03-interrupts-exceptions-timers.md) |
| Timer: $f_{event} = f_{clk}/((PSC + 1)(ARR + 1))$; PWM resolution $\log_2(f_{clk}/f_{PWM})$ bits; center-aligned period $2 \times ARR$, one bit less | Edge-aligned unless stated; resolution × frequency is fixed by $f_{clk}$ | [18-03](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-03-interrupts-exceptions-timers.md) |
| Input capture: period = $(c_2 - c_1) \bmod 2^n$ ticks | Correct across one wrap; slower signals need an overflow count | [18-03](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-03-interrupts-exceptions-timers.md) |
| Watchdog timeout = prescaler × reload / $f_{osc}$; require worst kick interval < shortest timeout (fastest oscillator) | Hang detected within the longest timeout (slowest oscillator) | [18-03](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-03-interrupts-exceptions-timers.md) |

## DMA and data movement

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Ping-pong: $L + a + bN \le N/f_s \Rightarrow N \ge (a + L)f_s/(1 - bf_s)$ | Processing $a + bN$, service latency $L$; needs $bf_s < 1$ | [18-04](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-04-dma-and-data-movement.md) |
| $k$ buffers: $N \ge \max\big((a + L)f_s/((k - 1) - bf_s),\ af_s/(1 - bf_s)\big)$ | Deadline condition and throughput floor; for $k = 2$ the first always binds | [18-04](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-04-dma-and-data-movement.md) |
| Worst latency = $N/f_s + L + a + bN$; memory = $kN$ samples | First sample of a block | [18-04](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-04-dma-and-data-movement.md) |
| CPU stall fraction ≈ $p\rho$ | DMA occupies a port a fraction ρ of cycles, CPU uses it a fraction $p$, DMA wins; separate banks remove it | [18-04](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-04-dma-and-data-movement.md) |
| Ring: head $= (S - \text{remaining}) \bmod S$; unread $= (\text{head} - \text{tail}) \bmod S$; need $S >$ byte rate × longest service interval | Circular DMA; overrun is invisible in the count alone | [18-04](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-04-dma-and-data-movement.md) |
| Cache lines touched = $\lfloor(a + n - 1)/\ell\rfloor - \lfloor a/\ell\rfloor + 1$ | DMA buffers on cached cores: align to $\ell$ and pad to whole lines | [18-04](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-04-dma-and-data-movement.md) |

## Serial buses

| Relation | Conditions / notes | Chapter |
|---|---|---|
| LED resistor $R \ge (V_{OH,max} - V_F)/I_{max}$ | Worst case: output at the rail, lowest $V_F$ | [18-05](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-05-gpio-uart-spi-i2c.md) |
| UART divisor $= f_{clk}/(16\,\text{baud})$; error = achieved/target − 1 | 16× oversampling; fractional divisors in sixteenths | [18-05](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-05-gpio-uart-spi-i2c.md) |
| 8N1 receiver window (sender bit time / receiver bit time $r$): $r_{max} = 9.5/9$; $r_{min} = (9.5 + 1/\text{OSR})/10$ | Centre sampling, start detected within one tick: −5.26%/+4.58% at 16×; aim for ±2% total | [18-05](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-05-gpio-uart-spi-i2c.md) |
| SPI: half period ≥ SCK delay + trace out + target $t_{CO}$ + trace back + setup | Round trip sets the limit | [18-05](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-05-gpio-uart-spi-i2c.md) |
| I²C: $R_{p,min} = (V_{DD} - V_{OL})/I_{OL}$; $R_{p,max} = t_r/(0.8473\,C_b)$ | $t_r$ from 30% to 70%; 0.8473 = ln(7/3) | [18-05](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-05-gpio-uart-spi-i2c.md) |
| I²C transaction = 9 periods per byte + 1 each for START, Sr, STOP | Register read: address, register, Sr, address, data | [18-05](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-05-gpio-uart-spi-i2c.md) |

## Analog interfaces

| Relation | Conditions / notes | Chapter |
|---|---|---|
| LSB $= V_{REF}/2^N$; quantization noise LSB/√12; SQNR $= 6.02N + 1.76$ dB; ENOB $= (\text{SINAD} - 1.76)/6.02$ | Full-scale sine | [18-06](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-06-adc-dac-pwm.md) |
| Settling to ½ LSB: $t_s \ge \tau\ln 2^{N+1} = (N + 1)\tau\ln 2$, $\tau = (R_s + R_{sw})C_{sh}$; $R_{s,max} = t_s/(C_{sh}\ln 2^{N+1}) - R_{sw}$ | Worst initial error $V_{REF}$ | [18-06](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-06-adc-dac-pwm.md) |
| Charge sharing: step $= (V - V_0)C_{sh}/(C_{ext} + C_{sh})$; ½ LSB needs $C_{ext} \ge C_{sh}(2^{N+1} - 1)$ | S/H arriving at $V_0$ | [18-06](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-06-adc-dac-pwm.md) |
| S/H as a resistor $R_{eq} = 1/(fC_{sh})$; DC error ≈ $(V_s - V_0)R_s/(R_s + R_{eq})$ | $R_sC_{ext} \gg 1/f$ | [18-06](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-06-adc-dac-pwm.md) |
| Averaging $M$ samples: noise ÷ $\sqrt M$, $\tfrac12\log_2 M$ bits, rate ÷ $M$ | White noise of at least about ½ LSB rms; deterministic errors do not average | [18-06](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-06-adc-dac-pwm.md) |
| PWM DAC: ripple ≈ $V\,T/(4\tau)$ at 50%; one LSB needs $\tau \ge 2^NT/4$; $f_c \le 2f_{clk}/(\pi 4^N)$; settling $\tau\ln 2^{N+1}$ | $T = 2^N/f_{clk}$, $\tau \gg T$; each bit costs 4× in bandwidth | [18-06](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-06-adc-dac-pwm.md) |
| Zero-order hold: $\lvert H(f)\rvert = \lvert\operatorname{sinc}(f/f_s)\rvert$ | 0.9003 (−0.91 dB) at $f_s/4$ | [18-06](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-06-adc-dac-pwm.md) |

## RTOS

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Kernel share = tick rate × tick cost + switch rate × switch cost | Tickless idle removes the tick while idle | [18-07](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-07-rtos-concepts.md) |
| RM: $U = \sum C_i/T_i \le n(2^{1/n} - 1)$ (0.828, 0.780, → ln 2); hyperbolic $\prod(1 + U_i) \le 2$ | Sufficient only; independent periodic tasks, implicit deadlines, one core | [18-07](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-07-rtos-concepts.md) |
| Exact: $R_i = C_i + B_i + \sum_{hp}\lceil R_i/T_j\rceil C_j \le D_i$ | Response-time analysis | [18-07](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-07-rtos-concepts.md) |
| EDF: schedulable iff $U \le 1$ | Implicit deadlines, one core | [18-07](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-07-rtos-concepts.md) |
| Priority ceiling: $B_i$ = longest critical section of a lower task on a resource whose ceiling ≥ $i$'s priority | Blocked at most once; inheritance can block several times | [18-07](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-07-rtos-concepts.md) |
| Queue slots $= \lfloor t_{stall}/T_{prod}\rfloor + 1$ | Arrivals at both ends of the stall | [18-07](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-07-rtos-concepts.md) |

## Boot and firmware update

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Image size: single slot $F - B$; two slots $(F - B)/2$; swap with scratch $(F - B - S)/2$ | $F$ flash, $B$ bootloader, $S$ scratch | [18-08](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-08-boot-and-firmware-update.md) |
| Sector copy = erase + (sector/word) × program time; overwrite = $n$ copies; swap via scratch = $3n$ | Scratch sector erased $n$ times per update: life = endurance / $n$ | [18-08](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-08-boot-and-firmware-update.md) |
| Secure boot = image bytes × hash cycles/byte / $f$ + signature cycles / $f$ | A hash engine leaves the signature dominant | [18-08](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-08-boot-and-firmware-update.md) |
| P(power cut in window $w$) $= 1 - e^{-\lambda w}$ | Poisson cuts at rate λ | [18-08](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-08-boot-and-firmware-update.md) |
| Anti-rollback life = fuse bits / security increments per year | One fuse per increment | [18-08](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-08-boot-and-firmware-update.md) |

## Ultra-low power

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\bar I = \big(\sum_k I_kt_k + I_{sleep}(T - \sum_k t_k)\big)/T$; life = usable capacity / $\bar I$ | Charge per period over the period | [18-09](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-09-ultra-low-power-design.md) |
| Deeper mode pays when idle time $> \Delta Q_{wake}/(I_{shallow} - I_{deep})$ | Extra wake-up charge against current saved | [18-09](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-09-ultra-low-power-design.md) |
| Fixed voltage: charge per task = $(I_0 + kf)N/f + I_{sleep}(T - N/f)$; racing saves $I_0N/f$ terms | Dynamic charge $kN$ independent of $f$ | [18-09](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-09-ultra-low-power-design.md) |
| Dynamic energy per cycle at the core ∝ $CV^2$; through an LDO the battery supplies the core's charge, so battery drain per cycle ∝ $V$; through a buck, ∝ $V^2/\eta$ | Voltage scaling | [18-09](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-09-ultra-low-power-design.md) |
| LDO: $I_{in} = I_{out} + I_q$, $\eta = V_{out}/V_{in}$; buck: $I_{in} = V_{out}I_{out}/(\eta V_{in}) + I_q$ | Buck wins when active, LDO often when asleep | [18-09](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-09-ultra-low-power-design.md) |
| Pulse droop: $\Delta V = IR_{int}(1 - e^{-t/R_{int}C})$; without $C$, $IR_{int}$ | Coin cell plus reservoir capacitor | [18-09](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-09-ultra-low-power-design.md) |

## Sensors

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Spring–mass: $k = m\omega_0^2$; deflection $x = a/\omega_0^2$; differential $\Delta C/C = 2x/d$ | Below resonance | [18-10](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-10-sensors.md) |
| Thermomechanical floor $a_n = \sqrt{4k_BT\omega_0/(mQ)}$ per √Hz | Brownian noise of the proof mass | [18-10](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-10-sensors.md) |
| rms noise = density × √B; tilt ≈ $a_n/g$ rad near level; averaging $M$ independent samples ÷ $\sqrt M$ | Brick-wall bandwidth | [18-10](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-10-sensors.md) |
| Coriolis $a_c = 2\Omega v$, $v = 2\pi f_dx_d$ | Drive amplitude $x_d$ at $f_d$ | [18-10](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-10-sensors.md) |
| Angle noise $\sigma_\theta = \rho\sqrt{t/2}$; ARW $= 60\rho/\sqrt2$ °/√h; bias drift $= bt$ | ρ the one-sided rate noise density in °/s/√Hz | [18-10](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-10-sensors.md) |
| Complementary filter: $\tau = \alpha\Delta t/(1 - \alpha)$; bias error $b\tau$; white-noise factor $\sqrt{(1 - \alpha)/(1 + \alpha)}$ | $\theta_n = \alpha(\theta_{n-1} + \omega\Delta t) + (1 - \alpha)\theta_{acc}$ | [18-10](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-10-sensors.md) |
| PPG shot-noise SNR $= m^2I/(4qB)$; LED average = $I_{LED} \times t_{pulse} \times f_{pulse}$ | $m$ perfusion index (modulation depth), $I$ DC photocurrent during illumination | [18-10](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-10-sensors.md) |
| SPL $= 20\log_{10}(p/20\ \mu\text{Pa})$; 94 dB = 1 Pa; full scale = 94 − sensitivity (dBFS) | Microphones | [18-10](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-10-sensors.md) |
| $dp/dh = -pMg/(RT)$ ≈ −12 Pa/m at sea level | Barometric altitude | [18-10](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-10-sensors.md) |

## Hardware security

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Average brute force $= (M + 1)/2$ guesses ÷ rate | $M$ equally likely secrets | [18-11](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-11-hardware-security.md) |
| Timing attack on an $n$-byte early-exit compare: $(n - 1) \times 256 \times r + 256$ queries at most | $r$ timings averaged per guess | [18-11](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-11-hardware-security.md) |
| CPA: $\rho = \sqrt{2/(2 + \sigma^2)}$; $N \approx (z/\rho)^2 \to z^2\sigma^2/2$ | Hamming-weight leakage of a uniform byte (variance 2), noise σ | [18-11](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-11-hardware-security.md) |
| PUF: $P_{bit} = P(\text{Bin}(n, p) > n/2)$; key failure $= 1 - (1 - P_{bit})^k$ | Odd repetition length $n$, $k$ key bits | [18-11](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-11-hardware-security.md) |
| Fault injection: expected time = 1/(success probability × attempt rate); independent duplicated checks square the probability | Only if the faults are truly independent | [18-11](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-11-hardware-security.md) |
| Attack cost per device = extraction cost / devices sharing the key | The honeypot argument for per-device keys | [18-11](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-11-hardware-security.md) |
