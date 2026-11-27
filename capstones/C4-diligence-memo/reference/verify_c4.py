#!/usr/bin/env python3
"""Verify the C4 diligence memo: recompute every derived number from the logged inputs in claims.py.

The serving model is checked two ways: through claims.serve() and by a brute-force search over the batch size
that confirms the closed-form batch is the largest feasible one. The prefill-aware throughput is recomputed by
balancing a prefill pool against a decode pool (requests in = requests out), independently of claims.combined(). The scorecard is recomputed from its table,
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
v.check("M.hB", hB[2])
v.check("M.gB", gB[2])
v.check("M.rB", gB[2] / hB[2])
v.assert_true("the decode-only ratio grows once the model leaves the 8-GPU server", gB[2] / hB[2] > 3 * gA[2] / hA[2])
v.check("M.step", gA[1] * 1e3)
v.check("M.steph", hA[1] * 1e3)
v.assert_true("every decode step meets the 50 ms deadline (the deadline does not bind)",
              all(r[1] < c.TTL_S for r in (hA, gA, hB, gB)))
gemm = gA[0] * 2 * 140e9 / (R["gpus"] * c.B200["nvfp4_dense_pf"] * 1e15)
v.check("M.gemm", gemm * 1e3)
v.assert_true("decode is memory-bound: weight multiplications take under a quarter of the step", gemm < 0.25 * gA[1])
bph, bpg = (140 + hA[0]) / hA[0], (70 + gA[0]) / gA[0]   # GB read per generated token
v.check("M.bph", bph)
v.check("M.bpg", bpg)
v.check("M.bpr", bph / bpg)
v.assert_true("bandwidth ratio times bytes-per-token ratio reproduces the decode ratio", abs(bw * bph / bpg - gA[2] / hA[2]) < 1e-9)


def pooled(decode_per_gpu, dense_pf, params, gpus=1000.0):
    """Split a fleet into prefill and decode pools so that requests in equal requests out; return tokens/s per GPU."""
    req_flop = 2 * params * c.IN_TOK                     # prefill FLOPs per request
    def imbalance(f):
        prefill_req = f * gpus * dense_pf * 1e15 / req_flop
        decode_req = (1 - f) * gpus * decode_per_gpu / c.OUT_TOK
        return prefill_req - decode_req
    lo, hi = 0.0, 1.0
    for _ in range(200):                                 # bisection on the prefill fraction
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if imbalance(mid) > 0 else (mid, hi)
    f = (lo + hi) / 2
    return (1 - f) * decode_per_gpu, f


res = {}
for name, h_dec, g_dec in (("A", hA, gA), ("B", hB, gB)):
    P = c.MODELS[name]["params"]
    h_tok, h_f = pooled(h_dec[2], H["fp8_dense_pf"], P)
    g_tok, g_f = pooled(g_dec[2], c.B200["nvfp4_dense_pf"], P)
    cmp_ = c.compare(name)
    v.assert_true(f"model {name}: pool balancing agrees with claims.combined()",
                  abs(h_tok - cmp_["h"]) < 1e-6 * h_tok and abs(g_tok - cmp_["g"]) < 1e-6 * g_tok)
    res[name] = (h_tok, g_tok, h_f, g_f, cmp_["h_pre"], cmp_["g_pre"])
v.check("M.hpA", res["A"][4])
v.check("M.gpA", res["A"][5])
v.check("M.hcA", res["A"][0])
v.check("M.gcA", res["A"][1])
v.check("M.hpB", res["B"][4])
v.check("M.gpB", res["B"][5])
v.check("M.hcB", res["B"][0])
v.check("M.gcB", res["B"][1])
v.check("M.preh", 100 * res["A"][2])
v.check("M.preg", 100 * res["A"][3])
rA, rB = res["A"][1] / res["A"][0], res["B"][1] / res["B"][0]
for key in ("M.rcA", "C.serveA"):
    v.check(key, rA)
for key in ("M.rcB", "C.serveB"):
    v.check(key, rB)
v.check("M.res", c.CLAIM_INFER / rA)
v.check("C.resid", c.CLAIM_INFER / rA)
v.assert_true("with prefill, both ratios sit near the dense-compute ratio (within 5% of 5.0x)",
              all(abs(r_ / (c.B200["nvfp4_dense_pf"] / H["fp8_dense_pf"]) - 1) < 0.05 for r_ in (rA, rB)))
g8 = c.serve(72, pg["bw_tbs"], pg["hbm_gb"], 140, 1.0)
eq_tok, _ = pooled(g8[2], c.B200["fp8_dense_pf"], 140e9)
v.check("M.eq", eq_tok)
v.check("M.eqr", eq_tok / res["A"][0])
for key, gpus, pf, P in (("M.ttA", 8, H["fp8_dense_pf"], 140e9), ("M.ttB", 16, H["fp8_dense_pf"], 1e12),
                         ("M.tgA", 72, c.B200["nvfp4_dense_pf"], 140e9), ("M.tgB", 72, c.B200["nvfp4_dense_pf"], 1e12)):
    v.check(key, 2 * P * c.IN_TOK / (gpus * pf * 1e15))
    v.assert_true(f"{key}: first-token prefill fits the 5 s limit at the dense peak", c.ttft(gpus, pf, P) < c.TTFT_S)
v.check("M.mfu", 100 * c.ttft(16, H["fp8_dense_pf"], 1e12) / c.TTFT_S)

each_way = 18 * 2 * 200e9 / 8 / 1e9                      # 18 links x 2 lanes x 200 Gb/s, one direction [R-521]
v.assert_true("NVLink 5 is 900 GB/s each way (half the 1.8 TB/s two-way figure)", each_way == c.NVLINK5_EACH_WAY_GBS == 900.0)
v.assert_true("a 400 Gb/s port is 50 GB/s each way", abs(400e9 / 8 / 1e9 - c.PORT_GBS) < 1e-12)
for key in ("M.port", "C.port"):
    v.check(key, each_way / c.PORT_GBS)

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
gpu_hi = sum(L["gpu_table"])
v.check("R.gpu", gpu_int)
v.check("R.gpuhi", gpu_hi)
v.check("R.pcthi", 100 * gpu_hi / L["unexpected"])
v.assert_true("the text's 58.7% matches the table only with 126 faulty GPUs, not 148",
              abs((gpu_hi - 148 + 126) / L["unexpected"] - L["gpu_share"]) < 5e-4)
for n_int, kr, kk, kd in ((gpu_int, "R.rate", ("R.rack", "C.rackyr"), "R.days"),
                          (gpu_hi, "R.ratehi", ("R.rackhi", "C.rackhi"), "R.dayshi")):
    rate = n_int / (L["days"] * L["gpus"]) * 365.25
    v.check(kr, rate)
    for key in kk:
        v.check(key, rate * R["gpus"])
    v.check(kd, 365.25 / (rate * R["gpus"]))

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
v.check("S.sw", 100 * var[names.index("Ecosystem and software")] / sum(var))
v.check("S.sup", 100 * var[names.index("Manufacturing and supply")] / sum(var))
v.check("S.road", 100 * var[names.index("Roadmap")] / sum(var))
iw, isup = names.index("Ecosystem and software"), names.index("Manufacturing and supply")
v.assert_true("software is the largest variance contribution and supply the second",
              sorted(range(7), key=lambda k: -var[k])[:2] == [iw, isup])
v.assert_true("software and supply carry two-thirds of the variance", abs((var[iw] + var[isup]) / sum(var) - 2 / 3) < 0.02)
v.assert_true("software is scored with the widest sigma, as the text says", sd[iw] == max(sd))

sys.exit(v.finish())
