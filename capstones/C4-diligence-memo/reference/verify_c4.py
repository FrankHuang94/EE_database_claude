#!/usr/bin/env python3
"""Verify the C4 diligence memo: recompute every derived number from the logged inputs in claims.py.

The serving model is checked two ways: through claims.serve() and by a brute-force search over the batch size
that confirms the closed-form batch is the largest feasible one. The scorecard is recomputed from its table,
which is parsed from the memo itself so that the table and the totals cannot drift apart.
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

import claims as c  # noqa: E402

v = Verifier.from_files("C4", HERE / "memo.md")
R, H = c.RACK, c.H100
pg = c.per_gpu()

# ----------------------------------------------------------------- per GPU and consistency
v.check("P.hbm", pg["hbm_gb"])
v.check("V.cap", pg["hbm_gb"])
v.check("P.bw", pg["bw_tbs"])
v.check("P.nvl", pg["nvlink_tbs"])
v.check("P.fp4s", pg["nvfp4_sparse_pf"])
v.check("P.fp4d", pg["nvfp4_dense_pf"])
v.check("P.fp8", pg["fp8_pf"])
v.check("P.bf16", pg["bf16_pf"])
v.check("P.cores", pg["cores_per_cpu"])
v.assert_true("superchip column matches the rack: 372 GB and 16 TB/s for two GPUs",
              abs(2 * pg["hbm_gb"] - 372) < 1.0 and abs(2 * pg["bw_tbs"] - 16) < 1e-9)
v.assert_true("NVLink per GPU rounds to the stated 1.8 TB/s", round(pg["nvlink_tbs"], 1) == c.NVLINK5_TBS)
v.assert_true("NVFP4 dense per GPU matches NVIDIA's per-GPU table (10 PF)", pg["nvfp4_dense_pf"] == c.B200["nvfp4_dense_pf"])
sparse_factor = pg["fp8_pf"] / c.B200["fp8_dense_pf"]
v.assert_true("the single FP8 row is twice the dense per-GPU rate, so it is sparse", sparse_factor == 2.0)
v.check("C.sparse", sparse_factor)
v.check("V.bf16", pg["bf16_pf"] / 2)

# ----------------------------------------------------------------- ratios to H100
bw = pg["bw_tbs"] / H["bw_tbs"]
for key in ("C.bw", "H.bw"):
    v.check(key, bw)
v.check("H.cap", pg["hbm_gb"] / H["hbm_gb"])
fp8 = c.B200["fp8_dense_pf"] / H["fp8_dense_pf"]
for key in ("C.fp8", "H.fp8"):
    v.check(key, fp8)
v.check("H.fp4", c.B200["nvfp4_dense_pf"] / H["fp8_dense_pf"])
v.check("H.nvl", c.NVLINK5_TBS / H["nvlink_tbs"])
v.check("H.dom", R["gpus"] / H["node_gpus"])
v.check("R.blast", R["gpus"] / H["node_gpus"])
v.check("H.tgp", c.B200["tgp_w"] / H["tgp_w"])
v.check("H.bytes", 1.0 / 0.5)                                   # bytes per weight, FP8 over FP4
ceil = bw * 2
v.check("H.ceil", ceil)
v.check("H.resid", c.CLAIM_INFER / ceil)

# ----------------------------------------------------------------- serving model
def brute(gpus, bw_tbs, cap_gb, w_gb, k_gb, ttl=c.TTL_S):
    """Largest integer batch meeting both limits, by direct search."""
    best = 0
    b = 0
    while True:
        need = (w_gb + (b + 1) * k_gb) * 1e9
        if need > gpus * cap_gb * 1e9 or need / (gpus * bw_tbs * 1e12) > ttl:
            break
        b += 1
        best = b
    return best


hA = c.serve(8, H["bw_tbs"], H["hbm_gb"], 140, 1.0)
gA = c.serve(72, pg["bw_tbs"], pg["hbm_gb"], 70, 1.0)
hB = c.serve(16, H["bw_tbs"], H["hbm_gb"], 1000, 1.0)
gB = c.serve(72, pg["bw_tbs"], pg["hbm_gb"], 500, 1.0)
v.assert_true("model B does not fit one 8-GPU H100 server", c.serve(8, H["bw_tbs"], H["hbm_gb"], 1000, 1.0)[0] == 0)
for res, args in ((hA, (8, H["bw_tbs"], H["hbm_gb"], 140, 1.0)), (gA, (72, pg["bw_tbs"], pg["hbm_gb"], 70, 1.0)),
                  (hB, (16, H["bw_tbs"], H["hbm_gb"], 1000, 1.0))):
    v.assert_true(f"closed-form batch matches a brute-force search for {args[:1]} GPUs and {args[3]} GB",
                  abs(res[0] - brute(*args)) <= 1)
v.assert_true("both systems are capacity-limited (step under 50 ms) in model A", hA[1] < c.TTL_S and gA[1] < c.TTL_S)
v.check("M.hA", hA[2])
v.check("M.bA", hA[0])
v.check("M.gA", gA[2])
v.check("M.gbA", gA[0])
v.check("M.rA", gA[2] / hA[2])
v.check("C.serveA", gA[2] / hA[2])
v.check("M.hB", hB[2])
v.check("M.gB", gB[2])
v.check("M.rB", gB[2] / hB[2])
v.check("C.serveB", gB[2] / hB[2])
v.assert_true("the ratio grows once the model leaves the 8-GPU server", gB[2] / hB[2] > 3 * gA[2] / hA[2])
port = c.NVLINK5_TBS * 1e3 / c.PORT_GBS
for key in ("M.port", "C.port"):
    v.check(key, port)
v.assert_true("a 400 Gb/s port is 50 GB/s", abs(400e9 / 8 / 1e9 - c.PORT_GBS) < 1e-12)

# ----------------------------------------------------------------- energy and training claims
v.check("E.pw", c.CLAIM_INFER / c.CLAIM_ENERGY)
for key, kw in (("E.lo", "nvidia_approx"), ("E.hi", "hpe_nominal"), ("F.lo", "nvidia_approx"), ("F.hi", "hpe_nominal")):
    v.check(key, c.RACK_KW[kw] / R["gpus"])
v.check("E.train", c.CLAIM_TRAIN / fp8)

# ----------------------------------------------------------------- competitive position
m, i = c.MI355X, c.IRONWOOD
v.check("K.mi", m["if_links"] * m["if_link_gbs"])
v.check("K.rg", c.B200["fp8_dense_pf"] * 1e15 / (pg["bw_tbs"] * 1e12))
v.check("K.rm", m["fp8_dense_pf"] * 1e15 / (m["bw_tbs"] * 1e12))
v.check("K.ri", i["fp8_peak_pf"] * 1e15 / (i["bw_tbs"] * 1e12))
v.check("K.rh", H["fp8_dense_pf"] * 1e15 / (H["bw_tbs"] * 1e12))
for key in ("K.cap", "C.mi355cap"):
    v.check(key, m["hbm_gb"] / pg["hbm_gb"])
v.check("K.ici", i["ici_tbs"] / c.NVLINK5_TBS)
v.check("K.fitr", R["hbm_tb"] * 1e12 / 0.5 / 1e12)
v.check("K.fitm", 8 * m["hbm_gb"] * 1e9 / 0.5 / 1e12)
v.check("K.fith", 8 * H["hbm_gb"] * 1e9 / 1.0 / 1e9)
v.assert_true("Ironwood all-in power per chip is about 1.09 kW", abs(i["pod_mw"] * 1e3 / i["pod"] - 1.09) < 0.005)

# ----------------------------------------------------------------- facility
v.check("F.prov", c.RACK_KW["hpe_provisioned"] / c.RACK_KW["hpe_nominal"])
over = [c.RACK_KW[k] / R["gpus"] - c.B200["tgp_w"] / 1e3 for k in ("nvidia_approx", "hpe_nominal")]
v.check("F.olo", over[0])
v.check("F.ohi", over[1])
v.check("F.plo", 100 * over[0] / (c.B200["tgp_w"] / 1e3))
v.check("F.phi", 100 * over[1] / (c.B200["tgp_w"] / 1e3))
v.check("F.mwh", c.RACK_KW["hpe_nominal"] * 8760 / 1e3)

# ----------------------------------------------------------------- reliability
L = c.LLAMA
gpu_int = L["gpu_share"] * L["unexpected"]
v.check("R.gpu", gpu_int)
rate = gpu_int / (L["days"] * L["gpus"]) * 365.25
v.check("R.rate", rate)
rack = rate * R["gpus"]
for key in ("R.rack", "C.rackyr"):
    v.check(key, rack)
v.check("R.days", 365.25 / rack)

# ----------------------------------------------------------------- export controls
mac = c.B200["nvfp4_dense_pf"] * 1e3 / 2                      # TFLOPS -> TOPS -> MacTOPS
v.check("X.mac", mac)
tpp4 = 2 * mac * 4
tpp8 = 2 * (c.B200["fp8_dense_pf"] * 1e3 / 2) * 8
v.check("X.tpp", tpp4)
v.check("X.tpp8", tpp8)
v.assert_true("FP4 and FP8 dense give the same TPP", tpp4 == tpp8)
v.check("X.ratio", tpp4 / c.TPP_THRESHOLD)

# ----------------------------------------------------------------- roadmap
gb300_dense = 1080.0 / 72                                     # GB300 NVL72 dense FP4 [R-460]
v.check("D.fp4", gb300_dense)
v.check("D.fp4r", gb300_dense / pg["nvfp4_dense_pf"])
v.check("D.mem", 288.0 / pg["hbm_gb"])
v.check("D.bw", 19.2 / pg["bw_tbs"])
v.check("D.fp4s", 50.0 / pg["nvfp4_sparse_pf"])

# ----------------------------------------------------------------- scorecard, parsed from the memo's table
text = (HERE / "memo.md").read_text(encoding="utf-8")
rows = re.findall(r"^\| (Architecture|Implementation|IP position|Team|Roadmap|Ecosystem and software|"
                  r"Manufacturing and supply) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \|", text, re.M)
v.assert_true("seven scorecard rows parsed", len(rows) == 7)
w = [float(r[1]) for r in rows]
s = [float(r[2]) for r in rows]
sd = [float(r[3]) for r in rows]
v.assert_true("weights sum to 1", abs(sum(w) - 1) < 1e-12)
S = sum(a * b for a, b in zip(w, s))
G = math.exp(sum(a * math.log(b) for a, b in zip(w, s)))
var = [a * a * b * b for a, b in zip(w, sd)]
for key in ("S.S", "C.S"):
    v.check(key, S)
for key in ("S.G", "C.G"):
    v.check(key, G)
v.assert_true("geometric score does not exceed the arithmetic (AM-GM)", G <= S)
v.check("S.sd", math.sqrt(sum(var)))
names = [r[0] for r in rows]
v.check("S.sup", 100 * var[names.index("Manufacturing and supply")] / sum(var))
v.check("S.road", 100 * var[names.index("Roadmap")] / sum(var))
v.assert_true("manufacturing and supply is the largest variance contribution",
              max(range(7), key=lambda k: var[k]) == names.index("Manufacturing and supply"))

sys.exit(v.finish())
