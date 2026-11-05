# Fast Stencil-Code Computation on a Wafer-Scale Processor

**Catalog id:** `rocki2020cerebras`
**Citation:** Kamil Rocki, Dirk Van Essendelft, Ilya Sharapov, Robert Schreiber, Michael Morrison, Vladimir Kibardin, Andrey Portnoy, Jean Francois Dietiker, Madhava Syamlal, Michael James. "Fast Stencil-Code Computation on a Wafer-Scale Processor." SC20, 2020. DOI 10.1109/SC41405.2020.00062; arXiv 2010.03660.
**Paper type:** experience
**Access:** open — full text read. The extraction lacks the "simple performance model" section announced in Sec. I; nothing below relies on it.
**Card status:** full-read

## Problem
Stencil-based PDE solvers and Krylov methods have low arithmetic intensity and are limited on CPU/GPU clusters by memory bandwidth and interconnect latency (HPCG top-20 systems reach 0.5-3.1% of peak, Sec. I). The paper asks whether a wafer-scale processor with on-wafer SRAM and a nanosecond-latency mesh removes these limits for problems that fit on the wafer, using BiCGStab on a 7-point 3D stencil.

## Input abstraction
Hand-written per-tile code in a C-like task model (Listing 1, Sec. IV.1): `float16` arrays; `tensor` descriptors driving hardware address generators; `fabric` descriptors binding a channel, length, thread slot and completion trigger; hardware `fifo`s that activate a task on push; event-triggered `task`s controlled with `block`/`unblock`/`activate`. A vector statement such as `xp_fifo[] = xp_rx[] * xp_a[]` launches a background thread. The code itself "specifies the communication connectivity between tiles"; no compiler inference is involved.

## Target
Cerebras CS-1 Wafer-Scale Engine (Sec. II): ~380,000 cores on a 462 cm^2 wafer, 48 KB SRAM per core (18 GB total, no shared memory), 2D mesh fabric with five-port routers, 16 B/cycle injection per core, 4-way fp16 SIMD, nine hardware threads, 20 kW; described as an MIMD distributed-memory machine. Experiments used a 602 x 595 fabric (Sec. V). Comparison cluster: NETL Joule 2.0 (Xeon Gold 6148, Omni-Path), 1024-16384 cores (Sec. V.A).

## Data decomposition
A "straightforward domain decomposition" (Sec. IV, Fig. 3): X and Y of the X x Y x Z mesh map onto the two fabric axes and each core holds the whole Z column: iterate `v[Z]`, zero-padded result `u[Z+2]`, six matrix diagonals (the main diagonal is unity after diagonal preconditioning), and solver vectors, 10Z words per core, about 31 KB of 48 KB at Z = 1536. A sketched 2D 9-point variant gives each core a rectangular sub-block with an *output halo*; up to 38 x 38 per core (22800^2 mesh), under 20% overhead at 8 x 8 (Sec. IV.2).

## Computation mapping
Spatial placement: one core per (x, y) column computes its SpMV as a sum of seven vectors (four streamed from neighbours, two shifted local copies, the identity diagonal), core-local AXPYs and local dot-product contributions (Sec. IV.1, IV.4). Six background threads multiply into in-memory FIFOs while a higher-priority `sumtask` accumulates; a tree of completion tasks returns control to the solver (Fig. 4). The 2D variant keeps all nine multiply-adds per element on one core at the cost of redundant halo sums (Sec. IV.2).

## Communication generation
Programmer-specified, hardware-executed. Each core pushes its iterate on one channel that the router fans out to four neighbours and receives four neighbour streams on distinct channels handled by separate threads, with channel colours distinct at every tile ("tessellation routing", Fig. 5) (Sec. IV.1). The four inner products per iteration need an AllReduce: reduction along rows to two central cores, then along two central columns to one core, broadcast in reverse (Sec. IV.3, Fig. 6a); the authors report a cycle count about 10% above the fabric diameter and under 1.5 microseconds for scalars (Sec. I, IV.3). The collective is blocking since no communication-hiding BiCGStab variant was used. Routes are built as a DAG of geometry operations compiled into router tables (Fig. 6b). No cost model appears in the available text.

## Compiler / runtime split
Routing is configured offline as part of compilation; virtual channels can be reprogrammed at run time; "there is no runtime software involved with communication", arriving words being deposited by hardware into memory, registers or functional units, and task scheduling being done in hardware (Sec. II.A). No compiler IR, placement or communication synthesis is described; the visible compiler role is turning the route DAG into routing tables (Fig. 6b).

## Evaluation
BiCGStab on a 600 x 595 x 1536 mesh: 28.1 microseconds per iteration (mean of 171, std. dev. ~0.2%); with 44 operations per meshpoint per iteration (Table I) this is 0.86 PFLOPS in mixed precision (fp16 for 40 of 44 ops), about one third of peak per the abstract (Sec. V). Sec. V.A, Figs. 7-8: MFIX BiCGStab on Joule (fp64, 600^3) takes 75 ms at 1024 cores and ~6 ms at 16K cores, put at ~214x the CS-1 time on a problem with over twice the meshpoints; 370^3 stops scaling past 8K cores. Sec. VI.B, Fig. 9: mixed precision tracks fp32 to iteration 7 then plateaus near relative residual 1e-2. Sec. VI.A, Table II: projected 80-125 time steps/s for 600^3, estimated >200x a 16,384-core Joule partition.

## Principal limitation
The authors name on-wafer memory (18 GB) as the limit: the problem must fit on one wafer, and real CFD adds 30-50% operations and more memory for matrix formation (Sec. VI, VIII.B); mixed-precision acceptability in MFIX is untested (Sec. VI.B); the AllReduce is blocking (Sec. IV.3). Our observation: placement, channel colouring and thread slots are all hand-specified for one stencil, so the paper documents what a compiler for this class of machine would have to automate rather than providing one.

## Relationship to earlier / later work
- Contrasted with special-purpose machines Anton [11] and MDGRAPE [12]; communication-avoiding Krylov methods [13, 14] cited as incremental fixes (Sec. VII).
- Mixed precision context: iterative refinement [6-8], Gordon Bell fp16 solver [9], NASA Fun3d fp16 [10] (Sec. VI.B).
- Flops-per-word motivation from McCalpin [2], HPCG data [1] (Sec. I); CFD case study is NETL's MFIX (Sec. VI).

## Sources used
| claim | section / page |
|---|---|
| Motivation | Sec. I |
| Architecture, hardware tasks/routing | Sec. II, II.A |
| Programming constructs | Listing 1, Sec. IV.1, Fig. 4 |
| Decomposition, per-core memory | Sec. IV, Fig. 3, IV.2 |
| Fan-out routing, AllReduce | Sec. IV.1, IV.3, Figs. 5-6 |
| Measured results, cluster comparison | Sec. V, V.A, Table I, Figs. 7-8 |
| Precision, CFD projection | Sec. VI.A-B, Table II, Fig. 9 |
| Memory limit | Sec. VI, VIII.B |
| Related work | Sec. VII |

## Open questions for the survey
- Which of these hand-built elements (column-per-core decomposition, channel colouring, reduction trees) were later absorbed by a compiler/SDK for wafer-scale targets?
- How should the survey classify "communication generation" when routing is static hardware configuration rather than generated message code?
- Is the 2D output-halo variant comparable to halo-overlap decompositions in classical distributed-memory compilers, given the redundant summation it incurs?
