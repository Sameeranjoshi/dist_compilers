# Compiling Affine Loop Nests for Distributed-Memory Parallel Architectures
**Catalog id:** `bondhugula2013compiling`
**Citation:** Uday Bondhugula. "Compiling Affine Loop Nests for Distributed-Memory Parallel Architectures." Proc. SC13: International Conference for High Performance Computing, Networking, Storage and Analysis, Denver, CO, 2013, pp. 1-12. DOI 10.1145/2503210.2503289 (DOI from the title page and catalog record).
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner. Full text read; the text layer is complete for the prose. Plots were read only as extracted labels.
**Card status:** full-read

## Problem
Distributed-memory compilation of affine loop nests needs generated communication code. The authors argue that the number and identity of communication partners depend on the process count and on problem sizes, which are unknown at compile time, so plain polyhedral projection does not give precise communication (Sec. 3). The paper generates that code for any affine computation partition, parametric in process count (Sec. 1, 4).

## Input abstraction
Unmodified sequential C with affine loop nests, extracted with Clan. No pragmas, directives or data distributions are supplied (Sec. 1, 5.3). The input may be any affine transformation sequence; Pluto supplies the one used in the experiments (Sec. 5.3).

## Target
MPI on clusters of multicore nodes. The experiments used 32 nodes of dual quad-core Xeon E5430 servers on InfiniBand, with one MPI process and one OpenMP thread per node (Sec. 6).

## Data decomposition
None is specified. Each process holds the full data space and touches what its partition needs; data move as the computation partition and dependences dictate (Sec. 5.4). Final results are gathered at rank 0 to match sequential behaviour. Allocation is left to future work (Sec. 5.4).

## Computation mapping
The computation partition comes from Pluto's tiling and skewing (Sec. 5.3). A tile is the work under one iteration of the parallel dimension (Sec. 4.2). A generated function pi maps tiles to ranks: block for rectangular spaces, block-cyclic for non-rectangular ones (Sec. 5.1, 6).

## Communication generation
Only flow (RAW) dependences generate communication (Sec. 4.1). Per tile, the paper computes a flow-out set (values read outside the tile) and a write-out set (final values, gathered at rank 0) by projection and parametric image (Sec. 4.2, Algorithms 1-2). A helper sigma returns the receiving ranks at run time, so each element goes only to processes that read it (Sec. 5.1). Transitive RAW and WAW edges are removed with ISL last-writer analysis (Sec. 5.2). Sends are non-blocking, completed before the next outer iteration (Sec. 5.1).

## Compiler / runtime split
Flow-out and write-out sets, buffer bounds, pi and sigma are generated at compile time. The sigma and pi helpers run at run time, once per parallel iteration, to resolve the process count and the receiver list (Sec. 5.1).

## Evaluation
Strong scaling on 32 nodes against icc sequential, Pluto sequential, a naive all-gather variant, hand-written MPI and pghpf, which failed on the non-rectangular codes (Sec. 6). Table 2 gives 32-node speedups over sequential of 194 (strmm), 570 (trmm), 80.8 (dsyr2k), 355 (covcol), 31.0 (seidel), 61.3 (jac-2d), 11.9 (fdtd-2d), 47.5 (2d-heat), 31.4 (3d-heat), 21.3 (lu) and 18.0 (floyd-warshall). Floyd-Warshall is reported within 25% of hand-tuned MPI at 32 nodes (Fig. 6d).

## Principal limitation
As the paper states it: data are not distributed, so every process holds all data (Sec. 5.4). Communication volume is not optimal when parts of one flow-out set have different receivers (Sec. 5.5). Duplicate communication grows when tiles outnumber processes, and a full solution "possibly" needs run-time techniques (Sec. 5.3). Our observation: the largest run uses 32 processes, so the cost of sigma and the per-iteration count exchange at larger process counts is not measured.

## Relationship to earlier / later work
- Pluto supplies the partitioning; Clan, ISL, Cloog-isl and Polylib do extraction, dependence testing and code generation (Sec. 5.3).
- Claims to remove the virtual-processor redundancy and the access-based sets of Amarasinghe and Lam [2], Adve and Mellor-Crummey [1] and Classen and Griebl [11] (Sec. 5.6).
- Names dHPF [27] and multipartitioning [14] as optimizations not implemented here (Sec. 5.6, 7).
- Calls Dathathri et al. [15] related concurrent work using flow-out sets and sigma/pi (Sec. 5.5, 7).
- Compares with OpenMP-to-MPI translation [22], R-STREAM's PGAS target [26], speculative pipelining [21] and dynamic scheduling [7] (Sec. 7).

## Sources used
| claim | section / page |
|---|---|
| Problem and parametric process count | Sec. 1, 3 |
| Input is unmodified sequential C; no pragmas | Sec. 1, 5.3 |
| Platform and MPI setup | Sec. 6 |
| Data distribution free | Sec. 5.4 |
| Flow-out and write-out sets | Sec. 4.2, Alg. 1-2 |
| pi and sigma helpers | Sec. 5.1 |
| Transitive dependences, ISL | Sec. 5.2 |
| Toolchain | Sec. 5.3 |
| Table 2 speedups, floyd within 25% | Sec. 6, Table 2 |
| Stated limitations | Sec. 5.3, 5.4, 5.5 |
| Related systems | Sec. 5.6, 7 |

## Open questions for the survey
- Does sigma-based receiver computation stay practical at process counts far beyond 32, and do later systems report its cost?
- Did later polyhedral systems keep the data-distribution-free model of Sec. 5.4, or add the allocation the paper defers?
- Does the flow-in refinement of Dathathri et al. [15] remove the non-optimality noted in Sec. 5.5?
