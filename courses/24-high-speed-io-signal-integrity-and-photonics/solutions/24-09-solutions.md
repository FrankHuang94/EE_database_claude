# Solutions 24-09 · Linear-Drive and Co-Packaged Optics

Problems: [24-09 problems](../problems/24-09-problems.md) · Chapter: [24-09](../chapters/24-09-lpo-and-cpo.md)

Every number is recomputed by [verify_24_09.py](../verify/verify_24_09.py).

---

## Solutions

### Solution 24-09.1

(a) $16 \times 6.4$ = **102.4** Tb/s.

(b) $102.4/0.8$ = **128** ports.

(c) $128 \times 3.5$ = **448** W.

(d) $128 \times 16$ = **2,048** W.

(e) **1,600** W per switch.

### Solution 24-09.2

LP **12.6** mW, HP **50.1** mW, SHP **398** mW. SHP is 15 dB above LP, a factor of **31.6**.

### Solution 24-09.3

(a) $1/\sqrt{2/144 + 1/49}$ = **5.40**.

(b) $Q(5.40)$ = **3.3** × 10⁻⁸.

(c) $20\log_{10}(5.40/3.49)$ = **3.8** dB.

The optical path, not the hosts, dominates the sum: $1/49$ is larger than $2/144$.

### Solution 24-09.4

(a) $1000 \times 10^{-22/20}$ = **79.4** mV.

(b) $1000 \times 10^{-4/20}$ = **631** mV.

Electrical loss in dB is a power ratio, so amplitude falls by $20\log_{10}$: the receiver on a front-panel path must recover an eye about eight times smaller.

### Solution 24-09.5

$26 - 2.5 - 1.0 - 3.69$ = **18.81** dB, a factor of **76.0**: up to **64** lanes with binary splitting.

### Solution 24-09.6

(a) $3.00/(15 \times 10^6)$ h = **200** FIT; $3.00/(50 \times 10^6)$ h = **60** FIT.

(b) $\chi^2_{0.95,4}/2$ = **4.74**, so $4.74/(15 \times 10^6)$ h = **316** FIT.

Each observed failure raises the bound: with one failure, the same 15 million hours give a bound **1.58** times higher than with none.

### Solution 24-09.7

(a) The ratio scales with the repair time: $48 \times 4/24$ = **8**.

(b) Equal when $400 \times t = 200 \times 1$ h: $t$ = **0.5** h. A CPO port matches a pluggable only if the engine is restored in half an hour, or if the fabric routes around the failure so that "repair" means rerouting.

### Solution 24-09.8

$9/1.6$ Tb/s = **5.6** pJ/bit.

### Solution 24-09.9

(a) $10^5 \times (20 - 15)$ W = **0.5** MW.

(b) LPO at 50–60% saves 10–12 W per module: **1.0** to **1.2** MW.

These are vendor figures against a vendor baseline; the size of the real saving is contested (24-09 §9).

### Solution 24-09.10

(a) $1.0/3.25$ = **31**%.

(b) $(2.25 + 2.25)/5.5$ = **82**%.

(c) $1.0 + 2 \times 2.25 + 2 \times 2.25$ = **$10.0 B**.

Paying mostly in stock means the sellers share in the acquirer's fortunes, and the share count, not the dollar figure, is fixed.

### Solution 24-09.11

(a) $512/4$ = **128** laser channels.

(b) $128/8$ = **16** ELSFP modules.

(c) $128 \times 10^{2.3}$ mW = **25.5** W optical.

(d) $25.5/0.15$ = **170** W electrical.

(e) $170/448$ = **38**%.

On these assumptions the lasers are over a third of the CPO optics' power budget, which is why laser efficiency and lanes per laser matter. The sources do not say whether Davisson's 3.5 W per port includes the external lasers; if it does not, this power comes on top of the 448 W rather than out of it.

### Solution 24-09.12

(a) $3.5/0.3$ = **11.7** W.

(b) $5 \times 5$ = **25** W.

(c) The baselines (11.7 W, 16–18 W, 25 W), port speeds and inclusion of host SerDes power differ. Ranking needs each vendor's watts per port at a stated rate on the same basis.

### Solution 24-09.13

(a) The bound is the rate at which seeing one failure or none would be only 5% likely:

$$
P(N \le 1) = e^{-\mu} + \mu e^{-\mu} = e^{-\mu}(1 + \mu) = 0.05 .
$$

The left side falls steadily as $\mu$ grows (its derivative is $-\mu e^{-\mu}$), so there is one root. Solving numerically, $\mu$ = **4.74**, so $\lambda_U = 4.74/T$. The chi-square form gives $\chi^2_{0.95,4}/2$ = **4.74**, the same number, as the identity in §3.4 of the chapter promises (Solution 24-09.6 used it).

(b) Over a long run of $n$ failure-and-repair cycles, the total up time is close to $n/\lambda$ and the total down time close to $n\,\text{MTTR}$ (law of large numbers). The down fraction is

$$
\frac{n\,\text{MTTR}}{n/\lambda + n\,\text{MTTR}} = \frac{\lambda\,\text{MTTR}}{1 + \lambda\,\text{MTTR}},
$$

which is $1 - \text{MTBF}/(\text{MTBF} + \text{MTTR})$ with MTBF $= 1/\lambda$. For small $u = \lambda\,\text{MTTR}$, $u/(1 + u) = u - u^2 + \dots \approx u$.

(c) $\lambda = 16 \times 400$ FIT = **6.4e-6** per hour. Approximately, $u = 6.4 \times 10^{-6} \times 24$ = **1.5360e-4**; exactly, $u/(1 + u)$ = **1.5358e-4**. Port-hours lost per port per year: $1.536 \times 10^{-4} \times 8766$ = **1.35**, as in Example 24-09.7(c).

(d) When each source's down fraction is small, the chance that two sources are down at once is of order $u^2$, negligible, so the down fractions (and port-hours) of separate failure sources simply add and each can be computed alone as $\lambda \times$ MTTR. The approximation fails only when repairs are long compared with the time between failures.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 24-09.1a | switch bandwidth | 102.4 | Tb/s |
| 24-09.1b | ports | 128 | |
| 24-09.1c | CPO optics power | 448 | W |
| 24-09.1d | pluggable optics power | 2048 | W |
| 24-09.1e | saving | 1600 | W |
| 24-09.2a | LP | 12.6 | mW |
| 24-09.2b | HP | 50.1 | mW |
| 24-09.2c | SHP | 398 | mW |
| 24-09.2d | SHP over LP | 31.6 | |
| 24-09.3a | linear Q | 5.40 | |
| 24-09.3b | BER | 3.3e-8 | |
| 24-09.3c | margin | 3.8 | dB |
| 24-09.4a | after 22 dB | 79.4 | mV |
| 24-09.4b | after 4 dB | 631 | mV |
| 24-09.5a | available for splitting | 18.81 | dB |
| 24-09.5b | split factor | 76.0 | |
| 24-09.5c | binary split lanes | 64 | |
| 24-09.6a | bound at 15 M h | 200 | FIT |
| 24-09.6a1 | bound at 50 M h | 60 | FIT |
| 24-09.6b0 | chi-square 95%, 4 dof, halved | 4.74 | |
| 24-09.6b | bound with one failure | 316 | FIT |
| 24-09.6c | one failure over none | 1.58 | |
| 24-09.7a | ratio with 4 h repair | 8 | |
| 24-09.7b | break-even repair time | 0.5 | h |
| 24-09.8 | energy per bit | 5.6 | pJ/bit |
| 24-09.9a | LRO saving | 0.5 | MW |
| 24-09.9b | LPO saving, low | 1.0 | MW |
| 24-09.9b1 | LPO saving, high | 1.2 | MW |
| 24-09.10a | cash share of upfront | 31 | % |
| 24-09.10b | stock share of maximum | 82 | % |
| 24-09.10c | maximum at doubled price | 10.0 | $B |
| 24-09.11a | laser channels | 128 | |
| 24-09.11b | ELSFP modules | 16 | |
| 24-09.11c | optical power | 25.5 | W |
| 24-09.11d | electrical power | 170 | W |
| 24-09.11e | share of optics power | 38 | % |
| 24-09.12a | baseline for 70% | 11.7 | W |
| 24-09.12b | baseline for 5x | 25 | W |
| 24-09.13a | Poisson root, one failure | 4.74 | |
| 24-09.13a1 | chi-square 95%, 4 dof, halved | 4.74 | |
| 24-09.13c0 | switch failure rate | 6.4e-6 | 1/h |
| 24-09.13c | unavailability, approximate | 1.5360e-4 | |
| 24-09.13c1 | unavailability, exact | 1.5358e-4 | |
| 24-09.13c2 | port-hours per port per year | 1.35 | port-h/yr |
