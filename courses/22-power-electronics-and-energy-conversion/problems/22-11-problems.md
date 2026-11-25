# Problems 22-11 · Electric Machines and Drives

Chapter: [22-11](../chapters/22-11-electric-machines.md) · Worked solutions: [22-11 solutions](../solutions/22-11-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Three-phase machines are Y-connected; $V$ and $E_f$ are phase values unless stated. Values marked "assumed" are illustrative. Problems marked *(lab)* can be checked with `labs/22-11-lab/machines.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 22-11.1 [A]

**A 48 V DC motor.** A PM DC motor has $V$ = 48 V, $R_a$ = 0.2 Ω and $k$ = 0.1 V·s/rad. Find (a) the no-load speed in rpm, (b) the stall current, (c) the stall torque and (d) the speed in rpm at 2 N·m.

### Problem 22-11.2 [A]

**A series motor's torque.** In an unsaturated series DC motor the flux is proportional to the current. By what factor does the torque change when the current doubles?

### Problem 22-11.3 [A]

**A 6-pole motor.** A 6-pole, 60 Hz induction motor runs at 1164 rpm. Find (a) the synchronous speed, (b) the slip and (c) the rotor frequency.

### Problem 22-11.4 [B]

**Power flow at 60 Hz.** *(lab)* A 4-pole, 60 Hz induction motor draws 50 kW with 1.5 kW of stator copper loss and 1 kW of core loss, at 2.5% slip, with 0.6 kW of friction and windage. Find (a) the air-gap power, (b) the rotor copper loss, (c) the mechanical power, (d) the output power, (e) the efficiency and (f) the output torque.

### Problem 22-11.5 [B]

**A voltage sag.** An induction motor runs at 3% slip in the linear region of its torque–slip curve. The supply sags to 90% of rated. (a) By what factor does the torque at a given slip change? (b) At what slip does it now carry the same load torque?

### Problem 22-11.6 [C]

**Designing for starting torque.** *(lab)* For the motor of Example 22-11.4, (a) what rotor resistance would put the maximum torque at standstill, and (b) what would the starting torque then be? (c) With that rotor, what torque would the motor produce at 3% slip, and (d) at what slip would it carry the 65.4 N·m of Example 22-11.4(g)? What does this cost?

### Problem 22-11.7 [B]

**A synchronous generator's power angle.** A 480 V (line), Y-connected generator has $X_s$ = 1.5 Ω and $E_f$ = 300 V per phase. Find (a) the phase voltage, (b) the power angle at 60 kW and (c) the pull-out power.

### Problem 22-11.8 [A]

**V/f at 45 Hz.** A 460 V, 60 Hz, 4-pole motor is run at 45 Hz with constant flux. Find (a) the voltage and (b) the synchronous speed.

### Problem 22-11.9 [B]

**A pump on a VFD.** A 30 kW pump is slowed to 80% speed. Find its (a) flow, (b) head and (c) power as fractions of rated, and (d) the energy saved over 6000 hours a year against running at full speed.

### Problem 22-11.10 [A]

**A 400 V battery.** Find the maximum fundamental line-to-line rms voltage of an inverter on a 400 V DC link (a) with sine-triangle PWM at $m$ = 1 and (b) with space-vector PWM.

### Problem 22-11.11 [C]

**Launching an EV.** A 2000 kg EV has the motor of Example 22-11.8 (400 N·m below 5000 rpm, 9:1 reduction, 0.35 m wheels). Ignoring losses and drag, find (a) the force at the wheels, (b) the acceleration, (c) the speed at base speed in m/s and (d) in km/h, and (e) the time to reach it.

### Problem 22-11.12 [B]

**Two efficiencies.** An 11 kW motor runs 5000 h a year at full load. Compare a 91%-efficient motor with a 93%-efficient one: find (a) and (b) their losses, and (c) the energy saved per year.

### Problem 22-11.13 [C]

**A two-phase rotating field.** Two windings 90° apart carry $I_m\cos\omega t$ and $I_m\sin\omega t$. Show that they produce a rotating field. In units of one winding's peak field, find the rotating field's amplitude for (a) this two-phase arrangement and (b) the three-phase arrangement of §3.3, and (c) the ratio of the two.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Torque, back EMF and the DC machine | 1, 2 |
| 2. Rotating field, synchronous speed and slip | 3, 13 |
| 3. Induction machine power flow and torque–slip | 4, 5, 6, 12 |
| 4. Synchronous machines | 7 |
| 5. Inverter-fed drives and EV envelopes | 8, 9, 10, 11 |
