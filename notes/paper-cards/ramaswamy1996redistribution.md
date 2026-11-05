# Optimizations for Efficient Array Redistribution on Distributed Memory Multicomputers
**Catalog id:** `ramaswamy1996redistribution`
**Citation:** Shankar Ramaswamy, Barbara Simons, and Prithviraj Banerjee. "Optimizations for Efficient Array Redistribution on Distributed Memory Multicomputers." Journal of Parallel and Distributed Computing 38 (1996): 217-228. Record used: supplied PDF (no DOI printed).
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner. Full text read; the text layer is complete for prose, tables and references. Figures were not interpreted beyond their captions.
**Card status:** full-read

## Problem
A runtime method for moving a distributed array between regular distributions on different or overlapping processor sets (Sec. 1.1, Fig. 1). The authors motivate it with phase changes and task-parallel pipelines, and argue that it beats runtime resolution, which computes each element's target at the source (Sec. 1.1, Sec. 2).

## Input abstraction
Each dimension may use ALL, BLOCK, CYCLIC or BLOCKCYCLIC(x) (Sec. 1.1). Source and target processor sets may be arbitrary subsets, handled with MPI groups and communicators (Sec. 2). Multidimensional arrays are handled per dimension (Sec. 3.4).

## Target
The implementation is an MPI-based library (GroupSend and GroupRecv) run on the Intel Paragon (Sec. 4). Own packing routines were used because the Paragon lacked MPI derived datatypes (Sec. 4).

## Data decomposition
A regular distribution of a one-dimensional array is represented as a FALLS (l, h, str), a family of equal, equally spaced line segments bounded by the array size (Sec. 3.2). The elements held by one processor form a FALLS, so the data to transfer between two processors is the intersection of two FALLS (Sec. 3, Fig. 2).

## Computation mapping
None. Redistribution is a data-movement operation. Each source and target runs the pack, send, receive and unpack steps of Fig. 9 (Sec. 3.3).

## Communication generation
Sources intersect their FALLS with each target's FALLS, pack and send; targets unpack (Sec. 3.3, Fig. 9). Intersections are computed within one period of length lcm(str1, str2) (Theorems 1-2, Sec. 3.2), and a constant-time Fourier-elimination test skips pairs that cannot intersect (Sec. 3.2.1). A locality optimization generates fewer, larger contiguous pieces (Sec. 3.2.3), and a schedule in which each source starts at a different destination index reduces contention (Sec. 3.3.1). Data for several arrays bound for the same processor share one message (Sec. 3.5).

## Compiler / runtime split
No compile-time analysis is described; the library computes intersections and messages at run time (Sec. 3.3, Sec. 4).

## Evaluation
The evaluation times 27 Paragon redistributions over three array sizes and three distribution pairs. Three variants are timed: Unopt (the earlier algorithm), Local (with the locality optimization), and Sched (locality plus scheduling) (Tables I-III). Local is faster than Unopt in every row; at 400x400 in Table III the time falls from 190.3 ms to 31.3 ms. Sched is slower than Local in several rows, for example 31.8 ms against 31.3 ms in Table III. The analysis overhead is 0.94 to 1.29 ms and does not grow with array size (Table IV). The only baseline is the authors' earlier algorithm (Sec. 4).

## Principal limitation
The paper states that it handles only regular distributions and does not consider reshaping of arrays in its current form (Sec. 1.1). Redistribution of array sections and a more thorough cost analysis are listed as future work (Sec. 5).
our observation: One machine and one earlier baseline; no comparison with other libraries.

## Relationship to earlier / later work
- Compiler communication techniques [8-12] cannot handle arrays on subsets of processors (Sec. 2).
- Agrawal, Sussman and Saltz [13] build reusable schedules but do not handle CYCLIC or BLOCKCYCLIC distributions or arbitrary processor sets (Sec. 2).
- The ScaLAPACK [15] and HPF runtime [17] routines are described as unclear for arbitrary processor sets or as pairwise (Sec. 2).
- Chatterjee et al. [12] give a more general state-machine method for local addresses; the authors call their own method simpler and adequate here (Sec. 3.2.2).
- No later work is discussed.

## Sources used
| claim | section / page |
|---|---|
| Regular distributions only; no reshaping; whole-array redistribution | Sec. 1.1, p. 217; Sec. 5, p. 227 |
| FALLS representation and intersection periods (Theorems 1-2) | Sec. 3.2, pp. 219-221 |
| Constant-time FALLS intersection test (Eqs. 18-21) | Sec. 3.2.1, pp. 222-223 |
| Locality and scheduling optimizations | Sec. 3.2.3, p. 223; Sec. 3.3.1, p. 224 |
| Paragon, MPI-based library, own packing routines | Sec. 4, pp. 225-226 |
| Unopt, Local and Sched timings (27 cases) | Tables I-III, pp. 226-227 |
| Analysis overhead 0.94 to 1.29 ms | Table IV, p. 227 |
| Prior redistribution work and comparisons | Sec. 2, p. 218 |

## Open questions for the survey
- How do FALLS-based schedules compare with the ScaLAPACK and HPF runtime redistribution routines on the same machine, given that the only baseline here is the authors' earlier algorithm?
- Does the benefit of scheduling depend on the machine or the processor count, since Sched is slower than Local in several rows of Tables II and III?
- Has the extension to array sections and reshaping (Sec. 5) been reported elsewhere?
