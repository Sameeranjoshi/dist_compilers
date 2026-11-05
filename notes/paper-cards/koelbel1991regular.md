# Compile-Time Generation of Regular Communications Patterns
**Catalog id:** `koelbel1991regular`
**Citation:** Charles Koelbel. "Compile-Time Generation of Regular Communications Patterns." ACM proceedings (venue not printed in the text layer), 1991, pp. 101-110. Record used: ACM copyright line 0-89791-459-7/91/0101.
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner. Full text read; the text layer is complete but some equation symbols are garbled. Rendered pages 6 and 9 to check the efficiency statements. Figures were not interpreted beyond their captions.
**Card status:** full-read

## Problem
Explicit message passing is hard to program. The paper gives formulas for the communication and iteration sets of forall loops over block- or cyclic-distributed arrays, so that a compiler can generate the messages (Sec. 1, Sec. 2.3).

## Input abstraction
The source language is Kali, whose forall loops carry an on clause naming the processor that runs each iteration (Fig. 1, Sec. 2.1). Subscripts are linear in one loop index, f(i) = c0*i + c1 (Sec. 3.1, Sec. 3.2), and the main results assume c0 > 0 (Sec. 3.1). Nested loops and multidimensional arrays are handled per dimension when the subscripts are affine and use distinct loop indices (Sec. 3.3).

## Target
The target is a nonshared-memory, message-passing machine, with generated C code run on iPSC/860 and iPSC/2 systems (Sec. 2.1, Sec. 3.1, Sec. 3.2).

## Data decomposition
Block and cyclic distributions define each processor's local set in closed form (Eq. 16 for block, Eq. 28 for cyclic; Sec. 2.2, Sec. 3.1, Sec. 3.2).

## Computation mapping
The on clause defines exec(p), the iterations run on processor p, as the inverse of the on-clause subscript, so the owner of New_A[i] runs iteration i (Def. 2, Eq. 5, Sec. 2.2). Each processor's iterations split into local_iter(p), which touch only local data, and nonlocal_iter(p) (Def. 4, Theorem 2, Sec. 2.4).

## Communication generation
Each processor sends, runs its local iterations, receives, and then runs its nonlocal iterations (Fig. 2, Sec. 2.1). Theorem 1 gives the receive set from q as the local data of q intersected with f(exec(p)) (Sec. 2.3). Theorems 3 and 4 give closed-form send and receive sets for block distributions, and Theorems 5 and 6 do the same for cyclic distributions (Sec. 3.1, Sec. 3.2). Local iterations overlap with message exchange (Fig. 2, Sec. 3.1).

## Compiler / runtime split
The closed forms are derived at compile time for linear subscripts. The paper states that when the subscript function is unknown until run time the analysis must be dynamic, and it does not treat that case (Sec. 2.5). The generated code evaluates the per-processor bounds at run time (Fig. 4, Fig. 7).

## Evaluation
Cyclic reduction on iPSC/860, N = 10000 to 40000, up to 32 processors (Fig. 5, Fig. 8). For the block version the paper reports parallel efficiency of 50 to 70 percent (Sec. 3.1). For the cyclic version it reports efficiency of 82 percent or better, an average overhead of 2.2 percent against a hand-coded version, and a largest difference of 4.5 percent (Sec. 3.2, p. 109). The author estimates that the block version is within 50 percent of hand coding on 32 processors, and points to the cyclic comparison as support (Sec. 3.1). The locality checks in the nonlocal loop cost about 2 percent on two processors and up to 40 percent on 32 (Sec. 3.1).

## Principal limitation
The paper concludes that the method "produces very efficient code in the cases where it can be applied" (Sec. 5). Within that scope the analysis is restricted to forall loops, which the author calls stricter than necessary (Sec. 3.3).
our observation: The evidence is one kernel on one compiler, and the hand-coded baseline was written by the same author.

## Relationship to earlier / later work
- Kali [8] (Koelbel, Mehrotra and Van Rosendale) supplies the forall and on-clause model (Sec. 2.1).
- Balasundaram, Fox, Kennedy and Kremer [2] show how to choose the communication loop level from reference locality; the Kali compiler did not implement this (Sec. 3.3).
- The thesis [7] covers negative and zero coefficients (Sec. 3.3).
- Other groups (Sec. 4) generally work from the innermost loops outward and do not give explicit communication-set formulas.
- No later work is discussed.

## Sources used
| claim | section / page |
|---|---|
| Kali forall with on clause; linear subscripts; block and cyclic | Sec. 2.1, Fig. 1, p. 101; Sec. 3.1-3.2, pp. 103-108 |
| exec(p) as inverse of on clause; local and nonlocal iterations | Def. 2, Eq. 5, p. 102; Def. 4, Thm. 2, p. 103 |
| Receive set equals local(q) intersected with f(exec(p)) | Thm. 1, p. 103 |
| Block closed forms (Thms. 3-4); cyclic closed forms (Thms. 5-6) | Sec. 3.1, pp. 104-105; Sec. 3.2, pp. 106-108 |
| Run-time analysis excluded | Sec. 2.5, p. 103 |
| Efficiency 50-70 percent (block); locality check cost 2-40 percent | Sec. 3.1, pp. 105-106 |
| 82 percent efficiency; 2.2 percent average overhead; 4.5 percent maximum | Sec. 3.2, p. 109, Fig. 8 |
| "very efficient code" conclusion; forall restriction | Sec. 5, p. 110; Sec. 3.3, p. 109 |
| Related work and its limits | Sec. 4, p. 110 |

## Open questions for the survey
- Do the closed forms extend to negative and zero coefficients and to run-time analysis, which the paper defers to the thesis and to other papers?
- How much of the 2 to 40 percent locality-check overhead remains once the compiler bug is fixed, and how does it scale on other machines?
- Do the cyclic and block results carry over to block-cyclic distributions, which the paper does not treat?
