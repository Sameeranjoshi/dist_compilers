# An MLIR Lowering Pipeline for Stencils at Wafer-Scale

**Catalog id:** `stawinoga2026mlir`  
**Citation:** Nicolai Stawinoga, David Katz, Anton Lydike, Justs Zarins, Nick Brown, George Bisbas, Tobias Grosser. "An MLIR Lowering Pipeline for Stencils at Wafer-Scale." ASPLOS 2026. DOI 10.1145/3779212.3790124 / arXiv 2601.17754.  
**Paper type:** compiler-technique  
**Access:** open (arXiv) — full text read.  
**Card status:** full-read

## Problem
The Cerebras Wafer-Scale Engine exposes an asynchronous, actor-like execution model through CSL: a time-step loop around communicating stencils cannot be written as a loop but must be recast into tasks and callbacks, and data must move in chunks because each PE has 48 kB (Sec. 2, Fig. 1). The authors hypothesize that stencil-level information already in MLIR pipelines suffices to generate optimized CSL with no application-level code changes (Sec. 1).

## Input abstraction
The architecture-agnostic `stencil` dialect as produced by PSyclone (Fortran DSL), Devito (SymPy-based Python DSL) and Flang with a stencil-extraction pass (Sec. 3). The pipeline starts from `stencil.apply`/`stencil.access` with value semantics (Listing 2).

## Target
Cerebras WSE2 (CS-2) and WSE3 (CS-3): up to 900,000 PEs, each with a core, router and 48 kB SRAM, four cardinal neighbor channels carrying 32-bit wavelets, 24 "colors" as virtual channels, 40/44 GB on-chip memory and no caches (Sec. 2).

## Data decomposition
A 3D x×y×z stencil is decomposed over the 2D PE grid so each PE holds one column of z values; z is "tensorized" (scalars become `tensor<512xf32>`), making operations rank-polymorphic (Sec. 5.1, Listing 3). Decomposition reuses the existing `distribute-stencil` pass and `dmp` dialect (`dmp.swap` with `#dmp.grid_slice_2d`, `#dmp.topo<254x254>`), originally built for MPI clusters. One column per PE follows Jacquelin et al. and is motivated by the PE count and small memory. The `csl-wrapper` dialect holds the layout metaprogram placing the (identical) program on PEs (Sec. 4.2, 5.2).

## Computation mapping
Each PE runs the same program on its column. `csl-stencil.apply` has two regions: one processing incoming remote chunks and one computing on local data (Sec. 4.1, Listing 4). These lower to software actors, a task activated per received chunk and one activated once all chunks from all neighbors arrive; enclosing control flow (e.g. the `scf.for` time loop) becomes a task graph of CSL functions and local tasks (Sec. 5.4). Compute goes through `linalg` (destination-passing style) to CSL DSD builtins such as `@fmacs` (Sec. 5.3, 5.5).

## Communication generation
`dmp.swap` becomes `csl-stencil.prefetch`, folded into `csl-stencil.apply` with `num_chunks` and exchange attributes (Sec. 5.2). Remote data is reduced chunk-by-chunk into an accumulator to save memory, constants may be applied to incoming data at zero cost, and only required column entries are sent (Sec. 4.1, 6.1). Wavelet routing is done by a CSL runtime library implementing Jacquelin et al.'s partitionable strategy for star-shaped stencils up to 3D, issuing asynchronous sends/receives in four directions; the WSE3 variant exploits improved switching (Sec. 5.6, 6). Generating hardware routing configurations is future work.

## Compiler / runtime split
Fully ahead-of-time: stencil → `dmp` → `csl-stencil` → `csl-wrapper` → `csl-ir`, with `tensor`, `linalg`, `memref`, bufferization and xDSL's `varith` in between; `csl-ir` is printed as CSL and compiled by the Cerebras SDK, whose staged compilation evaluates the layout metaprogram and `comptime` parameters (Sec. 4, 5, Fig. 3). Unlike CPU/GPU targets, stencil-level information is retained through most of the pipeline (Sec. 5). Optimization passes: stencil inlining, `varith-fuse-repeated-operands`, `linalg-fuse-multiply-add`, one-shot broadcast reductions (Sec. 5.7).

## Evaluation
Five benchmarks from three front ends: Jacobian (Flang, 6-pt), Diffusion and Acoustic (Devito, 13-pt), 25-point Seismic (Cerebras CSL), UVKBE (PSyclone); x×y sizes 100×100, 500×500, 750×994 (Sec. 6). Against the Cerebras-authored hand-written 25-pt kernel on WSE2 (28.2% of peak), generated code is up to 7.9% faster, attributed to single-chunk communication, sending only needed data and ~50% fewer tasks (Sec. 6.1, Fig. 5). WSE3 code is up to 38.1% faster than WSE2 (Fig. 4). The Devito acoustic kernel on one WSE3 is ~14x faster than 128 A100 GPUs and ~20x faster than 128 ARCHER2 nodes from Bisbas et al. 2025, with the stated caveat of differing problem sizes and an OpenACC baseline (Sec. 6.2, Fig. 6). All kernels are compute-bound on the WSE3 roofline (Sec. 6.3). Lines of code: 28–81 (DSL) versus 964–995 (full CSL) (Table 1).

## Principal limitation
As stated: the communication library covers star-shaped stencils only, hardware routing/switch generation is future work (Sec. 5.6), and the cluster comparison is not strictly direct (Sec. 6.2). Our observation: decomposition is fixed to one z-column per PE, so problems whose x×y footprint exceeds the PE grid are not addressed.

## Relationship to earlier / later work
Builds directly on Bisbas et al. 2024 (stencil/dmp dialects, xDSL, Devito/PSyclone integration) and Brown et al. 2023 (Flang stencil extraction); adopts the design of Rodriguez-Canal et al.'s FPGA lowering (Sec. 3). Communication strategy and hand-written baseline from Jacquelin et al. 2022 (Sec. 5.6, 6.1). Contrasted with Rocki et al., Woo et al., Sai et al., SPADA (Gianinazzi et al.), mlir-aie and tt-mlir (Sec. 7).

## Sources used
| claim | section / page |
|---|---|
| WSE architecture, CSL, actor model | Sec. 2, 2.1, Fig. 1 |
| Front ends and stencil dialect | Sec. 3, Listings 1–2 |
| csl-stencil, csl-wrapper, csl-ir | Sec. 4.1–4.3, Fig. 2 |
| Decomposition and tensorization | Sec. 5.1, Listing 3 |
| Placement, chunked communication, bufferization | Sec. 5.2–5.3, Listings 4–5 |
| Actor lowering, csl-ir, DSDs | Sec. 5.4–5.5 |
| Runtime communications library | Sec. 5.6 |
| Optimization passes | Sec. 5.7 |
| Benchmarks, results, LoC | Sec. 6.1–6.4, Fig. 4–7, Table 1 |
| Related work | Sec. 7 |

## Open questions for the survey
- Is the actor/task-graph lowering reusable for other CGRA-like spatial accelerators, and what IR would make it portable?
- How should decomposition parameters (columns per PE, chunk size) be chosen when the problem does not match the wafer geometry?
- Where should the boundary lie between compiler-generated routing and vendor runtime libraries for communication?
