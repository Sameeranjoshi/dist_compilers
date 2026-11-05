# Sequoia: Programming the Memory Hierarchy
**Catalog id:** `fatahalian2006sequoia`
**Citation:** Kayvon Fatahalian, Timothy J. Knight, Mike Houston, Mattan Erez, Daniel Reiter Horn, Larkhoon Leem, Ji Young Park, Manman Ren, Alex Aiken, William J. Dally, Pat Hanrahan. "Sequoia: Programming the Memory Hierarchy." SC2006, Tampa, Florida, 2006. No DOI printed in the supplied PDF; IEEE copyright line 0-7695-2700-0/06 used.
**Paper type:** language
**Access:** PDF supplied by the repository owner. Full text read; the text layer is complete (13 pages, references included).
**Card status:** full-read

## Problem
On exposed-communication machines, software must move data between separate address spaces at node level as well as across a cluster (Abstract, Sec. 1). Distribution-based languages such as UPC, Chapel and X10 address horizontal communication but not movement through a memory hierarchy (Sec. 1). Sequoia makes both kinds explicit while keeping programs portable (Sec. 1).

## Input abstraction
Programs are trees of tasks: side-effect-free functions with call-by-value-result parameters. Blocking primitives (rchop, ichop, gather) and mapping primitives (mappar, mapseq, mapreduce) express decomposition (Sec. 3.1-3.3, Table 1). Tasks can have several variants, and tunables are fixed at specialization (Sec. 3.4, 3.5).

## Target
Machines are modeled as trees of memory modules, with virtual levels for clusters (Sec. 2, Figs. 2-3). The evaluated platforms are a dual-Cell blade (16 SPEs in total) and a 16-node cluster of PCs connected by InfiniBand (Sec. 6).

## Data decomposition
Arrays are cut into regular, irregular (ichop) or index-selected (gather) blocks, and a generalized rchop can yield overlapping blocks (Sec. 3.3, Table 1). On the cluster, the mapping specification distributes arrays in a 2D block-block layout with 1024 by 1024 blocks (Sec. 4, Fig. 8).

## Computation mapping
mappar and mapreduce iterate over blocks in parallel. Subtasks run in isolation, so no locks are needed (Sec. 3.2, 3.3). Task instances bind tasks to machine levels, and the mapping specification sets the grid partition of a mappar loop (Sec. 3.5, Fig. 8).

## Communication generation
Communication occurs only through task arguments, which are copied by call-by-value-result (Sec. 3.1). On the cluster, argument blocks move by non-blocking MPI and are double-buffered or software-pipelined (Sec. 5.2, Fig. 8). On Cell, DMA transfers overlap parallel tasks (Sec. 5.1). Copies between parent and child in one memory level are removed statically on Cell and at runtime on the cluster (Sec. 5.3).

## Compiler / runtime split
The compiler emits C code that links to a platform runtime (Sec. 5). The per-machine mapping specification, separate from source, holds tunables, variant choices and copy directives (Sec. 4, Figs. 7-8). The compiler is not required to search or infer mappings (Sec. 4).

## Evaluation
Table 3 reports GFLOP/s for SAXPY, SGEMV, SGEMM, ITERCONV2D, FFT3D, GRAVITY and HMMER (Table 2). The text reports over 160 GFLOP/s for SGEMM on two Cells and nearly 100 GFLOP/s on the cluster (Sec. 6.1). Speedups are in Figs. 9-10 and a time breakdown in Fig. 11. FFT3D is compared with a hand-tuned IBM FFT, GRAVITY with GRAPE-6A, and HMMER with a GPU implementation (Sec. 6.1). Portability needed only leaf and mapping changes; one SGEMM leaf line switched to Intel MKL (Sec. 6.2).

## Principal limitation
As the authors state it, it is unclear whether the minimal primitives can express dynamic applications whose data accesses cannot be listed as task arguments, and the effect of inner tasks being unable to read array elements is not explored (Discussion and Future Work). The evaluation covers only regular algorithms (Sec. 6).
Our observation: portability is shown on two platforms, and the effort to write each mapping specification is not reported.

## Relationship to earlier / later work
- Builds on space-limited procedures (Alpern et al. 1995) and extends the parallel memory hierarchy model of Alpern et al. (1993) (Sec. 2).
- Hierarchically tiled arrays [Bikshandi et al. 2006] are described as less flexible and less portable (Related Work).
- Sequoia tasks generalize stream kernels (Brook) and resemble the thread-less concurrency of Cilk, X10, Chapel and Fortress (Related Work).
- Contrasted with cache-oblivious algorithms and Lim et al. (2001); related to meta-compilation and telescoping languages (Related Work).
- No later work is discussed.

## Sources used
| claim | section / page |
|---|---|
| Problem and motivation | Abstract, Sec. 1 |
| Tasks and blocking primitives | Sec. 3.1-3.3, Table 1 |
| Machine tree model | Sec. 2, Figs. 2-3 |
| Variants, tunables and mapping specs | Sec. 3.4-3.5, Sec. 4, Figs. 7-8 |
| Cell and cluster runtimes | Sec. 5.1-5.2 |
| Copy elimination | Sec. 5.3 |
| Results | Sec. 6.1, Tables 2-3, Figs. 9-11 |
| Portability | Sec. 6.2 |
| Limitations | Discussion and Future Work |
| Related work | Related Work |

## Open questions for the survey
- Does the task-with-working-set model hold for irregular or dynamically generated work, which the paper leaves open?
- Which later systems automate the per-machine mapping specifications that Sequoia leaves to the programmer?
- Do later distributed compilers keep Sequoia's copy boundary at task calls, or hoist copies across them?
