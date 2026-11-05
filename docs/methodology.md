# Survey Methodology

This is the reproducible literature-discovery and evidence protocol for the
survey.  Deviations must be recorded in `docs/discovery-log.md`.

## 1. Scope and inclusion criteria

See `docs/scope.md`.  The operational definition and the inclusion list there
are normative; this document covers *how* papers are found and verified.

## 2. Sources

Bibliographic sources, in order of preference for metadata:

1. DOI / official publisher page (ACM Digital Library, IEEE Xplore, Springer,
   Elsevier) via the Crossref API;
2. arXiv (API);
3. official author or institution PDF (university tech-report servers,
   author home pages);
4. official project page or documentation (OpenXLA, MLIR, Legion, Chapel ...);
5. trusted bibliographic indexes (DBLP, OpenAlex, Semantic Scholar) for
   cross-checking venue, year, and author lists.

Paywalls are never bypassed and restricted content is never scraped.  For a
paper whose full text is not accessible we record the metadata, set
`access_status: paywalled` or `abstract-only`, and do not infer detailed
contributions from the title; anything derived from the abstract is labelled
as such in the `evidence` list.

`scripts/fetch_metadata.py` queries Crossref, DBLP, and arXiv and prints JSON
for human review.  It never writes to the catalog directly.

## 3. Search queries

Initial query set (each run against ACM DL, IEEE Xplore, DBLP, arXiv, OpenAlex):

- "distributed memory compiler"
- "compiler distributed-memory multicomputer"
- "data distribution compiler"
- "data decomposition compiler"
- "communication generation compiler message passing"
- "automatic message passing code generation"
- "automatic MPI generation"
- "Fortran D compiler"
- "High Performance Fortran compiler"
- "global array distributed memory compiler"
- "owner computes compiler"
- "communication set generation"
- "array redistribution compiler"
- "inspector executor distributed memory"
- "irregular distributed array compiler"
- "polyhedral distributed memory compiler"
- "multi GPU compiler partitioning"
- "distributed tensor compiler"
- "SPMD partitioner compiler"
- "mesh sharding compiler"
- "distributed sparse tensor compiler"
- "MLIR distributed memory"
- "wafer scale compiler"
- "spatial accelerator distributed compiler"
- "communication cost model data distribution compiler"

Every query execution is logged in `docs/discovery-log.md` with date, source,
number of hits examined, and screening decisions.

## 4. Snowballing

For every anchor paper (initially: the seed corpus in `catalog/papers.yaml`):

1. **Backward** – read related-work and reference sections; add earlier works
   that introduced techniques, systems, or terminology.
2. **Forward** – find citing papers (Crossref `is-referenced-by`, OpenAlex,
   Semantic Scholar); prioritise works that extend, critique, evaluate, or
   revive the anchor's ideas.
3. **Lateral** – search by the same system, project, authors, or compiler
   family.
4. **Survey** – compare reference lists across surveys; papers cited by
   several independent surveys get high priority.
5. **Gap** – for each empty taxonomy cell (see `docs/taxonomy.md`), search
   specifically for that combination.

## 5. Screening levels

| level | meaning |
|-------|---------|
| `discovered` | metadata only |
| `screened` | abstract / introduction checked |
| `core` | clearly relevant to the taxonomy |
| `read` | enough of the paper read to summarise accurately |
| `verified` | metadata, categorization, and summary reviewed against the primary source |

A paper is not called a *survey* unless it is a survey or an invited overview.
For example, PeiZong Lee's "Techniques for Compiling Programs on Distributed
Memory Multicomputers" (1995) is a technique paper, not a survey, and is
catalogued as `paper_type: compiler-technique`.

## 6. Reading strategy

For most papers: abstract, introduction, system/model overview, related work,
conclusion.

The entire paper is read when it (a) introduced a major compiler/system,
(b) defines a taxonomy category, (c) supports a key historical claim,
(d) has experiments that are compared, or (e) supplies a mechanism central to
the synthesis.

## 7. Paper cards

Every `core` paper gets a card in `notes/paper-cards/<id>.md` with: full
citation; paper type; problem; input abstraction; target; data decomposition;
computation mapping; communication generation; compiler/runtime split;
evaluation; principal limitation; relationship to earlier/later work; exact
source sections/pages used.  Cards contain no long quotations and never a
copied abstract.

## 8. Verification

`verified: true` in the catalog means a human (or an agent run whose log is in
the discovery log) has checked, against the official page or an open copy:

- title, author list, year, venue, DOI or arXiv id;
- that the summary is original and consistent with the paper's own description;
- that every taxonomy tag can be justified from the evidence sections listed.

Metadata-only verification (Crossref/DBLP agree) is recorded as
`status: discovered` or `screened`, never `verified`.

## 9. Evidence labels in prose

The paper distinguishes three kinds of statements:

1. **source-supported fact** – cited to a primary paper, specification, or
   official documentation;
2. **survey taxonomy introduced by us** – flagged with "we categorize" /
   "we group";
3. **inference or synthesis** – flagged with "appears", "we observe",
   "we hypothesise", and listed in `docs/historical-claims.md` with the
   evidence currently available.

Conflicts between sources are recorded, not silently resolved.

## 10. Limitations of the methodology

- Full text of many 1988–2000 papers is paywalled; summaries of those rely on
  open author copies (Rice, ICASE, CSRD technical reports) where available and
  are otherwise marked `abstract-only`.
- Citation counts are not used as a relevance criterion because they penalise
  older work and non-ACM/IEEE venues.
- The "first survey" claim is not made until an explicit search for prior
  surveys has been completed and logged.
