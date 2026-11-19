# Problems 05-09 · Software Engineering Practices

Chapter: [05-09](../chapters/05-09-software-engineering-practices.md) · Worked solutions: [05-09 solutions](../solutions/05-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** where a problem asks for tests or measurements, write them in Python; probabilities assume independence unless stated.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 05-09.1 [A]

**Classifying and fixing requirements.** Classify each as functional or non-functional, and rewrite any that cannot be tested: (a) "The logger shall store each sample with a timestamp." (b) "The firmware shall be fast." (c) "The device shall draw less than 5 µA in sleep mode at 25 °C." (d) "The API shall be easy to use."

### Problem 05-09.2 [A]

**Choosing a process.** Which process model best fits each, and why? (a) Brake-by-wire controller firmware for a car. (b) A web dashboard for internal yield data, with requirements that change weekly. (c) A boot ROM that will be masked into silicon. (d) A cloud service for firmware-update distribution.

### Problem 05-09.3 [A]

**Cyclomatic complexity.** Count decision points and give $M$ for each function body: (a) a straight sequence of five assignments; (b) one `if`/`else`; (c) an `if` containing `a and b and c`, followed by a `while` loop; (d) a `for` loop containing an `if`/`elif`/`elif`/`else` chain.

### Problem 05-09.4 [B]

**Boundary values for two inputs.** A function takes an ADC channel number (valid 0 to 15) and a sample rate in hertz (valid integers 1 to 1000). (a) List the boundary-value test inputs for each parameter (just below, at and just above each boundary). (b) How many single-parameter tests is that? (c) How many tests would all combinations of those values need?

### Problem 05-09.5 [B]

**Measuring coverage.** For the function below and the tests `clamp_gain(5)` and `clamp_gain(20)`, measure line coverage with a small tracer, then add the fewest tests needed for full line and branch coverage.

```python
# not run
def clamp_gain(g):
    if g < 1:
        g = 1
    if g > 16:
        g = 16
    return g
```

### Problem 05-09.6 [B]

**MC/DC sets.** Give minimal MC/DC test sets for (a) `a and b`, (b) `a or b` and (c) `(a and b) or c`, and verify each with a search.

### Problem 05-09.7 [B]

**Strengthening a filter.** 80 defects enter a process with three independent filters, each catching 50%. (a) How many escape? (b) To halve the escapes by improving one filter, what must its catch rate become? (c) Alternatively, what catch rate must a fourth filter have to achieve the same?

### Problem 05-09.8 [B]

**Semantic versions.** A library is at version 2.7.3. Give the next version after (a) a bug fix; (b) a new, backward-compatible function; (c) removing a deprecated function. (d) Show why sorting version strings as text is wrong, and fix it.

### Problem 05-09.9 [B]

**A traceability matrix.** Requirements R1–R5 are covered by tests as follows: T1 → R1; T2 → R1, R2; T3 → R3; T4 → R3; T5 → none; T6 → R2. Find the untested requirements, the orphan tests, and the requirement coverage.

### Problem 05-09.10 [C]

**Debounced low-battery alarm.** Extend Example 05-09.1: LOW_BATT asserts only after **3 consecutive** samples below 3.30 V, and deasserts when a sample is at or above 3.40 V. (a) Write the function and tests including the sequence 3.25, 3.25, 3.31, 3.25, 3.25, 3.25, 3.35, 3.41 V. At which sample does the alarm assert and at which does it clear? (b) A colleague's version resets the counter only on samples ≥ 3.40 V. Which test catches it?

### Problem 05-09.11 [B]

**Estimating defects nobody has found.** Two reviewers inspect the same design independently. Reviewer A finds 25 defects, reviewer B finds 30, and 15 are found by both. Estimate the total number of defects and the number still undiscovered (the capture–recapture method). State the assumptions.

### Problem 05-09.12 [B]

**Canary releases.** A firmware update is first sent to a "canary" group of devices. A defect affects 0.1% of devices (independently). (a) With 1000 canary devices, what is the chance that at least one shows the defect? (b) How many devices give 95% confidence of seeing it at least once? (c) What does this imply for rare defects?

### Problem 05-09.13 [B]

**Critique a design.** A battery-monitor firmware handles messages from a fuel-gauge chip in its UART interrupt handler:

```python
# not run
battery_mv = 0                     # global: written here, read anywhere
alarm_on = False

def on_uart_byte(b):               # interrupt handler, one call per received byte
    global battery_mv, alarm_on
    buf.append(b)
    if b == ord("\n"):
        fields = bytes(buf).decode().split(",")
        battery_mv = int(fields[2])                                  # field 2 holds millivolts
        if battery_mv < 3300:
            alarm_on = True
            write_reg(0x40020014, read_reg(0x40020014) | 0x20)      # LED on
        buf.clear()
```

(a) Identify at least four violations of the design principles of §3.3 (abstraction, information hiding, low coupling, high cohesion) or of the firmware practices of 05-07 and 05-08, and say what each will cost. (b) Propose a restructured design: name the modules and give each one's interface. (c) Which parts become testable on a PC, and which requirement of Example 05-09.1 does the current code violate?

---

## Objective coverage

| Learning objective (chapter 05-09) | Problems |
|---|---|
| 1. Testable requirements and traceability | 1, 9, 10 |
| 2. Process models | 2, 12 |
| 3. Design principles and complexity | 3, 13 |
| 4. Test design and coverage | 4, 5, 6, 10 |
| 5. Version control, review, release and defect filters | 7, 8, 11, 12 |
