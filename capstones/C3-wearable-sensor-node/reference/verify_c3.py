#!/usr/bin/env python3
"""Verify the C3 design report: recompute every published number from budget.py and energy_sim.py, and check the
claims the report makes about them.

- Budget facts (B.*) from budget.py, with the event charge and the cell currents also recomputed by hand here.
- Simulation facts (E.*) by running the event-level simulation and the discharge integration.
- Scenario facts (Z.*) by changing one input at a time through budget.scenario().
- Link facts (L.*) from the Friis free-space loss, recomputed here independently of budget.fspl_db().
- Part, power-tree, firmware and risk facts (S.*, P.*, F.*, R.*) by direct arithmetic; the firmware constants are
  read from the C headers so that the report and the code cannot drift apart.
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(HERE))
from eeverify import Verifier  # noqa: E402

import budget as b  # noqa: E402
import energy_sim as sim  # noqa: E402

v = Verifier.from_files("C3", HERE / "design-report.md")

# ----------------------------------------------------------------- part selection
t_rx, t_tx = 8 * 10 / 1e6, 8 * (1 + 4 + 2 + 27 + 4 + 3) / 1e6          # empty packet; 27-octet encrypted payload
pre = 3e-3 * 300e-6


def q_event(i_rx, i_tx):
    return pre + i_rx * (t_rx + 150e-6) + i_tx * t_tx


q_cc, q_efr = q_event(5.3e-3, 5.1e-3), q_event(3.6e-3, 4.1e-3)
v.check("S.qcc", q_cc * 1e6)
v.check("S.qefr", q_efr * 1e6)
v.check("S.dq", (q_cc - q_efr) * 1e6)
rail = sum(b.soc_rail_items().values())
v.check("S.dqpct", 100 * (q_cc - q_efr) / b.T_CI / rail)
v.assert_true("budget's event model matches the hand formula at 0 dBm", abs(b.ble_event_charge(b.SOC_TX0) - q_cc) < 1e-15)

# ----------------------------------------------------------------- power tree
v.check("P.chg", b.CAP_MAH * 1.0)                                       # 1C in mA
v.assert_true("1C charge is within the nPM1300 charger's 32-800 mA range", 32 <= b.CAP_MAH <= 800)
v.check("P.pmic2", (1.1 - 0.8))                                         # both bucks against one, auto mode [R-435]
f3, f18 = b.V_SOC / (b.ETA * b.V_BAT), b.V_IMU / (b.ETA * b.V_BAT)
v.check("P.imu3", b.IMU_LP25 * f3 * 1e6)
v.check("P.save", b.IMU_LP25 * (f3 - f18) * 1e6)
v.check("P.net", b.IMU_LP25 * (f3 - f18) * 1e6 - (1.1 - 0.8))

# ----------------------------------------------------------------- budget
v.check("B.tx", b.packet_time(b.LL_PAYLOAD) * 1e6)
v.check("B.rx", b.packet_time(0) * 1e6)
v.assert_true("air times agree with the hand count", abs(b.packet_time(b.LL_PAYLOAD) - t_tx) < 1e-15
              and abs(b.packet_time(0) - t_rx) < 1e-15)
v.assert_true("a 20-octet value plus 7 header octets fills the 27-octet link-layer payload",
              b.LL_PAYLOAD == 27 and b.PAYLOAD == 23 - 3)
q8 = b.ble_event_charge(b.SOC_TX8)
v.check("B.qev", q8 * 1e6)
items = b.soc_rail_items()
v.check("B.ble", items["BLE connection events"] * 1e6)
v.check("B.wid", items["BLE window widening"] * 1e6)
v.check("B.hr", items["CPU: heart rate, steps, packing"] * 1e6)
v.check("B.wake", items["CPU: wake and interrupt per PPG sample"] * 1e6)
v.check("B.ti2c", b.i2c_time() * 1e6)
v.assert_true("I2C time is 2 values x 6 bytes x 9 clocks at 400 kHz", abs(b.i2c_time() - 108 / 400e3) < 1e-15)
v.check("B.i2c", items["I2C read per PPG sample (CPU idle, DMA)"] * 1e6)
v.check("B.rail", rail * 1e6)
v.check("B.f3", f3)
v.check("B.f18", f18)
cell = b.battery_items()
v.check("B.cell3", cell["3.0 V rail through its buck"] * 1e6)
v.check("B.imu", cell["1.8 V rail (IMU) through its buck"] * 1e6)
v.check("B.led", cell["PPG LED pulses (TX_SUP)"] * 1e6)
ibat = b.battery_current()
hand = (rail * f3 + b.IMU_LP25 * f18 + b.LED_I * b.LED_T * b.FS + b.AFE_TXQ + b.PMIC_IQ + b.LEAK)
v.assert_true("battery current equals the hand sum", abs(ibat - hand) < 1e-15)
v.check("B.ibat", ibat * 1e6)
afe = (b.AFE_RX + b.AFE_IO) * f3
v.check("B.ppgpct", 100 * (afe + b.LED_I * b.LED_T * b.FS + b.AFE_TXQ) / ibat)
v.check("B.afepct", 100 * afe / ibat)
cpu = (items["CPU: heart rate, steps, packing"] + items["CPU: wake and interrupt per PPG sample"]
       + items["I2C read per PPG sample (CPU idle, DMA)"]) * f3
v.check("B.cpupct", 100 * cpu / ibat)
v.check("B.blepct", 100 * (items["BLE connection events"] + items["BLE window widening"]) * f3 / ibat)
v.check("B.life", b.life_hours())
v.check("B.days", b.life_hours() / 24)
v.assert_true("the baseline misses the 7-day requirement", b.life_hours() < 168)

# ----------------------------------------------------------------- simulation
i0, _ = sim.simulate_hour(0.0)
i10, retx = sim.simulate_hour(0.10)
v.check("E.sim0", i0 * 1e6)
v.assert_true("event simulation equals the budget with no packet loss", abs(i0 - ibat) / ibat < 1e-9)
v.check("E.retx", retx)
v.assert_true("retransmissions are close to 10% of 3600 events", abs(retx - 360) < 3 * math.sqrt(3600 * 0.1 * 0.9))
v.check("E.dper", (i10 - i0) * 1e6)
v.check("E.dis", sim.discharge())
v.check("E.vavg", 3.0 + 1.2 * (1.0 + (1.0 - b.USABLE)) / 2)
v.assert_true("discharge life is within 1% of the constant-voltage estimate",
              abs(sim.discharge() / b.life_hours() - 1) < 0.01)

# ----------------------------------------------------------------- dominance and scenarios
allow = b.USABLE * b.CAP_MAH * 1e-3 / 168
v.check("B.allow", allow * 1e6)
v.check("B.afecell", afe * 1e6)
v.assert_true("the AFE receiver and interface alone exceed the 7-day allowance", afe > allow)
v.check("Z.base", b.scenario())
v.check("Z.afeon", b.scenario(AFE_RX=b.AFE_RX_ON))
v.check("Z.afe200", b.scenario(AFE_RX=200e-6))
i_pd = (b.AFE_RX - 0.1 * b.AFE_RX_ON) / 0.9
v.check("Z.afepd", i_pd * 1e6)
v.check("Z.win", 0.1 / 100 * 1e3)                                       # 10% of a 10 ms period
duty25 = 1e-3 * 25
v.check("Z.duty25", 100 * duty25)
i25 = (1 - duty25) * i_pd + duty25 * b.AFE_RX_ON
v.check("Z.afe25i", i25 * 1e6)
v.check("Z.afe25", b.scenario(AFE_RX=i25))
v.check("Z.led10", b.scenario(LED_I=10e-3))
v.check("Z.fs12", b.scenario(FS=12.5, WAKES_PER_S=12.5))
v.check("Z.fifo", b.scenario(WAKES_PER_S=1.0))
v.check("Z.tci05", b.scenario(T_CI=0.5))
v.check("Z.eta80", b.scenario(ETA=0.80))
v.check("Z.hr1m", b.scenario(HR_CYCLES=1e6))
v.check("Z.tx0", b.life_hours(b.SOC_TX0) / 24)
v.check("Z.cap80", b.scenario(CAP_MAH=80.0))
v.check("Z.cap100", b.scenario(CAP_MAH=100.0))
v.assert_true("scenario() restores every constant", b.CAP_MAH == 60.0 and b.AFE_RX == 300e-6 and b.FS == 25.0
              and b.WAKES_PER_S == 25.0 and b.ETA == 0.90 and abs(b.scenario() - b.life_hours() / 24) < 1e-12)
afemax = (allow - (ibat - b.AFE_RX * f3)) / f3
v.check("B.afemax", afemax * 1e6)
v.assert_true("the receiver limit sits just under the feature list's 200 uA", 195e-6 < afemax < 200e-6)
v.check("B.gap", 7 - b.life_hours() / 24)
v.check("B.capneed", ibat * 168 / b.USABLE * 1e3)
v.assert_true("100 mAh meets 7 days with more than 20% margin; 80 mAh with less than 2%",
              b.scenario(CAP_MAH=100.0) > 7 * 1.2 and 7 < b.scenario(CAP_MAH=80.0) < 7 * 1.02)
v.check("Z.widlf", b.SOC_RX * 550e-6 * 1e6)
v.check("Z.lfosc", b.scenario(SOC_STANDBY=b.SOC_STANDBY_LFOSC, SCA_PPM=550.0))
v.check("Z.polled", b.scenario(SOC_IDLE_DMA=b.SOC_ACTIVE))

# ----------------------------------------------------------------- link budget (independent Friis)
lam = 299_792_458.0 / 2.44e9
fspl = 20 * math.log10(4 * math.pi * 5.0 / lam)
v.check("L.fspl", fspl)
v.assert_true("budget's path loss matches", abs(b.fspl_db() - fspl) < 1e-12)
prx = 8 - 10 + 0 - fspl - 10
v.check("L.prx", prx)
v.check("L.m90", prx + 90)
v.check("L.m95", prx + 95)
v.check("L.m70", prx + 70)
v.check("L.m90tx0", prx - 8 + 90)
v.check("L.r10", 5.0 * 10 ** ((prx + 90 - 10) / 20))
v.check("L.r10s", 5.0 * 10 ** ((prx + 70 - 10) / 20))
v.assert_true("range_for_margin agrees", abs(b.range_for_margin(8, -90, 10) - 5.0 * 10 ** ((prx + 80) / 20)) < 1e-9)
v.check("L.spare", prx + 90 - 10)
v.assert_true("R4 met at +8 and at 0 dBm", prx + 90 >= 10 and prx - 8 + 90 >= 10)
txcost = b.battery_current(b.SOC_TX8) - b.battery_current(b.SOC_TX0)
v.check("Z.txcost", txcost * 1e6)
v.check("Z.txpct", 100 * txcost / ibat)
v.check("L.x8", 10 ** (8 / 20))
v.check("L.half", 20 * math.log10(2))
down = 0 - 10 + 0 - fspl - 10 + 96.5
v.check("L.down", down)
v.check("L.bal", (prx + 90) - down)
v.assert_true("budget's downlink matches", abs(b.link_margin(b.PHONE_TX_DBM, b.SOC_SENS) - down) < 1e-12)

# ----------------------------------------------------------------- firmware
fw = HERE / "firmware"
ring_cap = int(re.search(r"#define RING_CAP (\d+)u", (fw / "ring.h").read_text()).group(1))
notify_len = int(re.search(r"#define NOTIFY_LEN (\d+)u", (fw / "notify.h").read_text()).group(1))
v.assert_true("notification length in the code equals the budgeted value", notify_len == b.PAYLOAD)
tproc = b.HR_CYCLES / (b.CPU_MHZ * 1e6)
v.check("F.tproc", tproc * 1e3)
t_evt = b.PRE_T + b.packet_time(0) + b.T_IFS + b.packet_time(b.LL_PAYLOAD)
v.check("F.evt", t_evt * 1e3)
lead = 10e-3
v.check("F.lead", lead / tproc)
v.check("F.per", 1e3 / b.FS)
v.assert_true("a connection event is shorter than a PPG sample period", t_evt < 1 / b.FS)
v.check("F.duty", 100 * (tproc + b.WAKES_PER_S * (b.SOC_WAKE + b.ISR_T)))
v.check("F.lat", b.T_CI + lead)
v.check("F.latr", 2 * b.T_CI + lead)
v.check("F.over", (2 * b.T_CI + lead - 2.0) * 1e3)
v.assert_true("first-transmission latency meets R2", b.T_CI + lead <= 2.0)
v.check("F.mem", ring_cap * 4)
slots = ring_cap - 1
v.check("F.slots", slots)
v.check("F.span", slots / b.FS)
per_run = int(b.FS * b.T_CI)
v.check("F.two", 2 * per_run)
v.assert_true("the ring survives one missed run but not two", 2 * per_run <= slots < 3 * per_run)
v.check("F.drop2", 3 * per_run - slots)
v.check("F.imufifo", 2048 / (6 * b.FS))
v.check("F.shelf", b.USABLE * b.CAP_MAH * 1e-3 / b.PMIC_SHIP / (365.25 * 24))
month_h = 365.25 * 24 / 12
v.check("F.sd1", 0.01 * b.CAP_MAH * 1e-3 / month_h * 1e6)
v.check("F.sd2", 0.02 * b.CAP_MAH * 1e-3 / month_h * 1e6)
v.assert_true("self-discharge exceeds ship-mode current", 0.01 * b.CAP_MAH * 1e-3 / month_h > b.PMIC_SHIP)

# ----------------------------------------------------------------- risks
v.check("R.vph", 1239.84 / 530)
v.check("R.txs", 3.0 + 0.5)
soc35 = (3.5 - 3.0) / 1.2
v.check("R.soc35", 100 * soc35)
v.check("R.frac", 100 * (soc35 - (1 - b.USABLE)) / b.USABLE)
v.check("R.vend", 3.0 + 1.2 * (1 - b.USABLE))

sys.exit(v.finish())
