# Advanced Compilation Techniques in the PARADIGM Compiler for Distributed-Memory Multicomputers
**Catalog id:** `su1995advanced`
**Citation:** Ernesto Su, Antonio Lain, Shankar Ramaswamy, Daniel J. Palermo, Eugene W. Hodges IV, and Prithviraj Banerjee. "Advanced Compilation Techniques in the PARADIGM Compiler for Distributed-Memory Multicomputers." Proc. ICS '95, Barcelona, Spain, 1995, pp. 424-433. Record used: printed page numbers and ACM copyright line (0-89791-726-6/95/0007); no DOI printed.
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner. Full text read (10 PDF pages, printed pp. 424-433). The text layer is present and mostly readable, but Mathematica names and some figure labels are garbled, and the plotted speedup values are not in the text layer.
**Card status:** full-read

## Problem
PARADIGM's earlier implementation, built on Processor Tagged Descriptors (PTDs), handled symbolic array sizes, affine loop bounds and subscripts, and a variable number of processors, but only block distributions (p. 424). The paper extends the compiler to block, cyclic and block-cyclic distributions within one symbolic framework (p. 424). The authors argue that the added symbolic power should come from an existing package, Mathematica, rather than from new hand-written code (p. 425).

## Input abstraction
The input is a sequential FORTRAN 77 or HPF program (p. 424). Loop nests contain array references whose subscripts and loop bounds are affine in the enclosing indices, and each array dimension may be block, cyclic, block-cyclic, replicated or sequentialized (p. 427). Distributions come either from PARADIGM's automatic partitioner or from HPF directives (p. 427). Symbolic coefficients with unknown signs lead to multiversion code (p. 426, footnote 1).

## Target
The target is a distributed-memory multicomputer. The processor count need not be fixed at compile time, so the generated program can run on an arbitrarily sized system (p. 427). Experiments run on an IBM SP-2 using MPIF (p. 431). Global references are not translated into local address spaces, so arrays are not scaled down as more processors are used (p. 427).

## Data decomposition
Each dimension may be block, cyclic or block-cyclic, written cyclic(b), replicated along a processor dimension, or collapsed onto one processor (p. 427). Block-cyclic is modelled as a b-by-N array on each processor, and block and cyclic are special cases (p. 428-429). The same expressions extend to multi-dimensional arrays on multi-dimensional processor meshes (p. 428).

## Computation mapping
Loops are partitioned by the owner-computes rule (p. 427). Loop bounds reduction uses Fourier-Motzkin elimination over the loop inequalities and the data inequalities of the left-hand-side reference, yielding bounds that visit only the processor's ACCESS set, so no run-time ownership test is needed (p. 427-428). When several left-hand-side references exist, a conservative union of their ACCESS sets sets the bounds, and each assignment is masked by its own set (p. 429).

## Communication generation
For each right-hand-side reference, the COMM set of iterations that need remote data is computed by Fourier-Motzkin elimination from the loop inequalities, the left-hand-side data inequalities and the right-hand-side data inequalities (p. 429-430). The same polytope drives the pack/send and receive/unpack loops, which are placed at the outermost loop that dependence analysis allows, so element messages are vectorized (p. 429; Fig. 5, p. 430). The sending or receiving processor set can be derived with one extra elimination, which narrows the processor loops for shift-like patterns (p. 431). Ancourt's method for removing redundant transfers is described, but the paper says the compiler does not yet use it (p. 426-427).

## Compiler / runtime split
The symbolic work happens at compile time in a Mathematica process that communicates with the compiler through MathLink, using UNIX pipes locally and sockets remotely (p. 425). The generated SPMD code computes its bounds at run time from the processor coordinates and the processor count (p. 428-430). Communication generation is not fully integrated, so the communication code produced by Mathematica was added to the parallel program by hand (p. 431). The run-time system is MPI (p. 431).

## Evaluation
Two programs were compiled: LU factorization on 1024 by 1024 arrays with column-cyclic and row-cyclic layouts, and POTENG from the MDG Perfect benchmark with cyclic and cyclic(3) distributions (p. 431). Speedups for LU (Fig. 6) and for POTENG at N = 3000 (Fig. 7) are plotted up to 32 processors on the IBM SP-2 (p. 431-432). For LU, the authors note that the broadcast pattern must be recognized before MPI collectives can replace point-to-point messages, and that this recognition is not yet implemented (p. 431). The authors also state that compilation time has not been a major problem in their experience (p. 425).

## Principal limitation
As the paper states it: communication generation is not yet fully integrated with the rest of the compiler (p. 431), global references are not translated into local address spaces (p. 427), and the broadcast structure of LU is not detected automatically (p. 431).
our observation: The results cover two programs on one machine, shown only as plots, and the communication code for both was inserted by hand.

## Relationship to earlier / later work
- The earlier PARADIGM implementation used Processor Tagged Descriptors, cited as ref. 22 (p. 424, 427). Later PTD extensions handled purely cyclic distributions (p. 424).
- Fourier-Motzkin elimination follows Banerjee's algorithm with added symbolic simplification (ref. 6, p. 426). The communication approach is described as basically similar to Ancourt's (ref. 4, p. 429), and the redundant-access method builds on Gallivan et al. (ref. 13) as refined by Ancourt (ref. 4) (p. 426).
- Loop bounds reduction is attributed to Hiranandani, Kennedy and Tseng (ref. 16, p. 427). Automatic data distribution comes from the authors' PARADIGM work (ref. 14, p. 427).
- The introduction names Fortran D (ref. 16), Fortran 90D (ref. 10), SUIF (ref. 2) and SUPERB (cited as ref. 11) as related systems (p. 424). Reference 11 in the list is Chapman, Mehrotra and Zima on Vienna Fortran, so the SUPERB citation does not match the reference list (p. 432).
- The paper points to ref. 5 for the planned integration of all PARADIGM features (p. 424). The PILAR irregular runtime (ref. 18) is named as the target for inspector code generated from Mathematica (p. 426).

## Sources used
| claim | section / page |
|---|---|
| Earlier PTD implementation, block distributions only | Abstract, Sec. 1; p. 424 |
| Mathematica interface and conversion routines | Sec. 2.1; p. 425-426 |
| Fourier-Motzkin, unimodular transforms, redundant access | Sec. 2.2-2.3; p. 426-427 |
| Block-cyclic model and ACCESS sets | Sec. 3.1; p. 427-429 |
| COMM sets and pack/unpack code | Sec. 3.2; p. 429-431; Figs. 4-5 |
| Hand insertion of communication code; broadcast issue | Sec. 4; p. 431 |
| LU and POTENG results | Sec. 4; p. 431-432; Figs. 6-7 |

## Open questions for the survey
- Did later PARADIGM work remove the hand insertion of communication code and the unscaled local arrays described here, and when? Compare with banerjee1995paradigm and palermo1996dynamic.
- Does the broadcast recognition that the LU result calls for appear in later systems in this set, and at what stage (compile time or inspector)?
- How much overhead does delegating the symbolic algebra to Mathematica add across programs? The paper reports only that compilation time was not a major problem (p. 425).
