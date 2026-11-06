# Handoff: state of the survey and next tasks

Repository: https://github.com/Sameeranjoshi/dist_compilers (branch `main`).
Read first: `README.md`, `docs/methodology.md`, `docs/scope.md`, `docs/taxonomy.md`.

## Where things stand (commit 878080a)

- **Catalog** `catalog/papers.yaml`: 108 papers, 28 systems. `make validate` passes with 0 errors.
  - 71 papers have full text read (status `read` or `verified`). Four are `verified`: Xu 2021 (GSPMD), Zheng 2022 (Alpa), Kennedy-era Mehrotra 1990 (Kali), Saltz 1990 (runtime).
  - 37 are `screened` or `discovered`, i.e. bibliographic records only.
  - Every read paper has an independent second coding in `coding/second_coder_*.json` (A and B for the first 54, C for the four Era 4 papers added in the Era 4 round).
- **Paper cards** `notes/paper-cards/*.md` (about 60) with structured records in `notes/paper-cards/_records/*.json`. Records are merged into the catalog with `scripts/merge_card_records.py`.
- **Supplied PDFs** are not in the repository. `docs/supplied-papers.md` maps each file to its catalog id by SHA-256. The 58 files came from the owner's zips; 54 distinct papers.
- **Paper** `paper/main.tex` (18 pages, IEEEtran, builds with `latexmk`). Structure:
  - 01 introduction; 02 methodology; 03 foundations; 04 common architecture; 05 taxonomy (refined decision-procedure axis).
  - 06 history: six eras, each told in five parts (machines and problem, central idea, design space, what the era learned, what remained).
  - 07 to 11: mechanism sections (decomposition, communication, runtime, performance, modern ML and accelerators), each placing systems on the taxonomy.
  - 12 synthesis: then-and-now table (`tab:thennow`), counted patterns, HPF four causes applied to today, eight generalizations (`tab:generalizations`).
  - 13 open problems; 14 conclusion.
- **Generated outputs**: `paper/tables/*.tex` and `docs/tables/*.md` from `scripts/generate_tables.py` and `scripts/generate_insights.py`. Figures from `scripts/render_*.py`. README blocks from `scripts/generate_readme.py`.
- **TODO markers in the paper**: 11, each marking a claim that needs a card or a close reading.

## Known problems to fix (in priority order)

1. **Single-coder tags.** Every tag was assigned by one coder, so the counts behind G1 to G8 are not yet findings. Second independent coding of `data_decomposition`, `computation_mapping`, `communication_generation`, `compiler_runtime_boundary` and `optimization_objectives` for the 54 read papers is the precondition for calling any count a result.
2. **Era 4 (2000 to 2010) has 12 read papers** after the Era 4 round (Diaconescu 2005 and 2006, Su 2010, Pluto 2008 added). Still the thinnest era. Not retrieved from official open sources: UPC Language Specifications 1.2 (eScholarship returned a bot-check page), Strout 2003, Bikshandi 2006, X10 2005, Nieplocha 2006, Su and Yelick 2005, Diaconescu and Zima 2007. Log in `docs/discovery-log.md`.
3. **Foundations are read (done in the point 3 round).** Thirteen foundation papers have cards and second codings: Backus, Lamport, Barnes, Russell, Seitz, Hillis, Kuck, Misunas, Allen and Kennedy, Bik, Unat (survey), Thangamani (survey) and Kung. See `docs/discovery-log.md`.
4. **Kung 1982 was read from page images** (no text layer). The card is complete and its figure readings carry confidence labels; it cost about 255 thousand subagent tokens.
5. **Naming and version conflicts are resolved** (see `docs/discovery-log.md`, naming and version pass). The Chatterjee journal version and the PLuTo report and PLDI versions are catalogued as related entries. The Fortran D title variants and the Rogers SIMPLE reading are recorded.

6. **Unread items the paper depends on.** These are the 11 TODOs. Examples:
   - Vienna Fortran INDIRECT: the report says run-time techniques are needed but describes none. Read the VFCS paper on INDIRECT before using it as a counterexample to G1.
   - Jacquelin et al. 2022: the machine and results are not confirmed.
   - ZeRO (`rajbhandari2020zero`), Tiramisu (`baghdadi2019tiramisu`), Shardy and MLIR shard documentation: cards pending.
   - Gerndt 1990 and Chen 1988 (Crystal): what the performance-optimisation approach actually measures.
   - Kennedy 2007: confirm the attribution of HPF's decline by reading the full text.
7. **Then-and-now table needs a second reader.** Each row compares two cards. The "cites older line?" column was checked by one reader against cards, not reference lists. Check each citation claim against the newer paper's reference list.
8. **Stawinoga 2026 DOI** `10.1145/3779212.3790124` resolves in Crossref to the ASPLOS 2026 paper with the catalog title. Confirmed.
9. **Accelerator vendor compilers** (Graphcore, SambaNova, Tenstorrent, Groq) are named in the brief but not catalogued. Search only for primary publications or official documentation.
10. **Outdated file.** `docs/historical-claims.md` predates the restructure. Its hypotheses H1 to H11 are superseded by Table `tab:generalizations`. Replace it or mark it superseded.

## How to rebuild everything

```bash
pip install -r requirements.txt
make validate          # schema, taxonomy, bibliography
python3 scripts/merge_card_records.py   # after adding records
make tables readme
make figures
make paper             # latexmk; needs TeX Live with IEEEtran
```

## Rules for anyone continuing

- Never state a paper's content from its title. Write a card first, from the PDF text, with section references. Mark unread claims `\todo{}`.
- Do not add a tag without a section reference in the card's evidence list.
- Do not use the words "first", "first survey", or any pattern claim as a finding until its count is in a generated table and has a second coding.
- Do not commit PDFs. Only checksums go in `docs/supplied-papers.md`.
- Commit messages end with the attribution lines the session specifies.
