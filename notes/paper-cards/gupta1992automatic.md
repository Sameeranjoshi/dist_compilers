# Demonstration of Automatic Data Partitioning Techniques for Parallelizing Compilers on Multicomputers
**Catalog id:** `gupta1992automatic`
**Citation:** Manish Gupta and Prithviraj Banerjee. "Demonstration of Automatic Data Partitioning Techniques for Parallelizing Compilers on Multicomputers." IEEE Transactions on Parallel and Distributed Systems, March 1992. Record used: running header and printed page numbers 1-30; no DOI printed.
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner. Full text read (34 PDF pages: 30 article pages plus tables and figures). The body text layer is complete, but ligatures such as "fi" and "ff" are dropped and some symbols are lost. Tables 1 and 2 are extracted; the CAG diagram and the performance plot (Figs. 3 and 4) are not. The text cites a Table 3 that does not appear in the PDF.
**Card status:** full-read

## Problem
Array distributions determine communication and load balance, and choosing them by hand is hard. The authors cite Mace for NP-completeness of optimal storage patterns, even for one- and two-dimensional arrays, and note that component alignment is NP-complete (Sec. 1). The aim is a strategy that chooses distributions for whole programs with statically analyzable regular computation (Sec. 1, 3).

## Input abstraction
Fortran-like programs whose references can be analyzed at compile time (Sec. 1, 7). Only arrays are partitioned; scalars and small arrays are replicated (Sec. 2). For each parallelizable loop the compiler records constraints: parallelization constraints on the left-hand-side array and communication constraints relating the two sides (Sec. 3). Loop bounds and branch probabilities are assumed known or user-supplied (Sec. 6, Sec. 7). Parafrase-2 found the parallel loops; other steps were done by hand (Sec. 6).

## Target
An abstract D-dimensional processor grid, with the analysis restricted to two dimensions (Sec. 2). Costs are estimated for a 16-processor Intel iPSC/2 hypercube (Sec. 6). Table 1 gives hypercube complexities for Transfer, Reduction and the two multicast primitives (p. 31).

## Data decomposition
Each array dimension maps to a grid dimension with a distribution function floor((i - offset) / block) mod N, which is contiguous or cyclic; a dimension can be sequentialized or replicated along a grid dimension (Sec. 2). Constraints choose contiguous or cyclic distribution and the relative block sizes (Sec. 5, step 3). Table 2 lists the outcomes, such as cyclic by rows for tred2 and cyclic by cyclic or 1 x 16 for dgefa depending on n (p. 31).

## Computation mapping
Owner-computes (Sec. 3). Parallelization constraints favour an even spread of the assigned elements, and cyclic distribution is favoured when the inner trip count depends on the outer index (Sec. 3, Example 1; Sec. 5). No computation partitioning beyond owner-computes is described.

## Communication generation
Communication is estimated, not generated. For each right-hand-side reference the compiler finds aligned dimension pairs, classifies subscripts as constant, index or variable, identifies the loops from which messages can be combined, and composes the cost terms (Sec. 4, steps 1-5). The tred2 code used for measurement was written by hand for the iPSC/2 (Sec. 6, TRED2).

## Compiler / runtime split
The strategy runs entirely at compile time. Constraints carry penalty or execution-time quality measures, and Sec. 5 resolves conflicts in five steps: component alignment through a component affinity graph (Li and Chen heuristic), sequentialization, contiguous or cyclic choice with block sizes, processor counts by evaluating the execution-time expression, and replication (Sec. 5).

## Evaluation
Five Fortran programs are analyzed: dgefa (Linpack), tred2 (Eispack), and trfd, mdg and flo52 (Perfect Club) (Sec. 6). Only tred2 is measured, in four layouts on an iPSC/2 for n = 256 and n = 512 (Fig. 4). The strategy's layout performs much better at n = 512, while column distribution is slightly better at n = 256 with fewer processors (Sec. 6). The other programs receive distribution decisions without timings (Table 2).

## Principal limitation
As the paper states it: the strategy gives no optimality guarantee because the problem is NP-hard; its quality measures rest on simplifying assumptions; and loop bounds and branch probabilities must be supplied, with profiling planned for the future (Sec. 7).
our observation: Only one of the five programs was measured; the other four are hand-simulated decisions (Sec. 6).

## Relationship to earlier / later work
- Component alignment follows the Li and Chen heuristic (ref. 15), and communication costing builds on their synthesis of explicit communication from reference patterns (ref. 14) (Sec. 1, 4, 5).
- Ramanujam and Sadayappan (ref. 18), Hudak and Abraham (ref. 11), Socha (ref. 21) and Balasundaram et al. (refs. 1, 2) are reviewed as restricted in applicability or as enumerative (Sec. 1, 4).
- Owner-computes is credited to Fortran D (ref. 9). Fortran D, SUPERB (ref. 22), Kali (ref. 13), DINO (ref. 20), Crystal (ref. 5) and Id Nouveau (ref. 19) are listed as parallelizing projects (Sec. 1, 3).
- The authors cite their own constraint-based paper (ref. 7) and communication-estimation report (ref. 8). The Transfer cost model is taken from Hsu and Banerjee (ref. 10) (Sec. 3, 4, 6).

## Sources used
| claim | section / page |
|---|---|
| NP-completeness; prior approaches | Sec. 1 |
| Distribution functions, sequentialization, replication | Sec. 2 |
| Constraint types and examples | Sec. 3 |
| Communication primitives and estimation steps | Sec. 4; Table 1 (p. 31) |
| Five-step strategy | Sec. 5 |
| Program study and layouts | Sec. 6; Table 2 (p. 31) |
| tred2 measurements | Sec. 6; Fig. 4 (PDF p. 34) |
| Limitations and future work | Sec. 7 |

## Open questions for the survey
- Do the constraint quality measures predict the measured tred2 ranking? At n = 256 the column layout won for small processor counts (Sec. 6), which the cost model does not reproduce.
- Replication is allowed only for arrays written once (Sec. 5, step 5). Do later partitioners in this set relax that restriction, and at what analysis cost?
- The strategy assumes two distributed grid dimensions (Sec. 2). How do later systems handle arrays with three or more distributed dimensions, which the authors set aside?
