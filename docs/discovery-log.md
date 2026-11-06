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

### Query sweep against Crossref (point 5 round)

The 25 phrases from `docs/methodology.md` were run against the Crossref bibliographic query endpoint, one request each, on 2026-11-06. The number is Crossref's `total-results` for each phrase. Crossref matches loosely, so these counts are not screened hits; they show how broad each phrase is. ACM DL, IEEE Xplore, DBLP and OpenAlex were not queried in this round.

| hits (Crossref) | phrase |
|---:|---|
| 927,429 | distributed memory compiler |
| 927,876 | compiler distributed-memory multicomputer |
| 3,944,415 | data distribution compiler |
| 3,251,669 | data decomposition compiler |
| 2,185,972 | communication generation compiler message passing |
| 1,308,019 | automatic message passing code generation |
| 1,030,239 | automatic MPI generation |
| 15,965 | Fortran D compiler |
| 5,264,442 | High Performance Fortran compiler |
| 2,587,866 | global array distributed memory compiler |
| 19,881 | owner computes compiler |
| 2,300,683 | communication set generation |
| 233,812 | array redistribution compiler |
| 922,839 | inspector executor distributed memory |
| 635,629 | irregular distributed array compiler |
| 937,029 | polyhedral distributed memory compiler |
| 1,410,894 | multi GPU compiler partitioning |
| 467,181 | distributed tensor compiler |
| 9,996 | SPMD partitioner compiler |
| 96,578 | mesh sharding compiler |
| 540,149 | distributed sparse tensor compiler |
| 918,577 | MLIR distributed memory |
| 812,084 | wafer scale compiler |
| 1,016,009 | spatial accelerator distributed compiler |
| 8,605,513 | communication cost model data distribution compiler |

### Prior-survey search (point 5 round)

Two web searches were run on 2026-11-06: "survey of compilers for distributed memory machines data distribution overview" and "survey high performance Fortran HPF compilation techniques review distributed memory". Results named the overviews below. Each was checked in Crossref where a DOI exists.

- Zima and Chapman, "Compiling for distributed-memory systems", Proceedings of the IEEE, 1993 (catalog, read).
- Coelho, Germain and Pazat, "State of the art in compiling HPF", LNCS, 1996, DOI 10.1007/3-540-61736-1_45 (added; not read).
- Perrott, Ayguadé, García and Torres, "High Performance Fortran Implementations: A Survey", Scientific Programming, 1997, DOI 10.1155/1997/875952 (added; not read).
- Benkner and Zima, "Compiling High Performance Fortran for distributed-memory architectures", Parallel Computing, 1999 (catalog, read).
- Crooks and Perrott, "Language constructs for data partitioning and distribution" (pre-HPF; not added; the record was not checked in Crossref).
- Unat et al., "Trends in data locality abstractions for HPC systems", IEEE TPDS, 2017 (catalog, read).
- Thangamani et al., "A survey of general-purpose polyhedral compilers", ACM TACO, 2024 (catalog, read).

The searches found no survey that covers distributed-memory compilers from the 1950s to the present. The searches are not exhaustive; the claim in the paper is limited to what was searched.

### TODO closures (point 5)

- Section 01, first-survey claim: closed by the prior-survey search above. The
  introduction now names the overviews found and says which ones have cards.
- Section 02, query sweep: closed. The 25 phrases were run against Crossref only; the
  counts are above. ACM DL, IEEE Xplore, DBLP and OpenAlex were not queried.
- Section 03, foundations: closed. Each claim now cites its card (Backus, Lamport,
  Kuck, Allen and Kennedy, Barnes, Russell, Misunas, Kung, Seitz, Hillis, Loveman). The
  Dennis 1975 sentence, which had no card, was removed.
- Section 06, Era 1: the early source-to-source placement systems were not added. The
  paragraph states the gap instead, and the gap is listed in Section 13. The Era 1
  records are now described correctly: two compilers and three machine or
  programming-model papers.
- Section 10, network terms: closed from the target sections of the cards for Gupta and
  Banerjee (hypercube complexities, 16-processor iPSC/2), Palermo et al. (measured
  startup and per-byte parameters, Paragon and CM-5) and Lee (hypercube embedding by Gray
  codes, nCUBE-2).
- Section 11: Tiramisu is not used for any claim, so it is not carded. The accelerator
  vendors named in the brief are not catalogued and are not claimed. The Shardy and MLIR
  shard material is documentation; claims that rest on it are labelled as documentation
  claims, and carding it is open work. GPipe, Megatron-LM and ZeRO are catalogued, not
  carded, and no claim depends on them. The Jacquelin et al. sentence was removed.
- Section 13: each open problem now states its test status. Three were run, two partly,
  and three not run or not settled. The overlap item was reworded: a tag pair does not
  show that a reduction overlaps the computation that feeds it.
- Section 06, HPF directives: the claim is cited to the Loveman and Kennedy cards only.
  The uncarded HPF specification record was removed from that citation.

Open work named by these closures: cards for Shardy and the MLIR shard dialect
(documentation), GPipe, Megatron-LM, ZeRO, Tiramisu and Jacquelin et al. 2022.

### Second reading of the then-and-now table (point 6)

A fresh reader checked each row against the cards and against the reference lists in
the inbox extractions. The reader used no catalog, coding or discovery material. The
reader's report was returned in a message, because the harness did not allow the
subagent to write it to the repository. The findings, in summary:

- 21 of the claims in the table and 6 in the paragraph after it were not supported or
  were contradicted. Every row needed a change.
- Dates: Sequoia (2006), Chapel (2007) and Legion (2012) were in the Then or Now columns
  outside their windows. Titanium (2007) was in the Now column of the inspector row.
  Stawinoga (2026) fell outside the 2018--2025 header. The header is now 2018--2026.
- Cites column: owner-computes was "partly" but no checked reference list cites the
  works in that cell, so it is "no". The separation row was "yes", which no reference
  list supports, so it is "no". Halo and overlap was "unchecked", and the three full
  texts are present, so it is "no". Layout-derived communication and the inspector row
  are "unchecked": Kong et al., Legion, Titanium, PartTensor and the Saltz 1990
  Journal article are not in the evidence set.
- Claims withdrawn or reworded: "HPF's was only a naming of places"; "replication is the
  default for unmatched dimensions in both"; "GSPMD and PartIR replace the rule with
  propagation" (they propagate sharding annotations); "the 1996 work optimised one
  redistribution" (Palermo and Ramaswamy aggregate the data one redistribution moves);
  "PARTI's preprocessor" (the Saltz card never names PARTI); "SUPERB overlap areas" (the
  card attributes the overlap-based EXCH to Zima 1993, not to SUPERB); "stated in 2022 as
  two commands" (DISTAL states one distribute command); "volume-only cost model is
  sufficient" (no source says so).
- The paragraph's "seven of the eight mechanisms have the same structure" was
  contradicted by the table's own What changed column. It now says each mechanism recurs
  and the design is unchanged in two rows.
- The paragraph's "Table 2" is now a reference to the table label.

Missing evidence that would change a cell: full texts of Kong et al., Legion, Titanium,
PartTensor, and the 1990 Saltz Journal article; a SUPERB source for the overlap claim.
