# Solutions 18-05 · Peripherals and Serial Buses: GPIO, UART, SPI, I²C

Problems: [18-05 problem set](../problems/18-05-problems.md) · Chapter: [18-05](../chapters/18-05-gpio-uart-spi-i2c.md). Every number below is recomputed by [verify_18_05.py](../verify/verify_18_05.py).

---

## Solutions

### Solution 18-05.1

(a) Sensor: $V_{IH} = 0.7 \times 1.8$ = **1.26** V and $V_{IL} = 0.3 \times 1.8$ = **0.54** V. MCU: $V_{IH} = 0.7 \times 3.3$ = **2.31** V and $V_{IL} = 0.3 \times 3.3$ = **0.99** V.

(b) **No.** The sensor guarantees only $V_{OH} \ge 1.8 - 0.4$ = **1.4** V, below the MCU's 2.31 V threshold, so a 1 may read as either value. Use a level translator, or an MCU I/O bank powered at 1.8 V (many MCUs have a separate I/O supply).

(c) The levels work: the MCU's $V_{OH} \ge 2.9$ V exceeds 1.26 V, and its $V_{OL} \le 0.4$ V is below 0.54 V, with a low-side noise margin of $0.54 - 0.4$ = **0.14** V. But a 3.3 V high on a 1.8 V input forward-biases the sensor's upper clamp diode and pushes current into its 1.8 V rail, so check the sensor's absolute maximum input voltage (typically $V_{DD}$ plus a few hundred millivolts). Use a translator, or drive the line open-drain with the pull-up to 1.8 V (§3.1).

### Solution 18-05.2

(a) The frame is $1 + 8 + 1 + 1 = 11$ bits: $9600/11$ = **872.7** bytes/s, efficiency $8/11$ = **72.7** %.

(b) $1024 \times 10/115\,200$ = **88.9** ms.

(c) $10^6/10$ = **100 000** bytes/s: one interrupt every **10** µs. Interrupt entry and exit alone (18-03) then take a noticeable fraction of the CPU, and any higher-priority handler longer than 10 µs loses bytes. Use the UART's FIFO with a threshold interrupt, or DMA into a ring buffer (18-04).

### Solution 18-05.3

(a) Idle high is CPOL = 1; with an idle-high clock the first edge is falling, so capturing on the rising (second) edge is CPHA = 1: **mode 3**.

(b) Idle low is CPOL = 0. If the output changes on the falling edge it is captured on the rising edge, which is the first edge for an idle-low clock: CPHA = 0, **mode 0**.

(c) $1 + 3 + 256 = 260$ bytes of 8 clocks at 100 ns: $2080 \times 100\ \text{ns}$ = **208** µs, of which $256/260$ = **98.5** % carry data. (Full duplex: the controller clocks dummy bytes out on MOSI while the data come in on MISO.)

(d) $261 \times 8/(40\ \text{MHz})$ = **52.2** µs. The dummy byte gives the flash time to fetch the first data at the higher clock.

### Solution 18-05.4

(a) The address goes in the upper seven bits and the read/write bit (0 = write) in bit 0: write $0x48 \ll 1$ = **0x90**, read $(0x48 \ll 1) | 1$ = **0x91**.

(b) MSB first, 0x48 is 100 1000 and 0x4C is 100 1100. The first four bits agree; at bit **5**, A sends 0 and B sends 1. The open-drain bus is a wired-AND, so SDA is low; B sees a 0 where it sent a 1 and **B loses** and stops driving. A never saw anything but its own bits, so its message continues intact.

(c) The two groups of 8 are 16 addresses: $128 - 16$ = **112** remain.

### Solution 18-05.5

(a) $48 \times 10^6/(16 \times 10^6)$ = **3** exactly: the error is **0** %.

(b) Ideal $48 \times 10^6/(16 \times 921\,600)$ = **3.255**. The nearest integer is 3, which gives the 1 Mbaud of (a): $10^6/921\,600 - 1$ = **+8.51** %, far outside any receiver's window.

(c) $3.255 \times 16 = 52.08$, rounded to $52/16$ = **3.25**: $48 \times 10^6/(16 \times 3.25)$ = **923 077** baud, **+0.160** %.

(d) Ideal $48 \times 10^6/(8 \times 921\,600)$ = **6.510**, rounded to **7**: **857 143** baud, **−6.99** %. Lower oversampling does not help an integer divisor here.

(e) The register counts clocks per bit: $48 \times 10^6/921\,600 = 52.08$, so **52**, giving the same **+0.160** % as (c). A cycles-per-bit divisor is equivalent to a 16× divisor with 4 fraction bits. Round to nearest in integer arithmetic by adding half the divisor before dividing:

```c
uint32_t bauddiv = (f_clk + baud / 2u) / baud;   /* (48 000 000 + 460 800) / 921 600 = 52 */
```

(The sum fits in 32 bits for any clock below 4 GHz.)

### Solution 18-05.6

(a) $r$ is the ratio of the receiver's baud rate to the sender's. The extremes are $1.015/0.985$ = **1.0305** (receiver fast, sender slow) and $0.985/1.015$ = **0.9704**. As the sender's error against the receiver, that is **−2.96** % to **+3.05** %. Both lie inside the 16× window of −5.26% to +4.58%, though only by about 1.5 points on the fast side.

(b) The sender's baud is $(1 - 0.0355)$ times nominal on top of its oscillator error, so

$$
r_{max} = \frac{1.015}{0.985 \times 0.96451} = 1.0684 > 1.0556 .
$$

**No**: the stop-bit sample can land before the stop bit begins. The other extreme, $0.985/(1.015 \times 0.96451) = 1.006$, is fine.

(c) Solve $\frac{1 + x}{(1 - x)(0.96451)} = \frac{9.5}{9}$, that is $\frac{1 + x}{1 - x} = 1.01810$: $x = 0.01810/2.01810$ = **0.90** %. A ±0.9% budget is achievable with crystals but not with a typical ±1–2% internal RC oscillator, which is why the fractional divisor is the real fix.

### Solution 18-05.7

(a) With 11 bits, the stop bit is $k = 10$. The slow-sender condition $10 + \frac12 \ge 10r$ gives $r_{max} = 10.5/10$ = **1.0500**. The fast-sender condition $\frac{1}{16} + 10.5 < 11r$ gives $r_{min} = 10.5625/11$ = **0.96023**. Tolerances: $1/1.05 - 1$ = **−4.76** % (slow) and $1/0.96023 - 1$ = **+4.14** % (fast). The longer frame shrinks both sides, because the error accumulates over one more bit.

(b) The receiver still samples the first stop bit at $k = 9$, so the slow side is unchanged: $r_{max} = 9.5/9 = 1.0556$. On the fast side, that sample now only has to fall before the *second* stop bit ends, $9.5 + \frac{1}{16} < 11r$, which gives $r > 0.869$. That is no longer binding. The tightest condition becomes the last data bit, $k = 8$: $8.5 + \frac{1}{16} < 9r$, so $r_{min} = 8.5625/9$ = **0.95139**, a fast-sender tolerance of $1/0.95139 - 1$ = **+5.11** %. The extra stop bit adds high time *after* the sampled bit. That protects a sample arriving late (fast sender), but does nothing for one arriving early (slow sender), which still meets the first stop bit's leading edge.

### Solution 18-05.8

(a) With the clamp conducting, the pin sits at $3.3 + 0.3 = 3.6$ V, so $R \ge (5 - 3.6)/(2\ \text{mA})$ = **700** Ω. The next E12 value is **820** Ω.

(b) $(5 - 3.6)/820$ = **1.71** mA.

(c) $820 \times 10\ \text{pF}$ = **8.2** ns, against a bit time of $1/115\,200$ = **8.68** µs: negligible.

(d) Through the clamp into the 3.3 V rail. If the rest of the system draws less than 1.71 mA (the MCU asleep at microamps, or its regulator off), nothing absorbs the current: the rail rises, which can partly power an MCU that should be off (back-powering). That leaves it in an undefined state, upsets power sequencing, and can stress the clamp. Prefer a 5 V-tolerant pin, a resistive divider, or a level translator.

### Solution 18-05.9

(a) $C_b = 10 \times 10 + 30$ = **130** pF. $R_{p,min} = (3.3 - 0.4)/(3\ \text{mA})$ = **967** Ω and $R_{p,max} = 300\ \text{ns}/(0.8473 \times 130\ \text{pF})$ = **2724** Ω.

(b) 4.7 kΩ: $t_r = 0.8473 \times 4700 \times 130\ \text{pF}$ = **518** ns > 300 ns, so it **fails** (it would suit standard mode). 2.2 kΩ: **242** ns, so it **passes**, and 2.2 kΩ is above the 967 Ω minimum.

(c) $3.3/2200$ = **1.50** mA, so $3.3 \times 1.5$ mA = **4.95** mW per line while it is low. The tradeoff is that a smaller pull-up is faster but burns more power whenever the line is low, which matters on battery-powered buses.

### Solution 18-05.10

(a) Half period $\ge 1.5 + 0.5 + 8 + 0.5 + 4 = 14.5$ ns, so $f \le 1/(29\ \text{ns})$ = **34.5** MHz. That is above the controller's own 32 MHz rating, so here the controller limits the design, not the loop.

(b) The full period must now cover the loop: $f \le 1/(14.5\ \text{ns})$ = **69.0** MHz (above the controller's rating again, so useful only with a faster SPI). The new condition is **hold**. The next launching edge comes one period after the first, so the old bit must still be valid when it is sampled: the loop's *minimum* delay must exceed the controller's hold time. The target's own maximum SCK also applies.

(c) Half period $\ge 14.5 + 2 \times 3 = 20.5$ ns: $f \le 1/(41\ \text{ns})$ = **24.4** MHz. Now the loop, not the controller, limits the design.

### Solution 18-05.11

(a) Three header bytes and 6 data bytes at 9 clocks, plus three: $9 \times 9 + 3$ = **84** periods, $84 \times 2.5\ \mu\text{s}$ = **210** µs.

(b) $6 \times 200 \times 210\ \mu\text{s}$ = **25.2** % of the bus time.

(c) At 1 MHz: $6 \times 200 \times 84\ \mu\text{s}$ = **10.1** %. At 12.5 MHz: $6 \times 200 \times 84 \times 80\ \text{ns}$ = **0.806** %. (I3C's framing differs in detail, so this is only a rough model.)

(d) $N \times 200 \times 210\ \mu\text{s} < 0.5$ gives $N < 11.9$: **11** sensors. Latency suffers before that, because a high-priority read waits for any transaction already on the bus.

### Solution 18-05.12

(a) $1600 \times 12$ = **19 200** bytes/s = **153.6** kbit/s of data.

(b) $9 \times (3 + 12) + 3$ = **138** clocks, $138 \times 2.5\ \mu\text{s}$ = **345** µs, and $1600 \times 345\ \mu\text{s}$ = **55.2** % of the bus. Too much: little time is left for the PMIC or for retries, and the CPU takes 1600 transactions a second.

(c) $32 \times 12 = 384$ data bytes: $9 \times (3 + 384) + 3$ = **3486** clocks = 8.715 ms every 20 ms, **43.6** % busy. The FIFO replaces 32 transactions with one and removes most of the per-transaction overhead, but the data bits themselves fill most of a 400 kHz bus.

(d) $13 \times 8 = 104$ clocks at 125 ns: **13.0** µs per sample, $1600 \times 13\ \mu\text{s}$ = **2.08** % busy.

(e) A reasonable assignment, with pins:

| Device | Bus | MCU pins |
|---|---|---|
| IMU | SPI (shared SCK, MOSI, MISO; own CS) plus its data-ready interrupt | 3 shared + 1 CS + 1 INT |
| NOR flash | the same SPI bus, own CS (or its own quad-SPI port) | 1 CS |
| Bluetooth module | UART with RTS/CTS | 4 |
| PMIC | I²C | 2 |

Total $3 + 2 + 1 + 4 + 2$ = **12** pins. The main risk is contention on the shared SPI bus: a long flash transfer (an erase-and-write log, a firmware read) delays IMU reads. Bound the flash transfers, rely on the IMU's FIFO for slack, or give the flash its own (quad-)SPI port. I3C would carry the IMU on two wires with in-band interrupts if both parts support it.

### Solution 18-05.13

(a) The receiver samples bit $k$ at $t_k = \delta + s + k$ (receiver bit times from the sender's start edge), and the sender holds bit $k$ during $[kr, (k + 1)r)$. Slow sender: $t_k \ge kr$ requires $r \le (k + s)/k$. That bound decreases with $k$, so with $\delta = 0$ the stop bit $k = 9$ binds: $r_{max} = (9 + s)/9$. Fast sender: $t_k < (k + 1)r$ requires $r > (k + s + \delta)/(k + 1)$. That bound increases with $k$ whenever $s + \delta < 1$, so $k = 9$ binds again, and with $\delta$ approaching $1/16$:

$$
\frac{9 + s + \frac{1}{16}}{10} \le r \le \frac{9 + s}{9} .
$$

The low end is attained because $\delta$ is always strictly less than one tick.

(b) $s = 7/16$: $r_{max} = 9.4375/9$ = **1.0486** and $r_{min} = 9.5/10$ = **0.9500**. The tolerances are $1/1.0486 - 1$ = **−4.64** % (slow) and $1/0.95 - 1$ = **+5.26** % (fast). The worse side is 4.64%, against 4.58% for $s = 8/16$, so $s = 7/16$ tolerates the larger symmetric error. Sampling slightly early cancels part of the detection delay, which always makes the receiver late.

(c) Equate $1 - \frac{9}{9 + s} = \frac{10}{9.0625 + s} - 1$ and solve numerically: $s^*$ = **0.4672** bit (7.48 sixteenths), with ±**4.94** % on both sides. The cost of the detection delay is visible here: with $\delta = 0$ exactly, the optimum would be $s = 0.5$ and the tolerance $1/19 = 5.26$ % on both sides.

(d) The last grid point below 1.0486 is **1.0475**. At the low end, 0.9500 is itself a grid point, and the theory accepts it because $\delta < 1/16$ strictly. So the prediction is a pass range of **0.9500** to 1.0475, which is what the testbench reports when the comparison is changed to `tick == 6`.

(e) Real lines are not ideal. Slow or asymmetric rise and fall times (RS-232 transceivers, long RS-485 cables, opto-isolators) and noise shift the edges, and the sign of the clock mismatch is unknown. Sampling at the centre keeps the most distance from both edges, and taking three samples near the centre with a majority vote rejects noise spikes. The gain from moving the sample point, 4.58% to 4.64%, is smaller than these effects.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 18-05.1a | sensor V_IH | 1.26 | V |
| 18-05.1b | sensor V_IL | 0.54 | V |
| 18-05.1c | MCU V_IH | 2.31 | V |
| 18-05.1d | MCU V_IL | 0.99 | V |
| 18-05.1e | sensor V_OH min | 1.4 | V |
| 18-05.1f | low noise margin, MCU to sensor | 0.14 | V |
| 18-05.2a | 8E1 byte rate at 9600 baud | 872.7 | bytes/s |
| 18-05.2b | 8E1 efficiency | 72.7 | % |
| 18-05.2c | 1 KiB at 115 200 baud | 88.9 | ms |
| 18-05.2d | byte rate at 1 Mbaud | 100000 | bytes/s |
| 18-05.2e | time between byte interrupts | 10 | µs |
| 18-05.3d | SPI mode, (a) | 3 | — |
| 18-05.3e | SPI mode, (b) | 0 | — |
| 18-05.3a | 256-byte read at 10 MHz | 208 | µs |
| 18-05.3b | data fraction | 98.5 | % |
| 18-05.3c | fast read at 40 MHz | 52.2 | µs |
| 18-05.4a | write address byte | 0x90 | — |
| 18-05.4b | read address byte | 0x91 | — |
| 18-05.4c | bit at which B loses | 5 | — |
| 18-05.4d | usable 7-bit addresses | 112 | — |
| 18-05.5a | 16× divisor, 1 Mbaud | 3 | — |
| 18-05.5b | error, 1 Mbaud | 0 | % |
| 18-05.5c | ideal 16× divisor, 921 600 baud | 3.255 | — |
| 18-05.5d | error, integer divisor | 8.51 | % |
| 18-05.5e | fractional divisor | 3.25 | — |
| 18-05.5f | achieved baud, fractional | 923077 | baud |
| 18-05.5g | error, fractional | 0.160 | % |
| 18-05.5h | ideal 8× divisor | 6.510 | — |
| 18-05.5i | integer 8× divisor | 7 | — |
| 18-05.5j | achieved baud, 8× | 857143 | baud |
| 18-05.5k | error, 8× | −6.99 | % |
| 18-05.5l | cycles-per-bit divisor | 52 | — |
| 18-05.5m | error, cycles-per-bit divisor | 0.160 | % |
| 18-05.6a | r max, oscillators only | 1.0305 | — |
| 18-05.6b | r min, oscillators only | 0.9704 | — |
| 18-05.6c | most negative sender error | −2.96 | % |
| 18-05.6d | most positive sender error | 3.05 | % |
| 18-05.6e | r max with the integer divisor | 1.0684 | — |
| 18-05.6f | oscillator tolerance that just works | 0.90 | % |
| 18-05.7a | r max, 8E1 | 1.0500 | — |
| 18-05.7b | r min, 8E1 | 0.96023 | — |
| 18-05.7c | slow tolerance, 8E1 | −4.76 | % |
| 18-05.7d | fast tolerance, 8E1 | 4.14 | % |
| 18-05.7e | r min, 8N2 into an 8N1 receiver | 0.95139 | — |
| 18-05.7f | fast tolerance, 8N2 | 5.11 | % |
| 18-05.8a | smallest series resistor | 700 | Ω |
| 18-05.8b | E12 choice | 820 | Ω |
| 18-05.8c | clamp current | 1.71 | mA |
| 18-05.8d | added time constant | 8.2 | ns |
| 18-05.8e | bit time at 115 200 baud | 8.68 | µs |
| 18-05.9a | bus capacitance | 130 | pF |
| 18-05.9b | R_p min | 967 | Ω |
| 18-05.9c | R_p max | 2724 | Ω |
| 18-05.9d | rise time with 4.7 kΩ | 518 | ns |
| 18-05.9e | rise time with 2.2 kΩ | 242 | ns |
| 18-05.9f | current while low | 1.50 | mA |
| 18-05.9g | power while low | 4.95 | mW |
| 18-05.10a | SCK from the timing loop | 34.5 | MHz |
| 18-05.10b | SCK with full-period sampling | 69.0 | MHz |
| 18-05.10c | SCK with translators | 24.4 | MHz |
| 18-05.11a | clock periods per read | 84 | — |
| 18-05.11b | read time at 400 kHz | 210 | µs |
| 18-05.11c | bus occupancy at 400 kHz | 25.2 | % |
| 18-05.11d | bus occupancy at 1 MHz | 10.1 | % |
| 18-05.11e | bus occupancy at 12.5 MHz | 0.806 | % |
| 18-05.11f | sensors below 50% at 400 kHz | 11 | — |
| 18-05.12a | IMU data rate | 19200 | bytes/s |
| 18-05.12b | IMU data rate | 153.6 | kbit/s |
| 18-05.12c | clocks per single-sample read | 138 | — |
| 18-05.12d | single-sample read time | 345 | µs |
| 18-05.12e | bus busy, single samples | 55.2 | % |
| 18-05.12f | clocks per FIFO read | 3486 | — |
| 18-05.12g | bus busy with the FIFO | 43.6 | % |
| 18-05.12h | SPI sample read time | 13.0 | µs |
| 18-05.12i | SPI bus busy | 2.08 | % |
| 18-05.12j | MCU pins | 12 | — |
| 18-05.13a | r max, s = 7/16 | 1.0486 | — |
| 18-05.13b | r min, s = 7/16 | 0.9500 | — |
| 18-05.13c | slow tolerance, s = 7/16 | −4.64 | % |
| 18-05.13d | fast tolerance, s = 7/16 | 5.26 | % |
| 18-05.13e | balanced sample point | 0.4672 | bit |
| 18-05.13f | balanced tolerance | 4.94 | % |
| 18-05.13g | simulated first pass, s = 7/16 | 0.9500 | — |
| 18-05.13h | simulated last pass, s = 7/16 | 1.0475 | — |
