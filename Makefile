# Self-Taught BSEE — local checks (the same ones CI runs).
# Usage: make check | make verify | make spice | make hdl | make notebooks | make docs | make figures | make site

PY ?= python

.PHONY: check docs verify spice hdl notebooks generated figures site

check: generated docs verify spice hdl notebooks
	@echo "All checks passed."

generated:
	$(PY) tools/build_curriculum.py --check
	$(PY) tools/build_glossary.py --check
	$(PY) tools/progress_stats.py --check

docs:
	$(PY) tools/check_links.py
	$(PY) tools/check_structure.py
	npx --yes markdownlint-cli2@0.13.0

verify:
	$(PY) -m pytest -q tools/tests
	$(PY) tools/run_verify.py

spice:
	$(PY) tools/run_spice.py

hdl:
	$(PY) tools/run_hdl.py

notebooks:
	$(PY) tools/run_notebooks.py

# Regenerate every committed figure from its script.
figures:
	for f in assets/figures/src/fig_*.py; do $(PY) $$f || exit 1; done

# Regenerate all generated Markdown (curriculum, course READMEs, glossary, stats).
regen:
	$(PY) tools/build_curriculum.py
	$(PY) tools/build_glossary.py
	$(PY) tools/progress_stats.py

site:
	mkdocs serve
