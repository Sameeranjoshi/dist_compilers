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
