#!/usr/bin/env python3
"""Compile and run every self-checking C test program.

Convention: a test file is named `*_test.c`. It is compiled together with every other
`.c` file in the same directory except other tests and files ending in `_demo.c`
(stand-alone demonstrations, which are compiled on their own so they at least build).
Compilation is strict and instrumented:

    cc -std=c17 -Wall -Wextra -Wpedantic -Werror -O1 -g
       -fsanitize=address,undefined -fno-omit-frame-pointer -fno-sanitize-recover=all ... -lm

A test passes if it exits with status 0, prints `TEST PASSED`, and prints neither
`TEST FAILED` nor a sanitizer report. A test may add flags on a line of its own of the form
`// EXTRA_CFLAGS: -std=c2x` (for example to use C23 features).

Usage: python tools/run_c.py [filter]   (filter: substring of the test's path)
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_FLAGS = ["-std=c17", "-Wall", "-Wextra", "-Wpedantic", "-Werror", "-O1", "-g",
              "-fsanitize=address,undefined", "-fno-omit-frame-pointer", "-fno-sanitize-recover=all"]
SANITIZER_MARKERS = ("ERROR: AddressSanitizer", "runtime error:", "ERROR: LeakSanitizer")


def extra_flags(src: Path) -> list[str]:
    m = re.search(r"^//\s*EXTRA_CFLAGS:\s*(.+)$", src.read_text(encoding="utf-8"), flags=re.M)
    return m.group(1).split() if m else []


def compile_c(cc: str, sources: list[Path], exe: Path, flags: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([cc, *flags, "-o", str(exe), *map(str, sources), "-lm"], capture_output=True, text=True)


def main() -> int:
    filt = next((a for a in sys.argv[1:] if not a.startswith("-")), "")
    cc = os.environ.get("CC") or shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if not cc:
        print("no C compiler (cc/gcc/clang) found on PATH")
        return 1
    tests = sorted(p for p in ROOT.glob("**/*_test.c")
                   if "/site/" not in str(p) and "/docs/" not in str(p) and filt in str(p.relative_to(ROOT)))
    demos = sorted(p for p in ROOT.glob("**/*_demo.c")
                   if "/site/" not in str(p) and "/docs/" not in str(p) and filt in str(p.relative_to(ROOT)))
    failed = 0
    leaks = "detect_leaks=1:" if sys.platform.startswith("linux") else ""   # LeakSanitizer is Linux-only
    env = dict(os.environ, ASAN_OPTIONS=leaks + "abort_on_error=0", UBSAN_OPTIONS="print_stacktrace=1")
    for test in tests:
        d = test.parent
        others = sorted(p for p in d.glob("*.c") if not p.stem.endswith("_test") and not p.stem.endswith("_demo"))
        rel = test.relative_to(ROOT)
        flags = BASE_FLAGS + extra_flags(test)
        with tempfile.TemporaryDirectory() as tmp:
            exe = Path(tmp) / "test.out"
            c = compile_c(cc, [test, *others], exe, flags)
            if c.returncode != 0:
                failed += 1
                print(f"FAIL  {rel} (compile)\n{c.stderr[-3000:]}")
                continue
            try:
                r = subprocess.run([str(exe)], cwd=d, capture_output=True, text=True, timeout=120, env=env)
            except subprocess.TimeoutExpired:
                failed += 1
                print(f"FAIL  {rel} (timeout)")
                continue
            out = r.stdout + r.stderr
            ok = (r.returncode == 0 and "TEST PASSED" in out and "TEST FAILED" not in out
                  and not any(m in out for m in SANITIZER_MARKERS))
            print(f"{'PASS' if ok else 'FAIL'}  {rel}")
            if not ok:
                failed += 1
                print(out[-3000:])
    for demo in demos:
        rel = demo.relative_to(ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            c = compile_c(cc, [demo], Path(tmp) / "demo.out", BASE_FLAGS + extra_flags(demo))
        ok = c.returncode == 0
        print(f"{'BUILD' if ok else 'FAIL '}  {rel} (demo, compiled only)")
        if not ok:
            failed += 1
            print(c.stderr[-3000:])
    total = len(tests) + len(demos)
    print(f"\nc: {total - failed}/{total} programs passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
