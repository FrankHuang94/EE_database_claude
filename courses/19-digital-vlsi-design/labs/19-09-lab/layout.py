"""Layout models for Lab 19-09.

Euler paths for ordering the transistors of a static CMOS gate so that each network is one unbroken strip of
diffusion; an illustrative lambda-based rule set and the transistor pitches it implies; standard-cell area and
utilization arithmetic. Networks are series-parallel expressions given as nested tuples.
"""
from __future__ import annotations

import itertools

# ---------------------------------------------------------------- series-parallel networks as graphs
# A network is ("t", name) for one transistor, ("s", [nets]) for series, ("p", [nets]) for parallel.


def to_edges(net, a, b, counter):
    """Edges (u, v, label) of the network between nodes a and b; new internal nodes come from counter."""
    kind = net[0]
    if kind == "t":
        return [(a, b, net[1])]
    if kind == "p":
        edges = []
        for sub in net[1]:
            edges += to_edges(sub, a, b, counter)
        return edges
    edges = []
    nodes = [a] + [next(counter) for _ in range(len(net[1]) - 1)] + [b]
    for sub, u, v in zip(net[1], nodes[:-1], nodes[1:]):
        edges += to_edges(sub, u, v, counter)
    return edges


def dual(net):
    """The dual network: series <-> parallel, same transistors (the pull-up of a static CMOS gate)."""
    if net[0] == "t":
        return net
    return ("p" if net[0] == "s" else "s", [dual(n) for n in net[1]])


def is_euler_path(edges, order):
    """True if visiting the labelled edges in this order traces a connected walk (each edge used once)."""
    by_label = {lab: (u, v) for u, v, lab in edges}
    if sorted(order) != sorted(by_label):
        return False
    u, v = by_label[order[0]]
    for start, cur in ((u, v), (v, u)):
        ok = True
        for lab in order[1:]:
            x, y = by_label[lab]
            if cur == x:
                cur = y
            elif cur == y:
                cur = x
            else:
                ok = False
                break
        if ok:
            return True
    return False


def common_euler_orders(pdn):
    """All input orderings that are Euler paths in both the pull-down network and its dual pull-up network."""
    c1 = itertools.count(100)
    c2 = itertools.count(200)
    e_n = to_edges(pdn, "out", "gnd", c1)
    e_p = to_edges(dual(pdn), "out", "vdd", c2)
    labels = sorted({lab for _, _, lab in e_n})
    return [list(o) for o in itertools.permutations(labels) if is_euler_path(e_n, list(o)) and is_euler_path(e_p, list(o))]


def diffusion_breaks(edges, order):
    """Fewest breaks needed to place the transistors in one row in this order. Consecutive transistors share a
    diffusion region only if they share a node; at a break the next strip may start from either end of the next
    transistor. Tracked exactly: for every node where the current strip could end, the fewest breaks so far."""
    by_label = {lab: (u, v) for u, v, lab in edges}
    u, v = by_label[order[0]]
    ends = {u: 0, v: 0}                       # strip end node -> fewest breaks to get there
    for lab in order[1:]:
        x, y = by_label[lab]
        nxt = {}
        least = min(ends.values())
        for start, end in ((x, y), (y, x)):
            cost = ends[start] if start in ends else least + 1
            cost = min(cost, least + 1)
            nxt[end] = min(nxt.get(end, cost), cost)
        ends = nxt
    return min(ends.values())


def stack_variants(net):
    """Every network obtained by reordering the members of series stacks (same logic function, different graph)."""
    if net[0] == "t":
        yield net
        return
    for combo in itertools.product(*[list(stack_variants(n)) for n in net[1]]):
        if net[0] == "s":
            for perm in itertools.permutations(combo):
                yield ("s", list(perm))
        else:
            yield ("p", list(combo))


def fewest_breaks(pdn):
    """(total breaks, ordering) minimizing pull-down plus pull-up breaks over all input orderings and over all
    stack orders of each network (each network's stacks may be reordered independently)."""
    nets_n = [to_edges(n, "out", "gnd", itertools.count(100)) for n in stack_variants(pdn)]
    nets_p = [to_edges(p, "out", "vdd", itertools.count(200)) for p in stack_variants(dual(pdn))]
    labels = sorted({lab for _, _, lab in nets_n[0]})
    best = None
    for order in itertools.permutations(labels):
        o = list(order)
        total = min(diffusion_breaks(e, o) for e in nets_n) + min(diffusion_breaks(e, o) for e in nets_p)
        if best is None or total < best[0]:
            best = (total, o)
    return best


# ---------------------------------------------------------------- illustrative lambda rules (this chapter's own set)
RULES = {
    "poly_width": 2, "poly_space": 3, "active_width": 3, "contact": 2, "contact_to_poly": 2,
    "active_enclose_contact": 1, "poly_extension": 2, "metal1_width": 3, "metal1_space": 3,
}


def contacted_pitch(r: dict = RULES) -> int:
    """Pitch between adjacent transistors that share a contacted source/drain: poly + 2 x contact-to-poly + contact."""
    return r["poly_width"] + 2 * r["contact_to_poly"] + r["contact"]


def uncontacted_pitch(r: dict = RULES) -> int:
    """Pitch between series transistors with no contact between them: poly width + poly spacing."""
    return r["poly_width"] + r["poly_space"]


def strip_length(n_gates: int, contacted_internal: bool, r: dict = RULES) -> int:
    """Length of a diffusion strip of n series transistors: a contacted end, the gates, and between gates either a
    contact (contact-to-poly, contact, contact-to-poly) or just poly spacing; then the other contacted end."""
    end = r["active_enclose_contact"] + r["contact"] + r["contact_to_poly"]
    between = (2 * r["contact_to_poly"] + r["contact"]) if contacted_internal else r["poly_space"]
    return 2 * end + n_gates * r["poly_width"] + (n_gates - 1) * between


# ---------------------------------------------------------------- standard-cell area
def cell_area(sites: int, site_w: float, site_h: float) -> float:
    return sites * site_w * site_h


def core_area(cell_area_total: float, utilization: float) -> float:
    return cell_area_total / utilization


def gates_area_mm2(kgates: float, density_kgates_per_mm2: float) -> float:
    return kgates / density_kgates_per_mm2
