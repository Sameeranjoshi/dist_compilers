# A shared compilation stack for distributed-memory parallelism in stencil DSLs

**Catalog id:** `bisbas2024shared`  
**Citation:** George Bisbas, Anton Lydike, Emilien Bauer, Nick Brown, Mathieu Fehr, Lawrence Mitchell, Gabriel Rodriguez-Canal, Maurice Jamieson, Paul H. J. Kelly, Michel Steuwer, Tobias Grosser. "A shared compilation stack for distributed-memory parallelism in stencil DSLs." ASPLOS 2024. DOI 10.1145/3620666.3651344 / arXiv 2404.02218.  
**Paper type:** compiler-technique  
**Access:** open (arXiv) — full text read.  
**Card status:** full-read

## Problem
Stencil DSL compilers (Devito, PSyclone, the Open Earth Compiler) are siloed and each reimplements generic HPC machinery: OpenMP directives, MPI halo exchange, vectorization, tiling (Sec. 1, Fig. 1a). MLIR provides shared dialects for arithmetic, loops, GPUs and OpenMP but none for distributed-memory parallelism (Sec. 4). The paper contributes SSA dialects for domain decomposition and message passing so distributed stencil code generation becomes a shared component.

## Input abstraction
Front ends keep their interfaces: Devito's SymPy-based symbolic equations (Listing 5), PSyclone's Fortran with coding conventions (NEMO API), and the OEC stencil IR. All lower to a common `stencil` dialect (`field`, `temp`, `load`, `apply`, `access`, `store`, `return`) with value semantics, extended by the authors with bounds carried in types, arbitrary dimensionality and a tiling-based CPU lowering (Sec. 4.1, 5).

## Target
CPU clusters (ARCHER2 HPE Cray EX, dual AMD EPYC 7742, Slingshot), NVIDIA V100 GPUs (Cirrus) via the MLIR `gpu`/CUDA path, and an AMD Alveo U280 FPGA via an HLS dialect (Sec. 6, Table 1).

## Data decomposition
The `dmp` dialect expresses geometric decomposition into "rank-local" domains. A shared pass, parameterized by rank topology and a *decomposition strategy* class, equally decomposes the `stencil` domain across ranks; the stencil dialect adds halos whose shape is derived from `stencil.access` offsets (Sec. 4.1–4.2). `dmp.swap` carries a `dmp.grid` Cartesian topology and a list of `dmp.exchange` attributes, each naming a rectangular receive region, its size, the send offset and the relative neighbor (Listing 2, Fig. 3). A standard slicing strategy covers 1D, 2D and 3D; only contiguous hyper-rectangular subdomains are supported.

## Computation mapping
Each MPI rank computes the stencil over its local domain (Fig. 4). Within a rank, `scf.parallel` lowers to the `omp` dialect (with tiling) or the `gpu` dialect; the FPGA path uses the HLS dialect (Sec. 5, 6). No placement optimization beyond the decomposition strategy is described.

## Communication generation
`dmp.swap` is inserted before every `stencil.load`; an SSA data-flow pass removes redundant exchanges (Sec. 4.2). Lowering to the `mpi` dialect allocates temporary buffers, builds the exchange mapping, packs/unpacks, issues non-blocking `mpi.isend`/`mpi.irecv` and ends with `mpi.waitall`; loop-invariant calls are hoisted (Sec. 4.3, Fig. 4). The `mpi` dialect mirrors a subset of MPI 1.0 (point-to-point, Isend/Irecv, Test/Wait/Waitall, Reduce/Allreduce, Bcast/Gather, init/finalize), has been upstreamed to MLIR, and lowers to `func` calls with constants extracted from mpich headers. The authors note there is no communication/computation overlap and one exchange per halo (Sec. 4.2 Limitations).

## Compiler / runtime split
Entirely ahead-of-time: the stencil dialect needs compile-time-known bounds, so a new problem size means recompilation (Sec. 4.1 Limitations). Pipeline: xDSL (Python MLIR clone) for the new dialects → MLIR standard dialects → LLVM IR via `mlir-opt`; PSyclone's non-stencil Fortran goes through FIR/Flang and links with stencil objects (Sec. 3, 5.2.1, Fig. 6). The only runtime is the MPI library.

## Evaluation
Devito: 2D/3D heat diffusion and acoustic wave at space orders 2/4/8 (Sec. 6.1). Single node (8 ranks × 16 threads): xDSL-Devito 1.2–1.5x faster on low-arithmetic-intensity kernels, 0.6–0.8x on high-AI ones, attributed to weaker vectorization (Fig. 7). Strong scaling to 128 nodes / 1024 ranks / 16384 cores follows Devito's trend, but Devito stays faster thanks to diagonal exchanges (Fig. 8). On V100, the CUDA lowering beats Devito's OpenACC by >1.5x on 3D kernels (Fig. 9). PSyclone (PW advection, NEMO tracer advection, Sec. 6.2): single node slightly exceeds Cray-compiled PSyclone on PW but lags on tracer advection (18 separate OpenMP regions); on GPU up to 24x on PW and 0.62–0.95x on tracer advection; FPGA throughput improves 100–214x after dataflow optimization (Table 1); strong scaling to 8 nodes with a 2D decomposition (Fig. 11).

## Principal limitation
As stated: compile-time bounds, no boundary-condition abstraction, hyper-rectangular domains only, one exchange per halo (hindering overlap and diagonal exchanges), and inefficient `scf.parallel` → OpenMP/GPU lowerings (Sec. 4.1, 4.2, 6, 8). Our observation: decomposition is static and uniform, with no load balancing or cost model.

## Relationship to earlier / later work
Extends the Open Earth Compiler's stencil and GPU dialects (Gysi et al. 2021) and uses xDSL (Fehr et al. 2023) (Sec. 2–4.1). Integrates Devito and PSyclone (Sec. 5); compares against native Devito, whose MPI support is in Bisbas et al. 2023, and PSyclone (Sec. 6). FPGA path from Rodriguez-Canal et al. 2023 (Sec. 6.2). Related work lists Distributed Halide, ExaSlang, PETSc, ParallelStencil.jl, MSC, OPS (Sec. 7).

## Sources used
| claim | section / page |
|---|---|
| Siloed DSLs, missing DMP in MLIR | Sec. 1, 4, Fig. 1 |
| Stencil dialect and extensions | Sec. 4.1, Listing 1 |
| dmp dialect, decomposition strategy, halos | Sec. 4.2, Listing 2, Fig. 3 |
| mpi dialect and lowering | Sec. 4.3, Fig. 4, Listings 3–4 |
| Devito / PSyclone integration, pipeline | Sec. 5, Fig. 6 |
| Hardware, numbers | Sec. 6, Fig. 7–11, Table 1 |
| Limitations and future work | Sec. 4.1, 4.2, 8 |
| Related work | Sec. 7 |

## Open questions for the survey
- Can `dmp` be generalized beyond hyper-rectangular halo exchange (unstructured, sparse, adaptive) without losing its static simplicity?
- How should overlap and diagonal exchanges be expressed at the IR level rather than in per-DSL runtimes?
- Where is the right boundary between a generic `mpi` dialect and domain-specific decomposition dialects once other domains join the stack?
