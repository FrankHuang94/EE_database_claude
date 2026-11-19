"""Unit tests for the answer-key parser and tolerance logic in tools/eeverify.py."""
import math
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eeverify import Verifier, load_answer_key, parse_value  # noqa: E402


@pytest.mark.parametrize("raw,value,halfulp", [
    ("2.20", 2.20, 0.005),
    ("−0.5", -0.5, 0.05),
    ("6.32e-3", 6.32e-3, 0.005e-3),
    ("6.32 × 10⁻³", 6.32e-3, 0.005e-3),
    ("6.32×10^-3", 6.32e-3, 0.005e-3),
    ("16", 16.0, 0.5),
])
def test_parse_real(raw, value, halfulp):
    p = parse_value(raw)
    assert p.kind == "real"
    assert math.isclose(p.parts[0].value, value)
    assert math.isclose(p.parts[0].halfulp, halfulp)


def test_parse_rect_and_polar():
    p = parse_value("3 − j4.5")
    assert p.kind == "rect" and p.parts[0].value == 3 and p.parts[1].value == -4.5
    p = parse_value("−j2")
    assert p.kind == "rect" and p.parts[0].value == 0 and p.parts[1].value == -2
    assert p.parts[0].halfulp == p.parts[1].halfulp == 0.5  # implied real part at the same precision
    p = parse_value("2.236∠−63.43°")
    assert p.kind == "polar" and p.parts[0].value == 2.236 and p.parts[1].value == -63.43


def test_verifier_rounding_and_coverage(tmp_path, capsys):
    md = tmp_path / "k.md"
    md.write_text("text\n\n<!-- answer-key -->\n| ID | Quantity | Value | Unit |\n|---|---|---|---|\n"
                  "| a | x | 1.43 | V |\n| b | z | 5∠53.13° | Ω |\n| c | w | 3 + j4 | |\n\nmore\n", encoding="utf-8")
    assert set(load_answer_key(md)) == {"a", "b", "c"}
    v = Verifier.from_files("t", md)
    assert v.check("a", 12 * math.exp(-100 / 47))      # 1.4294 rounds to 1.43
    assert not v.check("a", 1.4361)                     # would round to 1.44
    assert v.check("b", complex(3, 4))
    assert v.check("c", complex(3, 4))
    assert v.check("c", complex(3.4, 3.6))              # within ±0.5 on each component
    with pytest.raises(SystemExit):                      # one failure recorded above -> exit 1
        v.finish()


def test_unchecked_entry_fails(tmp_path):
    md = tmp_path / "k.md"
    md.write_text("<!-- answer-key -->\n| ID | Quantity | Value | Unit |\n|---|---|---|---|\n| a | x | 1.0 | |\n",
                  encoding="utf-8")
    v = Verifier.from_files("t", md)
    with pytest.raises(SystemExit):
        v.finish()


def test_run_python_blocks(tmp_path):
    from eeverify import run_python_blocks
    md = tmp_path / "doc.md"
    md.write_text(
        "Intro\n\n```python\nx = 2 + 3\nprint(x)\n```\n\n```text\n5\n```\n\n"
        "```python\n# not run\nraise SystemExit\n```\n\n```python\nprint(x * 2)\n```\n\n```text\n11\n```\n",
        encoding="utf-8")
    v = Verifier("t", {})
    ns = run_python_blocks(v, md)
    assert ns["x"] == 5
    assert v.passes == 1 and len(v.failures) == 1      # first block matches; third prints 10, not 11


@pytest.mark.skipif(not (shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")), reason="no C compiler")
def test_run_c_blocks(tmp_path):
    from eeverify import run_c_blocks
    md = tmp_path / "doc.md"
    md.write_text(
        "```c\n// file: twice.c\nint twice(int x) { return 2 * x; }\n```\n\n"
        "```c\n// with: twice.c\n#include <stdio.h>\nint twice(int x);\nint main(void) { printf(\"%d\\n\", twice(21)); return 0; }\n```\n\n"
        "```text\n42\n```\n\n"
        "```c\n// expect: sanitizer\n#include <limits.h>\n#include <stdio.h>\n"
        "int main(void) { volatile int big = INT_MAX; printf(\"%d\\n\", big + 1); return 0; }\n```\n\n"
        "```text\nsigned integer overflow\n```\n\n"
        "```c\n// expect: error\nint main(void) { return undeclared; }\n```\n\n"
        "```c\n// expect: warning -Wparentheses\nint f(int x) { return x & 1 == 0; }\n```\n\n"
        "```c\n// expect: warning -Wsign-compare\nint g(int x) { return x & 1 == 0; }\n```\n\n"
        "```c\n#include <stdio.h>\nint main(void) { printf(\"7\\n\"); return 0; }\n```\n\n```text\n8\n```\n",
        encoding="utf-8")
    v = Verifier("t", {})
    run_c_blocks(v, md)
    # passes: file, linked block, sanitizer, error, named warning; failures: wrong warning named, 7 not 8
    assert v.passes == 5 and len(v.failures) == 2
