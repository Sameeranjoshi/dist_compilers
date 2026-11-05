# Automatic Generation of Distributed-Memory Mappings for Tensor Computations

**Catalog id:** `kong2023automatic`
**Citation:** Martin Kong, Raneem Abu-Yosef, Atanas Rountev, P. Sadayappan. "Automatic Generation of Distributed-Memory Mappings for Tensor Computations." SC '23 (International Conference for High Performance Computing, Networking, Storage and Analysis), 2023. DOI 10.1145/3581784.3607096.
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner — full text read.
**Card status:** full-read

## Problem
Sec. 1-2: distributed tensor algorithms (Cannon, SUMMA, 2.5D) are hand-derived per operator and grid shape, and frameworks such as DISTAL, Tiramisu, ScaLAPACK, COSMA and CTF only express and run them. The one automatic path, Pluto-Dist [5], is said to be limited to affine schedules (excluding Cannon), 1D partitioning, intricate code that blocks tuned-library calls, and no MPI communicators. Per-operator choices also ignore inter-operator data flow (Sec. 2, Fig. 1). DiMage ("distributed mapping generator") searches computation placement, data placement and grid shape jointly for DAGs of tensor operators under per-node memory limits.

## Input abstraction
A topologically sorted DAG of operators, each a perfectly nested loop with fixed bounds and only parallel or reduction loops, with linear index expressions without constant shifts (`A[i][j]`, not `X[i+j]`); loops may be tagged non-partitionable (Sec. 5). Each operator has an iteration space, each tensor a data space, and access relations connect them (Sec. 3, Fig. 3). Further inputs: grid dimensionality N, PE count, per-node capacity C_node and a machine parameter MEM2COMP_RATIO (Sec. 5, Table 5, Eq. 7).

## Target
Clusters of homogeneous nodes viewed as an N-dimensional processor grid whose extents the tool chooses (Sec. 1, 3). Generated MPI code calls MKL DGEMM for local work (Sec. 6, 7). Evaluation: Broadwell nodes (2x Xeon E5-2680 v4, 28 cores, 128 GB), fat-tree EDR InfiniBand, 2-64 nodes, one process per node (Sec. 7).

## Data decomposition
Each data-space dimension of a tensor maps to at most one grid dimension via a 0/1 variable pi, and each grid dimension receives at most one dimension (Eq. 1). A mapped dimension is "partitioned": contiguous elements placed as evenly as possible across that grid dimension's PEs (block); an unmapped dimension is present in full on every PE, i.e. replicated along unused grid dimensions (Sec. 4, 5). Local extent N/P_k when mapped (Eq. 2) yields per-node memory and the constraint that an operator's tensors fit C_node; an all-reduce needs 3x buffers (Sec. 4, 6). Placement is fixed at first write (Sec. 5.1). Solutions cover row, column, 2D-block and replicated layouts (Tables 2-4, 7-9).

## Computation mapping
Iteration-space dimensions map through mu variables under the same rules: a mapped loop is split block-wise along a grid dimension, an unmapped loop runs in full on every PE, and a grid dimension no loop maps to implies redundant execution (Sec. 5). Reduction loops may be mapped at the price of an all-reduce (Sec. 4, Table 4, Fig. 5). Grid extents are decision variables too. The objective (Eq. 7) sums per-operator local work plus MEM2COMP_RATIO times communication volume, which penalizes full replication. Operators run sequentially in the given order; fusion is not modelled (Sec. 5).

## Communication generation
Communication is deduced from the IS->PS, IS->DS and DS->PS maps (Sec. 5). Match variables lambda (Eq. 4) are 1 when mu and pi agree on a grid dimension, making read volume zero; write volume uses replication variables that fire when a reduction loop is mapped or a data dimension is unmapped, modelling an all-gather whose cost is the number of grid dimensions it spans (Eq. 5). Eq. 6 forbids "crossed" mu/pi solutions that would need point-to-point traffic, restricting codegen to collectives. From a solution, per (operator, tensor) communication vectors (0/1 per grid dimension) are derived; `MPI_COMM_WORLD` is split by colour into sub-communicators per vector, and all-gather (tensors fed into the DAG) or all-reduce (mapped reduction, or replicated data updated by one PE) is inserted around the local kernel (Sec. 6). The cost model is volume-only, without latency or bandwidth terms.

## Compiler / runtime split
Fully static: PE count, extents, capacity and grid dimensionality are compile-time inputs. DiMage emits a non-linear formulation, takes a first Z3 solution, iterates by adding G_new < G_old until none is better, and generates instance-specific MPI code (Sec. 6, Appendix). Only the rank-to-coordinate tuple is computed at run time (Sec. 6). Solver cost (Table 6): 3-11 Z3 calls per DAG, 0.6-3.9 s per call for 1D grids and 5-111 s for 2D.

## Evaluation
Seven DAGs (2mmC, 2mmK, 3mmC, 3mmV, 4mmC, 4mmY, mttkrp-proxy) at 16K extents (512 for mttkrp), double precision, mean of five runs, 1D and 2D grids on 2-64 nodes (Sec. 7, Table 6). Baselines: CTF 1.5.5 with ScaLAPACK 2.1.0, and Pluto-Dist autotuned over four tile sizes; Pluto is reported slower because tile size couples communication granularity to local efficiency and it cannot call MKL (Sec. 7). Findings (Sec. 7.1-7.2, Figs. 6-7): chain DAGs (2mmC/3mmC/4mmC) get communication-free 1D mappings whose time is all local compute; kernel-feeding DAGs (2mmK/3mmV/4mmY) favour 2D grids with sub-communicators, while 1D at many nodes degenerates to all-to-all and 256-column blocks; mttkrp-proxy 1D on 2 nodes is about 2x slower than CTF, 2D is best at 64 nodes and beats CTF at 8 and 16 with an inversion at 32. Sec. 7.3 shows three capacity settings for 2mmC on 4 nodes yielding row-, column- and reduction-mapped (all-reduce) solutions (Tables 7-9). Sec. 8 claims DiMage outperforms CTF "on a variety of tensor DAGs"; Fig. 1 (2mmC) is the headline, but the text gives no numeric speedups.

## Principal limitation
Stated: linear indexing without shifts, no fusion, pre-decided operator order, homogeneous nodes, compile-time extents (Sec. 3, 5); point-to-point patterns excluded by Eq. 6; mttkrp local kernels untuned (Sec. 7.1); 1D mappings lose local efficiency at scale (Sec. 7.1). Our observation: an all-gather is scored by the number of grid dimensions it spans, ignoring latency and bandwidth, and predicted versus measured communication is never validated beyond the Fig. 7 breakdown.

## Relationship to earlier / later work
- Positioned against Pluto-Dist [5] and follow-ups (Reddy [27], Dathathri et al. [16, 15]); Pluto-Dist is a baseline (Sec. 1, 2, 7).
- Earlier automatic distribution: Amarasinghe and Lam [2], Ramanujam and Sadayappan [26], Classen and Griebl [13], Griebl et al. [19]; Fortran layout: Chapman, Fahringer and Zima [10], Kennedy and Kremer [22], Gupta and Banerjee [20] (Sec. 1).
- Table 1 contrasts Cannon, Johnson 3D, SUMMA, 2.5D, CTF [30] and DISTAL [32] on multi-operator support, placement automation, grid shape and external kernels; CTF is the main baseline (Sec. 2, 7).
- Frameworks that express but do not derive algorithms: DISTAL, (Distributed) Tiramisu [3, 21], ScaLAPACK, COSMA (Sec. 1).

## Sources used
| claim | section / page |
|---|---|
| Problem, critique of Pluto-Dist, contributions | Sec. 1 |
| Motivation, Table 1, 2mmC example | Sec. 2, Figs. 1-2 |
| IS/DS/PS entities, access relations | Sec. 3, Fig. 3 |
| 0/1 mapping variables, examples, 3x buffers | Sec. 4, Tables 2-4, Figs. 4-5 |
| Program class, partitioned dimension, data-movement deduction | Sec. 5 |
| Capacity, volume, match and replication variables, Eq. 6, objective | Sec. 5.1, Eqs. 1-7, Table 5 |
| Z3 iteration, grid geometry, CVs, communicators, collectives | Sec. 6 |
| Setup, baselines, results | Sec. 7, 7.1, 7.2, Table 6, Figs. 6-7 |
| Capacity-driven mappings | Sec. 7.3, Tables 7-9 |
| Artifact workflow | Appendix |

## Open questions for the survey
- The 0/1 dimension-to-grid-axis encoding resembles mesh-axis sharding specifications in ML partitioners; what distinguishes DiMage's cost model and search from auto-sharding searches?
- How much of the algorithm space does the collective-only restriction (Eq. 6) remove, given the paper's own critique of Pluto for excluding Cannon-style shifting?
- Can the formulation admit non-uniform or sparse partitions, so that it could drive a dialect such as PartTensor (vaidya2025distributed)?
