# Dynamic Data Partitioning for Distributed-Memory Multicomputers
**Catalog id:** `palermo1996dynamic`
**Citation:** Daniel J. Palermo, Eugene W. Hodges IV, and Prithviraj Banerjee. "Dynamic Data Partitioning for Distributed-Memory Multicomputers." Journal of Parallel and Distributed Computing 38, 158-175 (1996), article no. 0138. Record used: journal header and printed page numbers; no DOI printed.
**Paper type:** compiler-technique
**Access:** PDF supplied by the repository owner. Full text read (18 PDF pages, printed pp. 158-175). The text layer is present and readable with a few dropped letters. Figure graphics (graphs, plots, pseudo-code boxes) are not in the text layer; Tables I-III are extracted.
**Card status:** full-read

## Problem
A single static distribution is a compromise when a program's access pattern changes between phases, as in a 2-D FFT that works along rows and then along columns (p. 158-159). The paper selects, automatically, distributions that change during a run by weighing redistribution cost, as an extension of PARADIGM's static partitioner (p. 158, 160-161).

## Input abstraction
A serial program analyzed by Parafrase-2. Flow dependences, weighted by communication cost, form a communication graph over statements (p. 161-162). Phases are not given by the user; the program is split recursively at statement boundaries (p. 162-164). Shallow was inlined and a GOTO loop rewritten as an explicit loop (p. 171).

## Target
Cost models for an Intel Paragon and a TMC CM-5, using measured startup and per-byte parameters (p. 162, Table I). The Table II estimates use 32 processors (p. 165); Table III gives measured transpose times from 8 to 128 processors (p. 172).

## Data decomposition
Each array dimension is BLOCK or * on a two-dimensional abstract mesh, and the static partitioner chooses the mesh shape and each layout (p. 165, 172-173). ADI2D phases alternate between (*, BLOCK) and (BLOCK, *) (Table II). Shallow uses only BLOCK, on an 8 by 4 mesh (p. 172).

## Computation mapping
Loop-level partitioning is not restated; the static partitioner fixes each phase's distribution (p. 160-161). In static ADI, two recurrences are software-pipelined with a granularity chosen from compile-time estimates (p. 170). The dynamic ADI version uses data-parallel phases separated by transposes (p. 170).

## Communication generation
Redistribution is generated as transposes, and transposes at the same program point are aggregated into one message (p. 170). Each phase-transition edge is costed for redistribution (p. 165). Pipelined loops use a coarse granularity from the compile-time pipeline model (p. 170-171; Fig. 11).

## Compiler / runtime split
All decomposition, costing and selection happen at compile time. The phase tree comes from repeated maximal cuts of the communication graph, and branch and bound accepts a split only if the summed estimated times improve (p. 163-164). The phase transition graph is solved by a shortest-path search, using Dijkstra's algorithm in O(V^2) time (p. 165). The output is an MPI program from the prototype compiler (p. 173).

## Evaluation
ADI2D on a 512 by 512 problem runs on a Paragon and a CM-5, comparing fine-grain and coarse-grain static pipelining with dynamic redistribution with and without aggregation (p. 169-171; Figs. 10-12). On the Paragon, aggregated dynamic is reported to be over 70 percent faster than fine-grain static and 60 percent faster than coarse-grain static. On the CM-5 it is more than twice as fast as fine-grain static, but beats coarse-grain only at extremely large processor counts (p. 170). For Shallow, the partitioner selects a static 2-D layout with no redistribution. It matches the 1-D layout at small processor counts and outperforms it by up to 1.6 times (Paragon) and 2.7 times (CM-5) at larger counts (p. 171-173; Fig. 14).

## Principal limitation
As the paper states it: the static pipeline cost model is very conservative, which is why a dynamic scheme was chosen for ADI on both machines (p. 170); cut windows are resolved by always taking the earliest cut point (p. 164); and the hierarchical component affinity graph is not implemented, so interprocedural partitioning is future work (p. 169).
our observation: The Shallow runs needed hand loop distribution and hand removal of copy loops (p. 173), so the reported times include manual changes.

## Relationship to earlier / later work
- The method extends the static partitioning algorithm of PARADIGM (refs. 14, 16) and its cost estimation (ref. 15), and builds on the authors' earlier dynamic selection paper (ref. 27) (p. 158, 161).
- Anderson and Lam (ref. 1) show that dynamic decomposition is NP-hard (p. 160). Bixby, Kennedy and Kremer (ref. 5), Kremer (ref. 23) and Garcia et al. (ref. 12) use 0-1 integer programming; Kennedy and Kremer (ref. 24) use dynamic programming (p. 160, 165-166).
- Hudak and Abraham (refs. 18, 19) insert remapping points, and Sheffler et al. (ref. 34) apply graph contraction (p. 161).
- Kennedy and Kremer (ref. 21) predicted a one-dimensional column-wise distribution for Shallow (p. 173).
- The pipeline cost model is from the authors' earlier work (ref. 28), and redistribution costs follow Ramaswamy and Banerjee (ref. 31) (p. 165, 170).

## Sources used
| claim | section / page |
|---|---|
| Motivation: FFT row and column phases | Sec. 2; p. 158-159; Fig. 1 |
| Related work | Sec. 3; p. 159-161 |
| Communication graph and cost scaling | Sec. 4.1; p. 161-162; Table I |
| Maximal cut, cut windows, branch and bound | Sec. 4.1; p. 162-164; Figs. 3-5 |
| Phase transition graph and shortest path | Sec. 4.2; p. 164-166; Table II |
| Hierarchical component affinity graph (not implemented) | Sec. 5; p. 168-169 |
| ADI2D results | Sec. 6.1; p. 169-172; Figs. 10-12; Table III |
| Shallow results and manual changes | Sec. 6.2; p. 171-173; Figs. 13-14 |
| Conclusions and future work | Sec. 7; p. 173-174 |

## Open questions for the survey
- The authors say a more accurate pipeline model would have selected a static scheme on the CM-5 (p. 170). Do later systems in this set adopt pipeline cost models, and does the static-versus-dynamic choice change under them?
- Statement reordering and loop distribution could reduce redistribution (p. 170, footnote 9; p. 174). Did later work in this set adopt them?
- Redistribution across procedure boundaries is listed as future work (p. 174). Which later systems in the set handle it?
