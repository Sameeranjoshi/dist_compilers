# The Paradigm Compiler for Distributed-Memory Multicomputers
**Catalog id:** `banerjee1995paradigm`
**Citation:** P. Banerjee, J. A. Chandy, M. Gupta, E. W. Hodges IV, J. G. Holm, A. Lain, D. J. Palermo, S. Ramaswamy, and E. Su. "The Paradigm Compiler for Distributed-Memory Multicomputers." Computer (IEEE), October 1995. Record used: PDF of the article, ISSN 0018-9162 from the copyright line; no DOI printed.
**Paper type:** full-system
**Access:** PDF supplied by the repository owner. Full text read (11 PDF pages). The text layer is present and readable but has dropped drop-cap letters and garbled figure labels, and figure contents are not in it. Page references are PDF page numbers, since the text layer has no printed page numbers.
**Card status:** full-read

## Problem
Distributed-memory multicomputers such as the Paragon, SP-1/SP-2 and CM-5 are scalable, but without a global address space the programmer must distribute data and computation and manage communication by hand (PDF p. 1). Paradigm is presented as a framework that automates this for sequential Fortran 77 or HPF programs, covering data distribution, communication optimization, irregular computations, functional parallelism and multithreading (PDF p. 1-2).

## Input abstraction
Sequential Fortran 77 or HPF (PDF p. 2). Parafrase-2 builds flow, dependence and call graphs and applies transformations such as constant propagation (PDF p. 2). Figure 1 contrasts a serial Jacobi program with the message-passing code a skilled programmer might write (PDF p. 1-2).

## Target
A generic library interface targets CMMD, Parasoft Express, MPI, Intel NX, PVM and PICL (PDF p. 4). A linear transfer model (overhead plus rate times size) is measured per machine (PDF p. 4, 6). Experiments use a 64-processor CM-5, a 32-processor SP-1, and the Paragon and CM-5 (PDF p. 6-10).

## Data decomposition
The partitioning pass chooses interdimensional alignment, then a blocked or cyclic distribution per array dimension (refined to block-cyclic when needed), then the mesh shape, collapsing dimensions that are not parallelized (PDF p. 4-5). The mesh shape comes from evaluating a cost expression per configuration (PDF p. 5). Regular partitioned sets are represented by processor tagged descriptors, with Fourier-Motzkin projection over linear inequalities for harder cases (PDF p. 5).

## Computation mapping
Owner-computes, with loop partitioning done statically (PDF p. 5). Functional parallelism uses a macro dataflow graph: processors are allocated to data-parallel tasks by convex programming and the tasks are list-scheduled (PDF p. 8-9). Multithreading maps several virtual processors onto each physical processor (PDF p. 9). Coarse-grain pipelining picks a block granularity from an analytic model (PDF p. 6-7).

## Communication generation
Coalescing removes redundant messages, vectorization lifts element messages to the outermost loop that dependences allow, and aggregation merges messages with the same endpoints (PDF p. 6; Figs. 5-6). For irregular code, PILAR describes small regular blocks with intervals and other patterns by enumeration, and inspector and executor code calls PILAR routines (PDF p. 8).

## Compiler / runtime split
Regular code is handled entirely at compile time (PDF p. 5). Irregular code is split into a preprocessing inspector, whose schedule can be reused across steps, and an executor (PDF p. 7-8). The multithreading transformation turns blocking receives inside while loops into message-driven code and returns control to the runtime at each receive (PDF p. 9-10).

## Evaluation
Figure 6 (64-processor CM-5) shows overhead falling as coalescing, aggregation and vectorization are added. Figure 8 compares CHAOS/Parti and PILAR on Rotor edge redistribution (32-processor SP-1). Figure 10 reports MPMD over SPMD speedups that are two to three times larger at higher processor counts, for Strassen and a spectral CFD code. Figure 12 shows message-driven versions beating SPMD on four kernels except Impl-1D, with the best thread count depending on the application (PDF p. 6-10).

## Principal limitation
As the paper states it: integrating all capabilities into one framework is still in progress (PDF p. 2), and the partitioning pass performs only interdimensional alignment (PDF p. 4).
our observation: Results are kernels and selected applications shown as plots; no full application is compiled end to end.

## Relationship to earlier / later work
- Parafrase-2 is the analysis platform (PDF p. 2). PILAR is presented as an improvement on Chaos/Parti (PDF p. 8).
- Data partitioning relies on the authors' earlier work (ref. 5, PDF p. 4), communication optimization on ref. 6 (PDF p. 2), and functional parallelism on ref. 8 (PDF p. 8).
- Fortran D, SUPERB and HPF are named as related efforts (PDF p. 1). The text cites SUPERB as ref. 2, but the reference list gives ref. 2 as Chapman, Mehrotra and Zima on Vienna Fortran (PDF p. 1, 11).

## Sources used
| claim | section / page |
|---|---|
| Input is Fortran 77 or HPF; Parafrase-2 analysis | Compiler framework, Program analysis; PDF p. 2 |
| Library interfaces; cost parameters | Generic library interface; PDF p. 4, 6 |
| Alignment, distribution and mesh passes | Automatic data partitioning; PDF p. 4-5 |
| PTDs and Fourier-Motzkin projection | Regular computations; PDF p. 5 |
| Coalescing, vectorization, aggregation | Communication optimizations; PDF p. 6; Figs. 5-6 |
| Coarse-grain pipelining | PDF p. 6-7 |
| Irregular computation, PILAR, Chaos/Parti | Irregular computations; PDF p. 7-8; Fig. 8 |
| Functional parallelism, MDG allocation | PDF p. 8-9; Figs. 9-10 |
| Multithreading and message-driven transform | PDF p. 9-10; Figs. 11-12 |
| Stated limitations | PDF p. 2, 4 |

## Open questions for the survey
- Which of the four capability areas (partitioning, communication optimization, irregular runtime, multithreaded execution) reappear in the later Paradigm papers in this set, such as su1995advanced and palermo1996dynamic?
- The message-driven gains depend on thread count and application (PDF p. 10). Does any later system give a compile-time rule for choosing the thread count?
- How much of the aggregation gain in Fig. 6 survives on machines other than the 64-processor CM-5?
