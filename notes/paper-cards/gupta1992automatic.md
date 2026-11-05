# Demonstration of Automatic Data Partitioning Techniques for Parallelizing Compilers on Multicomputers
**Catalog id:** `gupta1992automatic`
**Citation:** Manish Gupta and Prithviraj Banerjee. "Demonstration of Automatic Data Partitioning Techniques for Parallelizing Compilers on Multicomputers." IEEE Transactions on Parallel and Distributed Systems, March 1992. Record used: running header and printed page numbers 1-30; no DOI printed.
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner. Full text read (34 PDF pages: 30 article pages plus tables and figures). The body text layer is complete, but ligatures such as "fi" and "ff" are dropped and some symbols are lost. Tables 1 and 2 are extracted; the CAG diagram and the performance plot (Figs. 3 and 4) are not. The text cites a Table 3 that does not appear in the PDF.
**Card status:** full-read

## Problem
Multicomputers are hard to program because data must be partitioned by hand, and the partitioning determines both communication and load balance (Sec. 1). The authors note that optimal storage patterns are NP-complete even for one- and two-dimensional arrays, citing Mace, and that component alignment is also NP-complete (Sec. 1). Earlier approaches were limited to single loop nests or required exhaustive enumeration of schemes (Sec. 1). The aim is a compiler strategy that chooses distributions for whole programs with regular, statically analyzable computation (Sec. 1, 3).

## Input abstraction
The inputs are Fortran-like programs whose references can be analyzed at compile time (Sec. 1, 7). Only arrays are partitioned; scalars and small arrays are replicated (Sec. 2). For each parallelizable loop the compiler records constraints: parallelization constraints on the left-hand-side array, and communication constraints relating the distributions of the arrays on the two sides (Sec. 3). Loop bounds and branch probabilities are assumed known or supplied by the user (Sec. 6, TRED2; Sec. 7). In the study, Parafrase-2 identified the parallel loops and the remaining steps were carried out by hand (Sec. 6, Methodology).

## Target
The abstract target is a D-dimensional grid of processors, with the analysis restricted to two grid dimensions (Sec. 2). Costs are estimated for the Intel iPSC/2 hypercube with 16 processors, using a Transfer cost fitted to message length and per-operation times for floating-point work (Sec. 6, Methodology). Table 1 gives hypercube complexities for Transfer, Reduction, OneToManyMulticast and ManyToManyMulticast (p. 31).

## Data decomposition
Each array dimension maps to one grid dimension and has its own distribution function of the form floor((i - offset) / block) mod N, which may be contiguous or cyclic, with a block size and an offset (Sec. 2). A dimension can be sequentialized (one processor along its grid dimension) or replicated along a grid dimension, written X (Sec. 2). Constraints decide between contiguous and cyclic distribution and set the relative block sizes of aligned dimensions (Sec. 5, step 3). Table 2 lists the resulting layouts: for tred2, cyclic by rows with sequential columns on 16 processors; for dgefa, cyclic by cyclic on 2 x 8 or 1 x 16 depending on n; and cyclic blocks of three for the 1029-element arrays in the Perfect programs (p. 31; Sec. 6).

## Computation mapping
The paper follows the owner-computes rule, under which the processor that owns the assigned element performs the computation (Sec. 3). Parallelization constraints push for an even spread of the assigned elements, and cyclic distribution is favoured when the inner loop trip count depends on the outer index, since contiguous distribution then causes load imbalance (Sec. 3, Example 1; Sec. 5). No computation-partitioning method beyond owner-computes is described.

## Communication generation
Communication is estimated, not generated. For each right-hand-side reference the compiler identifies aligned dimension pairs, classifies subscripts as constant, index or variable, determines the loops from which messages can be combined, and composes the communication terms for the statement (Sec. 4, steps 1-5). Each term is costed with one of the four primitives: Transfer, OneToManyMulticast, Reduction or ManyToManyMulticast (Sec. 4; Table 1). The parallel tred2 code used in the measurements was written by hand for the iPSC/2 (Sec. 6, TRED2).

## Compiler / runtime split
The whole strategy runs at compile time. Constraints carry quality measures expressed as penalties or as execution-time functions, and Sec. 5 resolves conflicts in five steps: component alignment through a component affinity graph and the Li and Chen heuristic; sequentialization of dimensions that need no parallelism; choice of contiguous or cyclic distribution and block sizes; choice of processor counts by evaluating the execution-time expression; and replication decisions (Sec. 5). The communication primitives are assumed to be supplied by the operating system or run-time library (Sec. 4).

## Evaluation
Five Fortran programs are analyzed: dgefa from Linpack, tred2 from Eispack, and trfd, mdg and flo52 from the Perfect Club (Sec. 6). Only tred2 is measured. Four versions run on the iPSC/2 for n = 256 and n = 512: the strategy's row-cyclic layout, a column-cyclic layout, a contiguous row layout, and a blocked grid layout (Sec. 6, Fig. 4). The authors report that the strategy's layout performs much better at n = 512, while column distribution is slightly better at n = 256 when fewer processors are used (Sec. 6). The other programs receive distribution decisions without timings (Sec. 6; Table 2).

## Principal limitation
As the paper states it: the strategy gives no optimality guarantee because the problem is NP-hard, the quality measures rest on simplifying assumptions, and loop bounds and branch probabilities must be supplied by the user, with profiling planned for the future (Sec. 7).
our observation: Only one of the five programs was measured; the other four distributions come from hand simulation of the strategy (Sec. 6).

## Relationship to earlier / later work
- The paper states that its component alignment step follows the Li and Chen heuristic (ref. 15), and that its communication costing builds on Li and Chen's synthesis of explicit communication from reference patterns (ref. 14) (Sec. 1, 4, 5).
- Earlier partitioning work by Ramanujam and Sadayappan (ref. 18), Hudak and Abraham (ref. 11), Socha (ref. 21) and Balasundaram et al. (refs. 1, 2) is reviewed as restricted in applicability or as requiring exhaustive enumeration (Sec. 1, 4).
- The owner-computes rule is credited to Fortran D (ref. 9). Fortran D, SUPERB (ref. 22), Kali (ref. 13), DINO (ref. 20), Crystal (ref. 5) and Id Nouveau (ref. 19) are listed as parallelizing compiler projects (Sec. 1, 3).
- The authors cite their own earlier constraint-based paper (ref. 7) and their compile-time communication estimation report (ref. 8) (Sec. 3, 4).
- The Transfer cost model is taken from Hsu and Banerjee (ref. 10) (Sec. 6).
- Data reorganization between program segments, interprocedural analysis and profiling are named as future work, not as later systems (Sec. 7).

## Sources used
| claim | section / page |
|---|---|
| NP-completeness; prior approaches | Sec. 1; pp. 1-4 |
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
