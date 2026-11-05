# Generating efficient tiled code for distributed memory machines
**Catalog id:** `tang2000tiled`
**Citation:** Peiyi Tang, Jingling Xue. "Generating efficient tiled code for distributed memory machines." Parallel Computing 26(11): 1369-1410, 2000. DOI 10.1016/s0167-8191(00)00040-5.
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner. Full text read; the text layer is complete for the prose, with some ligatures and equations garbled by extraction. Figures were read as extracted text only.
**Card status:** full-read

## Problem
Tiled loop nests can expose coarse-grain parallelism on distributed-memory machines if communication is kept coarse. The paper gives compiler techniques that generate SPMD message-passing code for rectangularly tiled iteration spaces. Unlike HPF-style compilers, it distributes computation first, by mapping tiles to processors, and then derives data placement (Sec. 1, 3, 4).

## Input abstraction
Perfectly nested loops with unit stride, affine bounds and constant flow dependences in single-assignment form. Anti and output dependences are removed beforehand, for example by array expansion, and skewing makes dependences non-negative (Sec. 2.2, 2.3.1).

## Target
A Fujitsu AP1000 with 128 SPARC cells on a 2D torus, each with 16 MB of memory (Sec. 9). The machine model is an m-dimensional processor mesh with message passing between any pair (Sec. 2.4).

## Data decomposition
Data are placed by the "computer-owns" rule: a processor owns the data it computes (Sec. 4). Placement is block-cyclic on the tile grid, and skewed when the iteration space is skewed. The authors note that HPF's block and cyclic directives cannot express the skewed case (Sec. 1, 4). Nonlocal data sit in overlap areas (Sec. 6).

## Computation mapping
Tiles are allocated cyclically along the first m dimensions of the tile space, with the other dimensions collapsed. Each tile is an atomic unit of work (Sec. 3). Cyclic allocation is claimed to reduce load imbalance and to let computation overlap communication (Sec. 3, 9).

## Communication generation
Only flow dependences are handled. For each tile, a communication set holds the values the tile produces for a neighbouring processor, and all data for one processor pair travel in one message (Sec. 2.2, 5.1). Packing and unpacking use regular array sections (Sec. 5.1, 6.3.3). A receive is posted just before the first dependent tile runs, which a run-time test on tile validity decides (Sec. 5.2).

## Compiler / runtime split
Tile loops, communication sets and address translation are generated at compile time, using Fourier-Motzkin elimination and the Omega Calculator (Sec. 2.3.3, 5.2, 6.2). The remaining run-time work is a validity test on tiles, which the authors say takes under 3% of execution time (Sec. 5.2, 9).

## Evaluation
Skewed SOR, a five-point stencil with an expanded and skewed array, on the AP1000. The paper reports speedup of about 14 on 25 cells, against an upper bound of about 23 with communication removed. It also measures the validity-test cost, the two memory optimizations (address folding and memory recycling), tile granularity, load balance and processor layout (Sec. 9, Fig. 13).

## Principal limitation
As the paper states it: the code generator targets rectangular tilings of skewed spaces, and other parallelepiped tilings are out of scope (Sec. 2.3.1). Tile loops can enumerate empty tiles (Sec. 2.3.3). Memory use falls, but "future research is still needed" to reduce it further (Sec. 9). Tile sizes, shapes and processor layout are left open (Sec. 9, 11). Our observation: every result comes from one stencil kernel on 1990s hardware, so the generality claimed in the abstract rests on a single benchmark.

## Relationship to earlier / later work
- The authors' earlier paper, Tang and Zigman [33], handled rectangular tiled spaces. This paper extends the communication code to arbitrary convex spaces (Sec. 10).
- Fortran D [19] and Vienna Fortran [2] first find a data distribution and then infer computation placement; this paper reverses the order (Sec. 1, 10).
- The atomic-tile constraint is credited to Irigoin and Triolet [20] and Xue [39] (Sec. 1).
- Communication-set enumeration follows Chatterjee et al. [8], Koelbel [21] and Thirumalai and Ramanujam [34]; overlap areas follow Gerndt [15] (Sec. 10).
- Later work is not discussed. Tile-size selection and integration with data-parallel compilers are listed as future work (Sec. 11).

## Sources used
| claim | section / page |
|---|---|
| Problem and computation-first order | Sec. 1, 3 |
| Program model, flow-only dependences | Sec. 2.2 |
| Rectangular tilings and skewing | Sec. 2.3.1 |
| Cyclic tile allocation | Sec. 3 |
| Computer-owns rule | Sec. 4 |
| Communication sets and scheme | Sec. 5.1-5.3 |
| Memory management and optimizations | Sec. 6, 8 |
| AP1000 setup and results | Sec. 9, Fig. 13 |
| Related work and future work | Sec. 10, 11 |

## Open questions for the survey
- Which later compilers adopted the computation-first order with computer-owns placement, and did any go beyond rectangular tilings?
- Do flow-only communication sets carry over to kernels with broadcast or multicast patterns, which this paper does not test?
- Which tile-size and processor-layout selection methods (Sec. 9, 11) were published later, and do they model communication cost?
