# The Cosmic Cube
**Catalog id:** `seitz1985cosmic`
**Citation:** Charles L. Seitz. "The Cosmic Cube." Communications of the ACM 28(1), pp. 22-33, January 1985. Record used: supplied PDF (no DOI printed in it).
**Paper type:** hardware
**Access:** PDF supplied by the repository owner. Full text read (text layer complete on all 12 pages; some OCR errors in numbers and figure labels, which I did not rely on).
**Card status:** full-read

## Problem
The paper presents the Cosmic Cube, an experimental 64-node message-passing machine (p. 22). Each node has its own storage, with no switching network to shared storage (p. 23), and processes communicate by message passing, not shared variables (p. 22). Process placement is discussed (pp. 24-26). The authors say compilers do not find concurrency in sequential programs (p. 26), and the paper does not describe compiler generation of communication.

## Input abstraction
A process is a sequential program that sends and receives messages, and each has a global ID (p. 23). Process code is written in ordinary languages such as Pascal or C, extended with statements or external procedures for sending and receiving (p. 24). The primitives were added to languages as external functions, which the authors say makes process code unnecessarily complex (p. 31).

## Target
64 nodes, each with an Intel 8086 and an 8087 floating-point coprocessor at 5 MHz, 128 KB of storage and 8 KB of read-only storage (pp. 28-29). Each node has six bidirectional channels, wired as a binary 6-cube (pp. 22-23).

## Data decomposition
Application-defined. In the N-body formulation each process hosts one body (p. 27). The circuit simulator's admittance matrix is partitioned by rows into processes (p. 31). No general distribution scheme for arrays is described.

## Computation mapping
Task placement. The embedding of the process structure into the machine graph determines communication locality and load balance (p. 25). A library process can choose a node for a new process from load and storage data (p. 25). A process stays in its node once instantiated (p. 24).

## Communication generation
Programmer-explicit. Send and receive are the explicit communication and synchronization primitives the programmer sees (p. 22). The calls do not block: each creates a pending request, tested through a lock variable, while execution continues (p. 30). No compiler-generated communication is described.

## Compiler / runtime split
Process code is compiled on other computers and loaded into each node (p. 24). The kernel handles routing and scheduling at run time (pp. 23-24, 30). The text gives the compiler two roles: generating process code (p. 26), and, as a suggested improvement, inserting lock-variable tests by data-flow analysis (p. 32). Our observation: Fig. 5 (p. 27) shows the send and receive code that such a compiler would have to emit.

## Evaluation
Applications run up to 3 million floating-point operations per second (p. 31). One node runs at one-sixth the speed of a VAX 11/780, so the authors expect 64 nodes to run at best about ten times faster (p. 31). Measured overhead values range from 0.025 to 0.500 (p. 31).

## Principal limitation
As the authors state, the approach is limited to applications with highly concurrent formulations (p. 32), and most deficiencies lie in representing and compiling process code (p. 31). Our observation: the paper gives no route from sequential programs to process code (p. 26).

## Relationship to earlier / later work
The authors state that the design is based largely on Lang's modeling and simulations (1980-1982), and that its origins lie in Browning and Locanthi's Caltech research (1978-1980) (p. 33). They cite Hoare's communicating sequential processes, Hewitt's actors, Martin's processing surfaces and Kung's systolic algorithms as influences (p. 33). They relate the hypercube to Omega and banyan networks (p. 23). The paper cites no later systems, but describes the single-chip Mosaic node developed at Caltech (p. 33).

## Sources used
| claim | section / page |
|---|---|
| Message passing instead of shared variables; MIMD | The message-passing architecture, p. 22 |
| Node-local storage; no switching network; node-count conjecture | Message-passing architecture, p. 23 |
| Process model, global IDs, message order | Process programming, p. 23 |
| Kernel per node; routing; no process relocation | Process programming; Process distribution, pp. 23-24 |
| Process code in ordinary languages | Process distribution, p. 24 |
| Process structure embedding; library placement | Concurrency approach, p. 25 |
| Compilers do not find concurrency in sequential programs | Concurrency approach; Concurrent formulations, p. 26 |
| N-body formulation and process code | Figure 3, p. 25; Figure 5, p. 27 |
| Hardware: 8086 and 8087, 5 MHz, 128 KB | Cosmic Cube hardware, pp. 28-29 |
| Overhead and speedup model | Cosmic Cube hardware, p. 28 |
| Non-blocking calls and fragmentation | Software, p. 30 |
| Performance figures and VAX comparison | Applications and benchmarks, p. 31 |
| Lock-test suggestion (data-flow analysis) | Future perfect cubes, pp. 31-32 |
| Limit to highly concurrent formulations | Future perfect cubes, p. 32 |
| Origins and related work | Appendix, p. 33 |

## Open questions for the survey
- The paper gives the compiler two roles, generating process code and suggesting lock-test insertion (pp. 26, 32). Should the survey separate compiler-inserted synchronization from compiler-generated messages?
- Placement is chosen by the programmer or a library process and fixed at spawn time (pp. 24-25). Should the survey record it as load-time or runtime placement?
