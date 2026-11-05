# DISTAL: The Distributed Tensor Algebra Compiler

**Catalog id:** `yadav2022distal`  
**Citation:** Rohan Yadav, Alex Aiken, Fredrik Kjolstad. "DISTAL: The Distributed Tensor Algebra Compiler." PLDI 2022. DOI 10.1145/3519939.3523437 / arXiv 2203.08069.  
**Paper type:** full-system  
**Access:** open (arXiv) — full text read.  
**Card status:** full-read

## Problem
Dense tensor algebra on distributed, heterogeneous machines. The authors argue that hand-written distributed kernels are long (they estimate ~500 lines for COSMA's distribution logic versus 15 lines of DISTAL schedule), that CTF decomposes every expression into distributed GEMM/transpose calls and so cannot use the best algorithm per expression, and that ScaLAPACK-style libraries force data into fixed input distributions (Sec. 1). DISTAL lets data distribution and computation distribution be specified independently so that known algorithms (Cannon, SUMMA, PUMMA, Johnson, 2.5D, COSMA) and new ones become schedules.

## Input abstraction
Three sub-languages (Sec. 2, Fig. 2): TACO tensor index notation; a format language in which a tensor's distribution is part of its format, written in "tensor distribution notation" (TDN); and a scheduling language with TACO's `parallelize`, `split/divide`, `collapse`, `reorder`, `precompute` plus three new commands `distribute`, `communicate`, `rotate` (Sec. 3.3). Leaf loops can be `substitute`d by vendor kernels such as cuBLAS GEMM.

## Target
Nodes with multi-core CPUs and multiple GPUs; evaluated on Lassen (dual-socket Power9, 4 V100 per node, NVLink 2.0, InfiniBand EDR) at up to 256 nodes (Sec. 7). Tensors may be pinned to GPU framebuffer memory (`Memory::GPU_MEM`, Fig. 2).

## Data decomposition
A machine is a multidimensional grid of abstract processors with local memory; grids nest (node grid, then GPU grid per node) (Sec. 3.1). A TDN statement `T X↦→Y M` names tensor and machine dimensions: shared names are partitioned into equal-sized contiguous blocks; machine dimensions absent from the tensor either *fix* the partition to a coordinate (a face of the grid) or *broadcast* (`*`) it. Formally a distribution is a coloring `P : T → color` composed with `F : color → M set` (Sec. 3.2). Hierarchical distributions give one TDN per level. Blocked partitioning is used, though a cyclic function could be substituted.

## Computation mapping
The iteration space is mapped to an "execution space" with processor and time dimensions. `distribute(v)` runs iterations of the named index variables on different processors simultaneously; a compound `distribute(targets, dist, local, m)` = divide + reorder + distribute tiles the iteration space over the grid (Sec. 3.3). Distributing output-indexing variables gives owner-computes; distributing reduction variables gives distributed reductions. `rotate` offsets each processor's start in time to produce systolic nearest-neighbor patterns. Ranks and explicit sends are deliberately absent, so schedules affect only performance.

## Communication generation
Inferred from data accesses: a naive completion fetches data at every point where it is not local; `communicate(T, i)` aggregates T's transfers at the start of each iteration of `i`, trading memory for message count (Sec. 3.3). No cost model is given. At lowering, each tensor communicated under a loop becomes a Legion partition whose hyper-rectangle bounds come from index-variable bounds analysis (Sec. 6.2); Legion performs the physical movement (NVLink intra-node, GASNet-EX inter-node) and overlaps it with computation (Sec. 6).

## Compiler / runtime split
Schedules are rewrite rules on TACO's concrete index notation (`s.t.` clauses) (Sec. 5). Distributed loops lower to Legion index task launches, nested ones flattened into multi-dimensional launches; a custom mapper places tasks on the requested processor grid (Sec. 6.2). Legion performs dynamic dependence analysis and data movement; the authors call this a "combined static-dynamic approach" that avoids brittle fully static analyses (Sec. 8). Four cores per node are reserved for the runtime (Sec. 7.1.1).

## Evaluation
Weak-scaling GEMM on up to 256 Lassen nodes versus ScaLAPACK, CTF and COSMA (Sec. 7.1). CPU: CTF/ScaLAPACK reach at most 80% of DISTAL/COSMA at 256 nodes; DISTAL's best schedule is within 10% of COSMA throughout and 5% at 256 nodes; COSMA matches DISTAL when restricted to 36 cores. GPU: 2x COSMA on one node; COSMA 15% faster at 256 nodes; Cannon's schedule beats SUMMA/PUMMA at scale thanks to `rotate`; Johnson/COSMA schedules exhaust GPU memory at 32 nodes; Legion's DMA reaches 18 of 25 GB/s from GPU memory. Higher-order kernels TTV, inner product, TTM, MTTKRP against CTF (Sec. 7.2): 1.8x–3.7x speedups with a 45.7x outlier; MTTKRP declines after 64 nodes due to Legion's handling of replicated regions.

## Principal limitation
As stated: users must write the distribution schedule (CTF automates it), recursive algorithms like CARMA are inexpressible (Sec. 4.1), Legion costs 5–10%, and only dense tensors are supported (Sec. 7, 9). Our observation: without a cost model the design space is explored manually.

## Relationship to earlier / later work
Extends TACO and targets Legion (Sec. 1, 5, 6). Compares against ScaLAPACK, CTF, COSMA (Sec. 7). Positions itself relative to HPF, ZPL, Chapel, Sequoia; Dryden et al. and FLAME distribution notations; polyhedral distributed compilation (Amarasinghe & Lam, Bondhugula) as possible MPI-backend analyses; Distributed Halide and Tiramisu (Sec. 8). Sparse support named as ongoing future work (Sec. 9). inferred: that work is SpDISTAL.

## Sources used
| claim | section / page |
|---|---|
| Motivation, LoC comparison, library critique | Sec. 1 |
| Three input sub-languages | Sec. 2, Fig. 2 |
| Machine grid, hierarchy | Sec. 3.1 |
| TDN syntax, fix/broadcast, coloring semantics | Sec. 3.2, Fig. 4–5 |
| distribute / communicate / rotate, execution spaces | Sec. 3.3, Fig. 6–8 |
| Algorithm case studies | Sec. 4, Fig. 9 |
| Concrete index notation rewrites | Sec. 5 |
| Legion lowering, mapper, partitions | Sec. 6.1–6.2 |
| Benchmarks and numbers | Sec. 7.1–7.2, Fig. 15–16 |
| Related work, static/dynamic discussion | Sec. 8 |
| Future work | Sec. 9 |

## Open questions for the survey
- How far can the TDN + schedule separation be automated, and what cost model would an auto-scheduler need?
- How much of the performance rests on Legion's runtime data movement versus the compile-time partition derivation?
- Does the abstract-grid machine model capture real topology (racks, NVLink islands) well enough for systolic schedules?
