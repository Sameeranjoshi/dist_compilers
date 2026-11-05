# Advanced Compilation Techniques in the PARADIGM Compiler for Distributed-Memory Multicomputers
**Catalog id:** `su1995advanced`
**Citation:** Ernesto Su, Antonio Lain, Shankar Ramaswamy, Daniel J. Palermo, Eugene W. Hodges IV, and Prithviraj Banerjee. "Advanced Compilation Techniques in the PARADIGM Compiler for Distributed-Memory Multicomputers." Proc. ICS '95, Barcelona, Spain, 1995, pp. 424-433. Record used: printed page numbers and ACM copyright line (0-89791-726-6/95/0007); no DOI printed.
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner. Full text read (10 PDF pages, printed pp. 424-433). The text layer is present and mostly readable, but Mathematica names and some figure labels are garbled, and the plotted speedup values are not in the text layer.
**Card status:** full-read

## Problem
PARADIGM's PTD-based implementation handled symbolic sizes, affine bounds and a variable processor count, but only block distributions (p. 424). This paper extends it to cyclic and block-cyclic distributions within one symbolic framework (p. 424), using Mathematica for the symbolic algebra instead of new hand-written code (p. 425).

## Input abstraction
A sequential FORTRAN 77 or HPF program (p. 424). Subscripts and loop bounds are affine in the enclosing indices, and each dimension may be block, cyclic, block-cyclic, replicated or sequentialized (p. 427). Distributions come from the automatic partitioner or from HPF directives (p. 427).

## Target
A distributed-memory multicomputer. The processor count need not be fixed at compile time (p. 427). Experiments use an IBM SP-2 with MPIF (p. 431). Global references are not translated into local address spaces, so arrays are not scaled down as processors increase (p. 427).

## Data decomposition
Each dimension may be block, cyclic, block-cyclic written cyclic(b), replicated along a processor dimension, or collapsed (p. 427). Block-cyclic is modelled as a b-by-N array on each processor, with block and cyclic as special cases (p. 428-429). The same expressions extend to multidimensional arrays on multidimensional meshes (p. 428).

## Computation mapping
Owner-computes (p. 427). Loop bounds reduction uses Fourier-Motzkin elimination over the loop inequalities and the left-hand-side data inequalities, so each processor's loops visit only its ACCESS set and no run-time ownership test is needed (p. 427-428). With several left-hand-side references, a conservative union of their ACCESS sets sets the bounds, and each assignment is masked (p. 429).

## Communication generation
For each right-hand-side reference, the COMM set is computed by elimination from the loop, left-hand-side and right-hand-side inequalities (p. 429-430). One polytope drives both pack/send and receive/unpack, placed at the outermost loop that dependences allow, so messages are vectorized (p. 429; Fig. 5). A further elimination derives the sender or receiver processor set, which narrows the processor loops for shift patterns (p. 431).

## Compiler / runtime split
The symbolic work runs at compile time in a Mathematica process linked by MathLink (p. 425). The generated SPMD code evaluates its bounds at run time from processor coordinates and the processor count (p. 428-430). Communication generation is not fully integrated, so the communication code that Mathematica produced was inserted by hand; the run-time system is MPI (p. 431).

## Evaluation
LU on 1024 by 1024 arrays (column- and row-cyclic) and POTENG from the MDG Perfect benchmark (cyclic and cyclic(3)) are run on an IBM SP-2 (p. 431). Speedups for LU (Fig. 6) and for POTENG at N = 3000 (Fig. 7) are plotted up to 32 processors (p. 431-432). For LU, the broadcast pattern must be recognized before MPI collectives can replace point-to-point messages, and that recognition is not yet implemented (p. 431).

## Principal limitation
As the paper states it: communication generation is not fully integrated with the compiler (p. 431); global references are not translated into local address spaces (p. 427); and the LU broadcast is not detected automatically (p. 431).
our observation: The results cover two programs on one machine, shown only as plots, with communication code for both inserted by hand.

## Relationship to earlier / later work
- The earlier PARADIGM implementation used PTDs, cited as ref. 22 (p. 424, 427). Later PTD extensions handled purely cyclic distributions (p. 424).
- Fourier-Motzkin elimination follows Banerjee's algorithm (ref. 6, p. 426). Communication generation is described as basically similar to Ancourt's work (ref. 4, p. 429), and redundant-access elimination builds on Gallivan et al. (ref. 13) as refined by Ancourt (p. 426).
- Loop bounds reduction is attributed to Hiranandani, Kennedy and Tseng (ref. 16, p. 427). Automatic data distribution comes from the authors' PARADIGM work (ref. 14, p. 427).
- SUIF (ref. 2), Fortran 90D (ref. 10), Fortran D (ref. 16) and SUPERB (cited as ref. 11) are named as related systems (p. 424). Reference 11 in the list is Chapman, Mehrotra and Zima on Vienna Fortran, so the SUPERB citation does not match the reference list (p. 432).

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
- Did later PARADIGM work remove the hand insertion of communication code and the unscaled local arrays described here, and when? Compare banerjee1995paradigm and palermo1996dynamic.
- Does the broadcast recognition that the LU result calls for appear in later systems in this set, and at what stage (compile time or inspector)?
- How much overhead does delegating the symbolic algebra to Mathematica add across programs? The paper reports only that compilation time was not a major problem (p. 425).
