# Tools

| Script | Purpose |
|---|---|
| [build_curriculum.py](build_curriculum.py) | Generates CURRICULUM.md, the generated blocks of README.md, STUDY_PLAN.md and every course README, and stub files for planned chapters, from [data/curriculum.yml](data/curriculum.yml). `--check` fails if anything is stale. |
| [build_glossary.py](build_glossary.py) | Generates reference/glossary.md from reference/glossary.yml |
| [progress_stats.py](progress_stats.py) | Updates the statistics block in PROGRESS.md |
| [eeverify.py](eeverify.py) | Library for verify scripts: parses answer-key tables and checks each published value at its published precision |
| [run_verify.py](run_verify.py) | Runs every `verify/` script |
| [run_spice.py](run_spice.py) | Runs every ngspice netlist with `* EXPECT` lines and compares against published answers |
| [run_hdl.py](run_hdl.py) | Compiles and runs every `*_tb.v` testbench with Icarus Verilog; lints designs with Verilator |
| [run_notebooks.py](run_notebooks.py) | Executes every notebook top to bottom |
| [check_links.py](check_links.py) | Checks every relative link and anchor in the Markdown |
| [check_structure.py](check_structure.py) | Enforces the chapter template, problem/solution consistency and flashcard format |
| [plotstyle.py](plotstyle.py) | Shared Matplotlib style and `save()` helper for figures |
| [smoke/](smoke/) | Toolchain smoke tests (RC netlist, half-adder testbench) |

## The answer-key convention

Every number published in a chapter's worked examples, a solutions file or an exam appears in an answer-key table:

```markdown
<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 07-02.1a | time constant τ | 47.0 | ms |
| 07-02.5b | current at t = 0⁺ | 3.00 | mA |
```

The course's verify script recomputes each value independently and calls `v.check("Ex 07-02.1a", tau_ms)`. The check passes only if the published value is the correctly rounded computed value; the precision is inferred from the digits shown. Values may be real (`2.20`, `6.32e-3`), rectangular complex (`3 + j4`) or polar (`5∠53.13°`).
