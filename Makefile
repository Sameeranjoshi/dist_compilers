# Build automation for the distributed-memory compiler survey.
#
#   make validate   -- schema / taxonomy / bibliography checks
#   make figures    -- regenerate SVG (README) and PDF (LaTeX) figures
#   make tables     -- regenerate LaTeX + Markdown tables from the catalog
#   make readme     -- regenerate the generated blocks of README.md
#   make paper      -- build paper/main.pdf with latexmk
#   make all        -- validate, figures, tables, readme, paper
#   make check-stale-- fail if generated files differ from the catalog (CI)
#   make clean      -- remove LaTeX build products

PYTHON ?= python3
LATEXMK ?= latexmk

GENERATED_FIGS = assets/timeline.svg assets/taxonomy.svg assets/compiler-architecture.svg \
                 assets/decomposition-taxonomy.svg assets/rediscovery-map.svg assets/citation-map.svg

.PHONY: all validate figures tables readme paper clean check-stale deps

all: validate figures tables readme paper

deps:
	$(PYTHON) -m pip install -r requirements.txt

validate:
	$(PYTHON) scripts/validate_catalog.py
	$(PYTHON) scripts/validate_bib.py

figures:
	$(PYTHON) scripts/render_timeline.py
	$(PYTHON) scripts/render_taxonomy.py
	$(PYTHON) scripts/render_architecture.py
	$(PYTHON) scripts/render_decomposition.py
	$(PYTHON) scripts/render_rediscovery_map.py
	$(PYTHON) scripts/render_citation_graph.py

tables:
	$(PYTHON) scripts/generate_insights.py
	$(PYTHON) scripts/generate_tables.py
	$(PYTHON) scripts/second_coding_agreement.py
	$(PYTHON) scripts/coding_sensitivity.py

readme:
	$(PYTHON) scripts/generate_readme.py

paper: tables
	cd paper && $(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error main.tex

check-stale: tables readme
	@git diff --exit-code -- README.md paper/tables docs/tables || \
	  (echo "ERROR: generated files are stale; run 'make tables readme' and commit" && exit 1)

clean:
	cd paper && $(LATEXMK) -C main.tex || true
	rm -f paper/sections/*.aux
