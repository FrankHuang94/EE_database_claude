#!/usr/bin/env python3
"""C3 reference: the analytic power budget, battery life and BLE link budget of the wearable sensor node.

Every input is either a data-sheet value (with its research-log ID) or a labelled design assumption; the design
report explains each. energy_sim.py simulates the same design event by event as a check, and verify_c3.py
recomputes every published number from this module.

Power tree: the nPM1300 PMIC's two bucks make a 3.0 V rail (the SoC, and the PPG front end's receiver and I/O
supplies) and a 1.8 V rail (the IMU). Each load sits at the supply voltage its data sheet specifies its current at.
The PPG LED driver supply (TX_SUP) runs directly from the cell.
"""
from __future__ import annotations

import math

# ---------------------------------------------------------------- data-sheet values
V_SOC = 3.0                  # V, CC2340R5 currents are specified at VDDS = 3.0 V, DC/DC on; AFE4404 at RX_SUP 3 V [R-702]
SOC_STANDBY = 0.74e-6        # A, CC2340R5 standby, RTC from the 32 kHz crystal (LFXT), full RAM retention [R-702]
SOC_STANDBY_LFOSC = 0.71e-6  # A, the same with the internal RC oscillator (LFOSC) [R-310, R-702]
SOC_TX0, SOC_TX8, SOC_RX = 5.1e-3, 10.7e-3, 5.3e-3   # A, TX at 0 dBm and +8 dBm, RX at 1 Mb/s [R-310, R-702]
SOC_ACTIVE = 2.6e-3          # A, CPU running CoreMark from flash at 48 MHz [R-702]
SOC_IDLE_DMA = 0.8e-3        # A, idle with flash off and DMA on (CPU asleep while DMA moves I2C data) [R-702]
SOC_WAKE = 43e-6             # s, standby to active (upper end of 33-43 us) [R-310, R-702]
SOC_SENS = -96.5             # dBm, CC2340R5 1M PHY sensitivity, BER 1e-3, typical [R-370, R-406]
BLE_REF_SENS = -70.0         # dBm, Bluetooth Core 6.2 reference sensitivity [R-406]
GOOD_PHONE_SENS = -95.0      # dBm, nRF52840 product brief, 1 Mb/s: a stand-in for a good phone radio [R-406]
V_IMU = 1.8                  # V, the supply at which the BMI270 current below is specified [R-311]
IMU_LP25 = 10e-6             # A, Bosch BMI270 accelerometer-only low-power mode at 25 Hz [R-311]
AFE_RX = 300e-6              # A, AFE4404 RX_SUP, dynamic power-down 90% / active 10% of the period, 100 Hz PRF [R-311, R-702]
AFE_RX_ON = 620e-6           # A, AFE4404 RX_SUP with the receiver always on [R-311, R-702]
AFE_IO = 20e-6               # A, AFE4404 IO_SUP in dynamic power-down [R-702]
AFE_TXQ = 5e-6               # A, AFE4404 TX_SUP with the LED currents at zero [R-702]
I2C_HZ = 400e3               # Hz, AFE4404 maximum I2C clock [R-702]
PMIC_IQ = 1.1e-6             # A, nPM1300 with both bucks in auto mode, no load [R-435]
PMIC_SHIP = 370e-9           # A, nPM1300 ship mode [R-435]
T_IFS = 150e-6               # s, BLE inter-frame space [R-676]

# ---------------------------------------------------------------- design assumptions (labelled in the report)
V_BAT, ETA = 3.7, 0.90                       # nominal cell voltage; buck efficiency at light load (both rails)
CAP_MAH, USABLE = 60.0, 0.80                 # LiPo capacity and the usable fraction (aging, cut-off, cold)
CPU_MHZ = 48.0
HR_CYCLES = 200e3                            # CPU cycles per second for heart rate, steps, IMU FIFO read, packing
FS = 25.0                                    # PPG and accelerometer sample rate, Hz
WAKES_PER_S = FS                             # CPU wakes per second for PPG reads (one per sample: no AFE FIFO)
ISR_T = 30e-6                                # s of active CPU per wake: interrupt entry, DMA set-up, ring push
VALUES = 2                                   # 24-bit values read per sample: green LED phase and ambient phase
I2C_BYTES = 6                                # per value: address+W, register, address+R, three data bytes
LED_I, LED_T = 20e-3, 100e-6                 # PPG LED pulse current and width (TX_SUP, from the cell)
LEAK = 2e-6                                  # A, board leakage and pull-ups (from the cell)
PRE_I, PRE_T = 3e-3, 300e-6                  # connection-event wake: crystal, radio ramp, link layer
SCA_PPM = 100.0                              # combined sleep-clock accuracy, ppm (32 kHz crystals, both ends)
T_CI = 1.0                                   # connection interval, s
PAYLOAD = 20                                 # notification value, octets: the most a default 23-octet ATT MTU allows
ATT_L2CAP = 7                                # octets of L2CAP (4) and ATT (opcode 1, handle 2) headers (27-03)
LL_PAYLOAD = PAYLOAD + ATT_L2CAP             # 27-octet link-layer payload, sent on the 1M PHY, encrypted
TX_DBM = 8.0                                 # chosen transmit power
D_M, F_HZ = 5.0, 2.44e9                      # range and carrier
G_TAG, G_PHONE, BODY_LOSS = -10.0, 0.0, 10.0 # dBi, dBi, dB (antenna gains within the SIG's -10..+10 dBi range)
PHONE_SENS = -90.0                           # dBm, the phone receiver the requirement assumes (between the two above)
PHONE_TX_DBM = 0.0                           # dBm, the phone's transmit power for the downlink


def packet_time(payload, mic=True, rate=1e6, preamble=1):
    return 8 * (preamble + 4 + 2 + payload + (4 if mic and payload else 0) + 3) / rate


def i2c_time():
    """Seconds of I2C transfer per PPG sample (nine clocks per byte; start and stop conditions ignored)."""
    return VALUES * I2C_BYTES * 9 / I2C_HZ


def ble_event_charge(tx_current):
    """Charge per connection event: wake, receive the central's empty packet, turn around, transmit."""
    t_rx, t_tx = packet_time(0), packet_time(LL_PAYLOAD)
    return PRE_I * PRE_T + SOC_RX * (t_rx + T_IFS) + tx_current * t_tx


def soc_rail_items(tx_current=None):
    """Average currents on the 3.0 V rail, in amperes."""
    tx = SOC_TX8 if tx_current is None else tx_current
    return {
        "SoC standby (32 kHz crystal)": SOC_STANDBY,
        "BLE connection events": ble_event_charge(tx) / T_CI,
        "BLE window widening": SOC_RX * SCA_PPM * 1e-6,
        "CPU: heart rate, steps, packing": SOC_ACTIVE * HR_CYCLES / (CPU_MHZ * 1e6),
        "CPU: wake and interrupt per PPG sample": WAKES_PER_S * SOC_ACTIVE * (SOC_WAKE + ISR_T),
        "I2C read per PPG sample (CPU idle, DMA)": FS * SOC_IDLE_DMA * i2c_time(),
        "PPG receiver (AFE4404 RX_SUP)": AFE_RX,
        "PPG interface (AFE4404 IO_SUP)": AFE_IO,
    }


def battery_items(tx_current=None):
    """Average currents drawn from the cell, in amperes: each rail through its buck, plus the direct loads."""
    soc = sum(soc_rail_items(tx_current).values())
    return {
        "3.0 V rail through its buck": soc * V_SOC / (ETA * V_BAT),
        "1.8 V rail (IMU) through its buck": IMU_LP25 * V_IMU / (ETA * V_BAT),
        "PPG LED pulses (TX_SUP)": LED_I * LED_T * FS,
        "PPG LED driver quiescent (TX_SUP)": AFE_TXQ,
        "PMIC quiescent": PMIC_IQ,
        "Leakage": LEAK,
    }


def battery_current(tx_current=None):
    return sum(battery_items(tx_current).values())


def life_hours(tx_current=None, cap_mah=None):
    cap = CAP_MAH if cap_mah is None else cap_mah
    return USABLE * cap * 1e-3 / battery_current(tx_current)


def scenario(**changes):
    """Battery life in days with some module constants changed, restoring them afterwards."""
    g = globals()
    old = {k: g[k] for k in changes}
    g.update(changes)
    try:
        return life_hours() / 24
    finally:
        g.update(old)


def fspl_db(d=None, f=None):
    d = D_M if d is None else d
    f = F_HZ if f is None else f
    return 20 * math.log10(4 * math.pi * d * f / 299_792_458.0)


def link_margin(tx_dbm, sens_dbm, d=None):
    return tx_dbm + G_TAG + G_PHONE - fspl_db(d) - BODY_LOSS - sens_dbm


def range_for_margin(tx_dbm, sens_dbm, margin_db=0.0):
    """Distance at which the link margin falls to margin_db (free-space slope)."""
    excess = link_margin(tx_dbm, sens_dbm, 1.0) - margin_db
    return 10 ** (excess / 20)


if __name__ == "__main__":
    for k, val in soc_rail_items().items():
        print(f"3.0 V  {k:42s} {val * 1e6:8.3f} uA")
    for k, val in battery_items().items():
        print(f"cell   {k:42s} {val * 1e6:8.3f} uA")
    print(f"battery current {battery_current() * 1e6:.2f} uA, life {life_hours():.1f} h = {life_hours() / 24:.2f} days "
          f"(requirement: 7 days)")
    print(f"FSPL {fspl_db():.2f} dB; uplink margin at +{TX_DBM:.0f} dBm to a {PHONE_SENS:.0f} dBm phone: "
          f"{link_margin(TX_DBM, PHONE_SENS):.1f} dB (spec-minimum phone: {link_margin(TX_DBM, BLE_REF_SENS):.1f} dB); "
          f"downlink: {link_margin(PHONE_TX_DBM, SOC_SENS):.1f} dB")
    print(f"range at a 10 dB margin: {range_for_margin(TX_DBM, PHONE_SENS, 10):.1f} m")
