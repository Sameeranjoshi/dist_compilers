# Automatic Data Movement and Computation Mapping for Multi-level Parallel Architectures with Explicitly Managed Memories
**Catalog id:** `baskaran2008automatic`
**Citation:** Muthu Manikandan Baskaran, Uday Bondhugula, Sriram Krishnamoorthy, J. Ramanujam, Atanas Rountev, P. Sadayappan. "Automatic Data Movement and Computation Mapping for Multi-level Parallel Architectures with Explicitly Managed Memories." PPoPP '08, Salt Lake City, Utah, 2008. No DOI printed in the supplied PDF; ACM copyright line 978-1-59593-960-9/08/0002 used.
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner. Full text read; the text layer is complete (10 pages, references included).
**Card status:** full-read

## Problem
The paper targets accelerators with fast, software-managed local memories, where the programmer must move data between global and local memory and exploit several levels of parallelism (Abstract, Sec. 1). It proposes automatic creation of local buffers with generated move code, and multi-level tiling that distributes work over outer and inner parallel units (Sec. 1). The scope is regular programs with affine loop bounds and access functions (Sec. 2). Message passing is not treated, and the experiments run on one GPU.

## Input abstraction
The framework takes the iteration spaces of all statements in a block and their affine access functions (Sec. 3.1). No front end is described. Dependence polyhedra are introduced (Sec. 2) but are not used by the implemented framework (Sec. 3.1.4).

## Target
One GeForce 8800 GTX with 16 multiprocessors, each with 8 SIMD units and 16 KB of shared memory, programmed in CUDA (Sec. 5, 6). Multiprocessors are the outer parallel level and SIMD units the inner one (Sec. 5).

## Data decomposition
No array distribution is described. Accessed data is grouped into disjoint partitions, and each partition gets a local buffer sized from its convex hull (Sec. 3.1, 3.1.1). Outer space tiles are divided equally among thread blocks (Sec. 4, 6).

## Computation mapping
Space loops come from the outermost permutable band, with pipelining when no loop is communication-free (Sec. 4.1). Space loops are tiled once per parallel level, adding levels when a tile exceeds local memory (Sec. 4). Inner tiles are distributed over threads (Figs. 2-3).

## Communication generation
Not applicable in the message-passing sense. Generated code copies read data into local arrays and written data back, with loops that load each element once (Sec. 3.1.3). Copy code is hoisted out of redundant tiling loops (Sec. 4.2). All accessed data is moved, because dependence information is not yet used (Sec. 3.1.4).

## Compiler / runtime split
All analysis is at compile time, using Polylib, PIP for parametric bounds, and CLooG for code generation (Sec. 3.1.1, 3.1.2). Tile sizes minimize N x ((P x S) + V x L / P) under a memory bound and a minimum thread count, solved by sequential quadratic programming with rounding (Sec. 4.3). The paper does not say whether the search runs per problem size.

## Evaluation
Two kernels: Mpeg4 motion estimation, which needs no synchronization across thread blocks, and 1-D Jacobi, which does (Sec. 6). The authors report about 8x and 10x speedup from scratchpad use over GPU-only global memory, and over 100x and 15x over the CPU (Sec. 6). Figures 4-8 plot time against problem and tile size. There is no table and no comparison with other compilers.

## Principal limitation
As the paper states it, copy sets are not reduced by dependence information, and that optimization is deferred to future work (Sec. 3.1.4). The Jacobi results also rely on a concurrent-start transformation from earlier work [27] (Sec. 6).
Our observation: only one GPU and two kernels are measured.

## Relationship to earlier / later work
- Uses the affine framework of Bondhugula et al. [7] to find tiling hyperplanes (Sec. 4.1).
- Cites Kim et al. [26] for multi-level tiling and Krishnamoorthy et al. [27] for stencils (Sec. 6, 7).
- Related work cites Schreiber and Cronquist [38], Kandemir et al. [25], Eisenbeis et al. [12], Anantharaman and Pande [1], and Clauss [9] and Pugh [35] (Sec. 7).
- Lists Sequoia (Fatahalian et al. [13]) among works that tile for memory-hierarchy levels (Sec. 7).
- No later work is discussed.

## Sources used
| claim | section / page |
|---|---|
| Problem, buffers and tiling | Abstract, Sec. 1 |
| Affine scope and polyhedral model | Sec. 2, Sec. 3 intro |
| Local buffer construction | Sec. 3.1, 3.1.1, Algorithm 2 |
| Copy code and hoisting | Sec. 3.1.3, 4.2 |
| Copy-set optimization deferred | Sec. 3.1.4 |
| Tiling and parallel levels | Sec. 4, 4.1 |
| Tile-size cost model and solver | Sec. 4.3 |
| GPU target | Sec. 5, 6 |
| Results | Sec. 6, Figs. 4-8 |
| Related work and citations | Sec. 7 |

## Open questions for the survey
- Would the buffer-plus-tiling approach carry over to distributed memories, where each copy becomes a message?
- The cost model in Sec. 4.3 prices synchronization and transfer; how did later systems calibrate its constants?
- Did the dependence-based reduction of copy sets (Sec. 3.1.4) appear in later automatic data-movement compilers?
