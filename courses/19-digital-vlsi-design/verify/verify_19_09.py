#!/usr/bin/env python3
"""Verify every number in chapter 19-09 (layout, design rules and standard cells), its problems and its lab.

Independent routes:
- valid input orderings by brute force: graphs are built here from explicit edge lists (not the lab's converter),
  and each ordering is accepted if a walk exists in both graphs by depth-first search over start nodes;
- odd-degree counts from the same explicit graphs;
- strip lengths by laying out the strip feature by feature from the rule values;
- areas and percentages by direct arithmetic; the lab module is checked against these results.
"""
from __future__ import annotations

import itertools
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "19-09-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import layout as ly  # noqa: E402

v = Verifier.from_files("19-09", ROOT / "chapters" / "19-09-layout-and-standard-cells.md",
                        ROOT / "solutions" / "19-09-solutions.md", LAB / "README.md")

# explicit graphs: {label: (node, node)}
G = {
    "oai21": ({"A": ("o", "x"), "B": ("x", "g"), "C": ("x", "g")},
              {"A": ("v", "o"), "B": ("v", "y"), "C": ("y", "o")}),
    "aoi22": ({"A": ("o", "x"), "B": ("x", "g"), "C": ("o", "y"), "D": ("y", "g")},
              {"A": ("v", "m"), "B": ("v", "m"), "C": ("m", "o"), "D": ("m", "o")}),
    "oai22": ({"A": ("o", "x"), "B": ("o", "x"), "C": ("x", "g"), "D": ("x", "g")},
              {"A": ("v", "y"), "B": ("y", "o"), "C": ("v", "z"), "D": ("z", "o")}),
    "aoi211": ({"A": ("o", "x"), "B": ("x", "g"), "C": ("o", "g"), "D": ("o", "g")},
               {"A": ("v", "m"), "B": ("v", "m"), "C": ("m", "p"), "D": ("p", "o")}),
    "nand3": ({"A": ("o", "x"), "B": ("x", "y"), "C": ("y", "g")},
              {"A": ("v", "o"), "B": ("v", "o"), "C": ("v", "o")}),
    "nor3": ({"A": ("o", "g"), "B": ("o", "g"), "C": ("o", "g")},
             {"A": ("v", "x"), "B": ("x", "y"), "C": ("y", "o")}),
    # AB + C(D + E): pull-down (A-B) || (C - (D || E)); pull-up (A || B) - (C || (D - E))
    "big": ({"A": ("o", "x"), "B": ("x", "g"), "C": ("o", "y"), "D": ("y", "g"), "E": ("y", "g")},
            {"A": ("v", "m"), "B": ("v", "m"), "C": ("m", "o"), "D": ("m", "w"), "E": ("w", "o")}),
}


def walkable(edges, order):
    nodes = {n for e in edges.values() for n in e}
    for start in nodes:
        cur, ok = start, True
        for lab in order:
            a, b = edges[lab]
            if cur == a:
                cur = b
            elif cur == b:
                cur = a
            else:
                ok = False
                break
        if ok:
            return True
    return False


def count_valid(name):
    n, p = G[name]
    return sum(1 for o in itertools.permutations(sorted(n)) if walkable(n, o) and walkable(p, o))


def odd_nodes(edges):
    deg = Counter(n for e in edges.values() for n in e)
    return sum(1 for d in deg.values() if d % 2)


v.check("Ex 19-09.2a", count_valid("oai21"))
v.check("Ex 19-09.3a", count_valid("aoi22"))
v.check("19-09.3a", count_valid("nand3"))
v.check("19-09.4a", count_valid("aoi211"))
v.check("19-09.5a", count_valid("oai22"))
v.check("Lab 19-09.a", count_valid("nor3"))
v.check("Lab 19-09.b", count_valid("big"))
v.check("19-09.9a", odd_nodes(G["aoi22"][0]))
v.check("19-09.9b", odd_nodes(G["aoi22"][1]))
v.assert_true("A-C-D-B valid for AOI22", walkable(G["aoi22"][0], "ACDB") and walkable(G["aoi22"][1], "ACDB"), "")
v.assert_true("A-B-C-D valid for AOI211", walkable(G["aoi211"][0], "ABCD") and walkable(G["aoi211"][1], "ABCD"), "")


def breaks(edges, order):
    """Fewest breaks, by exhaustive recursion: after each transistor the strip either continues (if the next transistor
    touches the current end) or breaks and restarts from either end of the next transistor."""
    def rec(i, cur):
        if i == len(order):
            return 0
        a, b = edges[order[i]]
        options = [1 + rec(i + 1, b), 1 + rec(i + 1, a)]
        if cur == a:
            options.append(rec(i + 1, b))
        if cur == b:
            options.append(rec(i + 1, a))
        return min(options)
    a, b = edges[order[0]]
    return min(rec(1, b), rec(1, a))


v.assert_true("A-B-C-D fails in the AOI22 pull-down only", not walkable(G["aoi22"][0], "ABCD")
              and walkable(G["aoi22"][1], "ABCD"), "")
v.assert_true("A-C-B-D needs one break in each AOI22 network",
              breaks(G["aoi22"][0], "ACBD") == 1 and breaks(G["aoi22"][1], "ACBD") == 1, "")
v.check("Ex 19-09.3b", breaks(G["aoi22"][0], "ABCD"))
v.check("Ex 19-09.3c", breaks(G["aoi22"][1], "ABCD"))
loop = "ABDC"
rots = {loop[i:] + loop[:i] for i in range(4)} | {(loop[i:] + loop[:i])[::-1] for i in range(4)}
valid = {"".join(o) for o in itertools.permutations("ABCD") if walkable(G["aoi22"][0], o) and walkable(G["aoi22"][1], o)}
v.assert_true("valid AOI22 orderings are the rotations of one loop", rots == valid, str(sorted(valid)))
v.check("Ex 19-09.3d", len({loop[i:] + loop[:i] for i in range(4)}))
v.assert_true("lab agrees on AOI22 count", len(ly.common_euler_orders(
    ("p", [("s", [("t", "A"), ("t", "B")]), ("s", [("t", "C"), ("t", "D")])]))) == 8, "")

# A(BC + DE): every stack order, written out. Pull-down: A in series with the two stacks in parallel; A may sit at the
# output end or the ground end, and each two-transistor stack may be drawn either way up (2 x 2 x 2 = 8 graphs).
pdn_variants = []
for a_top in (True, False):
    top, bot = ("n", "g") if a_top else ("o", "n")
    for s1 in ("BC", "CB"):
        for s2 in ("DE", "ED"):
            e = {"A": ("o", "n") if a_top else ("n", "g")}
            e[s1[0]], e[s1[1]] = (top, "x"), ("x", bot)
            e[s2[0]], e[s2[1]] = (top, "y"), ("y", bot)
            pdn_variants.append(e)
# Pull-up: A in parallel with (B || C) in series with (D || E); the two pairs may be stacked either way (2 graphs).
pun_variants = [{"A": ("v", "o"), "B": ("v", "m"), "C": ("v", "m"), "D": ("m", "o"), "E": ("m", "o")},
                {"A": ("v", "o"), "B": ("m", "o"), "C": ("m", "o"), "D": ("v", "m"), "E": ("v", "m")}]
orders5 = list(itertools.permutations("ABCDE"))
common = sum(1 for o in orders5 for en in pdn_variants for ep in pun_variants if walkable(en, o) and walkable(ep, o))
v.check("Lab 19-09.e", common)
v.assert_true("each A(BC + DE) network alone has Euler paths",
              all(any(walkable(e, o) for o in orders5) for e in pdn_variants + pun_variants), "")
fewest = min(min(breaks(e, o) for e in pdn_variants) + min(breaks(e, o) for e in pun_variants) for o in orders5)
v.check("Lab 19-09.f", fewest)
big5 = ("s", [("t", "A"), ("p", [("s", [("t", "B"), ("t", "C")]), ("s", [("t", "D"), ("t", "E")])])])
v.assert_true("lab agrees on A(BC + DE)",
              sum(len(ly.common_euler_orders(x)) for x in ly.stack_variants(big5)) == 0
              and len(list(ly.stack_variants(big5))) == 8 and len(list(ly.stack_variants(ly.dual(big5)))) == 2
              and ly.fewest_breaks(big5)[0] == fewest, str(ly.fewest_breaks(big5)))
aoi22_net = ("p", [("s", [("t", "A"), ("t", "B")]), ("s", [("t", "C"), ("t", "D")])])
v.assert_true("lab break counter agrees on every AOI22 ordering",
              all(ly.diffusion_breaks(ly.to_edges(aoi22_net, "o", "g", itertools.count(1)), list(o))
                  == breaks(G["aoi22"][0], o) for o in itertools.permutations("ABCD")), "")

# ---------------------------------------------------------------- rules and strips, feature by feature
R = dict(poly=2, poly_sp=3, contact=2, c2g=2, encl=1)


def strip(n_gates, contacted_internal, r=R):
    length = 0
    length += r["encl"] + r["contact"] + r["c2g"]          # left end
    for i in range(n_gates):
        length += r["poly"]
        if i < n_gates - 1:
            length += (r["c2g"] + r["contact"] + r["c2g"]) if contacted_internal else r["poly_sp"]
    length += r["c2g"] + r["contact"] + r["encl"]          # right end
    return length


v.check("Ex 19-09.1a", R["poly"] + 2 * R["c2g"] + R["contact"])
v.check("Ex 19-09.1b", (R["poly"] + 2 * R["c2g"] + R["contact"]) * 0.1)
v.check("Ex 19-09.1c", R["poly"] + R["poly_sp"])
v.check("Ex 19-09.1d", (R["poly"] + R["poly_sp"]) * 0.1)
v.check("Ex 19-09.1e", strip(3, True) - strip(3, False))
v.check("Ex 19-09.1f", 100 * (1 - 5 / 8))
v.check("19-09.1a", R["contact"] + 2 * R["encl"])
R3 = dict(R, c2g=3)
v.check("19-09.2a", R3["poly"] + 2 * R3["c2g"] + R3["contact"])
v.check("19-09.2b", R3["poly"] + R3["poly_sp"])
v.check("19-09.7a", strip(3, False))
v.check("19-09.7b", strip(3, True))
v.check("19-09.7c", 100 * (1 - strip(3, False) / strip(3, True)))
v.check("Lab 19-09.c", strip(3, True, R3))
v.check("Lab 19-09.d", strip(3, False, R3))
v.assert_true("lab pitches", ly.contacted_pitch() == 8 and ly.uncontacted_pitch() == 5, "")
v.assert_true("lab strip lengths", all(ly.strip_length(3, c) == strip(3, c) for c in (True, False))
              and all(ly.strip_length(3, c, dict(ly.RULES, contact_to_poly=3)) == strip(3, c, R3) for c in (True, False)), "")

# ---------------------------------------------------------------- areas
site = 0.46 * 2.72
ff = 16 * site
v.check("Ex 19-09.4a", site)
v.check("Ex 19-09.4b", ff)
v.check("Ex 19-09.4c", 10_000 * ff * 1e-6)
v.check("Ex 19-09.4d", 10_000 * ff * 1e-6 / 0.7)
v.check("Ex 19-09.4e", 200 / 160)
v.check("Ex 19-09.4f", 10_000 * ff * 1e-6 / 0.7 + 200 / 160)
v.check("Ex 19-09.4g", 100 * 10_000 / 210_000)
v.check("Ex 19-09.4h", 100 * (10_000 * ff * 1e-6 / 0.7) / (10_000 * ff * 1e-6 / 0.7 + 200 / 160))
v.check("Ex 19-09.5a", 2.72 * 7.5 / 9)
v.check("Ex 19-09.5b", 100 * (1 - 7.5 / 9))
v.check("Ex 19-09.6a", 0.2 * 2500 / (0.5 * 2))
v.check("Ex 19-09.6b", 400 * 1.0 / 0.2)
v.check("Ex 19-09.6c", 400 * 1.0 / 0.2 / 1000)
v.check("19-09.6a", 500 / 160)
v.check("19-09.6b", 30_000 * 20.02e-6)
v.check("19-09.6c", 30_000 * 20.02e-6 / 0.65)
v.check("19-09.6d", 30_000 * 20.02e-6 / 0.8)
v.check("19-09.8a", 100 * 3.0 / 4.0)
v.check("19-09.8b", 3.0 / 0.85)
v.check("19-09.8c", 100 * (1 - (3.0 / 0.85) / 4.0))
v.check("19-09.10a", 0.150 * 0.420)
v.check("19-09.10b", 400 * 0.150 * 0.420)
v.check("19-09.10c", 400 * 0.150 * 0.420 / 0.14)
v.check("Txt 19-09.a", 100 * ((0.48 * 3.33) / (0.46 * 2.72) - 1))
v.check("Txt 19-09.b", 0.150 / 0.048)

# problems 10(b), 11 and 13
v.check("19-09.10d", 25.2 / (2 * 0.35) - 0.14)
v.check("19-09.11a", ly.strip_length(2, False))
v.check("19-09.11b", ly.strip_length(2, True))
v.check("19-09.11c", ly.strip_length(2, False) * 0.075)
v.check("19-09.11d", ly.strip_length(2, True) * 0.075)
import json  # noqa: E402
lib = json.loads((ROOT / "labs" / "19-10-lab" / "sky130_hd_subset.json").read_text())
w_nand2 = lib["cells"]["nand2_1"]["area"] / 2.72
v.check("19-09.13a", w_nand2)
v.check("19-09.13b", w_nand2 / 0.46)
v.check("19-09.13c", 100 * (ly.strip_length(2, True) * 0.075 / w_nand2 - 1))

sys.exit(v.finish())
