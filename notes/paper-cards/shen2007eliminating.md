# Eliminating Redundant Communication of Code Generation for Distributed Memory Machines
**Catalog id:** `shen2007eliminating`
**Citation:** Ya Nan Shen, Rong Cai Zhao, and Lei Wang. "Eliminating Redundant Communication of Code Generation for Distributed Memory Machines." Eighth ACIS International Conference on Software Engineering, Artificial Intelligence, Networking, and Parallel/Distributed Computing (SNPD 2007), pp. 751-756, 2007. DOI 10.1109/SNPD.2007.482 (printed on p. 751).
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner. Full text read (text layer complete for the prose; equations and the Figure 9 axis labels are partly garbled, so formal statements are summarized rather than quoted).
**Card status:** full-read

## Problem
Communication-set algorithms for distributed-memory code generation, due to Amarasinghe and Lam, can produce redundant communication. The authors find that the iteration polyhedra used to build the sets include iteration variables that do not affect which element or which processor is involved (Sec. 1, pp. 751-752; Sec. 3, p. 753).

## Input abstraction
Loop nests with affine bounds and affine array access functions, using symbolic constants. Iteration, data and processor spaces are represented as parameterized convex polyhedra (Sec. 2, pp. 752-753). The examples are a two-deep loop with X[i] = X[i-3] (Fig. 1) and the LU decomposition kernel (Fig. 3).

## Target
Distributed-memory machines with explicit message passing. The experiment runs on a cluster of eight dual-processor 2.8 GHz Xeon nodes joined by a 100 Mb Fast Ethernet switch (Sec. 5.2, p. 755).

## Data decomposition
A data decomposition D maps array elements to processors, and a computation decomposition C maps iterations to processors (Sec. 2, p. 752). The method takes D as given. In the LU example, data and work use a block size blk, so the owner of an element is its index divided by blk (Sec. 5.1, pp. 754-755, Figs. 4-6).

## Computation mapping
Computation decomposition C assigns each iteration to a processor, and the send and receive loops are derived from that map (Sec. 2, p. 752; Figs. 4-6, p. 755).

## Communication generation
A communication set is the set of tuples (read iteration, source processor, write iteration, destination processor, array element) for which the last-write relation holds and the processors differ (Theorems 2.1 and 2.2, pp. 752-753). The generated code is point-to-point send and receive with pack and unpack (Fig. 2, p. 753; Figs. 4-6, p. 755). The revised method projects out redundant iteration variables from these sets (Definitions 4.1-4.2, pp. 753-754; Corollaries 4.1-4.2, p. 754).

## Compiler / runtime split
Everything is compile time. The sets are built as linear inequalities and scanned in a chosen lexicographic order to produce loops (Sec. 2, p. 753). The paper describes no runtime component.

## Evaluation
The LU decomposition kernel with a 256 by 256 matrix is compiled with the original and the revised algorithms and run on the eight-node cluster (Sec. 5, pp. 754-756, Fig. 9). The authors report that their optimization reduces LU running time by 52 to 62 percent (p. 756). Where every iteration variable is needed, the revised method keeps the full space and generates the same code as before, so no change is expected (Sec. 4 and 5.1, pp. 754-755).

## Principal limitation
The authors state that one sample program does not prove that the algorithms always improve performance. For examples in which all iteration variables are necessary, the technique neither improves nor reduces performance, and more experiments are needed (Sec. 5.2, p. 756).
our observation: the only measured case is one kernel at one size on one Ethernet cluster, so the 52 to 62 percent figure cannot be separated from that setting.

## Relationship to earlier / later work
The paper states that it modifies the algorithms of Amarasinghe and Lam, which generate communication code for distributed-memory machines (Abstract; Sec. 1, p. 751). It cites Feautrier's array data-flow formulation [2], S. S. Wang's extension to iteration bounds [3], Ferner's mapping from virtual to physical processors to reduce messages [4], the first author's earlier work on automatic code generation of data decomposition [5], and Gong's communication optimizations [6] (Sec. 1, p. 751). It describes that work as minimizing communication, whereas its own aim is to remove redundant communication (p. 751). It names no later work; its stated next step is further optimization (Sec. 6, p. 756).

## Sources used
| claim | section / page |
|---|---|
| Redundant communication in Amarasinghe and Lam's algorithms | Sec. 1, p. 751 |
| Prior work and citations [1]-[6] | Sec. 1-2, pp. 751-752 |
| Iteration space, data and processor spaces | Sec. 2, pp. 752-753 |
| Last-write relation and Theorems 2.1-2.2 | pp. 752-753 |
| Cause of redundant communication | Sec. 3, p. 753 |
| Redundant iteration variables and projection | Definitions 4.1-4.2, pp. 753-754 |
| Revised communication sets (Corollaries 4.1-4.2) | Sec. 4, p. 754 |
| LU kernel analysis: third pair cannot be projected | Sec. 5.1, p. 754 |
| Cluster and LU timing result | Sec. 5.2, pp. 755-756; Fig. 9 |
| Limits of one sample program | Sec. 5.2, p. 756 |
| DOI | p. 751 |

## Open questions for the survey
- The paper gives no compile-time cost for the polyhedral projections. How does that cost grow with loop depth and statement count?
- The LU analysis notes a read-write pair in which the iteration variable cannot be projected (p. 754). How common is that pattern in real kernels?
- Only one kernel, one size and one Fast Ethernet cluster were measured. Do the gains hold for other kernels and faster interconnects?
