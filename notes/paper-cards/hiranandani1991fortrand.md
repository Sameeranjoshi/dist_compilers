# Compiler Optimization for Fortran D on MIMD Distributed-Memory Machines  
**Catalog id:** `hiranandani1991fortrand`  
**Citation:** Hiranandani, S., Kennedy, K., Tseng, C.-W. "Compiler Optimization for Fortran D on MIMD Distributed-Memory Machines." Supercomputing '91, Albuquerque, NM, November 1991 (venue as cited in ref. 20 of the 1992 Hiranandani et al. paper; the PDF prints only the ACM copyright line). No DOI printed; record used: PDF title page and ACM copyright line 0-89791-459-7/91/0086.  
**Paper type:** compiler-technique  
**Access:** PDF supplied by the repository owner. Full text read. The text layer is complete for all 15 pages, but the two-column layout is extracted out of order in places and the figures are only partly recoverable.  
**Card status:** full-read

## Problem
Message-passing code for MIMD distributed-memory machines is tedious and machine-specific, and the authors report source growth of three to ten times (Sec. 1). The paper proposes deriving the node program, with explicit messages, from user-given data decompositions while minimizing load imbalance and communication cost (Secs. 1, 3). The prototype targets the Intel iPSC/860 (Sec. 1).

## Input abstraction
Fortran D adds DECOMPOSITION, ALIGN and DISTRIBUTE statements (Sec. 2, Fig. 1). Alignment uses placeholder subscripts, and each decomposition dimension takes BLOCK, CYCLIC, BLOCK-CYCLIC or an undistributed marker (Sec. 2). Dynamic and irregular decomposition are also supported, with executable ALIGN and DISTRIBUTE (Secs. 2, 3.1.2).

## Target
The compiler is described for the iPSC/860, a MIMD distributed-memory machine (Sec. 1). Section 2 names topology, communication mechanism, memory size and processor count as the machine factors, but no topology or cost model is given.

## Data decomposition
Each processor computes its local index set from the alignment and distribution. For the Jacobi example with D(:,BLOCK) on four processors the local index set is [1:100,1:25] (Secs. 3.1.2, Fig. 3). Global subscripts are translated to local ones. Nonlocal data go to overlaps, which suit nearest-neighbour stencils, or to buffers and hash tables (Sec. 3.3.3). Scalars and unaligned arrays are replicated (Sec. 2).

## Computation mapping
Work follows the owner-computes rule. The local iteration set of a statement comes from its left-hand side, with pre, mid and post sets for boundary conditions (Sec. 3.1.3). A scalar private to one loop iteration takes the iteration set of its consumers (Sec. 3.1.3, Fig. 4). Cross-processor loops, found by the algorithm of Fig. 9, mark pipelined computations (Sec. 3.4.2). An owner-stores relaxation and on-clause partitioning are discussed as options (Sec. 3.2.4).

## Communication generation
Nonlocal sets are recorded as regular section descriptors (Sec. 3.1.4). Messages are vectorized to the outermost loop level that dependences allow (Sec. 3.2.1, Figs. 5-8). Constant subscripts become broadcasts, and mismatched alignments become transposes or all-to-all exchanges. Reductions use collective routines (Sec. 3.2.2). For pipelined loops the paper proposes message pipelining with loop interchange and strip mining, and the strip size is to be set empirically (Sec. 3.4.2).

## Compiler / runtime split
Dependence, decomposition, partitioning and communication analysis run at compile time, and the output is an SPMD node program (Secs. 3, 3.3). Subscripts that cannot be analyzed use an inspector and executor when there is no loop-carried true dependence, and guarded run-time communication otherwise (Sec. 3.2.3).

## Evaluation
The paper reports no measurements. Its evidence is worked examples (Jacobi, SOR, red-black SOR and Livermore kernel 23) with their generated code (Secs. 3.1-3.3, Figs. 3-8), and a qualitative comparison with related systems (Sec. 4.1). Section 5 mentions preliminary results without presenting them.

## Principal limitation
Stated: the prototype performs message vectorization for block-distributed arrays, and the other optimizations remain to be implemented (Sec. 5). Our observation: the gains claimed for pipelining, collective communication and dynamic decomposition are not measured in this paper.

## Relationship to earlier / later work
The paper says the compiler mostly builds on SUPERB, ParaScope, Id Nouveau, Crystal, ASPAR, Kali, PARTI and ARF, and lists AL, CM Fortran, DINO, MIMDizer, Pandore, Paragon and SPOT as related compilers (Sec. 4). It contrasts its up-front analysis with the transformation-based ParaScope, Id Nouveau and SUPERB systems, and notes that SUPERB and ASPAR find the parallelism in red-black SOR but their contiguous overlaps prevent exploiting it (Sec. 4.1). Collective-communication techniques are credited to Li and Chen (Sec. 3.2.2). The complete language is described in a separate Fortran D report (Sec. 2). The paper does not discuss later work.

## Sources used
| claim | section / page |
|---|---|
| Programming burden, source growth, goals | Sec. 1 |
| Fortran D statements, alignment, distribution, replication | Sec. 2, Fig. 1 |
| Reaching decompositions; Jacobi local index set | Secs. 3.1.2, Fig. 3 |
| Iteration sets, pre/mid/post sets, private scalars | Sec. 3.1.3, Fig. 4 |
| Nonlocal index sets as RSDs | Sec. 3.1.4 |
| Message vectorization; SOR and red-black examples | Secs. 3.2.1, Figs. 5-6 |
| Collective communication; runtime processing | Secs. 3.2.2-3.2.3 |
| Generated Jacobi and SOR code; storage choices | Secs. 3.3.2-3.3.3, Figs. 7-8 |
| Cross-processor loops, pipelining, strip mining | Sec. 3.4.2, Figs. 9-11 |
| Comparison with related systems | Secs. 4, 4.1 |
| Prototype status; preliminary results not shown | Sec. 5 |

## Open questions for the survey
- Which of the described optimizations were later measured, and on which machines?
- How conservative is the cross-processor loop test of Fig. 9 when subscripts are not affine?
- How should the owner-stores relaxation interact with owner-computes when both sides are distributed?
