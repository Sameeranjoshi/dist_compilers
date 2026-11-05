# An HPF Compiler for the IBM SP2
**Catalog id:** `gupta1995hpf`
**Citation:** Gupta, M., Midkiff, S., Schonberg, E., Seshadri, V., Shields, D., Wang, K.-Y., Ching, W.-M., and Ngo, T. "An HPF Compiler for the IBM SP2." Venue not printed in the supplied PDF; year 1995 from the catalog id. Record used: catalog id and PDF title page; no DOI printed.
**Paper type:** full-system
**Access:** PDF supplied by the repository owner. Full text read. The text layer is complete, but ligatures are dropped (for example "signi cant").
**Card status:** full-read

## Problem
HPF performance depends on communication optimizations, and the processor count is often unknown at compile time. The paper describes pHPF, a prototype HPF compiler for IBM SP machines, built to handle both (Abstract, pp. 1-2).

## Input abstraction
Fortran 90 and Fortran 77 programs with HPF directives (DISTRIBUTE, ALIGN, INDEPENDENT). pHPF is a native compiler that extends an existing Fortran 90 compiler, and array statements are scalarized before SPMDization (Section 2.1, pp. 2-4).

## Target
IBM SP series machines, with message passing through IBM MPL or MPI (Section 2, p. 7). The benchmarks ran on a 36-processor IBM SP2 with 32 thin and 4 wide nodes (Section 4.1, p. 13).

## Data decomposition
Block and cyclic distributions are supported; block-cyclic is not (footnote 2, p. 2). Each distributed array is shrunk to its local block through dynamically allocated pointers, with bounds expressed in terms of the processor count (Section 2.2, pp. 5-6). Cyclic distributions require subscript modification (footnote 3, p. 5). Scalars default to replication before privatization and alignment are applied (Section 3, pp. 11-12).

## Computation mapping
The owner-computes rule is generally used, except for reductions and some scalar assignments (Section 2.2, p. 7). Loop bounds are shrunk to local iteration sets when all statements in a loop share one set. Otherwise statement guards are inserted and hoisted out of loops where possible (Section 3, p. 12). Scalars are aligned with a producer or consumer reference, chosen by estimated communication cost (Section 3, pp. 11-12).

## Communication generation
Communication analysis selects the placement and the primitive for each grid dimension, and it generates closed-form, parameterized communication sets (Section 2.2, pp. 6-7). Messages are vectorized outside loops after loop distribution (p. 7). Broadcasts and reductions are recognized (p. 8), multi-dimensional shifts use d steps instead of 2d-1 messages (p. 10), redundant communication is removed by data-availability analysis, and wavefronting pipelines communication (Section 3, pp. 8-11).

## Compiler / runtime split
Symbolic analysis keeps the processor count, loop bounds and array bounds as general expressions, so communication is generated in parameterized form at compile time rather than determined at run time (Section 1, p. 2). The run-time library handles packing, buffering and overlapped unpacking, and the same object code runs on different processor counts (Section 2.2, p. 7; Section 4.1, p. 13).

## Evaluation
Four HPF benchmarks from the Applied Parallel Research suite (grid, tomcatv, NCAR shallow-water and x42) were run on up to 32 processors against serial XLF -O3 times, and three were compared with hand-written MPL (Section 4, pp. 13-15). At 32 processors the speedups are 30.49 for grid (MPL 30.43), 17.65 for tomcatv, 19.32 for NCAR with (BLOCK,BLOCK) (MPL 31.10) and 21.96 for x42 with (BLOCK,BLOCK) (MPL 24.70) (Tables 2-5). Table 1 gives static reference counts with and without redundancy elimination (p. 9).

## Principal limitation
The authors state that compiled HPF programs carry inherent overheads that leave them slower than highly tuned hand-coded programs (Section 4.2, p. 14). The NCAR program does not scale well with processor count and needed INDEPENDENT directives for loops it could not analyze (p. 14). The redundancy analysis covers only single loop nests (Section 3, p. 9).

our observation: the benchmarks come from one machine and one compiler, so the reported speedups do not show how the optimizations behave on other platforms.

## Relationship to earlier / later work
Stated by the paper: the communication analysis extends the methods of Gupta and Banerjee [9] (Section 2.2, p. 6), and the redundancy elimination is a simplified version of Gupta, Schonberg and Srinivasan [10] (Section 3, p. 9). SUPERB is described as the second generation of a Vienna compiler that pioneered message vectorization and overlap regions, but only for block distributions (Section 5, p. 15). The paper cites its reference [23] for SUPERB; that reference is Zima and Chapman, Proceedings of the IEEE, 1993 (reference list, p. 18). Fortran D needs a known processor count and partitions only one array dimension (Section 5, p. 15).

## Sources used
| claim | section / page |
|---|---|
| Architecture and native-compiler design | Section 2.1, pp. 2-4 |
| Data partitioning, shrunk local arrays | Section 2.2, pp. 5-6 |
| Communication analysis and run-time library | Section 2.2, pp. 6-7 |
| Vectorization, collective communication, redundancy | Section 3, pp. 7-9 |
| Shift and wavefront optimizations | Section 3, pp. 9-11 |
| Scalar mapping and guard optimization | Section 3, pp. 11-12 |
| Benchmark setup and speedups | Section 4, pp. 13-15 |
| Related work and SUPERB citation | Section 5, pp. 15-16; reference 23, p. 18 |

## Open questions for the survey
- Does the redundancy-elimination result (Table 1) carry over to codes whose redundant references span loop nests, given the paper's single-nest limit?
- Should the survey separate parameterized compile-time communication sets from the run-time schedules of ADAPTOR and Fortran D that the paper contrasts with it?
- Is four benchmarks on one machine enough to set pHPF against the other HPF compilers in the survey?
