# XLA SPMD partitioner (GShard → GSPMD → Shardy)

- `lepikhin2020gshard` (metadata-level): sharding annotations plus an SPMD
  partitioner in XLA for mixture-of-experts models.
- `xu2021gspmd` (card): per-tensor sharding representation (replicated,
  tiled, partially tiled), priority-based sharding completion, per-operator
  partitioning with collectives, halo exchange, uneven partitions, no cost
  model or search.
- `alabed2025partir` (card): schedule-of-tactics alternative with a formally
  verified lowering; evaluated against GSPMD.
- `openxla2024shardy` (documentation): the OpenXLA project states Shardy
  combines ideas from the GSPMD and PartIR teams.
- `mlir2025shard` (documentation): upstream MLIR dialect "inspired by GSPMD".

Lineage above is as stated by the sources themselves (Shardy and MLIR docs
name GSPMD/PartIR; Alpa states it compiles stages with XLA+GSPMD).
