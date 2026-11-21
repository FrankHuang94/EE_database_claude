"""Lab 18-03: interrupt timing and timer arithmetic.

- `response_time`: worst-case response time of a fixed-priority interrupt by the standard recurrence
  R = C + B + sum over higher-priority j of ceil(R / T_j) C_j (preemptive, priorities fixed, deadlines <= periods);
- `simulate`: a discrete-event simulation of the same interrupts on one core (preemptive, the highest pending
  priority runs, ties by order), with optional blocking sections, used to check the recurrence;
- timer helpers: prescaler and auto-reload search, PWM resolution, input-capture differences with wraparound,
  SysTick reload, watchdog timeouts with clock tolerance;
- `cpu_load`: fraction of the CPU an interrupt stream uses.

Times are in any consistent unit (the chapter uses microseconds).
"""
from __future__ import annotations

import heapq
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Irq:
    name: str
    C: float         # worst-case handler time, including entry and exit
    T: float         # minimum inter-arrival time (period)
    prio: int        # smaller = more urgent (as on Cortex-M)


def response_time(irqs: list[Irq], name: str, blocking: float = 0.0, max_iter: int = 1000) -> float:
    """Worst-case response time from the fixed-point recurrence; math.inf if it does not converge below T."""
    me = next(i for i in irqs if i.name == name)
    hp = [i for i in irqs if i.prio < me.prio]
    r = me.C + blocking
    for _ in range(max_iter):
        nxt = me.C + blocking + sum(math.ceil(r / j.T - 1e-12) * j.C for j in hp)
        if abs(nxt - r) < 1e-12:
            return r
        if nxt > 1e6 * me.T:
            return math.inf
        r = nxt
    return math.inf


def utilization(irqs: list[Irq]) -> float:
    return sum(i.C / i.T for i in irqs)


def simulate(irqs: list[Irq], horizon: float, offsets: dict | None = None, blocking_at: float | None = None,
             blocking_len: float = 0.0, trace: list | None = None) -> dict[str, float]:
    """Simulate periodic arrivals (each at its offset, then every T) and return each IRQ's worst observed response.

    A blocking section (interrupts disabled) of length `blocking_len` may start at `blocking_at`: while it runs,
    no handler can start, which models a critical section in main code. If `trace` is a list, the run appends
    (name, start, end) for every stretch of execution.
    """
    offsets = offsets or {}
    events = []
    for i in irqs:
        t = offsets.get(i.name, 0.0)
        while t < horizon:
            heapq.heappush(events, (t, i.name))
            t += i.T
    by_name = {i.name: i for i in irqs}
    order = {i.name: k for k, i in enumerate(irqs)}
    pending = []          # (prio, order, arrival, remaining)
    worst = {i.name: 0.0 for i in irqs}
    t = 0.0
    block_end = (blocking_at + blocking_len) if blocking_at is not None else -1.0
    running = None
    while events or pending or running:
        next_arrival = events[0][0] if events else math.inf
        if running is None and pending:
            if blocking_at is not None and blocking_at <= t < block_end:
                t = min(block_end, next_arrival)
                while events and events[0][0] <= t:
                    a, n = heapq.heappop(events)
                    heapq.heappush(pending, (by_name[n].prio, order[n], a, by_name[n].C))
                continue
            running = list(heapq.heappop(pending))
        if running is None:
            if not events:
                break
            t = max(t, next_arrival)
            while events and events[0][0] <= t:
                a, n = heapq.heappop(events)
                heapq.heappush(pending, (by_name[n].prio, order[n], a, by_name[n].C))
            continue
        finish = t + running[3]
        rname = [n for n, k in order.items() if k == running[1]][0]
        if next_arrival < finish:
            if trace is not None and next_arrival > t:
                trace.append((rname, t, next_arrival))
            running[3] -= next_arrival - t
            t = next_arrival
            while events and events[0][0] <= t:
                a, n = heapq.heappop(events)
                heapq.heappush(pending, (by_name[n].prio, order[n], a, by_name[n].C))
            if pending and pending[0][0] < running[0]:       # preempt
                heapq.heappush(pending, tuple(running))
                running = None
        else:
            if trace is not None:
                trace.append((rname, t, finish))
            t = finish
            name = rname
            worst[name] = max(worst[name], t - running[2])
            running = None
    return worst


def cpu_load(rate_hz: float, cycles_per_event: float, f_cpu_hz: float) -> float:
    return rate_hz * cycles_per_event / f_cpu_hz


# ------------------------------------------------------------------ timers
def timer_period(f_clk: float, psc: int, arr: int) -> float:
    """Update (overflow) period of an up-counting timer: (PSC + 1)(ARR + 1) / f_clk."""
    return (psc + 1) * (arr + 1) / f_clk


def find_psc_arr(f_clk: float, f_target: float, arr_bits: int = 16, psc_bits: int = 16):
    """Smallest prescaler giving an exact integer (PSC + 1)(ARR + 1) = f_clk / f_target, or None."""
    n = f_clk / f_target
    if abs(n - round(n)) > 1e-9:
        return None
    n = round(n)
    for p in range(1, 2 ** psc_bits + 1):
        if n % p == 0 and n // p <= 2 ** arr_bits:
            return p - 1, n // p - 1
    return None


def pwm_resolution_bits(f_clk: float, f_pwm: float, center_aligned: bool = False) -> float:
    steps = f_clk / f_pwm / (2 if center_aligned else 1)
    return math.log2(steps)


def capture_delta(first: int, second: int, bits: int = 16) -> int:
    """Counts between two captures of a free-running counter that may have wrapped once."""
    return (second - first) % (1 << bits)


def systick_reload(f_cpu: float, period_s: float) -> int:
    r = round(f_cpu * period_s) - 1
    if not 0 < r < 1 << 24:
        raise ValueError("does not fit the 24-bit SysTick reload register")
    return r


def watchdog_timeout(prescaler: int, reload: int, f_lsi: float) -> float:
    return prescaler * reload / f_lsi
