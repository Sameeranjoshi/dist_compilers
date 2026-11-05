# Distributed Sparse Tensor Computations in MLIR

**Catalog id:** `vaidya2025distributed`
**Citation:** Miheer Vaidya, Shreya Singh, Devanshu Mantri, Michael Shannon Eydenberg, Brian Michael Kelley, Sivasankaran Rajamanickam, Atanas Rountev, P. Sadayappan. "Distributed Sparse Tensor Computations in MLIR." SC Workshops '25 (Workshops of the International Conference for High Performance Computing, Networking, Storage and Analysis; the catalog's "LLVM-HPC 2025" label does not appear in the text), 2025. DOI 10.1145/3731599.3767484.
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner — full text read.
**Card status:** full-read

## Problem
Sec. 1: distributed sparse-tensor code is written against MPI's partitioned address space, with the programmer slicing tensors per process and orchestrating every transfer. MLIR's TACO-derived `sparse_tensor` dialect [4] covers single-node sparse code but, the authors state, nothing exists for distributed sparse tensors. The goal is a productive "global partitioned view" of such tensors inside MLIR, with types, operations, lowering and runtime support.

## Input abstraction
Naming: the text never calls PartTensor a tool or system. It is "the PartTensor dialect" (Sec. 1, 3, 4.2, 5, 6.1), MLIR namespace `part_tensor` (Fig. 2 caption "Partitioned BSDDMM using part_tensor"); the name also labels the "PartTensor conversion pass" (Sec. 3.2.1) and the "PartTensor runtime library" (Sec. 3.2.2). Input is an ordinary MLIR module: `sparse_tensor` encodings (`#csr`, `#csrv`) and `linalg.generic` with affine iteration-to-data maps (Sec. 2, Fig. 1). The dialect adds `part_tensor.encoding` wrappers (`#partCsr`) and ops `get_my_partition`, `get_slice`, `set_slice`, `update_slice`, `active_mask`, `get_slice_for_active_mask` (Sec. 3.1). A distributed operator is a set of local applications of the unchanged operator on hyper-rectangular slices; the dialect only builds the local operands (Sec. 1).

## Target
MPI processes on CPU clusters; after lowering, LAPIS [11] maps `scf` loops to Kokkos [8] for CPU or GPU nodes (Sec. 3.2.1, 5). Experiments: up to 4 nodes of 40-core Xeon Gold 6230, EDR InfiniBand, OpenMPI 4.1.6, with MPI ranks also used within nodes because multithreading was disabled (Sec. 5).

## Data decomposition
A tensor's modes span a Cartesian data space partitioned into disjoint hyper-rectangles, the "tensor partitions", one per process (Sec. 3.1.1). The dialect is "agnostic of the partitioning scheme": partitions may be non-uniform, the only assumption being disjoint coverage, so developers choose partitions from knowledge of sparsity (Sec. 3.1.1, 6.2). Partitions are materialized at run time by `NewPartTensor`, which filters coordinate/value lists against the local hyper-rectangle (Sec. 3.2.2); `get_my_partition` returns a bounds buffer (Sec. 3.1.1). Slices are requested in global coordinates and returned as zero-based local sparse tensors (Sec. 3.1.2). The GAT use case 1D-partitions every tensor along its outermost dimension and replicates the small weights (Sec. 4.2).

## Computation mapping
Owner-computes over the output partition: a process takes its own partition spec of the result, derives the input slices by inverting the operator's affine map on the iteration space (reduction axis in full) and applying the input maps (Sec. 3.1.4), gathers them, runs the unchanged `linalg.generic`, and writes back with `set_slice` (Sec. 3.1.2-3.1.3). The derivation is presented as reasoning the MLIR author follows (specs are explicit in Fig. 2); no automatic placement exists, and partition selection is future work (Sec. 3.1.1).

## Communication generation
All inter-rank movement goes through `get_slice`, `set_slice` and `update_slice`, blocking collectives executed by every rank; since they are the only primitives, any sequence is race-free (Sec. 3.1.2-3.1.3). `GetSlice` serves local requests directly; otherwise an MPI all-to-all exchanges slice requests, ranks pack sub-slices, and an all-to-allv moves values (Sec. 3.2.2). `set_slice` writes disjoint slices; `update_slice` accumulates overlapping contributions at the owning process (Sec. 3.1.3). Volume is reduced by compatible partitionings that make slices local (Sec. 3.1.5) and by sparsity masks: `active_mask` lists columns of A with local non-zeros and `get_slice_for_active_mask` fetches only those rows of K, costing an all-to-all, an all-to-allv for masks, packing, an all-to-allv for values and unpacking (Sec. 3.1.6, 3.2.2). MPI is not exposed in MLIR; there is no non-blocking communication, no early scheduling and no cost model (Sec. 3.1.1-3.1.2).

## Compiler / runtime split
Compile time: a PartTensor conversion pass removes all PartTensor ops and types, turning some into runtime-library calls; `sparse_tensor` passes then do TACO-style loop generation into `scf`; LAPIS lowers to Kokkos (Sec. 3.2.1). Stack: `part_tensor` -> `sparse_tensor`/`linalg` -> `scf` -> Kokkos. Run time: an MPI library modelled on `SparseTensorRuntime` holds partitions, resolves slice ownership, packs and communicates (Sec. 3.2.2). Partition specifications are not needed at compile time (Sec. 6.2).

## Evaluation
One application, a GAT layer (projections, BSDDMM, softmax, BSPMM, Linear; Sec. 4.1), on OGB ogbn-arxiv (169,343 nodes, 1,166,243 edges) and ogbn-products (2,449,029 nodes, 61,859,140 edges), F=256, 16 heads of 16 (Sec. 5). 1, 2 and 4 nodes with 1-32 ranks per node, up to 128 ranks; metric is the slowest rank, best of four runs; results are speedup curves only (Figs. 4-5), without absolute times or an external baseline. The authors report that performance depends mainly on total rank count, masks improve scalability on ogbn-arxiv, and masks are slower on ogbn-products for 2-64 ranks because active column segments stay numerous and packing/metadata overhead dominates (Sec. 5).

## Principal limitation
Stated: partition selection is manual, automation via sparsity analysis and cost modelling is future work (Sec. 3.1.1); no overlap or non-blocking communication (Sec. 3.1.2); the mask/no-mask choice needs a predictor (Sec. 5); multithreading was disabled because upstream `sparse_tensor` lowering races on BSDDMM/BSPMM (Sec. 5). Our observation: a single application, relative speedups and no comparison with SpDISTAL or hand-written MPI support scalability, not competitiveness.

## Relationship to earlier / later work
- Builds on MLIR `sparse_tensor` [4] (TACO [10]), LAPIS [11], Kokkos [8] (Sec. 1, 3.2.1).
- Contrasted with the MLIR `mpi` dialect [15] (lower level) and the Stencil dialect [5] (stencil-specific) (Sec. 6.1).
- Contrasted with the `shard` dialect [16]: explicit collectives, dense, uniform grid partitions, versus hidden communication and non-uniform partitions; Shardy [17] draws on GSPMD [22] and PartIR [1] (Sec. 6.1).
- SpDISTAL [23]: stand-alone, Legion-based, partition specs at compile time; PartTensor is an MLIR building block and partition-agnostic (Sec. 6.2).
- GSPMD-style frameworks ignore sparsity; Trilinos Tpetra `Map` import/export and PETSc resemble the mask and slice primitives (Sec. 6.2).
- inferred: the cost-model future work points toward kong2023automatic, which shares two authors.

## Sources used
| claim | section / page |
|---|---|
| Problem framing, three contributions | Sec. 1 (pp. 1088-1089) |
| Sparse input form, BSDDMM example | Sec. 2, Fig. 1 |
| Dialect name and ops, tensor partitions | Sec. 3, 3.1.1, Fig. 2 |
| get/set/update_slice semantics, race freedom | Sec. 3.1.2, 3.1.3 |
| Slice-spec derivation via affine maps | Sec. 3.1.4 |
| Compatible partitioning, sparsity masks | Sec. 3.1.5, 3.1.6 |
| Lowering pipeline, runtime library, MPI collectives | Sec. 3.2.1, 3.2.2 |
| GAT operators and partitioning | Sec. 4.1, 4.2 |
| Hardware, datasets, results, multithreading disabled | Sec. 5, Figs. 4-5 |
| Related work comparisons | Sec. 6.1, 6.2 |
| Future work on cost models | Sec. 3.1.1, 5, 7 |

## Open questions for the survey
- Can a solver-based mapper in the style of DiMage choose PartTensor partitions and the mask/no-mask variant from sparsity statistics?
- `get_slice` is a blocking all-to-allv pull per operator; how does it compare with inspector-executor schedules that amortize the request phase across repeated executions?
- What would interoperation between `part_tensor` and the `shard` dialect's device meshes require for mixed dense/sparse pipelines?
