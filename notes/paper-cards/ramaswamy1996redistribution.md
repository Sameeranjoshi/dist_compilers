# Optimizations for Efficient Array Redistribution on Distributed Memory Multicomputers
**Catalog id:** `ramaswamy1996redistribution`
**Citation:** Shankar Ramaswamy, Barbara Simons, and Prithviraj Banerjee. "Optimizations for Efficient Array Redistribution on Distributed Memory Multicomputers." Journal of Parallel and Distributed Computing 38 (1996): 217-228. Record used: supplied PDF (no DOI printed).
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner. Full text read; the text layer is complete for prose, tables and references. Figures were not interpreted beyond their captions.
**Card status:** full-read

## Problem
The paper gives a runtime method for moving a distributed array from one regular distribution to another, where the source and target may be different or overlapping processor sets (Sec. 1.1, Fig. 1). It is motivated by programs that change distributions between phases and by task-parallel pipelines in which an inter-task dependence forces a redistribution (Sec. 1.1). The authors argue that using distribution information directly beats the runtime resolution scheme, which computes each element's target at the source (Sec. 1.1, Sec. 2).

## Input abstraction
Each dimension may use ALL, BLOCK, CYCLIC or BLOCKCYCLIC(x) (Sec. 1.1). Source and target processor sets may be arbitrary subsets, handled with MPI groups and communicators (Sec. 2). Multidimensional arrays are handled by intersecting the per-dimension sets (Sec. 3.4). Reshaping is excluded, and only whole arrays are redistributed (Sec. 1.1, Sec. 5).

## Target
The implementation is an MPI-based library (GroupSend and GroupRecv) run on the Intel Paragon (Sec. 4). The authors wrote their own packing routines because the Paragon lacked support for MPI derived datatypes (Sec. 4).

## Data decomposition
A regular distribution of a one-dimensional array is represented as a FALLS (l, h, str), a family of equal, equally spaced line segments bounded by the array size (Sec. 3.2). The elements held by one processor form a FALLS, so the data to transfer between two processors is the intersection of two FALLS (Sec. 3, Fig. 2). Local addresses come from Eq. (22) (Sec. 3.2.2).

## Computation mapping
None. Redistribution is a data-movement operation. Each source and target runs the pack, send, receive and unpack steps of Fig. 9 (Sec. 3.3).

## Communication generation
Each source intersects its FALLS with each target's FALLS, packs the result, and sends it; the target does the reverse (Sec. 3.3, Fig. 9). Intersections are computed within one period of length lcm(str1, str2) (Theorems 1-2, Sec. 3.2), and a constant-time Fourier-elimination test skips pairs that cannot intersect (Sec. 3.2.1). A locality optimization generates fewer, larger contiguous pieces (Sec. 3.2.3), and a schedule in which each source starts at a different destination index reduces contention (Sec. 3.3.1). Data for several arrays bound for the same processor share one message (Sec. 3.5).

## Compiler / runtime split
No compile-time analysis is described. The library computes intersections and messages at run time from processor-grid and array descriptors (Sec. 3.3, Sec. 4).

## Evaluation
The evaluation covers 27 Paragon redistributions: three distribution pairs, arrays of 100x100 to 400x400, and three processor grids per pair. Three variants are timed: Unopt (the earlier algorithm), Local (with the locality optimization), and Sched (locality plus scheduling) (Tables I-III). Local is faster than Unopt in every row; at 400x400 in Table III the time falls from 190.3 ms to 31.3 ms. Sched is slower than Local in several rows, for example 31.8 ms against 31.3 ms in Table III. The analysis overhead is 0.94 to 1.29 ms and does not grow with array size (Table IV). The only baseline is the authors' earlier algorithm (Sec. 4).

## Principal limitation
The paper states that it handles only regular distributions and does not consider reshaping of arrays in its current form (Sec. 1.1). Redistribution of array sections and a more thorough cost analysis are listed as future work (Sec. 5).
our observation: All timings come from one machine and one earlier version of the algorithm, so no comparison with other libraries is available.

## Relationship to earlier / later work
- Compiler techniques for communication generation [8-12] could in principle perform redistribution, but cannot handle statements whose arrays lie on subsets of processors (Sec. 2).
- Agrawal, Sussman and Saltz [13] build reusable schedules but do not handle CYCLIC or BLOCKCYCLIC distributions or arbitrary processor sets (Sec. 2).
- The ScaLAPACK routine [15] is described as unclear for arbitrary processor sets, and the HPF runtime routines [17] treat source-target pairs individually with runtime resolution for general cases (Sec. 2).
- Chatterjee et al. [12] give a more general state-machine method for local addresses; the authors call their own method simpler and adequate here (Sec. 3.2.2).
- This work extends the authors' earlier report [19] (Sec. 2). No later work is discussed.

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
