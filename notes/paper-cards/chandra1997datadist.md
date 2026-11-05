# Data Distribution Support on Distributed Shared Memory Multiprocessors
**Catalog id:** `chandra1997datadist`
**Citation:** Rohit Chandra, Ding-Kai Chen, Robert Cox, Dror E. Maydan, Nenad Nedeljkovic, and Jennifer M. Anderson. "Data Distribution Support on Distributed Shared Memory Multiprocessors." Proceedings of PLDI '97 (ACM SIGPLAN Conference on Programming Language Design and Implementation), Las Vegas, pp. 334-345, 1997. DOI or record used: no DOI printed on the pages read; PDF text used.
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner. Full text read (text layer present on all 12 pages; some glyph errors in the extracted text, including the Table 2 unit label, which is garbled).
**Card status:** full-read

## Problem
On cache-coherent NUMA machines, a remote miss costs 2-3 times a local one, and the OS places data in pages of 16 KB. Data meant for different processors can share a page, causing page-level false sharing (Sec. 1, pp. 334-335). The paper offers directives to distribute arrays in explicitly parallel programs, with a way around page granularity (Sec. 1, p. 335).

## Input abstraction
Fortran programs with doacross loop directives and array distribution directives whose per-dimension forms are block, cyclic, cyclic(expr) and * (Sec. 3.1-3.2, pp. 335-336). An affinity clause ties each iteration to the processor holding an element (Sec. 3.4, p. 337).

## Target
SGI Origin-2000, a cache-coherent NUMA machine built from nodes of 195 MHz R10000 processors joined through a switch-based interconnect (Sec. 2, p. 335). The evaluation uses a 128-processor Origin-2000 (Sec. 8, p. 341). No controlled tag fits CC-NUMA, so target tags are empty.

## Data decomposition
Regular distribution allocates each processor's portion from that processor's local memory, overriding first-touch placement (Sec. 4.2, p. 337). Reshaped distribution rearranges the array so that each processor's portion is contiguous, through a processor array that points to the portions (Sec. 4.3, pp. 337-338, Fig. 3, Table 1). Dynamic redistribution is allowed only for regular arrays (Sec. 3.3, p. 336). The applications use block, cyclic, and two-dimensional block-block forms (Sec. 8, pp. 341-343).

## Computation mapping
Affinity scheduling runs iteration i on the processor holding A(i). Loop bounds for block, cyclic and block-cyclic distributions are generated per processor (Sec. 3.4 and 4.1, p. 337; Fig. 2).

## Communication generation
Not applicable: processors communicate through ordinary loads and stores (Sec. 1, p. 334). The compiler work concerns address computation for reshaped references, by tiling, peeling, hoisting and floating-point division (Sec. 7.1-7.3, pp. 339-341).

## Compiler / runtime split
At compile time, the compiler processes the directives and applies the reshaped-reference optimizations (Sec. 7, pp. 339-341). At link time, a pre-linker propagates reshape directives into called subroutines and clones them for each distribution (Sec. 5, pp. 337-338). At program start, the runtime library reads common-block annotations and makes the page-allocation calls (Sec. 4.2, p. 337). Optional run-time checks use a hash table to verify argument shapes (Sec. 6, p. 339).

## Evaluation
Measured on the 128-processor Origin-2000. NAS LU (class C) compares first-touch, round-robin, regular and reshaped placement. Reshaping is best at 64 processors, but only about 6 percent ahead of first-touch (Sec. 8.1, pp. 341-342, Fig. 4). For a 5000 by 5000 matrix transpose, the reshaped version is 30 to 50 percent faster than round-robin at moderate processor counts (Sec. 8.2, p. 342, Fig. 5). On one processor, LU reshaping overhead falls from 83.91 to 46.23 after tiling, peeling and hoisting, against 45.71 for the original code (Table 2, p. 341).

## Principal limitation
The authors state that reshaped arrays cannot be redistributed, because dynamic reshaping severely restricts compiler optimization (Sec. 3.3, p. 336). They also note legality restrictions on reshaped arrays, such as no equivalencing and matching common-block declarations, and the addressing overhead of reshaping (Sec. 3.2.1 and 4.3, pp. 337-338).
our observation: all results come from one vendor's compiler and one machine, so the gains from reshaping depend on that compiler's optimizations.

## Relationship to earlier / later work
The paper states that its directives are similar to HPF's distribution directives, that its doacross directive matches HPF's independent directive, and that its affinity clause corresponds to the ON directive of HPF-2.0 (Sec. 3, p. 335; Sec. 9, p. 344). It says its reference transformation is similar to that of Anderson, Amarasinghe and Lam [AAL95], and that its affinity and tiling transformations follow Hiranandani et al. [HKM+93] (Sec. 4.1, 4.3, 7.1; pp. 337, 339-340). Compiler-based approaches by Anderson and Lam, Gupta and Banerjee, Kennedy and Kremer, and Sheffler et al. are described as tied to loop-level parallelism detection (Sec. 9, p. 344).

## Sources used
| claim | section / page |
|---|---|
| Remote latency ratio and page granularity | Sec. 1, pp. 334-335 |
| Origin-2000 architecture and first-touch policy | Sec. 2, p. 335 |
| Directive forms block, cyclic, cyclic(expr), * | Sec. 3.2, p. 335 |
| Dynamic redistribution limited to regular arrays | Sec. 3.3, p. 336 |
| Restrictions on reshaped arrays | Sec. 3.2.1, p. 337 |
| Affinity scheduling transformations | Sec. 3.4 and 4.1, p. 337; Fig. 2 |
| Regular distribution via page allocation | Sec. 4.2, p. 337 |
| Reshaped layout and reference transformation | Sec. 4.3, pp. 337-338; Table 1 |
| Propagation and cloning of reshape directives | Sec. 5, pp. 337-338 |
| Run-time argument checks | Sec. 6, p. 339 |
| Tiling, peeling, interchange, hoisting | Sec. 7.1-7.4, pp. 339-341 |
| NAS LU, reshaping best at 64 processors | Sec. 8.1, pp. 341-342; Fig. 4 |
| Matrix transpose result | Sec. 8.2, p. 342; Fig. 5 |
| LU single-processor overhead | Table 2, p. 341 |
| Relation to HPF and HPF-2.0 | Sec. 9, p. 344 |

## Open questions for the survey
- The regular-versus-reshaped choice is left to the programmer, who must weigh array bounds and processor count (Sec. 3.2, p. 336). Could a compiler make this choice reliably?
- Reshaped routines are cloned for each distribution combination, and the authors expect few combinations (Sec. 5, p. 338). How does this scale in large codes?
- The gains depend on loop-nest optimizations specific to one compiler. Would the directive model keep its advantage in compilers without them?
