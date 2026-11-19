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

For programming chapters, ``run_python_blocks(v, path)`` executes every fenced
```python block of a Markdown file, in order and in one shared namespace, and
records one assertion per block. A ```python block immediately followed by a
```text block must print exactly that text. A block whose first line is
``# not run`` is skipped (use it for deliberately broken or interactive code).

``run_c_blocks(v, path)`` does the same for fenced ```c blocks, compiling each with the strict,
sanitizer-instrumented flags of ``tools/run_c.py``. Directives on a block's first lines:
``// file: NAME`` saves the block as NAME for later blocks (and compiles it if it is a .c file);
``// with: a.c b.c`` links those saved files into a block that has ``main``;
``// expect: warning`` / ``// expect: error`` asserts that compiling (without -Werror) warns / fails;
``// expect: warning -Wparentheses`` also requires that diagnostic by name, so that an unrelated
warning cannot satisfy the check;
``// expect: sanitizer`` asserts that running reports a sanitizer error, and each line of the
following ```text block must appear in that report; ``// fragment`` skips the block (fragments are
not compiled at all, so use them only for snippets that cannot stand alone, and keep them short);
``// EXTRA_CFLAGS: ...`` adds flags. A block without ``main`` is compiled with ``-c`` only.
"""
from __future__ import annotations

import cmath
import contextlib
import io
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import traceback
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
        im = _parse_real(m.group(3))
        # an omitted real part is an exact zero published at the imaginary part's precision
        re_part = _parse_real(m.group(1)) if m.group(1) else Num(0.0, im.halfulp)
        if m.group(2) == "-":
            im = Num(-im.value, im.halfulp)
        return Published(raw, "rect", (re_part, im))
    m = re.fullmatch(r"([-+]?)j([\d.]+(?:[eE][-+]?\d+)?)", t)
    if m:
        im = _parse_real(m.group(2))
        if m.group(1) == "-":
            im = Num(-im.value, im.halfulp)
        return Published(raw, "rect", (Num(0.0, im.halfulp), im))
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


# --------------------------------------------------------------------------- code blocks in Markdown
_FENCE = re.compile(r"^```([A-Za-z0-9_+-]*)[ \t]*\n(.*?)^```[ \t]*$", re.M | re.S)


def markdown_code_blocks(path: str | Path) -> list[tuple[str, str, int, int]]:
    """Return (language, code, start, end) for every top-level fenced block, in order."""
    text = Path(path).read_text(encoding="utf-8")
    return [(m.group(1).lower(), m.group(2), m.start(), m.end()) for m in _FENCE.finditer(text)]


def run_python_blocks(v: "Verifier", path: str | Path, label: str | None = None) -> dict:
    """Execute every ```python block of a Markdown file and check outputs shown in ```text blocks.

    Blocks run in order in one namespace, inside a temporary working directory (so example
    code may create files). Returns the final namespace so a verify script can reuse values
    the examples computed.
    """
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    blocks = markdown_code_blocks(path)
    name = label or path.stem
    ns: dict = {"__name__": "__main__"}
    old_cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            for i, (lang, code, _start, end) in enumerate(blocks):
                if lang != "python" or code.lstrip().startswith("# not run"):
                    continue
                expected = None
                if i + 1 < len(blocks) and blocks[i + 1][0] == "text" and not text[end:blocks[i + 1][2]].strip():
                    expected = blocks[i + 1][1]
                buf = io.StringIO()
                line = text.count("\n", 0, _start) + 1
                try:
                    with contextlib.redirect_stdout(buf):
                        exec(compile(code, f"{path.name}:{line}", "exec"), ns)
                except Exception:  # noqa: BLE001 - report any failure of the example code
                    v.assert_true(f"{name} code block at line {line} runs", False,
                                  traceback.format_exc(limit=2).strip().splitlines()[-1])
                    continue
                if expected is None:
                    v.assert_true(f"{name} code block at line {line} runs", True)
                else:
                    got = "\n".join(l.rstrip() for l in buf.getvalue().rstrip().splitlines())
                    want = "\n".join(l.rstrip() for l in expected.rstrip().splitlines())
                    v.assert_true(f"{name} code block at line {line} prints its shown output", got == want,
                                  f"expected {want!r}, got {got!r}")
        finally:
            os.chdir(old_cwd)
    return ns


# --------------------------------------------------------------------------- C code blocks
C_FLAGS = ["-std=c17", "-Wall", "-Wextra", "-Wpedantic", "-Werror", "-O1", "-g",
           "-fsanitize=address,undefined", "-fno-omit-frame-pointer", "-fno-sanitize-recover=all"]
C_SANITIZER_MARKERS = ("ERROR: AddressSanitizer", "runtime error:", "ERROR: LeakSanitizer")


def _c_directives(code: str) -> dict:
    """Read `// key: value` directives from the leading comment lines of a C block."""
    found = {}
    for line in code.splitlines():
        m = re.match(r"\s*//\s*(file|with|expect|EXTRA_CFLAGS|fragment)\b:?\s*(.*)$", line)
        if not m:
            break
        found[m.group(1)] = m.group(2).strip()
    return found


def build_and_run_c(code: str, workdir: Path, extra_sources=(), flags=None, werror=True, run=True,
                    timeout: int = 60) -> dict:
    """Compile one C block (plus saved sources) in workdir; optionally run it. Returns a result dict."""
    cc = os.environ.get("CC") or shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if not cc:
        return {"ok": False, "stage": "compile", "log": "no C compiler found"}
    d = _c_directives(code)
    base = [f for f in C_FLAGS if werror or f != "-Werror"] + (flags or []) + d.get("EXTRA_CFLAGS", "").split()
    src = workdir / "block_main.c"
    src.write_text(code, encoding="utf-8")
    has_main = re.search(r"\bint\s+main\s*\(", code) is not None
    if not has_main or not run:
        c = subprocess.run([cc, *base, "-c", "-o", str(workdir / "block.o"), str(src)],
                           capture_output=True, text=True, cwd=workdir)
        return {"ok": c.returncode == 0, "stage": "compile", "log": c.stderr, "stdout": ""}
    exe = workdir / "block.out"
    c = subprocess.run([cc, *base, "-o", str(exe), str(src), *map(str, extra_sources), "-lm"],
                       capture_output=True, text=True, cwd=workdir)
    if c.returncode != 0:
        return {"ok": False, "stage": "compile", "log": c.stderr, "stdout": ""}
    env = dict(os.environ, ASAN_OPTIONS=("detect_leaks=1:" if sys.platform.startswith("linux") else "")
               + "abort_on_error=0", UBSAN_OPTIONS="print_stacktrace=0")
    try:
        r = subprocess.run([str(exe)], capture_output=True, text=True, cwd=workdir, timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        return {"ok": False, "stage": "run", "log": "timeout", "stdout": ""}
    log = r.stdout + r.stderr
    clean = r.returncode == 0 and not any(m in log for m in C_SANITIZER_MARKERS)
    return {"ok": clean, "stage": "run", "log": log, "stdout": r.stdout, "returncode": r.returncode,
            "compile_log": c.stderr}


def run_c_blocks(v: "Verifier", path: str | Path, label: str | None = None) -> None:
    """Compile and run every ```c block of a Markdown file; check outputs shown in ```text blocks."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    blocks = markdown_code_blocks(path)
    name = label or path.stem
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        for i, (lang, code, start, end) in enumerate(blocks):
            if lang != "c":
                continue
            d = _c_directives(code)
            line = text.count("\n", 0, start) + 1
            where = f"{name} C block at line {line}"
            if "fragment" in d:
                continue
            expected = None
            if i + 1 < len(blocks) and blocks[i + 1][0] == "text" and not text[end:blocks[i + 1][2]].strip():
                expected = blocks[i + 1][1]
            if "file" in d:
                (work / d["file"]).write_text(code, encoding="utf-8")
                if d["file"].endswith(".c"):
                    r = build_and_run_c(code, work, run=False)
                    v.assert_true(f"{where} ({d['file']}) compiles cleanly", r["ok"], r["log"][-800:])
                continue
            extra = [work / f for f in d.get("with", "").split()]
            expect, *want_flags = d.get("expect", "").split() or [""]
            if expect == "error":
                r = build_and_run_c(code, work, extra, werror=False, run=False)
                v.assert_true(f"{where} fails to compile, as intended", not r["ok"])
            elif expect == "warning":
                r = build_and_run_c(code, work, extra, werror=False, run=False)
                named = all(f"[{flag}" in r["log"] for flag in want_flags)
                v.assert_true(f"{where} compiles with the intended warning{' ' + ' '.join(want_flags) if want_flags else ''}",
                              r["ok"] and "warning:" in r["log"] and named, r["log"][-800:])
            elif expect == "sanitizer":
                r = build_and_run_c(code, work, extra)
                got = r["log"]
                hit = r.get("stage") == "run" and any(m in got for m in C_SANITIZER_MARKERS)
                if expected is not None:
                    hit = hit and all(l.strip() in got for l in expected.strip().splitlines() if l.strip())
                v.assert_true(f"{where} is caught by a sanitizer, as intended", hit, got[-800:])
            else:
                r = build_and_run_c(code, work, extra)
                if not r["ok"]:
                    v.assert_true(f"{where} compiles and runs cleanly", False, r["log"][-800:])
                elif expected is None:
                    v.assert_true(f"{where} compiles and runs cleanly", True)
                else:
                    got = "\n".join(l.rstrip() for l in r["stdout"].rstrip().splitlines())
                    want = "\n".join(l.rstrip() for l in expected.rstrip().splitlines())
                    v.assert_true(f"{where} prints its shown output", got == want, f"expected {want!r}, got {got!r}")
