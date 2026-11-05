# Compiling for Distributed Memory Architectures
**Catalog id:** `rogers1994compiling`
**Citation:** Anne Rogers and Keshav Pingali. "Compiling for Distributed Memory Architectures." IEEE Transactions on Parallel and Distributed Systems 5, no. 3 (1994): 281-298. Record used: IEEE Log Number 9215362.
**Paper type:** full-system
**Access:** PDF supplied by the repository owner. Full text read; the text layer is complete, including tables, references and the appendix. Figure graphics (including Fig. 18) were not interpreted beyond their captions.
**Card status:** full-read

## Problem
Hand-written message-passing code is error-prone, so the paper proposes a compiler that takes a sequential program and a data decomposition and specializes the code for each process (Sec. I, Sec. II). Process decomposition is driven by data placement, not by program text (Abstract, Sec. II).

## Input abstraction
The source is an Id-like functional language with I-structures (Sec. III). The programmer gives mappings: wrapped rows or columns, blocks, an explicit process, an expression, or a same-as relation (Sec. III.A). Both sides of a full array assignment must share a mapping (Sec. III.A). The examples use loops with step 1 (Sec. V), and the SIMPLE compiler handles only flat arrays (p. 294, note 7).

## Target
The compiler generates C for the Intel iPSC/2 (Sec. II). The machine model is one process per processor, with explicit send and receive (Sec. III.B).

## Data decomposition
Each mapping supplies map, local and alloc functions (Sec. III.A). Wrapped (cyclic) and block mappings are the regular cases that support compile-time analysis, while irregular distributions are handled only by run-time resolution (Sec. III.A, Sec. IV).

## Computation mapping
The owner of a left-hand side computes the right-hand side (Principle 2, Sec. IV). Under run-time resolution, conditionals and loops run on all processes (Principle 4, Sec. IV). Compile-time resolution restricts work to evaluator sets and iterations that have work (Sec. V). Reductions are assigned to the process that owns most right-hand-side references (Sec. X).

## Communication generation
Run-time resolution sends each value to each process that needs it (Sec. IV). Compile-time resolution places sends and receives at the reference after partial evaluation (Sec. V). Vectorization combines messages for read-only references outside conditionals whose communication falls in contiguous iterations (Sec. VIII). Pipelining moves sends to the point where the value is ready, using mailbox numbers and, for array elements, a monotonicity condition (Sec. IX). Accumulation combines partial results of commutative, associative operators (Sec. X).

## Compiler / runtime split
Compile-time resolution performs ownership tests at compile time where the mappings allow it. Run-time resolution is the fallback for programs that cannot be analyzed (Abstract, Sec. II, Sec. V). Loops with wrapped mappings are summarized by periodic patterns rather than unrolled (Sec. V).

## Evaluation
Table I gives Gauss-Seidel on a 128x128 grid on iPSC/2 for 4 to 32 processors (p. 287). The blocked variant takes 864 to 153 ms and handwritten code 647 to 117 ms, so blocked code runs at about 75 to 77 percent of handwritten speed (computed here from Table I). Run-time resolution takes about 23 s and compile-time resolution about 15 s at every processor count (Table I, Sec. V.A). For SIMPLE on a 64x64 grid, Table II gives 14.02 s on one processor and 0.805 s on 32 (p. 294). Speedup is compared with a modeled handwritten program, not a measured one (Sec. XI-A).

## Principal limitation
The paper states that compile-time resolution "will not be helpful" for applications with complex data structures, such as sparse problems or irregular meshes, because their references may not be analyzable (Sec. XIII, p. 297). It also says the improvements are not enough to compete with handwritten code (Sec. XIII).
our observation: The abstract claims 60 to 70 percent of handwritten efficiency, but Table I gives about 75 percent for Gauss-Seidel. The SIMPLE comparison rests on a model, and the text gives the run-time time as 24 s where Table I shows 23.4 s.

## Relationship to earlier / later work
- Callahan and Kennedy [19], developed concurrently, use a similar run-time resolution with more aggressive optimizations (Sec. XII.A).
- Superb [29] uses overlap areas and vectorization of communication, while the AL compiler of Tseng [32], [24] sends data as soon as it is available (Sec. XII.B, XII.D).
- Kali [6], [30], [31] reuses saved communication patterns for hard-to-analyze forall loops, as does Saltz et al. [7] (Sec. XII.C).
- Crystal [20], [34] matches program references to aggregate communication routines (Sec. XII.E).
- Ramanujam and Sadayappan [26], [27] also explored pipelining (Sec. XII).
- No later work is discussed.

## Sources used
| claim | section / page |
|---|---|
| Owner-driven decomposition; run-time resolution fallback | Abstract, Sec. II, p. 281-282 |
| Mappings and map/local/alloc functions | Sec. III.A, pp. 283-284 |
| Run-time and compile-time resolution principles | Sec. IV, pp. 284-285; Sec. V, pp. 285-287 |
| Gauss-Seidel timings (Table I) | Sec. V.A, p. 287 |
| Vectorization restrictions | Sec. VIII, pp. 288-290 |
| Pipelining and monotonicity condition | Sec. IX, pp. 291-293 |
| Accumulation | Sec. X, p. 293 |
| SIMPLE timings (Table II) and model | Sec. XI, pp. 294-295 |
| Related work | Sec. XII, pp. 295-296 |
| Limitations and 60-70 percent statement | Sec. XIII, p. 297 |

## Open questions for the survey
- Does the vectorization and pipelining gain hold for irregular or sparse programs, which the paper excludes from compile-time resolution?
- How large is the gap between the Table I blocked variant and handwritten code when measured against the 60 to 70 percent claim, and does it hold on other machines?
- The SIMPLE comparison uses a modeled handwritten baseline. What is the measured gap on a real handwritten SIMPLE implementation?
