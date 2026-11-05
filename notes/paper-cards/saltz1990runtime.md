# Run-time Scheduling and Execution of Loops on Message Passing Machines

**Catalog id:** `saltz1990runtime`  
**Citation:** Joel Saltz, Kay Crowley, Ravi Mirchandaney, Harry Berryman. "Run-time scheduling and execution of loops on message passing machines." Journal of Parallel and Distributed Computing 8(4):303–312, 1990. DOI 10.1016/0743-7315(90)90129-D. Report version: ICASE Report 89-7 / NASA CR-181785, January 1989 (cover author order: Crowley, Saltz, Mirchandaney, Berryman). Open copy: NASA NTRS scan of CR-181785 (local file `saltz1989runtime.pdf`).  
**Paper type:** runtime  
**Access:** open — full text read (ICASE 89-7 / NASA CR-181785 OCR scan; the JPDC article is the catalog's primary record and was not read. The text cites an Appendix on a parallel preprocessor that is missing from the scan).  
**Card status:** full-read

## Problem
Sparse solvers and general PDE codes keep loop dependences in integer data structures (e.g. the `column` array of a compressed-row layout), not in program text, so neither compiler nor a naive runtime knows which elements a processor will need (Sec. 1.1, 2.1). Demand fetching on a message-passing machine pays a startup per access and translates global to local indices in every iteration (Sec. 2.1, 3.1). Scope is restricted to "start-time schedulable" loops: all dependences are fixed before the loop starts and do not change during it (Sec. 1.1, 2.3).

## Input abstraction
Sequential loops over 1-D arrays indexed through indirection arrays: sparse matrix-vector product (Fig. 3), sparse lower-triangular solve (Fig. 6), generalised to sequences of doall loops with inter-phase dependences (Fig. 5) and to blocks applying several functions over index subsets under start-time-evaluable conditionals (Sec. 3.4, Figs. 9–10). The system's input is a *schedule*: per phase and processor, the list of global indices to execute (Sec. 3.3).

## Target
Intel iPSC/2 hypercube, 1–32 processors, plus earlier iPSC/1 results (Sec. 4.1, 4.4). Model: distributed memory, no remote-access hardware, startup cost far above per-word cost (Sec. 1.1).

## Data decomposition
Arbitrary irregular partitions of left-hand-side arrays, derived from the dependence graph in the integer arrays or given a priori by the user; both were used (Sec. 2.3). Read-only arrays are placed where used; written arrays are stored locally in first-write order; off-processor values sit in receive buffers (Sec. 3.2). Experiments used equal contiguous index blocks (Sec. 4.1) and m×n strip/block aggregates for the triangular solve (Sec. 4.3–4.4).

## Computation mapping
Explicit per-phase iteration lists, `schedule(phase, pe, j)`, fix both assignment and execution order; order matters for clustered recursion solves (Figs. 4, 7; Sec. 2.1–2.2). An analytic model for the triangular solve argues the aggregation parameters should satisfy m ≥ n with n = P (Sec. 4.3).

## Communication generation
Entirely by the run-time preprocessor. From schedule and dependence DAG it (1) computes per phase what each processor must receive from every other, derives send lists via the transposed DAG, and pairs each send with a receive so both sides know the message layout; (2) assigns local addresses from the schedule's execution order and rewrites dependents and send/receive lists into local coordinates; (3) reorders input data so the executer is function-independent (Sec. 3.3). One message per destination per phase (Sec. 2.1, 3.3). In the executer, `CommunicateData()` builds and exchanges packets from the tables, and the inner loop pops a `local` flag and a `dependents` index to read local storage or the receive buffer (Sec. 3.2, Fig. 8).

## Compiler / runtime split
No compiler: preprocessor and executer are hand-written templates customised per loop body (Sec. 1.1, 3.4). The report proposes `begin-node`/`end-node` annotations so a tool could emit them, and says a system transforming annotated programs into dependence-graph-encoding code is being designed (Sec. 2.3, 3.4). Conclusion 2: compilers will likely customise tuned templates rather than generate such programs (Sec. 5).

## Evaluation
iPSC/2, up to 32 processors. Sparse MVM, 100×100 five-point mesh: 409 ms parallel-on-one vs 372 ms sequential (~9% executer overhead); 18 ms on 32 processors, overhead ~10% (Table 1, Sec. 4.1); 32-processor efficiency 0.65/0.75/0.81 for 100/150/200-point meshes (Sec. 4.1). Linda demand fetch: 17.9 s on 8 processors vs 0.055 s with the executer (Table 2, Sec. 4.2). Triangular solve, 32 nodes, 192×192 mesh: 295 ms at finest granularity vs 99 ms at n = m = 32; 576×576 mesh 34% efficiency, ~33% executer overhead (Table 3, Sec. 4.4). Reduced 300×300 system on a 32-node iPSC/1: best efficiency 53% (Table 4).

## Principal limitation
Stated: preprocessing cost is high, so the method pays only for loops executed many times, and only for start-time schedulable loops (Sec. 2.3, 5); overhead reached ~33% for fine-grained many-phase solves (Sec. 4.4). Our observation: the missing Appendix leaves the preprocessor's own parallelisation and cost undocumented in the copy read.

## Relationship to earlier / later work
Discusses DINO, Callahan & Kennedy, BLAZE (Koelbel, Mehrotra, Van Rosendale) and Linda as approaches suited to regular, compile-time-known patterns (Sec. 1.2); Linda is the experimental baseline (Sec. 4.2). Builds on the authors' 1988 runtime-support paper [6] and Saltz's aggregation methods [9] (Sec. 2.2, 4.4). Inferred: this "preprocessor/executer" is what saltz1991multiprocessor later calls inspector/executor, citing the JPDC version as [26].

## Sources used
| claim | section / page |
|---|---|
| start-time schedulable definition | Sec. 1.1, p. 3 |
| packetising, prescheduling, global→local translation | Sec. 2.1, p. 8 |
| preprocessor's three tasks, send/receive pairing | Sec. 3.3, p. 13–15 |
| executer structure (`local`, `dependents`, `datalist`) | Sec. 3.2, Fig. 8, p. 12–14 |
| schedule template struct | Sec. 3.4, Fig. 10, p. 16 |
| MVM timings, 9–10% overhead, efficiencies | Table 1, Sec. 4.1, p. 17–18 |
| Linda comparison | Table 2, Sec. 4.2, p. 19 |
| granularity model m ≥ n, n = P | Sec. 4.3, p. 19–21 |
| triangular solve timings, 33% overhead, 34% efficiency | Table 3, Sec. 4.4, p. 21–23 |
| iPSC/1 reduced system 53% | Table 4, p. 23 |
| conclusions on templates and preprocessing cost | Sec. 5, p. 23–24 |

## Open questions for the survey
- When did these per-phase send/receive tables become PARTI's reusable "schedule" object, and what changed?
- Is the ~33% executer overhead intrinsic to table-driven execution or removable by compiler specialisation?
- Does the JPDC version add results or adopt the inspector/executor vocabulary absent from the ICASE report?
