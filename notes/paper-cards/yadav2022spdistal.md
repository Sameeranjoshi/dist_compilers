# SpDISTAL: Compiling Distributed Sparse Tensor Computations

**Catalog id:** `yadav2022spdistal`  
**Citation:** Rohan Yadav, Alex Aiken, Fredrik Kjolstad. "SpDISTAL: Compiling Distributed Sparse Tensor Computations." SC22, 2022. DOI 10.1109/SC41404.2022.00064 / arXiv 2207.13901.  
**Paper type:** full-system  
**Access:** open (arXiv) — full text read.  
**Card status:** full-read

## Problem
Distributed sparse tensor algebra is served by libraries (PETSc, Trilinos) with fixed operations, formats and distributions, or by interpreters (CTF) that reduce expressions to distributed matrix operations and, per the authors, run one to two orders of magnitude slower (Sec. I). DISTAL separates data and computation distribution but has no notion of sparsity. SpDISTAL adds sparse data structures so that they compose with the distribution languages, and compiles to a task-based runtime for CPU and GPU nodes.

## Input abstraction
Tensor index notation (TACO/DISTAL syntax); TACO's per-dimension format language (Dense, Compressed levels); DISTAL's tensor distribution notation (TDN) for placement; and a scheduling language combining TACO's sparse iteration-space transformations (including non-zero strip-mining variants of split/divide, fuse, parallelize) with DISTAL's `distribute` and `communicate` (Sec. II-A–C, Fig. 1). The authors state this combination is unique to SpDISTAL.

## Target
Nodes with multi-core CPUs and multiple GPUs; evaluated on Lassen (40-core Power9, 4 V100, NVLink 2.0, InfiniBand EDR) (Sec. VI). Leaf kernels use OpenMP on CPUs and cuSPARSE or TACO-generated code on GPUs.

## Data decomposition
TDN gains three constructs (Sec. II-B, Fig. 5): a *universe partition* (default) splits a dimension's full coordinate range equally; a *non-zero partition* (`d̃`) splits stored non-zeros equally; *coordinate fusion* (`xy→f`) collapses dimensions so a matrix's non-zeros can be distributed evenly. Tensors are represented with Legion-ecosystem abstractions: index spaces, regions, and partitions (possibly overlapping). Each coordinate-tree level is Dense (an index-space `dom`) or Compressed (a `pos` region of lo/hi tuples plus a `crd` region) (Sec. III).

## Computation mapping
`distribute` assigns loop iterations to processors. Two SpMV schedules illustrate the space: row-based (distribute blocks of `i`) and non-zero-based (fuse `i`,`j`, non-zero split, distribute), the latter trading reduction traffic for load balance (Sec. II-D). Code generation maps coordinate-value loops to universe partitions and coordinate-position loops to non-zero partitions (Sec. IV-C).

## Communication generation
`communicate` sets granularity only; the compiler infers what moves and between whom (Sec. II-C). Communication is derived from partitions rather than messages: for each distributed index variable the generated code builds an initial level partition of every tensor, then derives the full coordinate-tree partition upward and downward via `image`/`preimage` dependent-partitioning calls emitted by new level functions (Table I, Fig. 9). Overlapping sub-regions (e.g., a shared parent coordinate) are kept coherent by the runtime. Sparse outputs reuse the input's metadata when the pattern is preserved, otherwise a two-phase assembly is used (Sec. V-B). No cost model is given.

## Compiler / runtime split
Compile time: schedule rewriting, generation of specialized partitioning code and leaf kernels. Run time: Legion executes the partitioning as distributed image/preimage operations without centralizing data, moves sub-regions between memories and manages coherence (Sec. III-A, V-A). The authors describe the design as combining compilation with runtime analysis to avoid imperative data-flow analyses (Sec. I).

## Evaluation
14 matrices/tensors from SuiteSparse, FROSTT and Freebase (Table II); kernels SpMV, SpMM, SpAdd3, SDDMM, SpTTV, SpMTTKRP; baselines PETSc 3.16.3, Trilinos/Tpetra 13.2.0, CTF (Sec. VI). CPU strong scaling to 16 nodes: median 1.8x/1.2x (SpMV) and 2.01x/3.8x (SpMM) over PETSc/Trilinos; 11.8x/38.5x on SpAdd3 via fusion; versus CTF 299x (SpMV), 161x (SpTTV), 19.2x (SpAdd3), 15.3x (SDDMM), and 97% of CTF on SpMTTKRP (Sec. VI-A.1). GPU: fastest in 28/38 SpMV configurations (1.07x/1.65x), 34/49 SpMM, 32/34 SpAdd3; GPU kernels 4.3x/2.0x/2.2x over SpDISTAL-CPU on SDDMM/SpTTV/SpMTTKRP (Sec. VI-A.2). SpMV weak scaling on banded matrices to 64 nodes/256 GPUs: 90–92% of PETSc on CPU, 1.05–1.29x on GPU (Sec. VI-B).

## Principal limitation
As stated: the prototype supports only some statement/output-format combinations (Sec. V-B); non-zero-based leaf kernels cost more synchronization than they gain on CPUs (Sec. VI-A.1); the memory-conserving GPU SpMM schedule is hypothesized to send more messages than Trilinos (Sec. VI-A.2). Our observation: formats, distributions and schedules are still chosen by hand.

## Relationship to earlier / later work
Extends DISTAL and TACO; targets Legion and its dependent partitioning (Sec. I, V). Uses Chou et al.'s format abstraction, Senanayake et al.'s sparse transformations and Henry/Hsu et al. for input construction (Sec. IV-B, VI). Compares against PETSc, Trilinos, CTF (Sec. VI); related work covers Herault et al., Bik, Halide/TVM/TC/Tiramisu, Distributed Halide (Sec. VII).

## Sources used
| claim | section / page |
|---|---|
| Library vs interpretation critique; contributions | Sec. I |
| Format, TDN extensions, scheduling language | Sec. II-B, II-C, Fig. 5 |
| Row vs non-zero SpMV schedules | Sec. II-D |
| Index space / region / partition, image & preimage | Sec. III-A, Fig. 6 |
| Coordinate tree encoding | Sec. III-B, Fig. 7 |
| Partition level functions, codegen | Sec. IV-B, IV-C, Table I, Fig. 9 |
| Legion implementation, sparse outputs | Sec. V-A, V-B |
| Experimental setup, numbers | Sec. VI, Table II, Fig. 10–13 |
| Related work | Sec. VII |

## Open questions for the survey
- Dependent partitioning moves sparse ownership computation to the runtime: what does it cost at scale, and could structured sparsity be handled statically?
- How do universe/non-zero/fused partitions compare with graph partitioning used by other sparse systems?
- Is the balance-versus-reduction-traffic trade-off amenable to an automatic selector?

## Reference list check (arXiv 2207.13901, checked 2026-11-07)
34 entries. Absent: Saltz 1990/1991, PARTI, CHAOS (Ponnusamy, Das), Kali (Mehrotra, Koelbel), HPF, Fortran D, Vienna Fortran, Koelbel 1991. Present: Legion [16], dependent partitioning (Treichler et al.) [14], Halide [21], distributed Halide [34], Tiramisu [23], DISTAL [13].
