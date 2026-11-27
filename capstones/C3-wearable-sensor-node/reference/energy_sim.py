#!/usr/bin/env python3
"""C3 reference: an event-level energy simulation of the sensor node, as a check on budget.py.

Two simulations:
  simulate_hour(per)  steps through one hour event by event: every PPG sample (wake and interrupt, I2C read with the
                      CPU idle, LED pulse), every connection event (with a retransmission at the next event when a
                      packet is lost, with probability per, seeded), the once-per-second processing, and the
                      continuous floors. It accumulates charge separately on each rail and from the cell directly.
                      With per = 0 its average current must equal budget.battery_current().
  discharge()         integrates the cell from full to the usable limit with an open-circuit voltage that falls
                      linearly from 4.2 V to 3.0 V across the state of charge (a simplification: a real LiPo curve
                      is flatter in the middle), so the bucks draw more current as the cell empties.
"""
from __future__ import annotations

import numpy as np

import budget as b


def simulate_hour(per=0.0, seed=7, seconds=3600):
    rng = np.random.default_rng(seed)
    q_soc = 0.0                                   # charge on the 3.0 V rail, C
    q_imu = 0.0                                   # charge on the 1.8 V rail, C
    q_cell = 0.0                                  # charge drawn directly from the cell, C
    t_i2c = b.i2c_time()
    for _ in range(int(seconds * b.FS)):          # PPG samples
        q_soc += b.SOC_ACTIVE * (b.SOC_WAKE + b.ISR_T)       # wake and interrupt
        q_soc += b.SOC_IDLE_DMA * t_i2c                      # I2C transfer by DMA, CPU idle
        q_cell += b.LED_I * b.LED_T                          # LED pulse from TX_SUP
    pending, retx = 0, 0
    q_event = b.ble_event_charge(b.SOC_TX8)
    q_retx = b.SOC_TX8 * b.packet_time(b.LL_PAYLOAD) + b.SOC_RX * (b.packet_time(0) + b.T_IFS)   # one more exchange
    for _ in range(int(seconds / b.T_CI)):        # connection events
        q_soc += q_event
        if pending:                               # resend the lost notification in this event
            q_soc += q_retx
            retx += 1
            pending = 0
        if rng.random() < per:
            pending = 1
        q_soc += b.SOC_ACTIVE * b.HR_CYCLES / (b.CPU_MHZ * 1e6) * b.T_CI   # heart rate, steps, packing
    q_soc += seconds * (b.SOC_STANDBY + b.SOC_RX * b.SCA_PPM * 1e-6 + b.AFE_RX + b.AFE_IO)
    q_imu += seconds * b.IMU_LP25
    q_cell += seconds * (b.AFE_TXQ + b.PMIC_IQ + b.LEAK)
    i_cell = (q_soc * b.V_SOC / (b.ETA * b.V_BAT) + q_imu * b.V_IMU / (b.ETA * b.V_BAT) + q_cell) / seconds
    return i_cell, retx


def discharge(dt=60.0):
    """Hours from full to the usable limit with OCV = 3.0 V + 1.2 V x state of charge."""
    p_rails = sum(b.soc_rail_items().values()) * b.V_SOC + b.IMU_LP25 * b.V_IMU     # W delivered by the bucks
    direct = b.LED_I * b.LED_T * b.FS + b.AFE_TXQ + b.PMIC_IQ + b.LEAK
    q_total = b.CAP_MAH * 3.6                     # C
    soc, t = 1.0, 0.0
    while soc > 1.0 - b.USABLE:
        v = 3.0 + 1.2 * soc
        i = p_rails / (b.ETA * v) + direct
        soc -= i * dt / q_total
        t += dt
    return t / 3600


if __name__ == "__main__":
    i0, _ = simulate_hour(0.0)
    i10, r = simulate_hour(0.10)
    print(f"simulated {i0 * 1e6:.3f} uA (budget {b.battery_current() * 1e6:.3f}); at 10% packet loss "
          f"{i10 * 1e6:.3f} uA with {r} retransmissions; discharge life {discharge():.1f} h")
