# Compiling for a Dataflow Runtime on Distributed-Memory Parallel Architectures
**Catalog id:** `dathathri2014thesis`
**Citation:** Roshan Dathathri. "Compiling for a Dataflow Runtime on Distributed-Memory Parallel Architectures." MS (Engineering) thesis, Indian Institute of Science, Bangalore, April 2014. No DOI; record used: PDF title page and publication list.
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner. Full text read (113 pages including front matter and references); the text layer is complete for the prose. Figures were read as extracted labels only.
**Card status:** full-read

## Problem
Automatic data movement for affine loop nests on distributed-memory and heterogeneous systems can send much redundant data, and bulk-synchronous MPI makes task-level dataflow parallelism hard to express (Sec. 1.2-1.4). The thesis proposes a source-to-source framework that moves only the data that semantics require (Sec. 3) and generates a dynamically scheduled dataflow runtime (Sec. 4).

## Input abstraction
Sequential code with arbitrarily nested affine loop nests. Pluto tiles and parallelizes the code before the framework runs (Sec. 3.5, 4.3). An iteration of the innermost distributed loop is the atomic unit on which communication is parameterized (Sec. 3.2.1).

## Target
A 32-node InfiniBand cluster of dual quad-core Xeon nodes with MVAPICH2 (Sec. 3.6.1, 4.4.2). A heterogeneous node with 12 Xeon cores and four Tesla C2050 GPUs, and an AMD APU with two discrete GPUs, both programmed through OpenCL (Sec. 3.6.2). A four-socket Opteron for shared-memory tests (Sec. 4.4.1).

## Data decomposition
Data are replicated: the entire data is made available on every device, and the final result is collected at a master device (Sec. 3.5). Computation placement is block, or block-cyclic for non-rectangular spaces (Sec. 4.2.3).

## Computation mapping
Tiles, or tasks, are placed by a function pi. The placement can be fixed or chosen before task initialization (Sec. 3.2.1, 4.2.3).

## Communication generation
Three schemes are compared: flow-out (FO), flow-out intersection flow-in (FOIFI) and flow-out partitioning (FOP). FOP partitions the RAW dependences into source-distinct sets at compile time, so each partition goes only to its own receivers (Sec. 3.4). Each partition is packed as multicast or unicast, chosen by compile-time or run-time non-redundancy conditions (Sec. 3.4.5). Transfers use non-blocking MPI (Sec. 3.5, 4.2.1).

## Compiler / runtime split
Communication sets, pi and receiver tests are compiler-generated and evaluated at run time. A set of parameterized task functions, the Synthesized Runtime Interface (Table 4.1), lets each node schedule tasks from local counters without building the whole task graph in memory (Sec. 4.2.2). The distributed scheduler uses one receiver thread and compute threads (Sec. 4.2.1, 4.2.3).

## Evaluation
On the cluster, FOP reduces volume by 1.4x to 63.5x over FO, with mean speedups of 1.55x over FO and 2.19x over hand-optimized UPC (Sec. 3.6.1). On heterogeneous devices FOP gives a mean speedup of 1.53x over FO (Sec. 3.6.2). The dataflow runtime reaches a geometric-mean speedup of 143.6x over sequential on 32 nodes with 8 threads each, and 1.6x over a bulk-synchronous automatic scheme. On a shared-memory machine it reaches 23.5x on 32 threads (Sec. 4.4). Benchmarks: floyd, lu, adi, fdtd-2d, heat-2d, heat-3d, plus cholesky in Chapter 4.

## Principal limitation
As the thesis states it: FOP gives the minimum volume for a majority of dependence patterns, not all (Sec. 1.4, 6.1). The partitioning procedure is "presented as is for clarity" (Sec. 3.4.2). Automatic placement and data tiling are outside the work (Sec. 4.2.3, 6.2). On shared memory, hand-written CnC with explicit data tiling beats the automatic code on floyd, lu and cholesky (Sec. 4.4.1). Our observation: the cluster runs use different thread counts (adi uses one thread per node, Fig. 4.8e), so the 143.6x figure mixes node-count and runtime effects.

## Relationship to earlier / later work
- FOP builds on the flow-out scheme of Bondhugula [13], which the thesis says it "builds upon and subsumes" (Sec. 3.2.1, 5.3).
- Inter-task dependences are extracted in the manner of Baskaran et al. [8], which the thesis describes as shared-memory only (Sec. 4.2.2, 5.3).
- Compared with LWT [2], dHPF [1, 23], CLGR [24] and OMPD [34] (Sec. 3.6.1, 5.1).
- Related dataflow runtimes include CnC, DAGuE, DPLASMA, StarPU, SWARM and OCR (Sec. 5.4).
- The thesis states that Reddy and Bondhugula [45] build on this work with data tiling and general placement (Sec. 5.3).

## Sources used
| claim | section / page |
|---|---|
| Problem and bulk-synchronous limits | Sec. 1.2-1.4 |
| Input model and tiling | Sec. 3.2.1, 3.5, 4.3 |
| Platforms | Sec. 3.6.1, 3.6.2, 4.4 |
| Replicated data, master gather | Sec. 3.5 |
| FO, FOIFI, FOP | Sec. 3.2-3.4 |
| SRI and DFDS runtime | Sec. 4.2.2-4.2.3, Tables 4.1-4.2, Alg. 2-6 |
| Results | Sec. 3.6, 4.4, Tables 3.2-3.7 |
| Limitations | Sec. 3.4.2, 4.2.3, 4.4.1, 6.1, 6.2 |
| Related work | Sec. 5.1-5.4 |

## Open questions for the survey
- How often do the non-redundancy conditions of Sec. 3.4.5 fail on real dependence patterns, and what does the multicast fallback then cost?
- How much of the cluster gain in Sec. 4.4.2 survives once the baseline uses matched thread counts and data tiling, as in Reddy and Bondhugula [45]?
- Would the task functions of Table 4.1 need changing for GPU-resident task graphs, as the future work in Sec. 6.2 proposes?
