# PLuTo: A Practical and Fully Automatic Polyhedral Program Optimization System

**Catalog id:** `bondhugula2008pluto`  
**Citation:** Uday Bondhugula, J. Ramanujam, P. Sadayappan. "PLuTo: A Practical and Fully Automatic Polyhedral Program Optimization System." Report form (the text calls itself "this report"), no venue printed, dated 2008/3/31 in the page footers. Record used: supplied PDF, 15 pages. Catalog title and author list differ (see JSON notes).  
**Paper type:** full-system  
**Access:** PDF supplied by the repository owner. Full text read (text layer complete: all 15 pages extracted).  
**Card status:** full-read

## Problem
The paper addresses automatic parallelization and locality optimization of affine loop nests in one end-to-end polyhedral framework. It argues that earlier frameworks lacked a realistic cost function and that most did not treat locality and parallelism together (Sec. 1, pp. 1-2). The stated scope is local and shared-memory parallel execution (Sec. 1, p. 2).

## Input abstraction
Inputs are affine loop nests, possibly imperfectly nested (Sec. 1, p. 1; Sec. 2, p. 2). Dependences are exact and affine, including input dependences (Sec. 2.2, p. 2). The implementation accepts C program sections and dependence polyhedra from LooPo (Sec. 4, p. 4). Non-affine accesses may be handled conservatively, but the method is not described (Sec. 2.2, p. 2).

## Target
The tool emits OpenMP C code (Sec. 4, p. 4). The text never describes a distributed-memory system, cluster or message passing. "Distributed Memory" appears only in the title of reference [22] (p. 14).

## Data decomposition
None described. The only partitioning the paper applies is of the iteration space into tiles (Sec. 1, p. 1). Data placement, ownership and replication are not discussed.

## Computation mapping
Transformations are statement-wise affine hyperplanes (Sec. 2.3, p. 2). An integer linear program minimizes a bounding function on dependence distance under affine legality constraints, with independent solutions found iteratively (Lemma 2, p. 3; Sec. 3.2, pp. 3-4). Hyperplanes are taken in priority order: synchronization-free first, then constant boundary communication, with non-constant cases pushed inward (Sec. 3.2, p. 4). Dependences between strongly connected components are cut when no solution is found (Algorithm 1, p. 4). OpenMP pragmas mark parallel loops, and OpenMP distributes tile-space blocks across cores (Sec. 5.4, p. 6; Sec. 6, p. 8). Where space loops still carry forward dependences, Algorithm 3 marks the next m transformed hyperplanes parallel and places a barrier at the end of the tile schedule loop (Sec. 5.4, pp. 6-7).

## Communication generation
None generated. Communication appears as a cost term tied to communication volume (Sec. 3.2, p. 3), as tile-boundary traffic before and after tile execution (Sec. 1, p. 1; Sec. 3.1, p. 3), and as a remark that it still occurs at tile boundaries (Sec. 5.4, p. 6).

## Compiler / runtime split
The tool is source-to-source, using PipLib as the ILP solver and CLooG for code generation (Sec. 4, p. 4). Tile sizes were picked by rough rules or set empirically, without comprehensive search (Sec. 6, p. 8; Sec. 7, p. 13). The authors call the system fully model-driven (Sec. 7, p. 13), with cost-model tile sizes and empirical search still in progress (Sec. 6.7, p. 12).

## Evaluation
Six kernels (1-d Jacobi, FDTD, LU, MVT, 3-D Gauss-Seidel, Advect3d) ran on one quad-core Core 2 Quad (Sec. 6, pp. 8-12). Baselines are icc, gcc, and Lim-Lam and Griebl transformations run through the same code generator (Sec. 6, p. 8). Reported gains are 4x to 7x single-core for Jacobi (Sec. 6.1, p. 9), and 2x to 5x in most cases over previous automatic approaches, with an order of 10x over the best native compilers (Sec. 6.7, p. 12). The text gives no run counts or variance and does not say how cache misses were counted (Sec. 6.1, p. 9). Plotted values are not in the text layer.

## Principal limitation
As the authors state, tile sizes were not optimized through any extensive search or model (Sec. 6.7, p. 12), and the cost function does not capture tile-size choice (Sec. 7, p. 13). Our observation: the communication term bounds per-hyperplane traffic and was evaluated only on shared memory, so message generation and data placement are not addressed.

## Relationship to earlier / later work
The paper says scheduling-based work (Feautrier [18, 19]; Griebl [22]) targets minimum latency or fine-grained parallelism, not tilability (Sec. 7, p. 13). It compares against Lim-Lam partitioning [33-35] and Griebl's forward-communication-only allocation (Sec. 6, p. 8). Earlier tile-shape studies, including Ramanujam and Sadayappan [46], addressed communication but only for very simple codes (Sec. 7, p. 13). Planned work is parametric tiling (Sec. 5, p. 5).

## Sources used
| claim | section / page |
|---|---|
| Scope: local and shared-memory parallel execution | Sec. 1, p. 2 |
| Affine loop nests; non-affine accesses handled conservatively | Sec. 1, p. 1; Sec. 2.2, p. 2 |
| Exact affine dependences, including input dependences | Sec. 2.2, p. 2 |
| Statement-wise affine hyperplanes | Sec. 2.3, p. 2 |
| Legality constraint per dependence (Lemma 2) | Sec. 3.1, p. 3 |
| Bounding cost function; communication volume for space loops | Sec. 3.2, p. 3 |
| ILP with lexicographic minimum via PIP; iterative independent solutions | Sec. 3.2, pp. 3-4 |
| Synchronization-free hyperplanes ordered first | Sec. 3.2, p. 4 |
| SCC cut when no solution is found | Algorithm 1, p. 4 |
| OpenMP tool; LooPo front end (text cites it as [2], which is Ahmed et al.; LooPo is [36]); PipLib and CLooG | Sec. 4, p. 4 |
| Input dependences used only in the bounding objective | Sec. 4.1, p. 4 |
| Tile-space loops and fixed tile sizes | Sec. 5.1, p. 5 |
| Pipelined parallel tile schedule with barrier | Sec. 5.4, pp. 6-7; Algorithm 3, p. 7 |
| Communication still happens along tile boundaries in the parallel code | Sec. 5.4, p. 6 |
| Tile communication needed only before and after execution | Sec. 1, p. 1; Sec. 3.1, p. 3 |
| Tile sizes set empirically, no comprehensive search | Sec. 6, p. 8 |
| Quad-core Core 2 Quad; icc 10.0 and gcc 4.1.1 | Sec. 6, p. 8 |
| Jacobi single-core speedups of 4x to 7x | Sec. 6.1, p. 9 |
| Speedups of 2x to 5x in most cases; order of 10x over native compilers | Sec. 6.7, p. 12 |
| Tile sizes not optimized by search or model | Sec. 6.7, p. 12 |
| Tile-shape studies aimed at communication, simple codes only | Sec. 7, p. 13 |
| "Distributed Memory" appears only in the title of reference [22] | Reference list, p. 14 |

## Open questions for the survey
- Does the bounding function count as a communication model? It bounds per-hyperplane traffic on one shared-memory machine; the paper does not show how messages or placement would follow.
- Reference [22] has a distributed-memory title, but the text mentions its allocation only briefly. Reading it would show what that work covers.
- The target vocabulary has no shared-memory multicore value, so target_hardware is left empty; the survey should decide how to tag such papers.
