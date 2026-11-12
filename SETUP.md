# Setup

Everything in this curriculum runs on free, open-source tools. Only the first block below (Python + ngspice) is needed for Terms 1–2. Install the rest when the course that uses it begins.

| Tool | Used for | Needed from |
|---|---|---|
| Python 3.10+ with NumPy, SciPy, SymPy, Matplotlib | Labs, verification scripts, figures | Course 01 |
| JupyterLab | Lab notebooks | Course 01 |
| ngspice | Circuit simulation | Course 06 (first used in 07-02) |
| Icarus Verilog | Verilog simulation | Course 08 |
| Verilator | Fast simulation, lint | Course 08 |
| GTKWave (or another VCD viewer) | Waveform viewing | Course 08 |
| Yosys | Logic synthesis | Course 08 (FPGA) / Course 19 |
| *Optional:* KiCad | Schematics/PCB | Capstone C3 (optional) |
| *Optional:* Docker + OpenLane-style flow on SkyWater 130 nm | RTL-to-GDS | Course 19, Capstone C2 |

## 1. Get the repository

```bash
git clone https://github.com/FrankHuang94/EE_database_claude.git
```

```bash
cd EE_database_claude
```

## 2. Python environment

### Option A: venv + pip (macOS, Linux, WSL)

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### Option B: conda / mamba (easiest on macOS and native Windows)

```bash
conda env create -f environment.yml
```

```bash
conda activate bsee
```

The conda environment also installs ngspice and Icarus Verilog from conda-forge.

Launch the notebooks with:

```bash
jupyter lab
```

## 3. Simulators and HDL tools

### Linux (Ubuntu/Debian) and Windows via WSL2

On Windows, install **WSL2 with Ubuntu** (Microsoft's documentation: "Install WSL"), then follow the Linux steps inside Ubuntu. WSL is the recommended Windows route, because ngspice, Icarus Verilog, Verilator and the ASIC flow all run natively there.

```bash
sudo apt-get update
```

```bash
sudo apt-get install -y ngspice iverilog verilator gtkwave yosys
```

### macOS (Homebrew)

```bash
brew install ngspice icarus-verilog verilator yosys
```

For waveforms, either install GTKWave (`brew install --cask gtkwave`; if that cask is unavailable for your macOS version, use the alternative below) or view `.vcd` files with a waveform-viewer extension in VS Code.

### All platforms: OSS CAD Suite (alternative)

YosysHQ's **OSS CAD Suite** bundles Yosys, Icarus Verilog, Verilator, GTKWave, nextpnr and the iCE40 FPGA tools as one download for Linux, macOS and Windows. Get it from the YosysHQ `oss-cad-suite-build` releases page on GitHub. It is a good choice when package managers lag behind.

## 4. Smoke test: confirm everything works

From the repository root, with your Python environment active:

```bash
python tools/run_spice.py smoke
```

```bash
python tools/run_hdl.py
```

```bash
python tools/run_verify.py
```

You should see `PASS` for the smoke netlist (an RC circuit whose voltage at one time constant must equal 63.2% of the step), `PASS` for the smoke testbench (a half adder), and `PASS` for every verification script.

To run **every** check that CI runs (generated files, links, template structure, markdown lint, verification, notebooks, ngspice, HDL):

```bash
make check
```

Markdown lint uses Node.js (`npx`). If you don't have Node, run the other targets individually (`make verify spice hdl notebooks`).

## 5. Reading the material as a website (optional)

```bash
mkdocs serve
```

Then open <http://127.0.0.1:8000>. The site uses symbolic links in `docs/`, which work on macOS, Linux and WSL. On native Windows, enable Git symlink support or use WSL.

## 6. The ASIC flow (Course 19 and Capstone C2; optional)

Course 19 takes a small block from RTL to layout with open-source tools (Yosys, OpenROAD and an OpenLane-style flow) on the SkyWater 130 nm open PDK, normally run inside Docker. The open-source ASIC flow ecosystem has been reorganizing (projects have been renamed, forked and re-homed), so **the exact installation steps will be written and verified when Course 19 is built** and dated at that time (tracked as an open issue in [PROGRESS.md](PROGRESS.md)). Until then, all you need is Docker Desktop (macOS/Windows) or Docker Engine (Linux).

The capstone also has a lighter path that needs no Docker: a passing Verilator testbench plus a Yosys synthesis report.

## 7. Optional hardware kit

Every lab is simulation-first, so no hardware is required. For learners who want physical intuition, these low-cost items support the optional hardware versions of selected labs. Product examples are as of Nov 2026; check current models and prices.

| Item | Why | Example |
|---|---|---|
| Solderless breadboard + jumper wires | Build circuits without soldering | Any 830-point board |
| Component kit | Resistors (E12 values), ceramic/electrolytic capacitors, inductors, diodes, LEDs, NPN/PNP BJTs, small MOSFETs, general-purpose op-amps, 555 timer | Assorted kits from electronics distributors |
| Digital multimeter | Voltage, current, resistance, continuity | Any auto-ranging DMM with a fused current input |
| USB oscilloscope + function generator | See transients and frequency response | A USB multi-instrument such as Digilent's Analog Discovery series |
| Microcontroller boards | Course 18 labs | A Raspberry Pi Pico-class (RP2040/RP2350) board and an ESP32-class board |
| Small FPGA board | Course 08 labs on real hardware | A Lattice iCE40-based board supported by the open-source toolchain (e.g., iCEBreaker-class boards) |
| Bench power supply (optional) | Variable supply with current limit | Any 0–30 V / 0–3 A linear or switching bench supply |

> **Safety.** Labs use low voltages (≤ 15 V). Never connect anything to mains voltage. Large inductors produce dangerous voltage spikes when their current is interrupted; Chapter [07-02](courses/07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md) explains why.
