"""eeverify — shared helpers for the curriculum's verification scripts.

Every number published in a chapter, problem solution or exam appears in a
machine-readable *answer key*: a Markdown table placed directly after the marker

    <!-- answer-key -->

with columns  | ID | Quantity | Value | Unit |.  A verify script loads the
key(s), recomputes every value independently, and calls ``v.check(ID, value)``.

Tolerance is derived from the precision *as published*: a value written as
``2.20`` must agree with the computed value to within half a unit in its last
displayed digit (±0.005), i.e. the published value must be the correctly
rounded result. A per-check ``tol=`` (absolute) or ``rtol=`` can override this
where a looser comparison is justified (state why in a comment).

Supported value formats in the key:
    real:         4.243   -0.5   −0.5   6.32e-3   6.32×10^-3   6.32 × 10⁻³
    rectangular:  3 + j4   -1 − j2.5   j5   −j0.25
    polar:        5∠53.13°   2.236 ∠ −63.43°

At the end, ``v.finish()`` fails if any key entry was never checked, or any
check referenced an ID not in the key. Exit status is non-zero on failure.
"""
from __future__ import annotations

import cmath
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

MARKER = "<!-- answer-key -->"
_SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")


# --------------------------------------------------------------------------- parsing
@dataclass
class Num:
    """A published real number with its implied absolute tolerance (half-ulp)."""
    value: float
    halfulp: float


@dataclass
class Published:
    raw: str
    kind: str  # "real" | "rect" | "polar"
    parts: tuple  # (Num,) | (re Num, im Num) | (mag Num, angle_deg Num)


def _clean(s: str) -> str:
    s = s.strip().replace("−", "-").replace("–", "-").replace(" ", " ").replace(" ", " ")
    s = s.replace("$", "").replace("\\,", "").replace("{", "").replace("}", "")
    return s


def _parse_real(s: str) -> Num:
    s = _clean(s).replace(" ", "")
    s = s.replace("\\times", "×").replace("x10", "×10")
    exp = 0
    m = re.fullmatch(r"([-+]?[\d.]+)(?:[eE]([-+]?\d+)|×10\^?([-+]?\d+|[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+))?", s)
    if not m:
        raise ValueError(f"cannot parse real number {s!r}")
    mant = m.group(1)
    if m.group(2) is not None:
        exp = int(m.group(2))
    elif m.group(3) is not None:
        exp = int(m.group(3).translate(_SUP))
    decimals = len(mant.split(".")[1]) if "." in mant else 0
    value = float(mant) * 10.0**exp
    halfulp = 0.5 * 10.0 ** (exp - decimals)
    return Num(value, halfulp)


def parse_value(raw: str) -> Published:
    s = _clean(raw)
    if "∠" in s:
        mag, ang = s.split("∠", 1)
        ang = ang.replace("°", "").strip()
        return Published(raw, "polar", (_parse_real(mag), _parse_real(ang)))
    t = s.replace(" ", "")
    m = re.fullmatch(r"([-+]?[\d.]+(?:[eE][-+]?\d+)?)?([-+])j([\d.]+(?:[eE][-+]?\d+)?)", t)
    if m:
        re_part = _parse_real(m.group(1)) if m.group(1) else Num(0.0, 0.0)
        im = _parse_real(m.group(3))
        if m.group(2) == "-":
            im = Num(-im.value, im.halfulp)
        return Published(raw, "rect", (re_part, im))
    m = re.fullmatch(r"([-+]?)j([\d.]+(?:[eE][-+]?\d+)?)", t)
    if m:
        im = _parse_real(m.group(2))
        if m.group(1) == "-":
            im = Num(-im.value, im.halfulp)
        return Published(raw, "rect", (Num(0.0, 0.0), im))
    return Published(raw, "real", (_parse_real(s),))


def load_answer_key(path: str | Path) -> dict[str, tuple[Published, str, str]]:
    """Return {ID: (Published, quantity, unit)} from every answer-key table in a Markdown file."""
    path = Path(path)
    lines = path.read_text(encoding="utf-8").splitlines()
    key: dict[str, tuple[Published, str, str]] = {}
    i = 0
    while i < len(lines):
        if lines[i].strip() == MARKER:
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("|"):
                i += 1
            header = True
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if header or set(lines[i].replace("|", "").strip()) <= set("-: "):
                    header = False
                    i += 1
                    continue
                if len(cells) < 3:
                    raise ValueError(f"{path}:{i+1}: answer-key row needs ID | Quantity | Value | Unit")
                ident, qty, val = cells[0], cells[1], cells[2]
                unit = cells[3] if len(cells) > 3 else ""
                if ident in key:
                    raise ValueError(f"{path}:{i+1}: duplicate answer-key ID {ident}")
                try:
                    key[ident] = (parse_value(val), qty, unit)
                except ValueError as e:
                    raise ValueError(f"{path}:{i+1}: {e}") from None
                i += 1
            continue
        i += 1
    return key


# --------------------------------------------------------------------------- checking
def _wrap_deg(d: float) -> float:
    return (d + 180.0) % 360.0 - 180.0


@dataclass
class Verifier:
    name: str
    keys: dict = field(default_factory=dict)
    checked: set = field(default_factory=set)
    failures: list = field(default_factory=list)
    passes: int = 0

    @classmethod
    def from_files(cls, name: str, *paths: str | Path) -> "Verifier":
        v = cls(name)
        for p in paths:
            for k, val in load_answer_key(p).items():
                if k in v.keys:
                    raise ValueError(f"answer-key ID {k} appears in more than one file")
                v.keys[k] = val + (str(p),)
        return v

    # ---- core comparison
    def _ok_real(self, computed: float, num: Num, tol, rtol) -> tuple[bool, float]:
        allowed = num.halfulp * (1 + 1e-9) + 1e-12 * abs(num.value)
        if tol is not None:
            allowed = tol
        if rtol is not None:
            allowed = max(allowed if tol is not None else 0.0, rtol * abs(num.value))
        return abs(computed - num.value) <= allowed, allowed

    def check(self, ident: str, computed, *, tol: float | None = None, rtol: float | None = None,
              angle_tol: float | None = None) -> bool:
        """Compare an independently computed value with the published answer-key value."""
        if ident not in self.keys:
            self.failures.append(f"{ident}: not found in any answer key")
            print(f"  FAIL {ident}: no such answer-key entry")
            return False
        pub, qty, unit, src = self.keys[ident]
        self.checked.add(ident)
        ok = True
        detail = ""
        if pub.kind == "real":
            c = complex(computed)
            if abs(c.imag) > 1e-9 * max(1.0, abs(c.real)):
                ok, detail = False, f"computed value is complex ({c}) but published value is real"
            else:
                ok, allowed = self._ok_real(c.real, pub.parts[0], tol, rtol)
                detail = f"computed {c.real:.10g}, published {pub.raw} (±{allowed:.3g})"
        elif pub.kind == "rect":
            c = complex(computed)
            ok_r, a_r = self._ok_real(c.real, pub.parts[0], tol, rtol)
            ok_i, a_i = self._ok_real(c.imag, pub.parts[1], tol, rtol)
            ok = ok_r and ok_i
            detail = f"computed {c.real:.10g}{c.imag:+.10g}j, published {pub.raw}"
        elif pub.kind == "polar":
            c = complex(computed)
            mag, ang = abs(c), math.degrees(cmath.phase(c))
            ok_m, _ = self._ok_real(mag, pub.parts[0], tol, rtol)
            ang_allowed = angle_tol if angle_tol is not None else pub.parts[1].halfulp * (1 + 1e-9)
            ok_a = abs(_wrap_deg(ang - pub.parts[1].value)) <= ang_allowed or mag < 1e-12
            ok = ok_m and ok_a
            detail = f"computed {mag:.10g}∠{ang:.8g}°, published {pub.raw}"
        if ok:
            self.passes += 1
            print(f"  ok   {ident:<14} {qty} = {pub.raw} {unit}")
        else:
            self.failures.append(f"{ident}: {detail}")
            print(f"  FAIL {ident:<14} {detail}")
        return ok

    def assert_true(self, label: str, condition: bool, detail: str = "") -> bool:
        """Record an independent (non-answer-key) assertion, e.g. an ODE residual or identity."""
        if condition:
            self.passes += 1
            print(f"  ok   [assert] {label}")
        else:
            self.failures.append(f"[assert] {label}: {detail}")
            print(f"  FAIL [assert] {label}: {detail}")
        return bool(condition)

    def finish(self) -> None:
        missing = sorted(set(self.keys) - self.checked)
        for m in missing:
            self.failures.append(f"{m}: published in {self.keys[m][3]} but never checked")
            print(f"  FAIL {m}: published but never checked")
        status = "PASS" if not self.failures else "FAIL"
        print(f"{status} {self.name}: {self.passes} checks passed, {len(self.failures)} failed, "
              f"{len(self.keys)} answer-key entries")
        if self.failures:
            sys.exit(1)


# --------------------------------------------------------------------------- small utilities
def polar(mag: float, angle_deg: float) -> complex:
    """Complex number from magnitude and angle in degrees."""
    return cmath.rect(mag, math.radians(angle_deg))


def deg(c: complex) -> float:
    """Angle of a complex number in degrees, in (-180, 180]."""
    return math.degrees(cmath.phase(c))


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]
