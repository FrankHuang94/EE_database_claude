"""Static timing analysis for Lab 19-10.

A small graph-based timing engine on real Liberty data: NLDM table lookup by bilinear interpolation (linear
extrapolation outside the table), rise/fall arrival times and slews propagated through a netlist with unateness,
late (max) and early (min) analysis, required times, slacks and the worst path; setup and hold checks against a
clock; on-chip-variation derating with clock reconvergence pessimism removal; and the statistical (POCV-style)
alternative. The library subset is SKY130 sky130_fd_sc_hd at tt_025C_1v80 (see README for the source).
Units: ns, pF, um^2.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

DATA = Path(__file__).with_name("sky130_hd_subset.json")


def load_library(path: Path = DATA) -> dict:
    return json.loads(Path(path).read_text())


# ---------------------------------------------------------------- NLDM tables
def _segment(index, x):
    """Index i of the table segment [index[i], index[i+1]] used for x (end segments are extended for extrapolation)."""
    for i in range(len(index) - 2):
        if x < index[i + 1]:
            return i
    return len(index) - 2


def interp2(index_1, index_2, values, x, y):
    """Bilinear interpolation in a Liberty 2-D table: x along index_1 (rows), y along index_2 (columns)."""
    i, j = _segment(index_1, x), _segment(index_2, y)
    tx = (x - index_1[i]) / (index_1[i + 1] - index_1[i])
    ty = (y - index_2[j]) / (index_2[j + 1] - index_2[j])
    v00, v01 = values[i][j], values[i][j + 1]
    v10, v11 = values[i + 1][j], values[i + 1][j + 1]
    return (1 - tx) * (1 - ty) * v00 + (1 - tx) * ty * v01 + tx * (1 - ty) * v10 + tx * ty * v11


def arc_delay(lib, cell, pin, out_edge, in_slew, load):
    """(delay, output transition) of a combinational arc for output edge 'rise' or 'fall'."""
    arc = lib["cells"][cell]["arcs"][pin]
    d = interp2(arc["index_1"], arc["index_2"], arc["cell_" + out_edge], in_slew, load)
    s = interp2(arc["index_1"], arc["index_2"], arc[out_edge + "_transition"], in_slew, load)
    return d, s


def input_edges(sense, out_edge):
    """Input edges that can cause this output edge."""
    if sense == "negative_unate":
        return ["fall" if out_edge == "rise" else "rise"]
    if sense == "positive_unate":
        return [out_edge]
    return ["rise", "fall"]


def clk_to_q(lib, clk_slew, load, edge, cell="dfxtp_1"):
    t = lib["cells"][cell]["clk_to_q"]
    return (interp2(t["index_1"], t["index_2"], t["cell_" + edge], clk_slew, load),
            interp2(t["index_1"], t["index_2"], t[edge + "_transition"], clk_slew, load))


def ff_check(lib, kind, clk_slew, d_slew, d_edge, cell="dfxtp_1"):
    """Setup or hold time of the flip-flop for a rising or falling D."""
    t = lib["cells"][cell][kind]
    return interp2(t["index_1_clk_slew"], t["index_2_d_slew"], t[d_edge], clk_slew, d_slew)


# ---------------------------------------------------------------- netlist and graph-based analysis
class Netlist:
    """Instances drive one output net each. inputs: {port: (arrival_rise, arrival_fall, slew)};
    outputs: {port: (net, load_pF)}; wire_cap: {net: pF}."""

    def __init__(self, lib, inputs, outputs, wire_cap=None):
        self.lib, self.inputs, self.outputs = lib, inputs, outputs
        self.wire_cap = wire_cap or {}
        self.insts = {}      # name -> (cell, {pin: net}, out_net)

    def add(self, name, cell, pins, out):
        self.insts[name] = (cell, dict(pins), out)
        return self

    def load(self, net):
        c = self.wire_cap.get(net, 0.0)
        for cell, pins, _ in self.insts.values():
            c += sum(self.lib["cells"][cell]["inputs"][p] for p, n in pins.items() if n == net)
        c += sum(cl for n, cl in self.outputs.values() if n == net)
        return c

    def order(self):
        """Instances in topological order (Kahn's algorithm)."""
        driver = {out: name for name, (_, _, out) in self.insts.items()}
        indeg = {name: sum(1 for n in pins.values() if n in driver) for name, (_, pins, _) in self.insts.items()}
        ready = sorted(n for n, k in indeg.items() if k == 0)
        done = []
        while ready:
            name = ready.pop(0)
            done.append(name)
            out = self.insts[name][2]
            for other, (_, pins, _) in self.insts.items():
                for n in pins.values():
                    if n == out:
                        indeg[other] -= 1
                        if indeg[other] == 0:
                            ready.append(other)
        if len(done) != len(self.insts):
            raise ValueError("combinational loop")
        return done

    def analyze(self, mode="late"):
        """Arrival times and slews per net and edge. mode 'late' takes the max over fan-in arcs (setup analysis);
        'early' takes the min (hold analysis). Graph-based: one slew per net and edge (the worst for the mode)."""
        pick = max if mode == "late" else min
        at, slew, came_from = {}, {}, {}
        for port, (ar, af, s) in self.inputs.items():
            at[(port, "rise")], at[(port, "fall")] = ar, af
            slew[(port, "rise")] = slew[(port, "fall")] = s
        self.arc_delays = {}
        for name in self.order():
            cell, pins, out = self.insts[name]
            c_load = self.load(out)
            for oe in ("rise", "fall"):
                cands = []
                for pin, net in pins.items():
                    sense = self.lib["cells"][cell]["arcs"][pin]["sense"]
                    for ie in input_edges(sense, oe):
                        d, s = arc_delay(self.lib, cell, pin, oe, slew[(net, ie)], c_load)
                        self.arc_delays[(name, pin, ie, oe)] = d
                        cands.append((at[(net, ie)] + d, s, (net, ie, name, pin)))
                best = pick(cands, key=lambda c: c[0])
                at[(out, oe)] = best[0]
                slew[(out, oe)] = pick(c[1] for c in cands)
                came_from[(out, oe)] = best[2]
        self.at, self.slew, self.came_from = at, slew, came_from
        return at, slew

    def required(self, required_at_outputs):
        """Late required times by backward propagation; required_at_outputs: {port: time}."""
        rt = {}
        for port, (net, _) in self.outputs.items():
            for e in ("rise", "fall"):
                rt[(net, e)] = min(rt.get((net, e), math.inf), required_at_outputs[port])
        for name in reversed(self.order()):
            cell, pins, out = self.insts[name]
            for oe in ("rise", "fall"):
                if (out, oe) not in rt:
                    continue
                for pin, net in pins.items():
                    sense = self.lib["cells"][cell]["arcs"][pin]["sense"]
                    for ie in input_edges(sense, oe):
                        r = rt[(out, oe)] - self.arc_delays[(name, pin, ie, oe)]
                        rt[(net, ie)] = min(rt.get((net, ie), math.inf), r)
        self.rt = rt
        return rt

    def fanout(self):
        fo = {}
        for name, (_, pins, _) in self.insts.items():
            for pin, net in pins.items():
                fo.setdefault(net, []).append((name, pin))
        return fo

    def count_paths(self, start, end):
        """Structural paths from net start to net end, by depth-first enumeration."""
        fo = self.fanout()

        def walk(net):
            if net == end:
                return 1
            return sum(walk(self.insts[name][2]) for name, _ in fo.get(net, []))
        return walk(start)

    def path_based(self, start, end):
        """Path-based analysis: every path from input port start to net end, each re-timed with the slews that travel
        along it (no merging). Returns {output edge: worst arrival}. Cost grows with the number of paths."""
        fo, loads, best = self.fanout(), {}, {}
        ar, af, s0 = self.inputs[start]

        def walk(net, edge, t, slew):
            if net == end:
                best[edge] = max(best.get(edge, -math.inf), t)
                return
            for name, pin in fo.get(net, []):
                cell, _, out = self.insts[name]
                if out not in loads:
                    loads[out] = self.load(out)
                sense = self.lib["cells"][cell]["arcs"][pin]["sense"]
                for oe in ("rise", "fall"):
                    if edge in input_edges(sense, oe):
                        d, s = arc_delay(self.lib, cell, pin, oe, slew, loads[out])
                        walk(out, oe, t + d, s)
        walk(start, "rise", ar, s0)
        walk(start, "fall", af, s0)
        return best

    def worst_path(self, net, edge):
        """Back-trace the arcs that set the arrival time at (net, edge): list of (net, edge, arrival)."""
        path = [(net, edge, self.at[(net, edge)])]
        while (net, edge) in self.came_from:
            net, edge, _, _ = self.came_from[(net, edge)]
            path.append((net, edge, self.at[(net, edge)]))
        return path[::-1]


# ---------------------------------------------------------------- clocked checks
def setup_slack(period, launch_latency, capture_latency, t_cq, t_logic, t_setup, uncertainty=0.0):
    """Required minus arrival at the capture flip-flop's D for a single-cycle path."""
    arrival = launch_latency + t_cq + t_logic
    required = period + capture_latency - t_setup - uncertainty
    return required - arrival


def hold_slack(launch_latency, capture_latency, t_cq_min, t_logic_min, t_hold, uncertainty=0.0):
    """Arrival minus required for the same-edge hold check."""
    arrival = launch_latency + t_cq_min + t_logic_min
    required = capture_latency + t_hold + uncertainty
    return arrival - required


def ocv_setup_slack(period, common, launch_branch, capture_branch, t_cq, t_logic, t_setup,
                    late=1.0, early=1.0, crpr=True):
    """Setup slack with flat OCV derates: the launch clock and data are late (x late), the capture clock early
    (x early). The common clock segment cannot be late and early at once; CRPR credits back (late - early) x common."""
    arrival = (common + launch_branch + t_cq + t_logic) * late
    required = period + (common + capture_branch) * early - t_setup
    slack = required - arrival
    if crpr:
        slack += (late - early) * common
    return slack


def path_sigma(sigmas, rho=0.0):
    """Standard deviation of a sum of stage delays with equal pairwise correlation rho."""
    var = sum(s * s for s in sigmas)
    var += rho * sum(sigmas[i] * sigmas[j] for i in range(len(sigmas)) for j in range(len(sigmas)) if i != j)
    return math.sqrt(var)


def count_paths(n_diamonds):
    """Input-to-output paths through a chain of n reconvergent diamonds (two branches each)."""
    return 2 ** n_diamonds
