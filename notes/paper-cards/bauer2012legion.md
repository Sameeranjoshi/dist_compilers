# Legion: Expressing Locality and Independence with Logical Regions
**Catalog id:** `bauer2012legion`
**Citation:** Michael Bauer, Sean Treichler, Elliott Slaughter, Alex Aiken. "Legion: Expressing Locality and Independence with Logical Regions." SC12, Salt Lake City, Utah, 2012. No DOI printed in the supplied PDF; IEEE copyright line 978-1-4673-0806-9/12 used.
**Paper type:** runtime
**Access:** PDF supplied by the repository owner. Full text read; the text layer is complete (11 pages, references included).
**Card status:** full-read

## Problem
Heterogeneous processors and deep, distributed memory hierarchies make misplaced data or computation costly (Sec. I). Legion lets programmers express locality and independence with logical regions, from which a runtime extracts parallelism and places data and tasks (Abstract, Sec. I).

## Input abstraction
Regions name sets of objects and may be partitioned into disjoint or aliased subregions by a coloring (Sec. I, II). Tasks declare region privileges (read-only, read-write, reduce) and coherence modes (exclusive, atomic, simultaneous, relaxed) (Sec. I, Fig. 2).

## Target
Clusters of CPUs and GPUs: Sapling, Viz and Keeneland (Fig. 4). The runtime uses pthreads, CUDA and GASNet (Sec. V).

## Data decomposition
The application partitions its regions. In the circuit example, user colorings yield disjoint private and shared node partitions and an aliased ghost-node partition (Sec. II, Listing 1). The AMR code partitions each refinement level recursively by node count and cache sizes (Sec. V-C).

## Computation mapping
A software out-of-order processor analyzes dependences among sibling tasks, then maps and distributes them, with stealing and pushing (Sec. III-A, III-B). A mapping interface picks processors and memories and can affect performance but not correctness (Sec. IV-A). The circuit mapper assigns each piece to a home GPU round-robin with no stealing (Sec. V-A). The AMR mapper places overlapping grids from different levels on the same node (Sec. V-C).

## Communication generation
When a task needs a valid region instance, the runtime issues copies and reductions, deferred until the producing tasks finish (Sec. III-C). Execution is deferred, so an operation waits only for its dependences (Sec. III-D). Shared circuit nodes move between GPUs through GASNet memory (Sec. V-A, Fig. 5).

## Compiler / runtime split
There is no compiler. Dependence analysis, instance creation and copying happen in the runtime (Sec. III). Mapping decisions are made at runtime and may depend on input data; custom mappers can be fully static, memoized, or dynamic (Sec. IV-A, IV-C).

## Evaluation
Strong and weak scaling on three clusters. The circuit simulation reaches 39.0x on 48 GPUs for the small problem and 62.5x on 96 GPUs for the larger one, relative to a hand-coded single-GPU CUDA version, and is within 5% of it on one GPU (Sec. V-A). The fluid code, a port of PARSEC fluidanimate, scales up to 5.4x from 1 to 16 nodes on the larger inputs (Sec. V-B). The AMR code reaches 2.6x over BoxLib on one node and 5.4x at higher node counts (Sec. V-C, Fig. 8).

## Principal limitation
As the authors state it, circuit communication overhead grows quadratically with node count (Sec. V-A). The AMR ghost-cell exchange uses GASNet memory, so network traffic grows linearly with node count, and a direct-exchange algorithm is planned as future work (Sec. V-C).
Our observation: the strongest results rely on application-specific mappers, so the paper does not separate runtime gains from mapper effort.

## Relationship to earlier / later work
- Sequoia [1] is a special case of Legion: only arrays are partitioned, access is exclusive, and decomposition is one-to-one (Sec. VI).
- Bauer et al. [10] add more dynamic mapping to Sequoia (Sec. VI).
- SSMP [11] is the closest model but supports one disjoint rectilinear partition and shared memory only (Sec. VI).
- Chapel [12, 13], X10 [15-18], DPJ [19], object assemblies [20], Galois [21], UPC and Titanium [3, 25] are compared (Sec. VI).
- Work stealing follows Cilk [5] with region-aware stealing (Sec. IV-B).
- Regions are first class following Gay and Aiken [27] (Sec. VI).
- No later work is discussed.

## Sources used
| claim | section / page |
|---|---|
| Problem and scope | Abstract, Sec. I |
| Regions, privileges, coherence | Sec. I, II, Fig. 2 |
| Circuit partitioning | Sec. II, Listing 1 |
| Scheduler stages | Sec. III-A to III-E |
| Mapping interface and default mapper | Sec. IV-A to IV-C |
| Systems and results | Sec. V, Figs. 4-8 |
| Related work | Sec. VI |

## Open questions for the survey
- Does the survey treat the runtime's region-based dependence analysis as compiler-visible information or as purely dynamic?
- How much of the reported scaling comes from application-specific mappers, and what do default-mapper results look like?
- Which later distributed compilers keep the separation of logical regions from physical placement?

## Reference list check (open copy legion.stanford.edu/pdfs/sc2012.pdf, checked 2026-11-07)
27 entries. Present: Sequoia [1], Chapel [2, 12, 13], UPC [3], Titanium [25], Gay and Aiken regions [27]. Absent: HPF, Fortran D, Kali, Koelbel 1991, Saltz/PARTI/CHAOS, Vienna Fortran, Co-Array Fortran.
