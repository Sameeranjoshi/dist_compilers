# Dependence Graphs and Compiler Optimizations
**Catalog id:** `kuck1981dependence`
**Citation:** D. J. Kuck, R. H. Kuhn, D. A. Padua, B. Leasure and M. Wolfe. "Dependence Graphs and Compiler Optimizations." Eighth Annual ACM Symposium on Principles of Programming Languages (named only in the PDF document properties, not in the body), 1981. No DOI printed; record used: supplied PDF, which prints ACM identifier 0-89791-029-X.
**Paper type:** foundational
**Access:** PDF supplied by the repository owner. Full text read (text layer complete on all 12 pages; some OCR errors, so the title page and Section 2 were also checked against page images).
**Card status:** full-read

## Problem
The paper proposes dependence graphs as the vehicle for formulating and implementing compiler optimizations of high-level programs, aiming to enhance performance (Sec. 1.1, p. 207). It argues that dependences matter on machines with simultaneous subsystems, such as parallel, pipelined, multiprocessor and virtual-memory hardware (Secs. 1.1-1.2, pp. 207-208).

## Input abstraction
Source programs are FORTRAN- or ALGOL-like, limited to assignments, DO loops (step one; constant or variable limit) and WHILE loops, over scalars and arrays (Sec. 2.1, p. 208). A preprocessor is assumed to bring source toward this form (Sec. 2.1, p. 208). Graph nodes are assignments and DO and WHILE headers, with five arc kinds: loop, flow, output, antidependence and input (Sec. 2.2, pp. 208-209; Fig. 1, p. 216).

## Target
The abstract says the transformations were applied to several high-speed architectures. The body names vector and array processors (Sec. 4.1.1, p. 213), vector-register machines such as the CRAY-1 (Sec. 4.2, p. 214), the Burroughs BSP (Sec. 3.2, p. 211) and the Burroughs FMP multiprocessor (Sec. 3.3, p. 212). Distributed-memory machines, message passing and data placement are not discussed.

## Data decomposition
Not applicable in this paper: no program data is distributed across processors. Expansion gives each iteration its own storage (Sec. 3.2, p. 211), and the FMP DO ALL copies local variables into each processor's local memory before a loop starts (Sec. 3.3, p. 212). Both are storage or privatization effects, not array decomposition.

## Computation mapping
The partial-order graph from loop distribution is used to schedule vector operations and recurrences on a parallel processor (Sec. 4.1.1, p. 213). Its longest chain gives the minimum execution time, and its maximum width an upper bound on usable processors (Sec. 4.1.1, p. 213). The paper does not describe how iterations are assigned to processors.

## Communication generation
Not applicable in this paper: no communication is generated. Outputs are regenerated source (Abstract, p. 207), vector and scalar operations (Sec. 4.1.1, p. 213; Sec. 5, p. 215) and transformed loops (Sec. 4.2, p. 214). Sections 3-5 contain no transfer or message constructs.

## Compiler / runtime split
The paper's steps are compile-time and source-to-source: graph transformations and source regeneration (Abstract, p. 207; Sec. 5, p. 215). Unknown subscripts and conditional execution force conservative assumptions (Sec. 2.2, p. 209). No runtime component is described beyond the DO ALL copy semantics (Sec. 3.3, p. 212).

## Evaluation
The authors report verifying the ideas on about 1,000 programs from many sources (Sec. 1.1, p. 207). The only quantitative results for the transformations are a loop nest whose data pages fall from 9 to 5 after loop distribution (Example 4.2, p. 213) and a factor-of-6 page reduction the authors cite from [AbKL79] (Sec. 4.1.2, p. 214). No speedup of the transformations is reported.

## Principal limitation
As the paper states, a powerful algorithm for renaming structured variables is an open problem (Sec. 3.1, p. 210), and a good expansion algorithm for array variables is likewise open (Sec. 3.2, p. 212).
our observation: the paper reports no measured speedup for any transformation, so its performance claims are qualitative.

## Relationship to earlier / later work
- Scalar renaming has been known for years [AhU173], and expansion is implemented in the BSP and CRAY-1 compilers (Secs. 3.1-3.2, p. 211).
- Graph abstraction has been used in data-flow analysis [Cock70] and the SIMPL optimizer [ZeBa74]; loop fusion was applied globally before [AlCo72], [Love77]. This paper uses abstraction differently and applies fusion selectively (pp. 212-214).
- The SCC step compares favorably with [GrWe76] (Sec. 4.1, p. 213). [DuKu78] is the only other published vector-register assignment method (Sec. 4.2, p. 215).
- The text cites Baker as [Bake78], but the reference list gives [Bake77] (Sec. 2.1, p. 208; references, p. 215). It names no later work.

## Sources used
| claim | section / page |
|---|---|
| Goal: enhance program performance through dependence-graph steps | Sec. 1.1, p. 207 |
| Dependences matter on machines with simultaneous subsystems | Secs. 1.1-1.2, pp. 207-208 |
| Source restrictions: DO index step one; scalars and arrays | Sec. 2.1, p. 208 |
| Node kinds and the five arc kinds | Sec. 2.2, pp. 208-209; Fig. 1, p. 216 |
| Conservative handling of nonlinear subscripts and conditionals | Sec. 2.2, p. 209 |
| Scalar renaming; structured-variable renaming is open | Sec. 3.1, pp. 210-211 |
| Expansion per iteration; array expansion is open | Sec. 3.2, pp. 211-212 |
| Node splitting; FMP DO ALL local copies | Sec. 3.3, p. 212 |
| Forward substitution before tree-height reduction | Sec. 3.4, p. 212 |
| Loop distribution, partial-order graph, vector operations | Secs. 4, 4.1, 4.1.1, pp. 212-213 |
| Data pages 9 to 5; factor of 6 citing [AbKL79] | Sec. 4.1.2, pp. 213-214 |
| Loop fusion for virtual memory and vector registers | Sec. 4.2, pp. 214-215 |
| About 1,000 test programs; implementation in PARAFRASE | Sec. 1.1, p. 207; Sec. 5, p. 215 |

## Open questions for the survey
- Which later distributed-memory compilers keep these arc-removal and abstraction steps unchanged, and which add placement or communication information to the same graph? The paper's arcs record only dependences among statements, loop headers and their atoms, with no placement information.
- The parallelism discussed is vector, pipeline and multiprocessor-style. Should the survey separate statement-level vectorization from processor-level distribution when it cites this paper?
- Does the survey need the FMP DO ALL local-copy behavior (Sec. 3.3), the paper's only per-processor memory reference, or can it be left out?
