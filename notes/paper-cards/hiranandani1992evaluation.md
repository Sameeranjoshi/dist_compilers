# Evaluation of Compiler Optimization for Fortran D on MIMD Distributed-Memory Machines  
**Catalog id:** `hiranandani1992evaluation`  
**Citation:** Hiranandani, S., Kennedy, K., Tseng, C.-W. "Evaluation of Compiler Optimization for Fortran D on MIMD Distributed-Memory Machines." ICS '92, Washington, D.C., 1992 (ACM International Conference on Supercomputing). No DOI printed; record used: PDF running head, title page and ACM copyright line 0-89791-485-6.  
**Paper type:** compiler-technique  
**Access:** PDF supplied by the repository owner. Full text read. The text layer is complete for all 14 pages. Tables are readable but several cells are garbled by extraction, so table values are cited only where the text repeats them.  
**Card status:** full-read

## Problem
Message-passing MIMD machines such as the iPSC/860 make programmers manage address spaces, communication and synchronization by hand, producing machine-specific code (Sec. 1). The paper asks which optimizations a Fortran D compiler needs, given decomposition-based data layouts, to reach acceptable efficiency. It classifies them, evaluates them and derives profitability formulas (Secs. 1, 4, 6).

## Input abstraction
Fortran D declares a DECOMPOSITION, aligns arrays to it with ALIGN, and distributes it with DISTRIBUTE, using BLOCK, CYCLIC, BLOCK-CYCLIC or an undistributed marker per dimension (Sec. 2, Fig. 1). Dynamic and irregular decomposition are also supported (Sec. 2).

## Target
Experiments run on a 32-node Intel iPSC/860 with 8 MB per node (Sec. 5). The cost model separates message startup, copy and transit time. The paper gives about 95 microseconds for the first byte and 0.4 microseconds per further byte on this machine (Sec. 4.1).

## Data decomposition
The kernels use one-dimensional block distributions (Sec. 5). Overlaps hold nonlocal stencil data when the set is contiguous. Buffers, which can be reused, and hash tables serve reused or sparse nonlocal data (Sec. 4.4). Section 6.3 derives nonlocal communication volumes for one-, two- and three-dimensional block partitions (Table 6).

## Computation mapping
Owner-computes is the base rule, applied from the left-hand side (Sec. 3). Private scalars take the iteration sets of their uses (Sec. 4.3). Reductions and scans are parallelized by relaxing owner-computes, with partial results combined by send/receive, broadcast or collectives (Sec. 4.3, Figs. 8-9). Pipelined loops are mapped to fine-grain or coarse-grain pipelining by loop interchange and strip mining (Sec. 4.3, Fig. 12).

## Communication generation
Optimizations are grouped by the cost term they reduce: startup (vectorization, coalescing, aggregation, collectives), copy and transit (pipelining, vector message pipelining, iteration reordering, nonblocking messages), and lack of parallelism (Sec. 4, Fig. 3). The paper introduces vector message pipelining, which moves vectorized sends and receives to hide transit time without adding messages (Sec. 4.2). Iteration reordering runs locally available iterations between a send and its receive (Sec. 4.2, Fig. 7).

## Compiler / runtime split
Analysis runs up front, and run-time resolution is used only for references that cannot be analyzed at compile time (Sec. 3, step 7). The paper says the compiler will use training sets to estimate communication and computation costs, and will compare dynamic decomposition against that estimate (Secs. 6.1-6.2).

## Evaluation
The kernels are Livermore 3, 11, 18 and 23, Jacobi, red-black SOR, SOR and ADI integration, on 8 to 32 processors (Sec. 5, Tables 2-4). For stencils, message vectorization is the main gain, about two to nine times over element messages (Sec. 5.1). Coarse-grain pipelining with block size 8 is best for Livermore 23, and block size 12 for SOR and ADI (Sec. 5.3). Iteration reordering slows Livermore 18, and dynamic decomposition for ADI costs more than pipelining (Secs. 5.1, 5.3).

## Principal limitation
Stated: the prototype implements vectorization, coalescing, aggregation and fine-grain pipelining, and the other optimizations were applied by hand (Sec. 5). The pipelining model assumes communication cost stays fixed as message size grows, which the authors call imprecise (Sec. 6.2). Further work is planned on larger programs and other MIMD machines (Sec. 7). Our observation: all results come from one machine, one compiler and a few kernels, so the formulas are untested elsewhere.

## Relationship to earlier / later work
The paper says its partitioning and optimization strategy is in earlier work [21], and that message vectorization, pipelining and code generation were presented in [20] (Sec. 1). It is similar to SUPERB and Vienna Fortran in vectorizing messages from dependence information, and CRYSTAL pioneered the collective-communication identification it uses (Sec. 8).

## Sources used
| claim | section / page |
|---|---|
| Fortran D overview; HPF contribution | Secs. 1, 2 |
| Classification of optimizations | Sec. 4, Fig. 3 |
| iPSC/860 startup and per-byte costs; cost terms | Sec. 4.1 |
| Vectorization, coalescing, aggregation, collectives; cost formulas | Secs. 4.1, Table 5 |
| Vector message pipelining, iteration reordering, nonblocking | Sec. 4.2, Fig. 7 |
| Reductions, scans, dynamic decomposition, pipelining | Sec. 4.3, Figs. 8-12 |
| Overlaps, buffers, hash tables, message blocking | Sec. 4.4 |
| Machine, compiler, versions, kernels | Sec. 5, Table 1 |
| Results for communication, reductions, pipelining | Secs. 5.1-5.3, Tables 2-4 |
| Profitability criteria; pipelining model; block size | Secs. 6.1-6.2, Fig. 13 |
| Scalability and nonlocal volumes | Sec. 6.3, Table 6, Figs. 14-15 |
| Related work | Sec. 8 |

## Open questions for the survey
- Do the Table 5 profitability formulas predict the measured crossovers on other machines, or at more than 32 processors?
- Iteration reordering slowed Livermore 18; what criterion would have avoided that before measurement?
- Does coarse-grain pipelining keep its advantage once communication cost is allowed to grow with message size?
