# Compiling High Performance Fortran for Distributed-Memory Systems

**Catalog id:** `harris1995dechpf`  
**Citation:** Jonathan Harris, John A. Bircsak, M. Regina Bolduc, Jill Ann Diewald, Israel Gale, Neil W. Johnson, Shin Lee, C. Alexander Nelson, Carl D. Offner. "Compiling High Performance Fortran for Distributed-Memory Systems." Digital Technical Journal 7(3):5–23, 1995. No DOI. Open copy: https://www.zx.net.nz/mirror/digital/DTJ/www.hpl.hp.com/hpjournal/dtj/vol7num3/vol7num3art1.pdf (mirror of the HP-hosted DTJ archive).  
**Paper type:** full-system  
**Access:** open — full text read (born-digital article PDF from the mirror above; the supplied scan of the whole issue was consulted only to confirm the article's location, pp. 5–23).  
**Card status:** full-read

## Problem
Distributed-memory machines were programmed almost entirely with hand-written SEND/RECEIVE code, which the authors liken to assembly programming (p. 8). HPF lets the programmer state only the data layout; the compiler must derive SPMD code, local addressing and all communication, and because network communication costs orders of magnitude more than local access, it must minimise messages (pp. 5–6).

## Input abstraction
HPF version 1.1 on Fortran 90, implemented in DEC Fortran 90 — stated to be the first implementation of the full language except transcriptive argument passing, dynamic remapping, and nested FORALL/WHERE (p. 5). Parallelism comes from Fortran 90 array assignment, FORALL, the INDEPENDENT directive on DO/FORALL, and intrinsics/library routines including XXX_SCATTER (pp. 10, 16). EXTRINSIC(HPF_LOCAL) is the escape to explicit SPMD (p. 9, p. 11). Interface ALIGN/DISTRIBUTE forms describe argument mappings (p. 10).

## Target
Clusters ("farms") of Alpha workstations or servers under Digital UNIX connected by FDDI/GIGAswitch, and SMP systems such as the AlphaServer 8400, where the same executable uses shared memory as the message medium (p. 11). Process launch and message passing are provided by Digital's Parallel Software Environment (PSE), a companion product (p. 11).

## Data decomposition
DISTRIBUTE per dimension with `*` (serial), BLOCK and CYCLIC, independently per dimension, e.g. (*, BLOCK), (*, CYCLIC), (BLOCK, BLOCK), and user-specified processor arrangements such as 4×5 (pp. 9, 14–15); ALIGN with offsets and strides, including alignment to the interior of a larger array (pp. 9–10). Default: unmapped arrays and scalars are fully replicated (p. 10); partial replication is also represented (p. 13). Internally, the DATA phase builds a *data space* per symbol describing shape, memory layout and processor layout; dope information is added to the symbol table (pp. 12–13).

## Computation mapping
The ITER phase assigns each computational expression node an *iteration space* chosen to minimise communication; the paper gives an example where strict owner-computes would move two CYCLIC operands to a BLOCK target, whereas computing where the operands are aligned and moving one result is cheaper (p. 13). The ARG phase inserts caller-side remapping to temporaries when actual and dummy mappings differ, with copy-out for OUT arguments (pp. 13–14). STRIP localises FORALL/array assignments into per-processor loops with bounds that are inlined expressions of the processor number, not run-time calls (pp. 14–15, Fig. 11).

## Communication generation
DIVIDE splits expressions into communication-free regions and materialises each inter-region transfer as an assignment to a temporary mapped as the consumer needs, classifying it as *full knowledge* (both sides know) or *partial knowledge* (one side knows; typical of vector-valued subscripts) (p. 14). STRIP inserts library calls and explicit SEND/RECEIVE; no barriers are inserted because sends/receives enforce ordering and PSE buffers early sends (p. 15). Optimisations: message vectorisation — one SEND/RECEIVE per array per processor pair, also for partial-knowledge and inlined XXX_SCATTER (pp. 15–16); nearest-neighbour recognition without user tags, giving each array "shadow edges" so halo values are moved once and the computation is then local, with no local copy and possible message merging (pp. 16–17); reductions inlined as local reduce, logarithmic combine, local copy (pp. 17–18); run-time preprocessing of irregular accesses whose indirection vectors are loop-invariant, computing addresses once so later statements become full-knowledge vectorised messages (p. 18); fast paths for contiguous sections, unique source/target processor, and replicated indirection vectors (p. 18).

## Compiler / runtime split
Static compiler: front end, *transform* (LOWER, DATA, ITER, ARG, DIVIDE, STRIP), middle end, GEM back end (pp. 11–12). Transform emits inlined addressing expressions "unlike other HPF implementations" (p. 15). Runtime: PSE for process invocation and messaging, plus library routines for data movement invoked by STRIP (pp. 11, 14). Irregular accesses are the one place run-time preprocessing is used (p. 18).

## Evaluation
Eight 275-MHz DEC 3000/900 workstations on a GIGAswitch and an 8-processor 300-MHz AlphaServer 8400; speedups relative to DEC Fortran 77 on one processor. Shallow-water, 512×512, ITMAX=50: 8.57× (farm) and 10.6× (SMP) on 8 processors (Table 1), versus Applied Parallel Research's published 7.50× (IBM SP2) and 7.38× (Paragon) (Table 2). Conjugate-gradient Poisson, 1000×1000: 14.1× farm, 17.0× SMP on 8 (Table 3). Red-black 3-D relaxation, 128³, GENESIS code: HPF 8.04× vs PVM 7.01× on 8 workstations (Table 4). Superlinear results are attributed to extra optimisation and cache effects (p. 19).

## Principal limitation
Stated: no transcriptive argument passing, dynamic remapping or nested FORALL/WHERE (p. 5); partial-knowledge communication is "much more expensive" in time or space (p. 16); benchmark-quality runs were not made beyond eight identical processors (p. 19). Our observation: all benchmarks are regular stencil/CG kernels; no irregular application performance is reported.

## Relationship to earlier / later work
States message vectorisation was widely studied, citing Amarasinghe & Lam, Tseng's Fortran D compiler and Rogers (p. 15); run-time preprocessing of irregular accesses is "a popular technique", citing Saltz, Mirchandaney & Crowley (p. 18); automatic parallelisation and data-layout research is cited as context (Albert/Knobe/Steele CM compilation, Knobe data optimisation, Gupta & Banerjee PARADIGM, Chatterjee et al., Anderson & Lam) (p. 6). The strip-mining approach follows Allen & Kennedy's vector register allocation (p. 16); data/iteration spaces follow Offner's HICSS paper (p. 12). Compared empirically with Applied Parallel Research's HPF results and with hand-written PVM (pp. 19–20).

## Sources used
| claim | section / page |
|---|---|
| HPF 1.1 coverage and exclusions | Introduction, p. 5 |
| distributions, ALIGN, replicated default | Overview of HPF, pp. 9–10 |
| target machines, PSE | The Target Machine, p. 11 |
| compiler components and transform phases | Architecture / Overview of Transform, pp. 11–12 |
| data space / iteration space, ITER counterexample to owner-computes | DATA, ITER, pp. 12–13 |
| ARG remapping | ARG, pp. 13–14 |
| DIVIDE regions, full vs partial knowledge | DIVIDE, p. 14 |
| STRIP localisation, inlined addressing, no barriers | STRIP, pp. 14–15, Fig. 11 |
| message vectorisation, SCATTER inlining | Some Optimizations, pp. 15–16 |
| shadow edges, nearest neighbour | pp. 16–17 |
| reductions | pp. 17–18 |
| run-time preprocessing, other optimisations | p. 18 |
| benchmark results | Performance, Tables 1–4, pp. 18–20 |

## Open questions for the survey
- How does the compiler's shadow-edge width get chosen when several shifted references with different offsets appear in one compilation unit?
- What is the actual mechanism of partial-knowledge communication (does the receiver poll, or does a count message precede data)?
- How much of the superlinear speedup is attributable to the -wsf optimiser versus the parallel decomposition?
