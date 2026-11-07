# Massively scalable stencil algorithm

**Catalog id:** `jacquelin2022wse`
**Citation:** Mathias Jacquelin, Mauricio Araya-Polo, Jie Meng. "Massively scalable stencil algorithm." arXiv:2204.03775v1, 7 Apr 2022. Preprint of the SC22 paper "Scalable Distributed High-Order Stencil Computations", DOI 10.1109/sc41404.2022.00035 (different title), not read.
**Paper type:** experience
**Access:** SC22 version paywalled, not read; open preprint read in full. Sections refer to the preprint.
**Card status:** full-read (of the preprint)

## Problem
Stencils are memory-bound on cache-hierarchy machines (§I, §II-A). The authors make a 25-point, 8th-order seismic wave-equation kernel compute-bound by "trading memory accesses for data communication" on the cache-less Cerebras WSE-2 (Abstract, §I).

## Input abstraction
Hand-written Cerebras Software Language (CSL), a Zig-based C-like language with explicit compile-time blocks, on Cerebras SDK 0.3.0; CSL "allows to express computations and communications across multiple cores" (§IV, §V-A). Visible constructs: array-view descriptors (`@get_dsd`) driving vector instructions such as `@fmacs` (Fig. 7b). Kernel: Minimod's acoustic isotropic kernel (§III).

## Target
CS-2 with WSE-2: 850,000 PEs, 48 KB SRAM each, 2D mesh routers with E/W/N/S links plus a ramp to the PE; packets carry a color that selects routing per router, orders a virtual channel, and can trigger a handler (§IV-A). No cache or shared memory (Table I). Fabric used: 755 x 994; baseline one NVIDIA A100 (§V-A).

## Data decomposition
X and Y are mapped onto the PE fabric, Z into a PE's local memory, "following the approach ... in Rocki et al. [24]" (§IV-B, Fig. 3a). Each PE owns a column of nz cells padded by 4 cells below and above (local padding, not a ghost region), two time steps stored (§IV-B, Fig. 3b). Work proceeds in blocks of size b, the largest that fits 2 x (nz + 8) cells plus buffers in memory (§IV-B, Table III). Our observation: no X/Y halo is stored; neighbour cells are consumed on the fly (§IV-C.2).

## Computation mapping
One PE per (x, y) column. Per block: four concurrent FMULs multiply the 5 x b incoming cells per direction by distance-dependent coefficients as they arrive, the centre term and previous time step folded into the West stream (§IV-C.2, §IV-D, Fig. 5); products are FADD-reduced into an accumulator; eight FMACs over local Z offsets finish the Laplacian, "embarrassingly parallel" since Z is PE-local (§IV-C.3, Figs. 6-7); FSUB updates the wavefield (§IV-D).

## Communication generation
Programmer-specified, router-executed. One color per neighbour as in Rocki et al. [24] "would have resulted in an excessive color use" for a 4-deep stencil, so the paper introduces "localized broadcast patterns": one per cardinal direction, two dedicated colors each (send, receive), concurrent on separate links (§IV-C.1). A Root PE sends b cells to its 4 neighbours in that direction (router configurations Root/intermediate/Last, Fig. 4a), then a router command to its own and the next 4 routers shifts the pattern one position; after 5 steps every PE has sent b and received 5 x b cells (4 neighbours plus itself, a hardware obligation) (§IV-C.1, Fig. 4b). Remote routing updates need no local-PE action, so computation continues, with "no bookkeeping" (§IV-C.1); no global reductions (§II-B). Our observation: this is the stencil's halo exchange, realised as hand-configured shifting multicasts, not generated code.

## Compiler / runtime split
Decomposition, colors, router configurations and block size are fixed by the programmer in CSL; the SDK compiler is not described (§IV). Run time is routing-table updates by in-band commands (§IV-A, §IV-C.1). No cost model or communication synthesis appears.

## Evaluation
Weak scaling at nz = 1000 from 200 x 200 to 755 x 994: 1,000-step time stays 0.0750-0.0764 s, over 98% efficiency, 9862.78 Gcell/s, 228x a single tuned A100 (§V-B, Table II, Figs. 8-9). An nz sweep 100-1,000 raises throughput slightly, read as confirming compute-boundedness (§V-B, Table III). Profiling: 69.6% busy cycles, load std. dev. 0.8%, 22 GFLOP/W (§V-C, Fig. 10). Roofline: 51 flops, 112 memory words, 17 fabric words per cell; 503 TFLOPs, compute-bound (§VI, Table IV, Fig. 11). Agreement with Minimod stated without figures (§V-A).

## Principal limitation
Authors: single-A100 baseline, multi-GPU "will likely narrow the gap" (§V-B); color budget "critical to the feasibility" (§IV-C.1); forced self-reception and extra flops (§VI); I/O and boundary kernels untested (§III). Our observation: every distribution and routing decision is hand-coded for one stencil shape, so the paper fixes requirements for a wafer-scale compiler rather than providing one.

## Relationship to earlier / later work
- Builds on Rocki et al. [24]: same X/Y-to-fabric, Z-to-memory mapping (§IV-B); replaces one-color-per-neighbour with localized broadcasts (§IV-C.1); fp32 only, no AXPY or reductions, so "not directly comparable" (§II-B).
- Baseline: Sai et al. [25], [26] A100 kernel; Minimod [18] (§III, §V-A).
- Precedents: Cell BE [3], Connection Machine [12], Anton 3 [28] (§I). Stencil DSLs cited as context: Devito [16], Gysi [11], ExaStencils [13], AN5D [17], Rawat [22] (§II-A).
- inferred: the catalog's SC22 record is the published form of this preprint.

## Sources used
| claim | section / page |
|---|---|
| Motivation, CSL, WSE-2 | Abstract, §I, §IV, §IV-A, Fig. 7b |
| Decomposition, compute, broadcast | §IV-B-D, Figs. 3-7 |
| Evaluation, roofline | §V-B-C, §VI, Tables II-IV, Figs. 8-11 |
| Relation to Rocki et al. | §II-B, §IV-B, §IV-C.1 |

## Open questions for the survey
- Does the SC22 version say what the SDK compiler generates?
- How to classify a halo exchange realised as router reconfiguration with no message code?
- Has any later tool automated color allocation?

## Reference list check
Total reference entries: 35 ([1]-[35]).

| line | present? | entry |
|---|---|---|
| High Performance Fortran | absent | |
| Fortran D | absent | |
| Kali | absent | |
| Koelbel 1991 | absent | |
| Saltz / PARTI / CHAOS | absent | |
| Vienna Fortran | absent | |
| Rocki et al. 2020 (Cerebras stencil, SC20) | yes | [24] K. Rocki, D. Van Essendelft, I. Sharapov, R. Schreiber, M. Morrison, V. Kibardin, A. Portnoy, J. F. Dietiker, M. Syamlal, and M. James, "Fast stencil-code computation on a wafer-scale processor," SC20, 2020, pp. 1-14. (Rocki 2020) |
| Legion | absent | |
| Sequoia | absent | |
| Chapel | absent | |
| Halide | absent | |
| Co-Array Fortran | absent | |
| Mesh-TensorFlow | absent | |
| GSPMD | absent | |

The only compiler or DSL works cited are stencil-specific: Devito [16], Gysi et al. [11], ExaStencils [13], AN5D [17], Rawat et al. [22], and the OpenACC/OpenMP directive studies [9], [21].
