# PartIR: Composing SPMD Partitioning Strategies for Machine Learning

**Catalog id:** `alabed2025partir`
**Citation:** Sami Alabed, Daniel Belov, Bart Chrzaszcz, Juliana Franco, Dominik Grewe, Dougal Maclaurin, James Molloy, Tom Natan, Tamara Norman, Xiaoyue Pan, Adam Paszke, Norman A. Rink, Michael Schaarschmidt, Timur Sitdikov, Agnieszka Swietlik, Dimitrios Vytiniotis, Joel Wee. "PartIR: Composing SPMD Partitioning Strategies for Machine Learning." ASPLOS, 2025. DOI 10.1145/3669940.3707284; arXiv 2401.11202 (text read: arXiv v4; venue/DOI from the catalog record, not printed in the text).
**Paper type:** full-system
**Access:** open — full text read.
**Card status:** full-read

## Problem
Training large NNs needs combined batch, model and optimizer-state sharding. The authors argue (Sec. 1) that annotation-driven partitioners such as GSPMD put sharding decisions inside model code, making it non-portable across topologies and forcing conflict resolution by trial and error, while automatic partitioners are unpredictable and slow. PartIR aims to decouple strategy from model, be predictable, and compose manual with automatic strategies.

## Input abstraction
An unmodified JAX function traced to StableHLO (Sec. 2.4), plus a named-axis device mesh and a *schedule*: an ordered list of *tactics*. `ManualPartition` maps input names to a dimension sharded along an axis; `AutomaticPartition` searches over axes; `PartIR.jit` returns the device-local program and per-tactic metadata (Sec. 3, Table 1). Tactics desugar into compiler *actions*: `tile<value, dim, axis>`, `atomic<value, axis>` (force replication) and `propagate`; `tag` names intermediates (Sec. 3, Sec. 8).

## Target
TPU and GPU meshes; the mesh is said to model host-tree and physical-mesh (TPU pod) topologies (Sec. 2.2). Experiments use TPUv3 (32/128 devices) and A100 (16 GPUs), backend XLA/OpenXLA (Sec. 7.1).

## Data decomposition
Sharding is a program rewrite: a *value tiling* action wraps a value in a `loop` over a mesh axis with `#tile<d>`, whose body yields `slice d %x[%r]`, the r-th of n equal contiguous chunks (Sec. 5.1); replication is a loop with `[any]` (Sec. 8). Formally (App. C.2), *distributed types* `dtensor<stacked axes, [{a}n, ...]>` let a dimension be split over several axes and use *stacked axes* for unstructured per-device collections. "Deep tiling" lets later tactics add axes without undoing earlier ones (App. B.1.2). Axis size must exactly divide the dimension (Sec. 8).

## Computation mapping
Flat SPMD. Propagation (Sec. 5.2) uses a *tile-mapping registry* of algebraic equivalences per op (e.g. tiling both contracting dims of `matmul` gives a `#sum` loop) and greedily, without cost heuristics, pushes tiling until every op is inside a loop. Nested loops over one axis are illegal and ambiguous matches are *conflicts* that tactic order, not the compiler, resolves (Sec. 5.2.3). Batch, Megatron, ZeRO-2/3 (FSDP), embedding, multi-query and edge-sharding strategies are built from these actions (Sec. 2.3, 7.3, App. A.4).

## Communication generation
PartIR:HLO adds mesh-axis collectives `all_reduce`, `all_slice`, `all_gather`; fusion yields `reduce_scatter` and `all_to_all` (Sec. 6, Listing 8). Lowering turns slices into `all_slice` and loop results into `all_gather`/`all_reduce`, cancelling slice/gather pairs (Sec. 6.1); `spmd.redistribute` lowers to one `all_gather` plus one `all_slice` (App. C.5). Rewrites for compute/communication overlap are mentioned (Sec. 6). The cost model is a simple analytical simulator over PartIR:HLO (live memory, FLOPs, bytes per device spec) whose relative, not absolute, estimates drive the Monte Carlo tree search in `AutomaticPartition` (Sec. 3, App. A.3).

## Compiler / runtime split
Entirely compile-time, in MLIR between tracing and XLA (Sec. 4, Fig. 3): StableHLO -> PartIR:Core (`loop`, `slice`) -> optional PartIR:Temporal (sequential/micro-batching) -> PartIR:SPMD (`dtensor`, `spmd.execute`, `redistribute`, `tile_reduce`) -> PartIR:HLO -> StableHLO for XLA. Core-to-SPMD lowering is proven correct (Theorem C.7); propagation is not (App. C). `partir.jit` runs at JAX compile time.

## Evaluation
Models U-Net, GNS, T32/T48 Transformers, IT32 inference (Sec. 7.1). Table 2: MFU/HBM on par with GSPMD within +/-1% (58.5 vs 58.3% on 16x2 TPU 5B; 52.3 vs 52.2% on 32x4 TPU 32B; 42.2 vs 42.9% on 8x2 GPU). Table 3: collective counts match analytic expectations (T32 batch parallelism: 290 AllReduces = 289 parameters + loss). Fig. 6 (8x4 TPUs): AllAuto comparable to manual for T32, BP+Auto+Z3 slower. Fig. 7 (U-Net): single-tactic PartIR runs out of memory, GSPMD without constraints is slower, and matching PartIR needed 5 hand-placed constraints per U-Net layer. Sec. 7.5: partitioning is at most 14% of XLA compile time; App. A.3.3: automatic search up to 1250 s.

## Principal limitation
Sec. 8: limited reshape support, exact-divisibility requirement, little padding/spatial partitioning, greedy propagation that may shard values meant to be replicated, and corner-case conflicts needing `tag`+`atomic`; MPMD/pipeline is future work (Sec. 10). Our observation: GSPMD parity is shown only on Transformers with hand-matched annotations, and the automatic tactic is judged by a simulator the authors call simple.

## Relationship to earlier / later work
- Compares against GSPMD [70] (Sec. 7.2, 7.4, 8); GSPMD builds on GShard (Sec. 9). PartIR and GSPMD learnings feed Shardy [39] (Sec. 1, 9).
- Schedule API inspired by Halide [47], TVM, TACO, Fireiron, DISTAL [71] (Sec. 3, 9).
- `AutomaticPartition` implements AutoMap [2, 54]; orthogonal to Alpa [73] (Sec. 3, 9, App. A.3.3).
- TMR likened to split annotations [41] (Sec. 5.2.1); Lift/RISE kin, DaCe and DistIR contrasted (Sec. 9); redistribution per Rink et al. [51] (App. C).

## Sources used
| claim | section / page |
|---|---|
| Problem framing | Sec. 1 |
| Schedule/tactics/actions | Sec. 3, Table 1, Sec. 8 |
| Mesh and hardware | Sec. 2.2, 7.1 |
| Tiling, distributed types | Sec. 5.1, App. B.1.2, App. C.2 |
| TMR, propagation, conflicts | Sec. 5.2 |
| Collectives, lowering, simulator | Sec. 6, 6.1, App. A.3, C.5 |
| Dialect pipeline, proof | Sec. 4, Fig. 3, App. C |
| Results | Sec. 7.2-7.5, Tables 2-3, Figs. 6-8, App. A.3 |
| Limitations, related work | Sec. 8-10 |

## Open questions for the survey
- How does "distribution as loop/slice rewrite" compare in expressiveness with layout-annotation propagation (GSPMD, Shardy) on reshapes and non-divisible shapes?
- Can "collective counts match the strategy's analytic expectation" serve as a predictability metric for other systems in the survey?
- Propagation is unverified and per-op; how does its trusted base compare with dependence-derived communication in polyhedral compilers?
