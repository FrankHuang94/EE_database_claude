# Lab 18-05 · Serial Links: Divisors, a UART Driver and a Receiver in Verilog

Chapter: [18-05 · Peripherals and Serial Buses: GPIO, UART, SPI, I²C](../../chapters/18-05-gpio-uart-spi-i2c.md)

## Objective

- Compute baud-rate divisors and their errors for common clocks, and see why "baud-friendly" crystals exist.
- Measure the clock-mismatch window of a 16× oversampling UART receiver in Verilog simulation, compare it with the derivation of §3.3, and predict how it moves when the sample point moves.
- Write a register-level driver for the CMSDK UART of QEMU's Cortex-M4 board and run it.
- Find where the I²C pull-up window closes as bus capacitance grows, for each speed mode.

## Background

A UART with $S$-times oversampling needs a divisor $f_{clk}/(S \cdot \text{baud})$; rounding it creates a baud error (§3.3). A receiver that samples each bit once, half a bit after detecting the start edge, accepts sender/receiver bit-time ratios $r$ from $(9.5 + 1/S)/10$ to $9.5/9$ for 8N1 frames. An I²C pull-up must satisfy $R_p \ge (V_{DD} - 0.4\ \text{V})/I_{OL}$ and $R_p \le t_{r,max}/(0.8473\,C_b)$ (§3.5); the window closes where the two bounds meet.

The firmware runs on QEMU's `mps2-an386` board, whose UART0 (an Arm CMSDK APB UART at 0x4000 4000) prints to QEMU's standard output. Its divisor register `BAUDDIV` holds the number of peripheral clock cycles per bit. QEMU clocks the board's UARTs at 25 MHz (`SYSCLK_FRQ` in QEMU's `hw/arm/mps2.c`). Its UART model (`hw/char/cmsdk-apb-uart.c`) stores `BAUDDIV`, refuses to transmit if it is below 16, and passes the resulting speed to the host's character device, but it moves characters with no line timing. So the driver's divisor is checked by reading it back, and the receiver's timing is checked in Verilog instead.

## Files

- `serialbus.py`: `uart_frame_bits`, `uart_bytes_per_s`, `baud_divisor`, `baud_error`, `uart_ratio_window`, `uart_sender_rate_tolerance`, `spi_max_clock`, `i2c_rp_min`, `i2c_rp_max`, `rc_rise_30_70`, `i2c_read_clocks`, `led_resistor_min`, `led_current`, `injection_resistor`, `e12_at_least`.
- `fw/main.c`: the UART driver (`uart_init`, `uart_putc`, `uart_puts`) and a test that prints the divisor and a greeting; `fw/startup.c`, `fw/link.ld`, `fw/semihost.h`, `fw/nvic.h` from Labs 18-02 and 18-03.
- `fwrun.py`: builds `fw/` with Lab 18-02's wrapper and runs it on QEMU.
- `hdl/uart_rx.v`: an 8N1 receiver with 16× oversampling and one sample per bit; `hdl/uart_rx_tb.v`: a self-checking testbench that sweeps $r$ from 0.940 to 1.070 in steps of 0.0025, with 16 start phases of 8 back-to-back frames each.
- `18-05-serial-lab.ipynb`: the guided notebook.

Run the testbench by hand with:

```bash
iverilog -g2012 -o /tmp/uart_rx_tb hdl/uart_rx.v hdl/uart_rx_tb.v && vvp /tmp/uart_rx_tb
```

## Procedure

1. **Divisors.** Predict the integer and 4-fraction-bit divisor errors for 9600, 115 200 and 1 000 000 baud from 16 MHz, 48 MHz and 14.7456 MHz; tabulate them with `baud_error`.
2. **The receiver's window.** Predict the first and last passing ratios on the testbench's grid; run it. Then copy `uart_rx.v`, change the start-bit comparison from `tick == 4'd7` to `tick == 4'd6` (sampling at $s = 7/16$ instead of $8/16$), predict the new window (Problem 18-05.13), and run it.
3. **The UART driver.** Predict the divisor `uart_init(115200)` computes from 25 MHz and the resulting baud rate; run the firmware at `-O2` and `-O0` and read the output.
4. **I²C pull-ups.** At 3.3 V, plot $R_{p,min}$ and $R_{p,max}$ against $C_b$ for standard mode (1000 ns, 3 mA), fast mode (300 ns, 3 mA) and fast-mode plus (120 ns, 20 mA); find where each window closes and compare with the specification's capacitance limits (400, 400 and 550 pF).
5. **SPI timing.** Plot the highest SCK against the target's clock-to-output delay from 5 to 40 ns for the delays of Example 18-05.4, with and without 3 ns translators.

## Expected results

- Part 1: from 16 MHz, 9600 baud is off by only +0.16% (divisor 104) but 115 200 by −3.55%. 48 MHz does well at both (+0.16%). 14.7456 MHz is exact for 9600 and 115 200 but cannot reach 1 Mbaud at 16× (its divisor would be below 1; the integer divisor 1 gives −7.84%).
- Part 2: the stock receiver passes from 0.9575 to 1.0550, the grid points just inside the derived 0.95625 and 1.05556; with `tick == 6` it passes from 0.9500 to 1.0475, the window shifted down by $1/144$ at the top and $1/160$ at the bottom.
- Part 3: `BAUDDIV 217`, `actual baud 115207` (+0.0064%), the greeting and `TEST PASSED` at both levels.
- Part 4: the windows close at about 1221 pF (standard), 366 pF (fast) and 977 pF (fast-mode plus). Only fast mode closes below its specification limit with the 3 mA (0.4 V) rule. The specification also requires fast-mode devices to sink 6 mA at 0.6 V for exactly this case: with that rule, $R_{p,min} = 2.7\ \text{V}/6\ \text{mA}$ = 450 Ω and the window stays open to about 787 pF, so a fully compliant fast-mode bus can use its 400 pF; one whose devices meet only the 3 mA row cannot.
- Part 5: the highest SCK falls as $1/(2(9\ \text{ns} + t_{CO}))$ (Example 18-05.4's other delays sum to 9 ns), so the translators matter most for fast targets.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 18-05.a | integer-divisor error, 16 MHz, 9600 baud | 0.16 | % |
| Lab 18-05.b | integer-divisor error, 14.7456 MHz, 1 Mbaud | −7.84 | % |
| Lab 18-05.c | first passing ratio, tick 6 | 0.9500 | — |
| Lab 18-05.d | last passing ratio, tick 6 | 1.0475 | — |
| Lab 18-05.e | BAUDDIV computed by the driver | 217 | — |
| Lab 18-05.f | resulting baud rate | 115207 | baud |
| Lab 18-05.g | resulting error | 0.0064 | % |
| Lab 18-05.h | window closes, standard mode | 1221 | pF |
| Lab 18-05.i | window closes, fast mode | 366 | pF |
| Lab 18-05.j | window closes, fast-mode plus | 977 | pF |

## Discussion

1. Why does the measured window sit just inside the derived one rather than on it?
2. Why does the testbench send frames back to back rather than with idle time between them?
3. The driver waits on the TX-full flag before each write. What happens to the program's timing at 115 200 baud if it prints a 100-character message, and how would you avoid blocking?
4. Why can the firmware's test check the divisor but not the baud rate itself?

## Answers

1. The testbench steps $r$ by 0.0025, and the derived limits 0.95625 and 1.05556 are not grid points, so the first and last passing ratios are the grid points just inside them. A finer grid near each limit would converge on the derived values, with the detection delay $\delta$ covering its range through the 16 start phases.
2. With idle time after each frame, a late stop-bit sample (fast sender) would still see the idle high level and pass; only the next start bit, arriving immediately, exposes it. Back-to-back frames are the worst case for the fast side and the normal case for a busy link.
3. Each character takes $10/115\,200 = 86.8$ µs, so 100 characters block the caller for about 8.7 ms, during which `main` does nothing else. Put characters in a ring buffer (18-04) and send from the UART's transmit interrupt, or by DMA.
4. QEMU's UART model only checks that `BAUDDIV` is valid (at least 16) and passes the speed to the host; it transfers characters with no line timing. Timing must be checked in simulation (the Verilog receiver) or on hardware with a logic analyzer.

## Optional hardware

On a real board, print a stream of 0x55 ('U', alternating bits) at 115 200 baud and measure the bit time with an oscilloscope or logic analyzer; compute the actual baud error and compare it with the divisor's prediction plus the oscillator tolerance. Then connect an I²C sensor with 10 kΩ, 4.7 kΩ and 2.2 kΩ pull-ups, measure the 30–70% rise time on SCL, and estimate the bus capacitance from $t_r = 0.8473\,R_pC_b$.
