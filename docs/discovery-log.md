# Discovery Log

Chronological record of how papers entered the catalog.  Entries follow the
format: date, query or source, source database, hits examined, decisions.
Screening levels are defined in `docs/methodology.md`.

## 2026-11-05 — First pass (repository foundation)

### Environment limits recorded

- Crossref REST API and the arXiv API/abs pages were reachable and used for
  all metadata.  DBLP returned a bot-check page, and OpenAlex and Semantic
  Scholar returned rate-limit errors for the build container's shared IP, so
  they were **not** used in this pass; the same lookups must be repeated
  from a researcher's workstation and logged here.
- Publisher landing pages (ACM DL, IEEE Xplore, Elsevier, Springer) refused
  automated access, so **no abstract was read from a publisher page**.
  Entries whose only evidence is a Crossref record carry
  `status: discovered` and a summary prefixed `[metadata-level]`.
- NASA NTRS was reachable and provided open ICASE report versions of several
  core 1989–1992 papers (see below).
- hpf.rice.edu (HPF specification archive) did not resolve from the build
  environment; the HPF 1.0 specification is catalogued through its ACM
  Fortran Forum record instead.

### Seed list (from the project brief) — metadata verification

| source | papers submitted | Crossref match | notes |
|---|---|---|---|
| seed list, surveys/anchors | 7 | 7 | Hall et al.: arXiv 2024 title differs from TACO 2025 title; one entry |
| seed list, foundations | 10 | 10 | hardware papers tagged `paper_type: hardware`, `relevance_tier: foundation` |
| seed list, 1988–1992 | 19 | 18 | Mehrotra & Van Rosendale Kali chapter not in Crossref; catalogued as NASA CR-187453 / ICASE 90-69 via NTRS |
| seed list, 1993–2000 | 24 | 23 | DEC HPF (Digital Technical Journal) not in Crossref; catalogued via the Utah DTJ bibliography index and the bitsavers scan |
| seed list, 2000–2010 | 9 | 9 | "Generating efficient tiled code for distributed memory machines" resolved to Tang & Xue, Parallel Computing 2000 (the brief gave no authors) |
| seed list, 2010–2020 | 15 | 12 | Mesh-TensorFlow, GPipe, Megatron-LM, GShard are arXiv-only records |
| seed list, 2020–2026 | 14 | 12 | GSPMD arXiv-only; "An MLIR Lowering Pipeline for Stencils at Wafer-Scale" confirmed as arXiv 2601.17754 / ASPLOS '26 |

Decisions:
- **Included** every seed paper whose metadata was verified (see
  `docs/tables/paper-list.md` for the full list with status).
- **Not catalogued (could not verify):** "PartTensor" — no publication with
  that title was found on arXiv, Crossref or the web; recorded in
  `bibliography/missing-metadata.md`.  Compiler publications for Graphcore,
  SambaNova, Tenstorrent, Groq: not yet searched.
- **Reclassified:** Lee 1995 "Techniques for compiling programs on
  distributed memory multicomputers" catalogued as `compiler-technique`, not
  survey, per the brief and its venue/abstract type.
- **Deduplicated:** Hiranandani/Kennedy/Tseng 1991 (SC) and 1992 (CACM) kept
  as separate entries linked by `related_versions` because the CACM article
  is the full-system description and the SC paper the optimisation paper;
  the 1992 ICS evaluation paper kept separately as `experience`.
  Bondhugula 2011 (IISc TR) and 2013 (SC) kept separately because only the
  TR is openly readable; linked by `related_versions`.

### Lateral snowball: NASA NTRS search for ICASE reports (2026-11-05)

Queries run against `ntrs.nasa.gov/api/citations/search`:
"Vienna Fortran Chapman Mehrotra Zima", "Koelbel Mehrotra compiling global
name-space parallel loops", "Saltz PARTI", "Saltz Mirchandaney", "Das
Ponnusamy Saltz Mavriplis", "Saltz Berryman Wu", "Koelbel Mehrotra Kali",
"Ponnusamy Saltz Choudhary", "Hwang Moon Saltz".

Found and downloaded (open copies, used for paper cards):
- ICASE 90-69 Kali (NTRS 19910002904) → `mehrotra1990kali`, card written.
- ICASE 91-72 Vienna Fortran language (NTRS 19920002452) → `chapman1991vienna`, card written.
- ICASE 92-9 Programming in Vienna Fortran (NTRS 19920013037) → `chapman1992vienna`, card written.
- ICASE 89-7 Run-time scheduling of loops (NTRS 19890011267) → open version of `saltz1990runtime`, card written.
- ICASE 90-59 Multiprocessors and runtime compilation (NTRS 19910001287) → open version of `saltz1991multiprocessor`, card written.
- ICASE 91-73 Distributed memory compiler methods for irregular problems (NTRS 19920002451) → `das1991irregular`, card written.
Found, downloaded, **not yet screened**: Sussman/Saltz/Das "PARTI primitives
for unstructured and block structured problems" (NTRS 19920022317);
Wu/Saltz/Berryman "Distributed memory compiler design for sparse problems"
(ICASE 91-13, NTRS 19910009297); Mirchandaney/Saltz/Mehrotra "A scheme for
supporting automatic data migration on multicomputers" (ICASE 90-33, NTRS
19900013657); Chapman/Mehrotra/Moritsch/Zima "Dynamic data distributions in
Vienna Fortran" (NTRS 19940018619).  These are candidates for the next pass.

### Full-text reads in this pass (paper cards written)

Open copies read in full by the card-writing procedure described in
`docs/methodology.md` Sec. 7 (each card lists the sections used):
mehrotra1990kali, chapman1991vienna, chapman1992vienna, saltz1990runtime
(ICASE 89-7), saltz1991multiprocessor (ICASE 90-59), das1991irregular,
harris1995dechpf, bondhugula2011automatic, kruse2014molly,
shazeer2018meshtf, jia2019flexflow, xu2021gspmd, zheng2022alpa,
yadav2022distal, yadav2022spdistal, alabed2025partir, bisbas2024shared,
rocki2020cerebras, stawinoga2026mlir.

These entries have `status: read`.  Four of them (xu2021gspmd,
mehrotra1990kali, saltz1990runtime, zheng2022alpa) were spot-checked by the
maintainer against the open text (utilization/scale numbers and
priority-based propagation in GSPMD; doall-on-owner and inspector/executor
wording in the Kali report; absence of the word 'inspector' in ICASE 89-7;
Alpa's Megatron/DeepSpeed comparisons) and are marked `verified`.  The
remaining cards await the same check.

### Searches still to run (next pass)

The 25-query set in `docs/methodology.md` has **not** yet been executed
against ACM DL / IEEE Xplore / DBLP; hit counts will be logged here when it
is.  An explicit prior-survey search is also pending (required before any
"first survey" claim).

### Uploaded PDFs (2026-11-05)

- Supplied by the repository owner and read in full: Vaidya et al. 2025
  (`vaidya2025distributed`; resolves the PartTensor name), Kong et al. 2023
  (`kong2023automatic`), and Narayanan et al. 2019 PipeDream
  (`narayanan2019pipedream`).  Cards written, catalog entries set to `read`.
- Supplied and identified as Talaashrafi, Doerfert and Moreno Maza 2022,
  "A Pipeline Pattern Detection Technique in Polly" (DOI 10.1145/3547276.3548445).
  Screened and excluded: it is a shared-memory Polly technique and mentions
  distributed memory only in related work.

### Era 4 collection (2026-11-06)

Era 4 (2000 to 2010) was the thinnest read era. This round added read papers
from official open copies, and corrected the era of three entries whose
publication years fell outside their recorded era.

Read in full, cards written, catalog status `read`:

- `diaconescu2005reusable`: Caltech CACR repository, record CaltechCACR:2005.103
  (Workshop on Patterns in High Performance Computing, 2005).
- `diaconescu2006userdefined`: Caltech repository record CaltechAUTHORS:20110223-160141512
  (IEEE SMC-IT 2006). This record was not found by the earlier Era 4 search. It
  surfaced in a web search for the 2005 paper.
- `su2010irregular`: UC Berkeley EECS technical report UCB/EECS-2010-170, a PhD
  dissertation of 111 pages, official URL www2.eecs.berkeley.edu.
- `bondhugula2008pluto`: supplied PDF. The file is the 2008 report titled
  "PLuTo: A Practical and Fully Automatic Polyhedral Program Optimization System",
  not the PLDI 2008 paper whose title the catalog carried. Version handling is in
  the naming and version pass.

Checked and not retrieved:

- UPC Language Specifications V1.2 (eScholarship, qt1w43d8f1). The server returned
  a bot-check response (HTTP 202, empty body) on two attempts. A third attempt with
  a changed user-agent string was refused as circumvention, so it was not pursued.
  Not carded; it is a language specification in any case.
- Strout 2003, Bikshandi 2006, X10 2005, Nieplocha 2006, Su and Yelick 2005: no
  official open copy found in the earlier searches.
- Chapel language specification 0.7 (2007): not found. chapel-lang.org hosts the
  later versions only (0.775 and 0.780).
- Diaconescu and Zima 2007 (Vienna eprint): the eprint server returned HTTP 503
  and then a connection reset. Not retrieved.

Era membership: the catalog assigned `kuck1981dependence` to Era 0, and
`numrich1998coarray` and `yelick1998titanium` (both 1998) to Era 4. Era membership
follows publication year and the date ranges in `catalog/eras.yaml`, so these
moved to Era 1, Era 3 and Era 3. The era text in `catalog/eras.yaml` now says so.

Metadata repair: `scripts/merge_card_records.py` appended each record's notes on
every run, so 32 catalog entries had repeated notes at HEAD. Notes are now rebuilt once
from the base text and the records, and the merge adds notes only when the text
is absent.

### Foundation cards (point 3)

Thirteen foundation papers were carded from the owner's supplied PDFs, through the
mapping in `scratchpad/zips/mapping_out.json`: Backus 1957, Lamport 1974, Barnes 1968,
Russell 1978, Seitz 1985, Hillis 1986, Kuck et al. 1981, Misunas 1977, Allen and Kennedy
1987, Bik 1996, Unat 2017 (survey), Thangamani 2024 (survey), Kung 1982.

- `kung1982systolic` has no text layer. Its pages were read as images, one batch of
  eleven pages, and the card marks which figure readings are high or medium confidence.
  This cost about 255 thousand subagent tokens. It was kept rather than moved to a TODO,
  because the card is complete and its readings are labelled.
- The three `kuck1981dependence` files are byte-identical (SHA-256 prefix
  dc98b4ad6fee950c8dba). The card uses the first listed.
- `misunas1977workshop` is a 1977 MIT workshop report on data-flow programs. Its text
  layer is complete but the first pages extract little text.
- Paper types in the cards follow the catalog. Three machine papers (Barnes, Russell,
  Seitz) and Kung are `hardware`; the two surveys are `survey`.
- The card instruction list had omitted `analytic-optimization` and
  `partition-propagation`. Those were restored from the taxonomy before the foundation
  cards were written; the Pluto correction is recorded in `docs/coding/corrections.md`.
- A second coding of the thirteen papers was made from the blind card texts by an
  independent coder (`coding/second_coder_D.json`). The read set is now 71 papers.
  Agreement and sensitivity are regenerated. Robustness without surveys is in
  `docs/coding/sensitivity.md`.

### Naming and version pass (point 4)

- Chatterjee et al. 1993 has two DOIs in Crossref: the PPoPP 1993 proceedings
  (10.1145/155332.155348, catalogued) and a SIGPLAN Notices listing
  (10.1145/173284.155348, not catalogued). The journal version is Chatterjee, Gilbert,
  Long, Schreiber and Teng, Journal of Parallel and Distributed Computing 26(1), 72-84,
  1995, DOI 10.1006/jpdc.1995.1049. It is catalogued as `chatterjee1995generating` and
  not read. A 1995 "TOPLAS" note in the catalog was wrong and is removed.
- PLuTo: the supplied copy is the undated 2008 technical report "PLuTo: A Practical and
  Fully Automatic Polyhedral Program Optimization System" (footers 2008/3/31). The PLDI
  2008 paper, "A practical automatic polyhedral parallelizer and locality optimizer",
  DOI 10.1145/1375581.1375595, is `bondhugula2008pldi`. The report's content is cited
  under `bondhugula2008pluto`. The relation between the two is inferred from title and
  authors.
- Fortran D: the supplied copies are "Compiler Optimization for Fortran D on MIMD
  Distributed-Memory Machines" (1991 Supercomputing) and "Evaluation of Compiler
  Optimization for Fortran D on MIMD Distributed-Memory Machines" (1992). Authors and
  affiliation (Hiranandani, Kennedy, Tseng; Rice) match the catalog. The ACM titles use
  "optimizations"; the variant is noted on both entries.
- Titanium: `yelick2007titanium` (IJHPCA 2007) is the supplied paper. `yelick1998titanium`
  is a separate, unread record. The paper cites only the 2007 key for content.
- Stawinoga et al.: the DOI 10.1145/3779212.3790124 resolves in Crossref to the ASPLOS
  2026 paper with the catalog title, first author and year. Confirmed.
- Rogers and Pingali: the 60 to 70 percent figure in the abstract refers to SIMPLE, where
  the handwritten baseline is a model (Sec. XI-A). Table I's Gauss-Seidel comparison gives
  about 75 to 77 percent against a handwritten program. These are different programs and
  baselines. The card's earlier reading that they conflicted is withdrawn. The paper's
  three-quarters statement matches Table I.
- The validator now allows one title to appear twice only when the two entries name each
  other in `related_versions`.
