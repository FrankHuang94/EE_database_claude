# Solutions 18-11 · Hardware Security

Problems: [18-11 problem set](../problems/18-11-problems.md) · Chapter: [18-11](../chapters/18-11-hardware-security.md). Every number below is recomputed by [verify_18_11.py](../verify/verify_18_11.py).

---

## Solutions

### Solution 18-11.1

(a) $(2^{20} + 1)/2/100$ s = 5243 s = **87.4** minutes.

(b) $36^6$ = **2 176 782 336** codes; on average $(36^6 + 1)/2/1000$ s = **12.6** days.

(c) Rate limiting with growing lockouts (or a permanent lock after a few failures), and replacing fixed codes by a challenge–response protocol with a per-device key, so that there is nothing to guess.

### Solution 18-11.2

Seven bytes by timing, at most $256 \times 50$ queries each, plus at most 256 accept/reject tries for the last byte: $7 \times 256 \times 50 + 256$ = **89 856** queries.

### Solution 18-11.3

$\sigma$ = 2: $\rho = \sqrt{2/6}$ = **0.577**, $N = (5/0.577)^2$ = **75**. $\sigma$ = 4: $\rho = \sqrt{2/18}$ = **0.333**, $N$ = **225**. $\sigma$ = 8: $\rho = \sqrt{2/66}$ = **0.174**, $N$ = **825**. The doublings multiply the traces by **3** and **3.67**, approaching 4, because once noise dominates, $\rho \approx \sqrt2/\sigma$ and $N \propto \sigma^2$.

### Solution 18-11.4

The smallest odd $n$ with $1 - (1 - P_{bit})^{256} \le 10^{-6}$ is **33**, using $256 \times 33$ = **8448** cells. At $n$ = 33 the key fails with probability **6.1e-7**; at $n$ = 31 with **1.75e-6**, above the target.

### Solution 18-11.5

(a) $1/(10^{-5} \times 50)$ s = 2000 s = **33.3** minutes.

(b) $1/(10^{-10} \times 50)$ s = $2 \times 10^8$ s = **6.34** years, if the faults are independent.

(c) Two identical checks back to back can be defeated by one longer glitch or by a fault that corrupts the shared value both read. The checks should read the value separately, test complementary encodings (a pattern and its bitwise complement), and ideally be separated by a random delay so that their timing differs between runs.

### Solution 18-11.6

(a) $\$200\,000/100\,000$ = **\$2** per device.

(b) **\$200 000** per device.

(c) At least **5** years, unless the product's expected lifetime is shorter; an early warning within **24** hours of becoming aware of active exploitation (the full notification within 72 hours).

### Solution 18-11.7

(a) Secure: the boot verification, the key store, the cryptographic services (the TLS library's private-key operations, or a crypto service it calls), attestation, and the firmware-update verification and installation. Non-secure: the RTOS, the TCP/IP stack, the TLS protocol logic and the application. The network-facing code is the most likely to have exploitable bugs, and keeping it Non-secure means an exploit cannot read keys or bypass update verification, only request services through the gateway.

(b) $1000 \times 50/64 \times 10^6$ = **0.078** % of the CPU.

(c) That a buffer passed in lies entirely in Non-secure memory (Armv8-M provides the TT instruction to test address attributes), so that a compromised Non-secure caller cannot trick Secure code into reading or overwriting Secure memory on its behalf.

### Solution 18-11.8

(a)

```c
#include <stddef.h>
#include <stdint.h>

int ct_compare(const uint8_t *a, const uint8_t *b, size_t n)
{
    uint8_t diff = 0;
    for (size_t i = 0; i < n; i++)
        diff |= (uint8_t)(a[i] ^ b[i]);   /* no branch on secret data */
    return diff;                          /* 0 if equal, nonzero otherwise */
}
```

(b) An optimizer may legally insert an early exit, since the result is the same, and that would bring the leak back. Inspect the generated assembly (as in 18-02), or use a vetted library function intended to be constant-time, and measure the timing on the target for equal and unequal inputs.

(c) Table look-ups indexed by secret data (for example a software AES S-box) when the memory system has caches or wait states that depend on the address; also branches on secret bits in modular exponentiation, and early returns on padding checks.

### Solution 18-11.9

(a) On average $(10^6 + 1)/2$ tries, in groups of 5 per minute: about 100 000 minutes = **69.4** days of continuous attack. That is feasible for a determined attacker with a device near the lock.

(b) *Assets:* the ability to unlock, the user's credentials and pairing keys, the access log. *Attackers:* a remote attacker (through the phone app or cloud), a nearby attacker over Bluetooth, an attacker with physical access to the outdoor unit. *Surfaces:* the Bluetooth pairing and protocol, the cloud and app interface, the firmware-update path, the physical unit (debug pads, wiring to the motor).

(c) Exponentially growing lockouts or a hard lock after a small number of failures (cost: a denial-of-service risk, where an attacker locks out the owner, so recovery needs a second factor); out-of-band pairing that needs physical presence inside, such as a button on the indoor unit (cost: user friction and an extra component); or a pairing protocol not based on a guessable PIN, such as numeric comparison with authenticated key exchange (cost: implementation complexity).

### Solution 18-11.10

(a) The leakage of the attacked look-up appears at the measured instant only one time in 16, so its correlation falls by about a factor of **16**.

(b) $\rho = 0.426/16 = 0.0267$, so $N \approx (4.5/0.0267)^2$ = **28 512** traces, **256** times more.

(c) Shuffling only dilutes the leakage; an attacker can still align or combine traces (integrating over the possible positions) and recover much of the loss. Masking removes the first-order dependence entirely. Combined, the attacker must defeat both the randomization in time and the randomization in value, which multiplies the effort.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 18-11.1a | average time, 20-bit code | 87.4 | min |
| 18-11.1b | number of 6-character codes | 2176782336 | — |
| 18-11.1c | average time, 6-character code | 12.6 | days |
| 18-11.2a | queries, 8-byte token | 89856 | — |
| 18-11.3a | correlation at σ = 2 | 0.577 | — |
| 18-11.3b | traces at σ = 2 | 75 | — |
| 18-11.3c | correlation at σ = 4 | 0.333 | — |
| 18-11.3d | traces at σ = 4 | 225 | — |
| 18-11.3e | correlation at σ = 8 | 0.174 | — |
| 18-11.3f | traces at σ = 8 | 825 | — |
| 18-11.3g | first doubling factor | 3 | — |
| 18-11.3h | second doubling factor | 3.67 | — |
| 18-11.4a | repetition length | 33 | — |
| 18-11.4b | cells | 8448 | — |
| 18-11.4c | key failure at n = 33 | 6.1e-7 | — |
| 18-11.4d | key failure at n = 31 | 1.75e-6 | — |
| 18-11.5a | expected time, single check | 33.3 | min |
| 18-11.5b | expected time, double check | 6.34 | years |
| 18-11.6a | cost per device, shared key | 2 | \$ |
| 18-11.6b | cost per device, per-device keys | 200000 | \$ |
| 18-11.6c | minimum support period | 5 | years |
| 18-11.6d | early-warning deadline | 24 | h |
| 18-11.7a | CPU fraction of gateway calls | 0.078 | % |
| 18-11.9a | online brute-force time | 69.4 | days |
| 18-11.10a | correlation reduction factor | 16 | — |
| 18-11.10b | traces with shuffling | 28512 | — |
| 18-11.10c | increase in traces | 256 | — |
