# Contributing

This repository is an evidence base first and a manuscript second.  The rules
below exist so that every claim in the paper stays traceable.

## Adding a paper

1. **Find verified metadata.**  Run

   ```bash
   python scripts/fetch_metadata.py --title "Exact title" --author Lastname --year 1993
   ```

   and compare the Crossref / arXiv hit against the official publisher page.
   Do not trust the script's first hit blindly.

2. **Create the entry.**

   ```bash
   python scripts/add_paper.py --id lastname1993keyword --doi 10.xxxx/yyyy
   ```

   creates a skeleton in `catalog/papers.yaml` and a matching BibTeX entry in
   `bibliography/references.bib`.  Fill in the taxonomy fields only for axes
   you can support with the `evidence` list.

3. **Write an original summary.**  One to three technical sentences.  Never
   paste the abstract.  Add a one-sentence `why_read` if the paper belongs in a
   README reading list.

4. **Set `status` honestly.**  `discovered` → `screened` → `core` → `read` →
   `verified`.  `verified: true` requires that you checked the primary source
   and recorded `verified_date`.

5. **Log the discovery.**  Add a line to `docs/discovery-log.md` saying how the
   paper was found (query, snowball from which paper) and why it was included.

6. **Validate and regenerate.**

   ```bash
   make validate
   make tables readme
   ```

   CI fails if `README.md` or `paper/tables/` are stale.

## Adding a system

Systems live in `catalog/systems.yaml` and group papers, versions, runtime,
targets, and artifact status.  Add a system when at least one `core` paper
describes it.  Write a note under `notes/systems/<id>.md` for anything that
needs more than a line.

## Paper cards

`notes/paper-cards/<id>.md` follows the template in
`notes/paper-cards/_TEMPLATE.md`.  Cards cite the exact sections or pages used
and contain no long quotations.

## What not to do

- Do not add PDFs of papers.
- Do not link to shadow libraries or unofficial mirrors.
- Do not call a technique paper a survey.
- Do not assert that system A influenced system B without a citation that
  says so; put inferences in `notes` prefixed with "inferred:".
- Do not mark `verified` from title or abstract alone.
- Do not hand-edit generated blocks in `README.md` or `paper/tables/`.

## Style

- Catalog ids: `firstauthorlastname` + `year` + one keyword, lower case
  (e.g. `hiranandani1992compiling`).  The same id is the BibTeX key.
- Taxonomy values are kebab-case ids from `catalog/taxonomy.yaml`.
- Calibrated language in prose: "appears", "we categorize", "the paper
  reports".
