# The Paradigm Compiler for Distributed-Memory Multicomputers
**Catalog id:** `banerjee1995paradigm`
**Citation:** P. Banerjee, J. A. Chandy, M. Gupta, E. W. Hodges IV, J. G. Holm, A. Lain, D. J. Palermo, S. Ramaswamy, and E. Su. "The Paradigm Compiler for Distributed-Memory Multicomputers." Computer (IEEE), October 1995. Record used: PDF of the article, ISSN 0018-9162 from the copyright line; no DOI printed.
**Paper type:** full-system
**Access:** PDF supplied by the repository owner. Full text read (11 PDF pages). The text layer is present and readable but has dropped drop-cap letters and garbled figure labels, and figure contents are not in it. Page references are PDF page numbers, since the text layer carries no printed page numbers.
**Card status:** full-read

## Problem
Distributed-memory machines such as the Intel Paragon, IBM SP-1/SP-2 and Thinking Machines CM-5 are scalable and cost-effective, but without a global address space the programmer must distribute computation and data and manage communication by hand (PDF p. 1). The paper presents Paradigm as a framework that automates this for sequential Fortran 77 or HPF programs. Its stated aims are automatic data distribution, communication optimization, support for irregular computations, simultaneous use of functional and data parallelism, and multithreaded code that hides communication latency (PDF p. 1-2).

## Input abstraction
The input is a sequential Fortran 77 or HPF program (PDF p. 2). Parafrase-2 parses it into an intermediate representation, builds flow, dependence and call graphs, and applies transformations such as constant propagation and induction variable substitution (PDF p. 2). Figure 1 contrasts a serial Jacobi program with a message-passing version that a skilled programmer might write, and the authors use it to motivate automation (PDF p. 1-2).

## Target
The generic library interface maps abstract communication operations onto CMMD, Parasoft Express, MPI, Intel NX, PVM and PICL (PDF p. 4). Architecture-specific costs are supplied as parameters for each machine, and a linear transfer model (overhead plus rate times message size) is measured empirically (PDF p. 4, 6). Experiments use a 64-processor CM-5 (Figs. 6 and 12), a 32-processor IBM SP-1 (Fig. 8), and the Paragon and CM-5 (Fig. 10) (PDF p. 6-10).

## Data decomposition
The partitioning pass chooses, in order, interdimensional array alignment, a blocked or cyclic distribution for each array dimension (refined to block-cyclic when needed), and the mesh configuration, with dimensions that are not parallelized collapsed onto one processor (PDF p. 4-5). The mesh shape is chosen by evaluating a cost expression for each feasible configuration (PDF p. 5). For regular code, partitioned data and iteration sets are represented by processor tagged descriptors, with symbolic linear inequalities and Fourier-Motzkin projection used for the harder cases (PDF p. 5).

## Computation mapping
For regular code the owner-computes rule is applied, and loop partitioning is done statically, so ownership is not tested at run time (PDF p. 5). Functional parallelism is handled by building a macro dataflow graph of data-parallel tasks, allocating processors to tasks by convex programming on posynomial cost functions, and scheduling them with list scheduling (PDF p. 8-9). Multithreaded execution maps several virtual processors onto each physical processor (PDF p. 9). Coarse-grain pipelining of recurrences chooses a block granularity from an analytic pipeline model (PDF p. 6-7).

## Communication generation
Redundant messages are removed by coalescing, element messages are vectorized to the outermost loop that dependences allow, and messages with the same source and destination are aggregated (PDF p. 6; Figs. 5 and 6). For irregular code, the PILAR library describes small regular blocks with intervals and irregular patterns by enumeration (PDF p. 8). Inspector and executor code is generated with embedded calls to PILAR routines (PDF p. 8).

## Compiler / runtime split
Regular computations are handled entirely at compile time, including the derivation of loop bounds (PDF p. 5). Irregular computations are split into a preprocessing inspector, whose schedule can be reused across steps, and an executor (PDF p. 7-8). The multithreading transformation converts blocking receives in while loops into a message-driven form, and control returns to the multithreading runtime at each receive (PDF p. 9-10).

## Evaluation
Figure 6 (64-processor CM-5) compares coalescing, aggregation and vectorization on ADI and hydrodynamics kernels, with time split into busy and overhead components. Figure 8 compares CHAOS/Parti with PILAR, under enumeration and interval representations, when redistributing the edges of the Rotor grid on a 32-processor SP-1. Figure 10 gives SPMD versus MPMD speedups for Strassen multiplication and a spectral CFD code, with a gain of two or three at larger processor counts. Figure 12 compares SPMD with message-driven versions of four kernels on a 64-processor CM-5. The message-driven versions win in all cases except Impl-1D, and the best thread count varies by application (PDF p. 6-10). All results are plots; the text gives no numeric table.

## Principal limitation
As the paper states it: integrating all of the capabilities into one framework is still in progress (PDF p. 2), and the partitioning pass performs only interdimensional alignment (PDF p. 4).
our observation: The evaluation uses kernels and selected applications shown only as plots, so no end-to-end compilation of a full application is reported.

## Relationship to earlier / later work
- Parafrase-2 is the analysis platform (PDF p. 2). Chaos/Parti is described as a state-of-the-art irregular runtime that PILAR is intended to improve on (PDF p. 8).
- The data partitioning pass is attributed to the authors' earlier work (ref. 5, PDF p. 4), and the communication optimizations to their compiler optimization work (ref. 6, PDF p. 2).
- Functional parallelism rests on the authors' earlier convex programming approach (ref. 8, PDF p. 8).
- The PTD representation is cited as ref. 10 (PDF p. 5).
- Fortran D, SUPERB and HPF are named as related efforts (PDF p. 1). The text cites SUPERB as ref. 2, but the reference list gives ref. 2 as Chapman, Mehrotra and Zima on Vienna Fortran (PDF p. 1, 11).

## Sources used
| claim | section / page |
|---|---|
| Input is Fortran 77 or HPF; Parafrase-2 analysis | Compiler framework, Program analysis; PDF p. 2 |
| Library interfaces; cost parameters | Generic library interface; PDF p. 4 |
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
- The message-driven gains depend on thread count and application (PDF p. 10). Does any later system give a compile-time rule for choosing thread count?
- How much of the aggregation gain in Fig. 6 survives on machines other than the 64-processor CM-5?
