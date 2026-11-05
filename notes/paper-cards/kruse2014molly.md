# Introducing Molly: Distributed Memory Parallelization with LLVM

**Catalog id:** `kruse2014molly`
**Citation:** Michael Kruse. "Introducing Molly: Distributed Memory Parallelization with LLVM." arXiv:1409.2088 [cs.PL], 7 Sep 2014. (The extracted text prints no author block; the author is taken from the arXiv record. The text carries a PLDI '14 template header with a placeholder DOI and is treated as an unrefereed preprint.)
**Paper type:** compiler-technique
**Access:** open — full text read.
**Card status:** full-read

## Problem
MPI and hybrid MPI/OpenMP programming is tedious, and the best data layout differs per machine, so performance-critical code is rewritten per platform (Sec. 1). The author's hand-optimization of a Lattice QCD code on Blue Gene/Q, where repeated layout changes forced rewrites of conceptually similar code, motivates a compiler that generates communication boilerplate while the programmer keeps control over layout and placement (Sec. 1, 8).

## Input abstraction
C++ with `#include <molly.h>`. Distributed arrays ("fields") are `molly::array<T, N0, N1, ...>` globals with compile-time shape; indexing lowers to the builtin `__builtin_molly_ptr` and the LLVM intrinsic `llvm.molly.ptr`, which "logically allows accessing remote memory" (Sec. 3.1-3.2, Fig. 2). Pointer arithmetic on fields is invalid; loops must be Polly-detectable SCoPs. Proposed but unimplemented: `#pragma molly transform(...)` for explicit layouts and `#pragma molly where(...)` for explicit statement placement (Sec. 7.1-7.2).

## Target
Homogeneous distributed-memory machines; concretely IBM Blue Gene/Q (Juelich) with MPI as the only backend; BG/Q SPI, SHMEM, PAMI and PGAS listed as future backends (Sec. 1, 4.4, 6).

## Data decomposition
Six spaces are modelled: statements, the *cluster space* P of node coordinates, iteration domains, fields, index sets, scatter space (Sec. 4.1). A field's *home location* pi_e : I_e -> 2^P maps each element to its storing node(s). Only a fixed block distribution with equal, non-overlapping blocks is implemented: an 8 x 8 node mesh with 128^2 tiles, pi(w, h) = (floor(w/128), floor(h/128)) (Sec. 5, Eq. 26). Sizes and geometry must be compile-time constants because i = p(N/P) + l is otherwise non-affine (Sec. 1). Future layouts: pragma-defined maps, tiling, space-filling curves, indirect addressing, dynamic switching (Sec. 7.1).

## Computation mapping
Each statement has a *where-mapping* pi_S : D_S -> 2^P and an *execution* is (S, i, p) (Sec. 4.1). Default is owner-computes: statements feeding the epilogue run at their data's home location, statements producing node-local scalars must run wherever consumed, so non-field flows pin the whole Game-of-Life body to pi_back(x, y) (Sec. 3.2, 3.4, 5). The executing node's coordinate becomes a SCoP parameter so Polly can restrict domains (Sec. 4.1).

## Communication generation
Only flow (RAW) dependences are used, computed exactly by ISL after each field access is isolated into its own statement and virtual *prologue*/*epilogue* statements are added (Sec. 3.3, 4.1). A `Transfers` relation links chunk representative, generator execution, consumer execution and field element. To avoid single-value messages, instances are grouped into *chunks* by a *chunking function* phi (Defs. 1-2); Algorithm 1 takes the outermost loop level at which all consumers follow all generators without violating dependences, giving one chunk per time step in the example. Per chunk, six statements replace the originals (`molly_send_wait`, buffer-writing generator, `molly_send`, `molly_recv_wait`, buffer-reading consumer, `molly_recv`), scheduled by scatter functions around the first generator and last consumer (Eqs. 2-4). Communication is point-to-point and asynchronous: MollyRT maps setup to MPI persistent requests, waits to `MPI_Wait`, send/recv to `MPI_Start` (Sec. 4.4); accesses outside SCoPs fall back to synchronous `molly_value_load/store` (Sec. 4.3). No cost model; the goal is few, equal-sized chunks.

## Compiler / runtime split
All decisions are compile-time. Clang emits intrinsics and per-field metadata; the module-level Molly pass intercepts Polly after SCoP detection and dependence analysis, rewrites the SCoP, then Polly applies optional PLuTo/ISL scheduling and CLooG/ISL code generation (Sec. 3.2-3.4, 4.2). Link-time optimization matters because layout is global. MollyRT wraps `main`, initializes MPI and aborts if the node geometry differs from the compiled one (Sec. 4.3-4.4). JIT is noted only as a reason for choosing LLVM (Sec. 1).

## Evaluation
A reduced 5-point Game of Life, 100 iterations, on Blue Gene/Q (Sec. 6, Table 1). With a 128^2 tile per rank the run takes ~1 s from 4 x 4 nodes (512^2) to 32 x 32 nodes (4096^2), read as near-perfect weak scaling; 4x larger tiles take 4x longer. The largest run, 128 x 128 nodes with 64 ranks each on a 16384^2 field, takes 1.7 s (16,168.6 million site updates/s). The author cautions that an optimized Game of Life reaches this without thousands of nodes and that generated code has unnecessary 32/64-bit conversions. No hand-written baseline is given.

## Principal limitation
Sec. 7: the prototype is "yet unusable for practical uses": no reductions (seen as non-field dependences forcing replication everywhere), scalar elements only, no periodic boundaries, no runtime layout information, globals only, no conditionals, plus compile-time geometry (Sec. 1). Our observation: the motivating QCD comparison against the manual code is deferred to the author's thesis, so the central claim is untested here.

## Relationship to earlier / later work
- Built on Clang/LLVM [9, 10], Polly [11], ISL [12], PLuTo [24], CLooG [25] (Sec. 1, 4.2).
- "Most similar" is Adve and Mellor-Crummey's dHPF [14] (integer-set communication events = Molly's chunks; Omega; block-cyclic; owner-computes); also HPF [13], Last Write Tree [16], Dathathri et al. [17] (Sec. 2).
- Tile-based virtual-processor approaches [18-20], naming Bondhugula's 2011 IISc report [18] and Classen and Griebl [19]; Ravishankar et al. [21]; ZPL [22]; OpenACC, OmpSs, C++ AMP, UPC (Sec. 2).
- Chunking after Bastoul and Feautrier [23]; element modelling after alpha [6, 7] and Groesslinger [8] (Sec. 1, 4.1).

## Sources used
| claim | section / page |
|---|---|
| Motivation, non-affine blocks | Sec. 1 |
| Fields, intrinsic, metadata | Sec. 3.1-3.2, Figs. 1-2 |
| Spaces, home location, where-mapping | Sec. 4.1 |
| Owner-computes default | Sec. 3.2, 3.4, 5 |
| Chunking, six statements, scatter eqs. | Sec. 4.1, Alg. 1, Eqs. 1-4 |
| MollyRT / MPI | Sec. 4.3-4.4 |
| Polly pipeline | Sec. 3.3, 4.2 |
| Example distribution | Sec. 5, Eqs. 26-28 |
| Results | Sec. 6, Table 1 |
| Missing features, pragmas | Sec. 7-7.2 |
| Related work | Sec. 2 |

## Open questions for the survey
- Molly models array elements, not only iterations, as polyhedral points; did later LLVM/MLIR distributed-memory work adopt element-level layout modelling?
- The compile-time geometry restriction follows from affine modelling; how do other polyhedral systems (e.g. Bondhugula 2011's runtime pi/sigma helpers) trade this against generality?
- Was the QCD application or the pragma-based explicit layout ever published with results against the hand-optimized code?
