# Problems 18-05 · Peripherals and Serial Buses: GPIO, UART, SPI, I²C

Chapter: [18-05](../chapters/18-05-gpio-uart-spi-i2c.md) · Worked solutions: [18-05 solutions](../solutions/18-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** CMOS inputs have $V_{IH} = 0.7V_{DD}$ and $V_{IL} = 0.3V_{DD}$; outputs guarantee $V_{OH} \ge V_{DD} - 0.4$ V and $V_{OL} \le 0.4$ V at their rated current. The UART receiver is the one of chapter §3.3: it detects the start edge within one tick (delay $0 \le \delta < 1/S$ of a bit), samples each bit once, half a bit after detection plus whole bits, and sees frames back to back. $r$ is the sender's bit time divided by the receiver's. An I²C byte takes 9 clock periods, and START, repeated START and STOP one period each. Problems marked *(lab)* can be checked with `labs/18-05-lab/serialbus.py` or the lab's Verilog testbench.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 18-05.1 [A]

**Mixed-voltage logic.** A 1.8 V sensor and a 3.3 V MCU follow the conventions above. (a) Find the sensor's input thresholds and the MCU's. (b) Can the sensor's push-pull output drive an MCU input reliably? (c) Can the MCU's output drive the sensor's input? What else must you check?

### Problem 18-05.2 [A]

**UART throughput.** (a) A link uses 8 data bits, even parity and one stop bit (8E1) at 9600 baud. Find its byte rate and its efficiency (data bits over line bits). (b) How long does a 1 KiB log take to send at 115 200 baud, 8N1? (c) At 1 Mbaud, 8N1, how many bytes arrive per second, and what does that mean for a design that takes one interrupt per received byte?

### Problem 18-05.3 [A]

**SPI modes and transfers.** (a) A target's data sheet says: "SCK idles high; data is captured on the rising edge." Which mode is this? (b) Another says: "SCK idles low; output changes on the falling edge." Which mode? (c) An SPI NOR flash read sends a 1-byte command and a 3-byte address, then clocks out data. How long does reading 256 bytes take at 10 MHz, and what fraction of the clocks carry data? (d) The flash's faster read command needs one extra dummy byte after the address but runs at 40 MHz. How long does the same read take?

### Problem 18-05.4 [A]

**I²C addressing and arbitration.** (a) Write the first byte a controller sends to write to, and to read from, the 7-bit address 0x48. (b) Controller A starts a write to 0x48 at the same moment as controller B starts a write to 0x4C. Which controller loses arbitration, and at which address bit (counting the first bit sent as bit 1)? Why is the winner's message not corrupted? (c) The 7-bit address space reserves the groups 0000 XXX and 1111 XXX. How many addresses remain for devices?

### Problem 18-05.5 [B]

**Baud divisors from 48 MHz.** A UART runs from 48 MHz. (a) Find the 16× divisor for 1 Mbaud and its error. (b) For 921 600 baud with 16× oversampling, find the ideal divisor and the error of the nearest integer divisor. (c) Repeat (b) with 4 fraction bits. (d) Repeat with 8× oversampling and an integer divisor. (e) A UART like the lab's CMSDK UART has a divisor register that counts clock cycles per bit. What value does it need for 921 600 baud, what is the error, and how would you compute it, rounded to the nearest integer, in C with integer arithmetic only?

### Problem 18-05.6 [B]

**A clock budget.** A sender and a receiver each run from an oscillator within ±1.5% of nominal. (a) With exact divisors at both ends, find the worst-case range of $r$, and express it as the sender's worst-case baud-rate error against the receiver. Does a 16× receiver accept it? (b) The sender is a 16 MHz MCU using the integer divisor of Example 18-05.2 (−3.55% at 115 200 baud). What is the worst-case $r$ now? (c) What symmetric oscillator tolerance $\pm x$ (the same at both ends) would make (b) just work?

### Problem 18-05.7 [B]

**Frame formats and the window.** *(lab)* (a) For a 16× receiver and 8E1 frames (11 bits, the stop bit being bit 10), find the accepted range of $r$ and the sender's baud tolerances. (b) A sender transmits 8N2 frames (two stop bits) to the same 16× receiver configured for 8N1, which samples only the first stop bit. Find the new accepted range of $r$ and the fast-sender tolerance. Why does the second stop bit help only one side?

### Problem 18-05.8 [B]

**A 5 V signal into a 3.3 V pin.** A 5 V logic output drives an MCU input powered at 3.3 V that is not 5 V tolerant. Its upper clamp diode conducts at 0.3 V and allows ±2 mA of injection current. (a) Find the smallest series resistor and choose an E12 value at or above it. (b) What current does the clamp carry with your resistor? (c) The pin has 10 pF. What RC time constant does the resistor add, and does it matter for a 115 200-baud UART? (d) Where does the injected current go, and what can go wrong when the MCU is asleep or powered down?

### Problem 18-05.9 [B]

**Pull-ups for a real bus.** A 3.3 V I²C bus in fast mode (300 ns maximum rise time, 3 mA sink at 0.4 V) has ten devices of 10 pF each and 30 pF of traces. (a) Find the bus capacitance and the allowed pull-up range. (b) Do 4.7 kΩ pull-ups meet the rise time? Do 2.2 kΩ? (c) With 2.2 kΩ, what current and power does one line draw while held low?

### Problem 18-05.10 [B]

**SPI timing and delayed sampling.** A controller's SCK output delay is 1.5 ns, the trace delay 0.5 ns each way, the target's clock-to-output 8 ns and the controller's setup 4 ns; the controller's SPI is rated to 32 MHz. (a) What SCK does the timing loop allow in mode 0, and what limits the design? (b) A controller with programmable sampling delay captures MISO one full period after the launching edge instead of half a period. What does the loop allow now, and what new condition must hold? (c) Back in (a), level translators adding 3 ns in each direction are inserted. What is the highest SCK?

### Problem 18-05.11 [B]

**Bus occupancy.** *(lab)* Six identical sensors share one I²C bus. Each is read 200 times a second with START, address + W, register, Sr, address + R, 6 data bytes, STOP. (a) How many clock periods does one read take, and how long at 400 kHz? (b) What fraction of the bus time do the six sensors use? (c) Repeat (b) at 1 MHz (fast-mode plus) and, as a rough model with the same number of clock periods, at I3C's 12.5 MHz. (d) At 400 kHz, how many such sensors fit while keeping the bus below 50% busy?

### Problem 18-05.12 [C]

**Choosing buses for a wearable.** A wearable's MCU connects to a 6-axis IMU producing 12-byte samples at 1600 Hz, a NOR flash, a Bluetooth module with a UART host interface, and a PMIC. (a) What data rate does the IMU produce, in bytes and bits per second? (b) Over I²C at 400 kHz, reading one sample per transaction (1 register byte), how many clocks and how long does each read take, and what fraction of the bus is busy? (c) The IMU has a FIFO; reading 32 samples in one transaction every 20 ms, how many clocks does it take and what fraction of the bus is busy? (d) Over SPI at 8 MHz, a sample read is 1 command byte and 12 data bytes. How long does it take and what fraction of the time is the bus busy? (e) Assign each device to a bus, count the MCU pins (include RTS/CTS for the Bluetooth UART and one interrupt line from the IMU), and name the main risk of your choice.

### Problem 18-05.13 [C]

**Moving the sample point.** *(lab)* Generalize the 16× receiver so that it samples the start bit $s$ bit times after detection (and every later bit one bit after that); the lab's receiver has $s = 8/16$, set by its `tick == 7` comparison. (a) Derive the accepted range of $r$ as a function of $s$ for 8N1. (b) Evaluate it for $s = 7/16$ (`tick == 6`) and give the sender's tolerances. Which of $s = 7/16$ and $s = 8/16$ tolerates the larger symmetric error? (c) Find the continuous $s^*$ that makes the slow and fast tolerances equal, and that tolerance. (d) Predict what the lab's testbench reports on its 0.0025 grid for $s = 7/16$, and explain the result at the low end. (e) Name one reason a real receiver still samples at the centre and uses majority voting rather than moving its sample point.

---

## Objective coverage

| Learning objective (chapter 18-05) | Problems |
|---|---|
| 1. GPIO electrical limits | 1, 8 |
| 2. UART framing, divisors and tolerance | 2, 5, 6, 7, 13 |
| 3. SPI modes and timing | 3, 10, 12 |
| 4. I²C protocol, pull-ups and timing | 4, 9, 11 |
| 5. I3C and choosing a bus | 11, 12 |
| 6. Drivers and receiver simulation | 5, 13 |
