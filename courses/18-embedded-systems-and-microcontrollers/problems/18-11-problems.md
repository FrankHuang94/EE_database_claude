# Problems 18-11 · Hardware Security

Chapter: [18-11](../chapters/18-11-hardware-security.md) · Worked solutions: [18-11 solutions](../solutions/18-11-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Brute force of a uniformly random secret with $M$ possible values takes $(M + 1)/2$ guesses on average. CPA uses a Hamming-weight leakage with noise $\sigma$, so $\rho = \sqrt{2/(2 + \sigma^2)}$ and $N \approx (z/\rho)^2$. PUF cells flip independently. Problems marked *(lab)* can be checked with `labs/18-11-lab/hwsec.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 18-11.1 [A]

**Short secrets.** (a) A debug-unlock code has 20 random bits and can be tried 100 times a second. How long does an attacker need on average? (b) A 6-character code of digits and capital letters (36 symbols) tried 1000 times a second? (c) What two design changes make such codes acceptable?

### Problem 18-11.2 [A]

**A shorter token.** *(lab)* An 8-byte token is checked with an early-exit comparison; an attacker averages 50 timings per guess. How many queries does a byte-by-byte attack need at most, counting the last byte's accept/reject tries?

### Problem 18-11.3 [B]

**Noise against traces.** *(lab)* For a 5-standard-deviation margin ($z$ = 5), find the correlation and the traces a CPA needs at noise $\sigma$ = 2, 4 and 8. By what factor does each doubling of the noise multiply the traces, and what factor does it approach?

### Problem 18-11.4 [B]

**A 256-bit PUF key.** *(lab)* SRAM cells flip with probability 0.10. With a repetition code and majority decoding, what repetition length keeps a 256-bit key's failure probability below $10^{-6}$, how many cells does that use, and what is the failure probability at that length and at the next shorter length?

### Problem 18-11.5 [B]

**Glitching with redundancy.** A glitch succeeds with probability $10^{-5}$ per attempt, at 50 attempts per second. (a) What is the expected time to skip a single check? (b) If the check is duplicated with complementary encodings, so that two independent faults are needed, what is it then? (c) Why should the two checks not be identical instructions back to back?

### Problem 18-11.6 [B]

**Pricing the honeypot.** Extracting a key from one device costs \$200 000. (a) What does it cost per device to compromise a fleet of 100 000 devices sharing the key? (b) With per-device keys? (c) Under the EU Cyber Resilience Act, what minimum support period should the manufacturer plan for vulnerability handling, and when must it give an early warning of an actively exploited vulnerability?

### Problem 18-11.7 [B]

**Partitioning with TrustZone-M.** A connected sensor runs an RTOS, a TCP/IP stack, a TLS library, an application, a firmware-update client and a key store. (a) Which components belong in the Secure world, and why? (b) The application makes 1000 secure-gateway calls a second, each costing 50 cycles of overhead on a 64 MHz core. What fraction of the CPU is that? (c) What must Secure code check about every pointer it receives?

### Problem 18-11.8 [B]

**Writing a constant-time comparison.** (a) Write a C function that compares two 16-byte buffers in constant time and returns 0 if they are equal. (b) Why must the compiler not turn it back into an early exit, and how do you check that it has not? (c) Name one other common timing leak in embedded cryptographic code.

### Problem 18-11.9 [C]

**A smart lock's pairing PIN.** A smart lock pairs over Bluetooth with a random 6-digit PIN. After 5 wrong tries it locks out for 1 minute. (a) How long does an online brute-force attack take on average? (b) Write a short threat model for the lock: three assets, three attackers, four attack surfaces. (c) Propose two improvements to the pairing scheme and say what each costs.

### Problem 18-11.10 [C]

**Shuffling as a countermeasure.** *(lab)* An AES implementation processes its 16 first-round S-box look-ups in a random order each run, so the attacked look-up falls at the measured instant only one time in 16. (a) Approximately by what factor does the correlation of the right key guess fall? (b) Starting from Example 18-11.3's $\sigma$ = 3 and $z$ = 4.5, how many traces does the attack now need? (c) Why is shuffling weaker than masking, and why are the two often combined?

---

## Objective coverage

| Learning objective (chapter 18-11) | Problems |
|---|---|
| 1. Threat models and attack economics | 1, 6, 9 |
| 2. Roots and chains of trust | 9 |
| 3. Isolation and key storage | 4, 7 |
| 4. Side channels and their countermeasures | 2, 3, 8, 10 |
| 5. PUF error correction and fault injection | 4, 5 |
| 6. Certification and regulation | 6 |
