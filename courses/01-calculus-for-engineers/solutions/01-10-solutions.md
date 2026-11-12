# Solutions 01-10 · Multivariable Calculus II: Multiple, Line and Surface Integrals

Problems: [01-10 problems](../problems/01-10-problems.md) · Chapter: [01-10](../chapters/01-10-multivariable-calculus-2.md)

Every numerical answer below is listed in the answer key at the end and is recomputed independently by [verify_01_10.py](../verify/verify_01_10.py).

---

## Solutions

### Solution 01-10.1

(a) The inner integral is $\int_0^2(x + y)\,dy = 2x + 2$. Then $\int_0^1(2x + 2)\,dx = 1 + 2 = $ **3**.

(b) The inner integral is $\int_0^xxy\,dy = x^3/2$. Then $\int_0^1x^3/2\,dx = $ **0.125**.

(c) The region is $0 \le y \le x \le 1$, a triangle. With $x$ outside: $\int_0^1\int_0^xe^{x^2}dy\,dx = \int_0^1xe^{x^2}dx = \tfrac{1}{2}(e - 1) = $ **0.8591**. In the original order the inner integral $\int e^{x^2}dx$ has no elementary form.

### Solution 01-10.2

(a) $\int_0^{2\pi}\int_1^2r\,dr\,d\theta = 2\pi\cdot\tfrac{3}{2} = 3\pi = $ **9.425**.

(b) $\int_0^{2\pi}\int_0^1r^2\cdot r\,dr\,d\theta = 2\pi\cdot\tfrac{1}{4} = $ **1.571** (π/2).

(c) $2\pi\int_0^2e^{-r^2}r\,dr = \pi(1 - e^{-4}) = $ **3.084**, already 98% of the whole-plane value π.

### Solution 01-10.3

(a) $\int_0^{2\pi}\int_0^\pi\int_0^2\rho^2\sin\phi\,d\rho\,d\phi\,d\theta = \tfrac{8}{3}\cdot2\cdot2\pi = \tfrac{32\pi}{3} = $ **33.51**.

(b) $\int_0^3\int_0^{2\pi}\int_0^1r\,dr\,d\theta\,dz = \tfrac{1}{2}\cdot2\pi\cdot3 = $ **9.425** (3π).

(c) $\int_0^14\pi\rho^2\cdot\rho^2\,d\rho = 4\pi/5 = $ **2.513**.

### Solution 01-10.4

(a) $\nabla\cdot\mathbf{F} = 2x + x + 1 = 3x + 1$, which is **4** at (1, 2, 3). $\nabla\times\mathbf{F} = (0 - 0,\ 0 - 0,\ y - 0) = (0, 0, y)$, which is **(0, 0, 2)** at (1, 2, 3).

(b) $\nabla\cdot\mathbf{G} = 0$ and $\nabla\times\mathbf{G} = (0, 0, 1 - (-1)) = (0, 0, 2)$: pure, uniform rotation with no sources.

### Solution 01-10.5

$Q = \int_0^{0.05}\int_0^{0.1}\sigma_0(1 + x/0.1)\,dx\,dy = \sigma_0\times0.05\times(0.1 + 0.05) = 2\times10^{-9}\times0.0075 = $ **15 pC**. The average is $Q/\text{area} = 15\text{ pC}/0.005\text{ m}^2 = $ **3 nC/m²**, the value of σ at the middle, $x = L/2$, because σ is linear in $x$.

### Solution 01-10.6

(a) $P = \int_0^6\int_0^8(0.3 + 0.9e^{-x/2})\,dx\,dy = 6\big[0.3(8) + 1.8(1 - e^{-4})\big] = 6(2.4 + 1.767) = $ **25.00 W**.

(b) Average $25.00/48 = $ **0.5209 W/mm²**. The peak, along $x = 0$, is 1.2 W/mm², a peak-to-average ratio of **2.304**.

### Solution 01-10.7

(a) $P = 2\pi I_0\int_0^\infty e^{-2r^2/w^2}r\,dr = 2\pi I_0\cdot\frac{w^2}{4} = \frac{\pi}{2}I_0w^2$, using the substitution $u = 2r^2/w^2$.

(b) The fraction within $a$ is $1 - e^{-2a^2/w^2}$: **86.47%** at $a = w$ and **98.89%** at $a = 1.5w$.

(c) $1 - e^{-2(4.5/5.2)^2} = 1 - e^{-1.498} = $ **77.64%**. (Real fiber coupling is governed by the overlap between the beam's field and the fiber mode, a related integral. Coupling losses of a few tenths of a dB to a few dB are typical, and they matter in every optical link budget.)

### Solution 01-10.8

(a) $\partial F_y/\partial x = 2y = \partial F_x/\partial y$, so $\mathbf{F}$ is conservative, with $\varphi = xy^2$. The integral is $\varphi(2, 1) - \varphi(0, 0) = $ **2**.

(b) With $x = 2\cos t$, $y = 2\sin t$: $\mathbf{G}\cdot\mathbf{r}' = (-2\sin t)(-2\sin t) + (2\cos t)(2\cos t) = 4$, so $\oint = 4\times2\pi = $ **25.13** (8π). Green's theorem: $\iint(\partial_xG_y - \partial_yG_x)\,dA = \iint2\,dA = 2\times4\pi = 8\pi$ ✓.

### Solution 01-10.9

(a) $V_A - V_B = \int_A^B\mathbf{E}\cdot d\mathbf{l} = 1000\times0.02 + 0\times0.01 = $ **20 V**. The field has no $y$ component, so moving in $y$ is moving along an equipotential.

(b) $W = \dfrac{1}{4\pi\varepsilon_0}\dfrac{q_1q_2}{r} = 8.988\times10^9\times10^{-18}/0.01 = $ **8.988×10^−7 J**, the line integral of the repulsive force from infinity to 1 cm.

### Solution 01-10.10

(a) By Ampère's law, $\oint\mathbf{B}\cdot d\mathbf{l} = \mu_0I = $ **2.513×10^−6 T·m**. At 1 cm, $B = \mu_0I/(2\pi r) = $ **40.00 µT**.

(b) The flux is $\Phi = BA = 10\text{ µT}\sin(\omega t)\times10^{-3}\text{ m}^2$, and the EMF is $-d\Phi/dt$, with peak $AB\omega = 10^{-3}\times10^{-5}\times2\pi\times50 = $ **3.142 µV**. KVL assumed $\oint\mathbf{E}\cdot d\mathbf{l} = 0$; Faraday's law says it equals $-d\Phi/dt$, so a few microvolts appear around the loop that no component "drops". **Shrink the loop area**: route the return path directly beside or beneath the signal (a ground plane), or twist the pair. The EMF scales with area, and for sensitive analog paths microvolts matter.

### Solution 01-10.11

(a) On the sphere, $\mathbf{F}\cdot\mathbf{n} = r = 2$, so the flux is $2\times4\pi(2)^2 = 32\pi = $ **100.5**. The divergence is 3, so the volume integral is $3\times\tfrac{4}{3}\pi(2)^3 = 32\pi$ ✓.

(b) $Q/\varepsilon_0 = 10^{-9}/8.854\times10^{-12} = $ **112.9 V·m**, independent of the radius. The field falls as $1/r^2$ while the area grows as $r^2$.

### Solution 01-10.12

(a) $Q(r) = \int_0^r\rho_0(1 - s/R)4\pi s^2\,ds = 4\pi\rho_0\left(\dfrac{r^3}{3} - \dfrac{r^4}{4R}\right)$.

(b) Gauss on a sphere of radius $r$: $E(r) = \dfrac{Q(r)}{4\pi\varepsilon_0r^2} = \dfrac{\rho_0}{\varepsilon_0}\left(\dfrac{r}{3} - \dfrac{r^2}{4R}\right)$. At $r = R/2 = 0.05$ m: $Q = $ **3.272×10^−10 C**, and $E = $ **1176 V/m**.

(c) $dE/dr = \dfrac{\rho_0}{\varepsilon_0}\left(\dfrac{1}{3} - \dfrac{r}{2R}\right) = 0$ at $r = 2R/3 = $ **0.06667 m**. There $E_{max} = \dfrac{\rho_0}{\varepsilon_0}\cdot\dfrac{R}{9} = $ **1255 V/m**, larger than the surface value of 941 V/m. Beyond $2R/3$, the little charge added in the thin, low-density outer shells cannot keep up with the $1/r^2$ spreading of the field. Electric field stress, which governs dielectric breakdown, can peak inside a structure.

### Solution 01-10.13

(a) $\delta = \sqrt{1.72\times10^{-8}/(\pi f\times1.2566\times10^{-6})}$: **0.2087 mm** at 100 kHz and **0.06601 mm** at 1 MHz.

(b) $I = \int_0^RJ_0e^{(r - R)/\delta}2\pi r\,dr$. By parts, $\int_0^Rre^{(r - R)/\delta}dr = \delta R - \delta^2\left(1 - e^{-R/\delta}\right)$. The effective area $I/J_0$ is **1.040 mm²** at 100 kHz and **0.3874 mm²** at 1 MHz, against $\pi R^2 = 3.142$ mm².

(c) The resistance ratios are about **3.02** at 100 kHz and **8.11** at 1 MHz. Solid round wire wastes most of its copper at high frequency. That is why switching converters use Litz wire (many insulated strands) or foil windings, and why high-speed PCB losses grow with the square root of frequency ([24-01](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md)).

### Solution 01-10.14

(a) With DPW $= \pi(150)^2/A - \pi(300)/\sqrt{2A}$ and $Y = e^{-0.001A}$ ($A$ in mm², since 0.1/cm² = 0.001/mm²):

| Die area (mm²) | Gross DPW | Yield | Good dies |
|---|---|---|---|
| 25 | **2694** | 97.53% | **2628** |
| 100 | 640.2 | **90.48%** | **579.3** |
| 400 | 143.4 | 67.03% | **96.12** |
| 800 | 64.80 | **44.93%** | **29.11** |

(b) Cost per good die is proportional to $1/(\text{good dies})$: $579.3/29.11 = $ **19.9×** more for 8× the area. Cost grows much faster than area, because of both edge loss and yield.

(c) A 200 mm² chiplet gives 306.3 gross and 250.8 good dies (Y = 81.87%), so **62.70** sets of four per wafer: 2.15× the monolithic good-die count. The saving must pay for advanced packaging, die-to-die interfaces and their power, test of known-good dies, and assembly yield. That is the real chiplet tradeoff ([25-07](../../25-fabrication-packaging-test-and-reliability/chapters/25-07-advanced-packaging-and-chiplets.md)).

### Solution 01-10.15

(a) With $P = -y/2$ and $Q = x/2$, Green's theorem gives $\iint(\tfrac{1}{2} + \tfrac{1}{2})\,dA = $ area. For the ellipse, $x\,dy - y\,dx = (3\cos t)(2\cos t)\,dt + (2\sin t)(3\sin t)\,dt = 6\,dt$, so the area is $\tfrac{1}{2}\times6\times2\pi = 6\pi = $ **18.85** ($\pi ab$ ✓). This is the principle of the planimeter, which measures area by tracing a boundary.

(b) On the unit circle, $\mathbf{F} = (-\sin t, \cos t)$ and $\mathbf{r}' = (-\sin t, \cos t)$, so $\mathbf{F}\cdot\mathbf{r}' = 1$ and the circulation is **6.283** (2π). Green's theorem requires the field to be smooth *throughout* the enclosed region, but $\mathbf{F}$ blows up at the origin, which is inside the loop. The curl is zero everywhere it is defined, yet a "hole" carries circulation. This is exactly the magnetic field of a straight wire along the $z$ axis, scaled: $\mathbf{B} = \frac{\mu_0I}{2\pi}\mathbf{F}$, with the current concentrated in the hole.

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 01-10.1a | (a) | 3 | — |
| 01-10.1b | (b) | 0.125 | — |
| 01-10.1c | (c) | 0.8591 | — |
| 01-10.2a | annulus area | 9.425 | — |
| 01-10.2b | (b) | 1.571 | — |
| 01-10.2c | (c) | 3.084 | — |
| 01-10.3a | ball volume | 33.51 | — |
| 01-10.3b | cylinder volume | 9.425 | — |
| 01-10.3c | (c) | 2.513 | — |
| 01-10.4a | div F at (1,2,3) | 4 | — |
| 01-10.4b | z-component of curl F at (1,2,3) | 2 | — |
| 01-10.4c | z-component of curl G | 2 | — |
| 01-10.5a | total charge | 15 | pC |
| 01-10.5b | average density | 3 | nC/m² |
| 01-10.6a | total power | 25.00 | W |
| 01-10.6b | average density | 0.5209 | W/mm² |
| 01-10.6c | peak-to-average | 2.304 | — |
| 01-10.7a | power within w | 86.47 | % |
| 01-10.7b | power within 1.5w | 98.89 | % |
| 01-10.7c | power on the fiber core | 77.64 | % |
| 01-10.8a | line integral | 2 | — |
| 01-10.8b | circulation | 25.13 | — |
| 01-10.9a | V_A − V_B | 20 | V |
| 01-10.9b | work | 8.988×10^-7 | J |
| 01-10.10a | circulation of B | 2.513×10^-6 | T·m |
| 01-10.10b | B at 1 cm | 40.00 | µT |
| 01-10.10c | peak induced EMF | 3.142 | µV |
| 01-10.11a | flux of F | 100.5 | — |
| 01-10.11b | electric flux | 112.9 | V·m |
| 01-10.12a | Q(R/2) | 3.272×10^-10 | C |
| 01-10.12b | E(R/2) | 1176 | V/m |
| 01-10.12c | location of max E | 0.06667 | m |
| 01-10.12d | max E | 1255 | V/m |
| 01-10.13a | δ at 100 kHz | 0.2087 | mm |
| 01-10.13b | δ at 1 MHz | 0.06601 | mm |
| 01-10.13c | effective area at 100 kHz | 1.040 | mm² |
| 01-10.13d | effective area at 1 MHz | 0.3874 | mm² |
| 01-10.13e | resistance ratio at 100 kHz | 3.02 | — |
| 01-10.13f | resistance ratio at 1 MHz | 8.11 | — |
| 01-10.14a | gross DPW, 25 mm² | 2694 | — |
| 01-10.14b | good dies, 25 mm² | 2628 | — |
| 01-10.14c | yield, 100 mm² | 90.48 | % |
| 01-10.14d | good dies, 100 mm² | 579.3 | — |
| 01-10.14e | good dies, 400 mm² | 96.12 | — |
| 01-10.14f | yield, 800 mm² | 44.93 | % |
| 01-10.14g | good dies, 800 mm² | 29.11 | — |
| 01-10.14h | cost ratio 800 vs 100 mm² | 19.9 | — |
| 01-10.14i | chiplet sets per wafer | 62.70 | — |
| 01-10.15a | ellipse area | 18.85 | — |
| 01-10.15b | circulation around the hole | 6.283 | — |
