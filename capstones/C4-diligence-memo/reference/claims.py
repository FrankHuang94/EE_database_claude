#!/usr/bin/env python3
"""C4 reference: the arithmetic behind the GB200 NVL72 diligence memo.

Every input is a published figure with its research-log ID, or a labelled hypothetical. The memo's derived
numbers come from these functions, and verify_c4.py recomputes each one.
"""
from __future__ import annotations

# ---------------------------------------------------------------- published figures (as of Nov 2026)
RACK = {                       # GB200 NVL72 rack column [R-690]
    "gpus": 72, "cpus": 36, "hbm_tb": 13.4, "hbm_bw_tbs": 576.0, "nvlink_tbs": 130.0,
    "nvfp4_pf": (1440.0, 720.0),           # the two NVFP4 figures; the lower is dense [R-690, R-460]
    "fp8_pf": 720.0, "bf16_pf": 360.0,     # single figures; sparse per the footnote read in R-221
    "arm_cores": 2592,
}
B200 = {"fp8_dense_pf": 5.0, "nvfp4_dense_pf": 10.0, "tgp_w": 1200.0, "hbm_gb": 192.0}      # [R-460]
H100 = {"fp8_dense_pf": 2.0, "bf16_dense_pf": 0.9895, "hbm_gb": 80.0, "bw_tbs": 3.35,      # [R-460, R-040]
        "tgp_w": 700.0, "nvlink_tbs": 0.9, "node_gpus": 8}                                  # [R-460, R-521]
NVLINK5_TBS = 1.8                                                                            # [R-521, R-690]
MI355X = {"hbm_gb": 288.0, "bw_tbs": 8.0, "fp8_dense_pf": 5.0, "mxfp4_pf": 10.1, "tbp_w": 1400.0,
          "if_links": 7, "if_link_gbs": 144.0}                                               # [R-692]
IRONWOOD = {"hbm_gb": 192.0, "bw_tbs": 7.37, "fp8_peak_pf": 4.614, "ici_tbs": 1.2, "pod": 9216,
            "pod_mw": 10.0}                                                                  # [R-693]
CLAIM_INFER, CLAIM_ENERGY, CLAIM_TRAIN = 30.0, 25.0, 4.0                                     # [R-690]
TTL_S = 0.050                    # token-to-token latency in the claim's footnote [R-690]
RACK_KW = {"nvidia_approx": 120.0, "hpe_nominal": 132.0, "hpe_provisioned": 192.0}           # [R-098, R-444]
PORT_GBS = 50.0                  # a 400 Gb/s network port per GPU (the class Meta used [R-694]; one per GPU assumed)
LLAMA = {"unexpected": 419, "gpu_share": 0.587, "days": 54, "gpus": 16384}                  # [R-694]
TPP_THRESHOLD = 4800             # ECCN 3A090.a.1 [R-659]


def per_gpu():
    g = RACK["gpus"]
    return {"hbm_gb": RACK["hbm_tb"] * 1e3 / g, "bw_tbs": RACK["hbm_bw_tbs"] / g, "nvlink_tbs": RACK["nvlink_tbs"] / g,
            "nvfp4_sparse_pf": RACK["nvfp4_pf"][0] / g, "nvfp4_dense_pf": RACK["nvfp4_pf"][1] / g,
            "fp8_pf": RACK["fp8_pf"] / g, "bf16_pf": RACK["bf16_pf"] / g, "cores_per_cpu": RACK["arm_cores"] / RACK["cpus"]}


def serve(gpus, bw_tbs, cap_gb, weights_gb, kv_gb, ttl_s=TTL_S):
    """Decode throughput per GPU in one scale-up domain, limited by memory bandwidth or capacity.

    Each decode step reads every weight once and every sequence's KV cache once, so a step with batch B takes
    t = (W + B K) / (G BW). The batch is the largest that meets both t <= ttl and W + B K <= G C.
    Returns (batch, step time in s, tokens/s per GPU); batch is 0 when the model does not fit.
    """
    w, k, bw, cap = weights_gb * 1e9, kv_gb * 1e9, bw_tbs * 1e12, cap_gb * 1e9
    b_bw = (ttl_s * gpus * bw - w) / k
    b_cap = (gpus * cap - w) / k
    b = max(0.0, min(b_bw, b_cap))
    if b == 0.0:
        return 0.0, float("nan"), 0.0
    t = (w + b * k) / (gpus * bw)
    return b, t, b / (t * gpus)


if __name__ == "__main__":
    pg = per_gpu()
    print({k: round(v, 3) for k, v in pg.items()})
    for name, wh, wg in (("A: 140 GB at FP8", 140, 70), ("B: 1 TB at FP8", 1000, 500)):
        h = serve(8 if wh <= 640 else 16, H100["bw_tbs"], H100["hbm_gb"], wh, 1.0)
        g = serve(72, pg["bw_tbs"], pg["hbm_gb"], wg, 1.0)
        print(f"{name}: H100 {h[2]:.0f} tok/s/GPU, NVL72 {g[2]:.0f} tok/s/GPU, ratio {g[2] / h[2]:.2f}")
