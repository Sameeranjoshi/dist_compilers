# Techniques for compiling programs on distributed memory multicomputers
**Catalog id:** `lee1995techniques`
**Citation:** Lee, P.-Z. "Techniques for compiling programs on distributed memory multicomputers." Parallel Computing 21 (1995) 1895-1923. Record used: PII 0167-8191(95)00052-6, printed on the first page; no DOI printed.
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner. Full text read. The prose text layer is complete, but Tables 6, 8 and 10 and some symbols are garbled, so no values are quoted from those tables.
**Card status:** full-read

## Problem
Programmers on distributed-memory machines must manage both parallelism and communication, which makes algorithm design slow and error-prone. The paper gives compiler techniques for data storage and execution schedules in Do-loop programs: a dynamic-programming choice of data layouts across loop nests, a cost model for communication primitives, and pipelining of reductions and broadcasts guided by data-dependence vectors (Section 1, pp. 1895-1898).

## Input abstraction
Nested Do-loop programs with one- and two-dimensional arrays (Section 2.1, p. 1899). The method handles each nested loop independently (Section 1, p. 1896) and assumes regular data-dependence vectors, meaning all are constant (Section 5.1, p. 1912). Sequential and concurrent parts of the program are run as SPMD code (Section 2, p. 1898).

## Target
An abstract q-dimensional processor grid, embedded in a hypercube by binary reflected Gray codes (Section 2, p. 1898). The experiments use a 32-node nCUBE-2 (Section 6, p. 1914).

## Data decomposition
Each array dimension has a distribution function giving the method, the partition (contiguous, cyclic, or contiguous-cyclic with 1 < block < m/N), the indexing direction, the grid dimension, the block size and an offset (Section 2.1, pp. 1899-1900). The two-dimensional form allows rotated dimensions, which goes beyond the independent-only form of Gupta and Banerjee (p. 1900). Scalars and small arrays are replicated (p. 1898).

## Computation mapping
The affinity graph relaxes the owner-computes rule. Operands of a binary operator can be combined first and sent once to the owner of the left-hand side, and lower-dimensional objects can be sent to the owner of a higher-dimensional one (Section 3, pp. 1903-1904). An iteration space mapping function assigns tiles to processing elements and fixes the direction of pipelined data (Section 5.1, pp. 1913-1914).

## Communication generation
The run-time library supplies Transfer, Shift, one-to-many multicast, Reduction, affine transfer, Scatter, Gather and many-to-many multicast, with hypercube cost formulas (Section 2.2, pp. 1901-1902; Table 1). Subscript patterns select a primitive, following Li and Chen's pattern matching (Table 3, p. 1905). For the loop-carried values of X in Jacobi, the method pipelines values around a ring instead of broadcasting them (Section 5, pp. 1910-1911).

## Compiler / runtime split
The distributions and the chosen schedule are computed at compile time from the component affinity graph and a dynamic program over consecutive loops (Sections 3-4, pp. 1902-1910). The paper notes that this analysis is done at compile time (p. 1910). At run time the generated code performs the communication and computation that the chosen layouts imply.

## Evaluation
Two linear-system kernels run on a 32-node nCUBE-2. Jacobi iteration is compared under dynamic and static distributions (Table 8, p. 1917), and Gauss elimination under a pipelined and a broadcast version (Table 10, pp. 1919-1920). Matrix sizes for Jacobi run from 25 to 29. The authors conclude that dynamic distribution beats static, and that pipelining is faster, with most of the Jacobi gain coming from the layout choice (Section 6.1, p. 1917).

## Principal limitation
The authors restrict the method to algorithms whose data-dependence vectors are all constant (Section 5.1, p. 1912), to one- and two-dimensional arrays (p. 1899), and to a two-dimensional abstract grid (Section 3, p. 1904). They also note that the component alignment problem is NP-complete and use a heuristic (Section 3, pp. 1903-1904).

our observation: the experiments cover two kernels on one 32-node machine, so the reported gains do not show how the method behaves on general loop nests.

## Relationship to earlier / later work
Stated by the paper: the affinity graph modifies the Li and Chen model, which is undirected and follows a restricted owner-computes rule (Section 3, pp. 1903-1904). The alignment heuristic is Li and Chen's, applied to the directed graph treated as undirected (p. 1904). The distribution function generalizes Gupta and Banerjee's (p. 1900). Ramanujam and Sadayappan derived a more general iteration-space tiling method independently (Section 5.1, pp. 1913-1914). The introduction cites Zima and Chapman [48] with Callahan and Kennedy [5] and Rogers and Pingali [39] for the point that programmers must manage both parallelism and communication (Section 1, p. 1896).

## Sources used
| claim | section / page |
|---|---|
| Motivation; citation of Zima and Chapman [48] | Section 1, pp. 1895-1897 |
| Distribution functions, 1-D and 2-D | Section 2.1, pp. 1899-1900 |
| Communication primitives and costs | Section 2.2, pp. 1901-1902 |
| Affinity graph and relaxed owner-computes | Section 3, pp. 1902-1905 |
| Dynamic programming over loops | Section 4, pp. 1907-1910 |
| Pipelining and dependence vectors | Section 5, pp. 1910-1914 |
| Experiments and conclusions | Section 6-7, pp. 1914-1921 |

## Open questions for the survey
- The dynamic program and the pipelining scheme are evaluated separately. Should the survey record them as two contributions?
- The constant-dependence restriction places this work away from the inspector-executor systems in the survey (Parti, Oxygen). Should they be grouped together?
- Are the nCUBE-2 timings usable as a comparison point beside the other survey entries, given one small machine and no external baseline?
