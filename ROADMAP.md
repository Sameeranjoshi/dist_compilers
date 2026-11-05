# Roadmap

Status of the project against the milestones in the original brief.

| milestone | state | notes |
|-----------|-------|-------|
| M1 Repository foundation | done (first pass) | structure, schema, taxonomy, validators, LaTeX skeleton, Makefile, CI |
| M2 Verified seed corpus | in progress | see `make validate` output and the status counts in README |
| M3 Mental map (figures, reading paths) | done (first pass) | timeline, architecture, taxonomy, decomposition, rediscovery map; citation map awaits evidence |
| M4 Historical anchor paper cards | in progress | cards exist for the anchors listed in `notes/paper-cards/`; several are still abstract-level |
| M5 Paper draft | skeleton + partial prose | introduction, methodology, architecture, taxonomy have prose; era sections are outlines with TODOs |

## Next research tasks (ordered)

1. Obtain and read open author copies of the Rice Fortran D reports and the
   ICASE Kali/PARTI reports to upgrade their cards from abstract-level to
   `read`/`verified`.
2. Run the full query set of `docs/methodology.md` against ACM DL and IEEE
   Xplore and log hit counts in `docs/discovery-log.md`.
3. Forward-snowball from Zima & Chapman 1993 and Benkner & Zima 1999 to fill
   the HPF-production-compiler gap (PGHPF, xlhpf, ADAPTOR, VFC).
4. Explicit prior-survey search (needed before any "first survey" claim).
5. Verify wafer-scale and spatial compiler publications (Cerebras SDK/CSL
   documentation, "MLIR lowering pipeline for stencils at wafer-scale")
   and add only entries with confirmed publication details.
6. Build the citation/influence map once `predecessors`/`successors` edges
   have source citations for at least 30 papers.

## Long-term

- 25–35 IEEE two-column pages.
- Public catalog and figures as supplementary artifacts.
- Community contributions through pull requests validated by CI.
