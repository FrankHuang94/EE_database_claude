"""Lab 18-09: energy arithmetic for ultra-low-power embedded design.

- duty-cycled current profiles: average current, charge per period, battery life with usable-capacity and
  self-discharge corrections;
- break-even time for entering a deeper sleep mode;
- energy per task against clock frequency at a fixed voltage (race to idle) and with voltage scaling;
- regulator battery current (LDO against buck), including quiescent current;
- battery internal resistance and a reservoir capacitor during a load pulse;
- an event-driven simulation of a sensor node's day, to check the averages against a time-stepped total.
"""
from __future__ import annotations

import math


# ------------------------------------------------------------------ duty cycling
def average_current(profile: list[tuple[float, float]], period: float, i_sleep: float) -> float:
    """profile: (current A, duration s) of each active phase in one period; sleep fills the rest."""
    active = sum(t for _, t in profile)
    if active > period:
        raise ValueError("active phases exceed the period")
    return (sum(i * t for i, t in profile) + i_sleep * (period - active)) / period


def battery_life_hours(capacity_mah: float, i_avg: float, usable: float = 1.0,
                       self_discharge_per_month: float = 0.0) -> float:
    """Hours until a battery of capacity_mah (usable fraction `usable`) is exhausted by i_avg (A), with self-discharge
    modelled as a constant equivalent current of self_discharge_per_month x capacity per 30 days."""
    q = capacity_mah * 1e-3 * 3600 * usable                       # coulombs
    i_sd = self_discharge_per_month * capacity_mah * 1e-3 * 3600 / (30 * 86400)
    return q / (i_avg + i_sd) / 3600


# ------------------------------------------------------------------ sleep modes
def break_even_time(q_transition: float, i_shallow: float, i_deep: float) -> float:
    """Sleep duration above which the deeper mode saves charge: the transition costs q_transition (C) more than
    staying in the shallow mode, and the deep mode saves (i_shallow - i_deep) every second."""
    return q_transition / (i_shallow - i_deep)


# ------------------------------------------------------------------ race to idle
def charge_per_task(f_hz: float, cycles: float, i_per_hz: float, i_static: float, i_sleep: float,
                    period: float) -> float:
    """Charge drawn in one period when a task of `cycles` runs at f_hz (active current i_per_hz * f + i_static)
    and the device sleeps at i_sleep for the rest of the period. Fixed supply voltage."""
    t_on = cycles / f_hz
    if t_on > period:
        raise ValueError("task does not fit in the period")
    return (i_per_hz * f_hz + i_static) * t_on + i_sleep * (period - t_on)


def dynamic_energy_ratio(v_low: float, v_high: float) -> float:
    """Dynamic energy per cycle scales as C V^2."""
    return (v_low / v_high) ** 2


# ------------------------------------------------------------------ regulators
def battery_current_ldo(i_load: float, i_q: float = 0.0) -> float:
    return i_load + i_q


def battery_current_buck(i_load: float, v_out: float, v_bat: float, efficiency: float, i_q: float = 0.0) -> float:
    return v_out * i_load / (efficiency * v_bat) + i_q


# ------------------------------------------------------------------ battery pulses
def droop_no_cap(i_pulse: float, r_int: float) -> float:
    return i_pulse * r_int


def droop_with_cap(i_pulse: float, r_int: float, c: float, t_pulse: float) -> float:
    """Battery (EMF, R_int) with a reservoir capacitor at the load, fully charged before a constant-current pulse:
    the load voltage falls by i R (1 - exp(-t / R C)) at the end of the pulse."""
    return i_pulse * r_int * (1 - math.exp(-t_pulse / (r_int * c)))


def cap_for_droop(i_pulse: float, r_int: float, t_pulse: float, max_droop: float) -> float:
    frac = max_droop / (i_pulse * r_int)
    if frac >= 1:
        return 0.0
    return t_pulse / (r_int * -math.log(1 - frac))


# ------------------------------------------------------------------ event simulation
def simulate_day(events: list[tuple[float, float, float, float]], i_sleep: float, horizon: float = 86400.0,
                 dt: float = 1e-4) -> float:
    """events: (period s, offset s, current A, duration s). Sums each event's occurrences over `horizon` and returns
    the total charge (C): the sleep current for the whole horizon, plus (event current - sleep current) for the time
    each event is on. It enumerates the events rather than stepping in time (`dt` is unused, kept for compatibility),
    so it checks the budget's bookkeeping (offsets, the last partial period), not its physics. Where two events
    overlap, both currents are added and the sleep floor is counted once less: i1 + i2 - i_sleep."""
    import numpy as np
    total = i_sleep * horizon
    for period, offset, i, dur in events:
        n = math.floor((horizon - offset) / period) + 1
        starts = offset + period * np.arange(n)
        ends = np.minimum(starts + dur, horizon)
        total += (i - i_sleep) * float(np.sum(np.maximum(ends - starts, 0.0)))
    return total
