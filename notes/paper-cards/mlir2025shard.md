# MLIR 'shard' Dialect (official documentation; formerly 'mesh')

**Catalog id:** `mlir2025shard`
**Citation:** LLVM/MLIR community. "'shard' Dialect." MLIR documentation, https://mlir.llvm.org/docs/Dialects/Shard/, 2025. No DOI.
**Paper type:** specification (documentation)
**Access:** open — official documentation, fetched 2026-11-07, read in full as plain text. The page states the dialect "was called mesh, but it was renamed to better reflect what it actually does" (dialect overview).
**Card status:** full-read

## Problem
The dialect defines "attributes, operations, and interfaces for working with tensor sharding and device communication" and "is inspired by GSPMD" (dialect overview). Unlike "traditional collectives ... defined in terms of message-passing between explicit buffers", its collectives are "defined in terms of how data moves across the dimensions of a tensor, and the participating processes are inferred from how the tensor is sharded" ("Collective Communication Operations"). No further motivation is given.

## Input abstraction
MLIR IR over ranked tensors (memrefs accepted by `all_gather`, `all_reduce`, `reduce_scatter`, `update_halo`; operand tables). Ops:
- `shard.grid`: symbol op with `sym_name` and `shape` "in the same notation as a tensor shape", with dynamic dimensions such as `4x?` "where the exact number of devices might not be determined during compile time" ("shard.grid" op).
- `shard.sharding`: refers to a grid; sub-array i of `split_axes` lists the grid axes along which tensor dimension i is split, `[[]]` meaning fully replicated; optional `halo_sizes` (start and end per sharded dimension, `?` for dynamic); optional `sharded_dims_offsets` (start offset of every shard plus an end value, e.g. shards `4x2, 4x3, 4x4, 4x5`); "only contiguous sharding is supported"; the two options are mutually exclusive ("shard.sharding" op).
- `shard.shard`: annotates a value with a sharding; `annotate_for_users` applies it to the value's uses instead of its defining op; conflicting annotations are undefined ("shard.shard" op).
Queries: `shard.get_sharding`, `shard.grid_shape`, `shard.shard_shape` ("might be used during partition"). No `partial_axes` field and no `sharding_constraint` op appear; the only "partial" token is the `#shard.partial<...>` mnemonic of `ReductionKindAttr` ("Attributes").

## Target
Not stated; the page speaks only of "devices" or "processes" in a grid and names no hardware or backend.

## Data decomposition
Contiguous block sharding of each tensor dimension along zero, one or several grid axes, full replication (`[[]]`), uneven shards via `sharded_dims_offsets`, and halos via `halo_sizes`, each possibly dynamic ("shard.sharding" op).

## Computation mapping
The execution model "assumes SPMD": "Every process runs the same program" and "At any collective operation, all processes are in sync" ("Purity and Execution Model"). `shard.process_multi_index` "is used in the SPMD format of IR"; `shard.process_linear_index` and `shard.neighbors_linear_indices` give a device's linear index and its previous/next neighbours along `split_axes`, negative where none exists (op descriptions). Per-device operator partitioning is not described.

## Communication generation
Collectives take `grid` and `grid_axes`; "Devices that have the same coordinates outside the listed grid_axes belong to the same group"; group order follows `grid_axes` "from outermost to innermost"; roots and endpoints are "in-group" multi-indices ("Device Groups", "In-group Devices"). Operations present, exactly: `all_gather` (concatenate along `gather_axis`, replicate), `all_reduce` (element-wise, `reduction` kind, result type may differ), `all_slice` (crop to in-group slice, "does not involve any communication"), `all_to_all` (`split_axis`/`concat_axis`), `broadcast` (`root`), `gather` (to `root`, undefined elsewhere), `reduce` (to `root`), `reduce_scatter` (`scatter_dim`), `scatter` (from `root`), `send`/`recv` (in-group `destination`/`source`; "not collective and are not pure"), `shift` (along a grid axis by `offset`, optional `rotate`), `update_halo` (refreshes halos after remote data "might have changed"; destination holds "the local data (not halos)") (op descriptions). Reduction kinds: sum, max, min, product, average, bitwise_and/or/xor, generic ("ReductionKindAttr"). Collectives are "considered pure" for DCE/CSE and deadlock avoidance; a removed collective "must be removed from every path and every process" ("Purity and Execution Model"). No pass that inserts collectives is named; "partition" ("shard.shard_shape" op) and "SPMD format of IR" ("shard.process_multi_index" op) are the only hints. No cost model is described.

## Compiler / runtime split
Sharding is declared by IR annotation (`shard.shard`); grid shape, halo sizes and shard offsets may stay dynamic for "configurations where the exact number of devices might not be determined during compile time" ("shard.grid", "shard.sharding" ops). No runtime or lowering is described.

## Evaluation
None; the page is a dialect reference.

## Principal limitation
As documented: contiguous sharding only; halos and shard offsets cannot be combined; non-root `gather`/`reduce` and non-rotating `shift` results are undefined; `all_slice` devices "may not have replicated input data" ("shard.sharding", "shard.gather", "shard.reduce", "shard.shift", "shard.all_slice" ops). Our observation: the page documents vocabulary, not the propagation or partitioning passes, so the dialect's compiler behaviour cannot be assessed from it.

## Relationship to earlier / later work
- "Inspired by GSPMD" (dialect overview; link text "General and Scalable Parallelization for ML Computation Graphs").
- Renamed from the `mesh` dialect (dialect overview).
- inferred: `vaidya2025distributed` contrasts its `part_tensor` dialect with this one; the page names neither it nor `bisbas2024shared`.

## Sources used
| claim | section / pages |
|---|---|
| Purpose, GSPMD, rename | dialect overview |
| Group semantics, order | "Collective Communication Operations", "Device Groups", "In-group Devices" |
| SPMD model, purity | "Purity and Execution Model" |
| Grid, sharding, annotation | "shard.grid", "shard.sharding", "shard.shard" ops |
| Collectives, p2p, halo | the named op entries |
| Reduction kinds | "ReductionKindAttr" |

## Open questions for the survey
- Which upstream pass propagates shardings and partitions to the "SPMD format of IR", and where is it documented?
- Does the dialect carry partial (pending-reduction) shardings as GSPMD does? This page shows no such field.
- What lowers `shard` collectives to the `mpi` dialect or vendor libraries, and is `update_halo` the bridge to `bisbas2024shared`?

## Reference list check
The page has no reference list. External names appearing in the page body: GSPMD (linked by its paper title "General and Scalable Parallelization for ML Computation Graphs"), a Wikipedia article on collective operations, the former dialect name `mesh`, and MLIR's own traits/interfaces (e.g. `SymbolUserOpInterface`, `DestinationStyleOpInterface`). The site navigation also lists sibling dialects (`mpi`, `sparse_tensor`, `gpu`, etc.), but the page body does not reference them. No RFC, paper beyond GSPMD, or external system (Shardy, PartIR, XLA, JAX) is named.
