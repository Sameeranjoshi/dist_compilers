# Automatic Distributed-Memory Parallelization and Code Generation using the Polyhedral Framework

**Catalog id:** `bondhugula2011automatic`
**Citation:** Uday Bondhugula. "Automatic Distributed-Memory Parallelization and Code Generation using the Polyhedral Framework." Technical report IISc-CSA-TR-2011-3, Dept. of Computer Science and Automation, Indian Institute of Science, Bangalore, Sep 2011.
**Paper type:** compiler-technique
**Access:** open — full text read.
**Card status:** full-read

## Problem
Compiling regular sequential programs for distributed-memory clusters hinges on generating good communication code; the report claims no practical end-to-end solution existed (Abstract, Sec. 1). Sec. 3 names the obstacles: the process count is a runtime parameter, so `my_rank*N/nprocs` is non-linear in the polyhedral model, and the number and identity of partners and the data to send may depend on it. The goal is communication generation for arbitrarily nested affine loop nests, parametric in sizes and process count, for any affine computation partitioning.

## Input abstraction
An unmodified sequential C program with affine loop nests, extracted by Clan; the authors state no pragmas, directives or distributions are provided (Sec. 5.3). Output is SPMD C with MPI and optional OpenMP (Sec. 1, 6, Fig. 6).

## Target
Clusters of multicores on InfiniBand or 10 GbE, with MPI as portable backend (Sec. 1). Experiments: 32 nodes, dual quad-core Xeon E5430, Mellanox InfiniBand, MVAPICH2-1.4 (Sec. 6).

## Data decomposition
None. Sec. 5.4 assumes each process holds the entire data space of every variable and touches only what its partition needs; Sec. 5.3 calls the chain "data distribution free" and "computation driven": "there exists no owning processor for data", data moving only as the computation partitioning and dependences dictate. An initial distribution would affect only start-up; final results are gathered at rank 0 to mirror the sequential program. Adopting Yuki and Rajopadhye's allocation [31] is future work.

## Computation mapping
Pluto first finds a tiling/skewing transformation; the scheme is said to work with any affine partitioning (Sec. 1, 5.3). A *tile* is the computation under one iteration of the parallel dimension (Sec. 4.2). A generated function pi(t1, ..., tl, tp) maps parallel-loop iterations to ranks: block by default, but block-cyclic, model-driven, dynamic or multidimensional allocations are possible (Sec. 5.1); generated code calls `polyrt_loop_dist(...)` for each rank's range (Fig. 6). Outer parallelism needs only a final gather; inner, wavefront and pipelined parallelism become a parallel loop plus communication (Sec. 4.1).

## Communication generation
Only flow (RAW) dependences generate communication; anti/output dependences need neither communication nor synchronization (Sec. 4.1). Per variable and tile two sets are computed with projection and parametric image: the *flow-out set* (written in the tile, next read outside; Algorithm 1) and the *write-out set* (last writes, via outgoing WAW edges; Algorithm 2) (Sec. 4.2). Last-writer analysis (ISL) must remove transitive RAW edges yet keep transitive WAW edges (Sec. 5.2). Copy-out/copy-back statements enter the polyhedral representation and are generated in one pass; discontiguous data is packed into buffers bounded from tile constraints (Sec. 4.3, 5.3). The naive scheme broadcasts flow-out sets with `MPI_Allgatherv` and gathers write-out sets with `MPI_Gatherv` (Sec. 4.3). The optimized scheme generates sigma_x(t1, ..., tp), which at run time scans the dependence polyhedron to enumerate dependent tiles and maps them via pi to receiver ranks, so every element sent is needed and only expecting ranks receive (Sec. 5.1). Sends are "send-synchronous": non-blocking `MPI_Isend`/`MPI_Irecv`, `MPI_Waitall`, copy-back before the next outer iteration; Fig. 6 also shows an `MPI_Alltoall` of counts. No explicit cost model; volume is admitted suboptimal when parts of a flow-out set have different receivers (Sec. 5.2).

## Compiler / runtime split
Source-to-source with Clan, ISL, Pluto, Cloog-isl and Polylib (Sec. 5.3). Communication sets, buffer bounds and the pi/sigma helpers are derived at compile time; the helpers execute at run time once per parallel-loop iteration to resolve the parametric process count (Sec. 5.1). Runtime is MPI plus a small `polyrt` helper (Fig. 6). Extra compile time is under 1.5 s (Sec. 6).

## Evaluation
Benchmarks (Table 1): strmm, tmm, dsyr2k, covcol (outer-parallel, write-out only) and stencils seidel, jac-2d, fdtd-2d (PolyBench), 2d-heat (Pochoir); strong scaling, one MPI process and one OpenMP thread per node (Sec. 6). Baselines: icc sequential, Pluto sequential, hand-written MPI, the allgather variant, and pghpf 12.1 where it compiled (it failed on non-rectangular codes). Table 2: 32-node speedups over sequential of 194 (strmm), 570 (tmm), 80.8 (dsyr2k), 355 (covcol), 31 (seidel), 61.3 (jac-2d), 11.9 (fdtd-2d), 47.5 (2d-heat); over the 1-process generated code 26.3, 24.5, 24.7, 23.8, 20.8, 9.6, 11, 11.7. Fig. 4 shows the optimized scheme above manual MPI and pghpf on stencils, credited to full space-time tiling with pipelined 3-d tiles. Fig. 5 splits compute+pack, communication and unpack at 4 and 32 processes.

## Principal limitation
Stated: no data allocation, so every process holds all data, conceded as a problem on very large machines (Sec. 5.4); suboptimal flow-out decomposition for heterogeneous receiver sets (Sec. 5.2); no multipartitioning (Sec. 7); no experimental comparison with prior systems, none being available (Sec. 6). Our observation: one process per node on 32 nodes leaves the runtime cost of sigma evaluation and per-iteration count exchange at scale uncharacterized.

## Relationship to earlier / later work
- Coupled with Pluto [8, 9, 26]; uses Clan [7], ISL [16], Cloog [11], Polylib [27] (Sec. 1, 5.3).
- Claims to overcome Amarasinghe and Lam [2], Adve and Mellor-Crummey [1], Classen and Griebl [10] (virtual-processor redundancy; access- rather than dependence-based sets) (Sec. 5.5, 7); dHPF [23] and multipartitioning [12] acknowledged, not implemented (Sec. 7).
- Griebl [15], Kennedy and Kremer [17], Yuki and Rajopadhye [31] on allocation (Sec. 5.4, 7); sigma likened to Baskaran et al. [6]; Kim et al. [18], R-Stream PGAS [22], OpenMP-to-MPI [19] discussed (Sec. 7); HPF compared via pghpf (Sec. 6).
- inferred: Kruse's Molly preprint (`kruse2014molly`) cites this report as a tile-based virtual-processor approach.

## Sources used
| claim | section / page |
|---|---|
| Problem, parametric processors | Abstract, Sec. 1, 3 |
| Input/output form | Sec. 1, 5.3, Fig. 6 |
| Hardware | Sec. 6 |
| Distribution-free, full data space | Sec. 5.3-5.4 |
| Tiles, pi, allocation | Sec. 4.2, 5.1 |
| Flow-out/write-out sets | Sec. 4.1-4.2, Alg. 1-2, Fig. 3 |
| Transitivity | Sec. 5.2 |
| Packing, collectives, sigma | Sec. 4.3, 5.1, Fig. 6 |
| Toolchain | Sec. 5.3 |
| Results | Sec. 6, Tables 1-2, Figs. 4-5 |
| Prior-scheme comparison | Sec. 5.5, 7 |

## Open questions for the survey
- The report separates communication generation from allocation; did later polyhedral work keep that separation or fold allocation back in (cf. [31])?
- How does the dependence-based flow-out/write-out formulation relate to Molly's chunking and to the access-based integer-set schemes it criticizes?
- How was the replicated full-array storage addressed in follow-ups, and how does it bound scalability beyond 32 nodes?
