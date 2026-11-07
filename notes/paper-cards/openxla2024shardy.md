# Shardy: an MLIR-based tensor partitioning system (official documentation)

**Catalog id:** `openxla2024shardy`
**Citation:** OpenXLA Project. "Shardy" documentation (overview, sharding_representation, propagation, compiler_api, dialect_agnostic_sharding). openxla/shardy repository, docs folder, branch main, 2024–. https://openxla.org/shardy.
**Paper type:** specification (documentation)
**Access:** open — official documentation; the five pages above fetched from raw.githubusercontent.com on 2026-11-07.
**Card status:** full-read of the five listed pages. Not read: `sdy_dialect.md` and `sdy_op_interfaces`, linked from propagation.md ("Data flow ops") and compiler_api.md ("Sharding Group"), and the `images/` figures. The overview has no table of contents.

## Problem
Shardy is "an MLIR-based tensor partitioning system for all dialects", built by the GSPMD and PartIR teams to combine "GSPMD's propagation with PartIR's incremental partitioning" for "more control and predictability", better reshapes "which notoriously generate extra communication", and usability (overview.md, "Benefits"). It currently depends on StableHLO (dialect_agnostic_sharding.md, intro).

## Input abstraction
An MLIR program with `sdy.sharding` attributes bound by name to a logical mesh, "a multi-dimensional view of devices, defined by a list of axis names and sizes" (sharding_representation.md, "Basic structure"). Users supply shardings on main-function I/O, `sdy.sharding_constraint` ops on intermediates, `sdy.sharding_group` ids tying tensors without data dependence, and `sdy.manual_computation` regions (compiler_api.md, "Overview"). User shardings reference only full axes, "as this is currently not supported by JAX" (sharding_representation.md, "Motivation").

## Target
Only "a set of available devices" viewed as logical meshes with arbitrary device-id orders (sharding_representation.md, "Background", "Multiple logical meshes"). No hardware is named.

## Data decomposition
Per-dimension shardings list mesh axes major to minor; unused axes are implicitly replicated (sharding_representation.md, "Basic structure"). Dimensions are open (`?`, propagation may add axes) or closed (final); no attribute means fully open ("Open/closed dimensions"). `replicated={...}` names axes propagation may never use ("Explicitly replicated axes"). A full axis splits into sub-axes `"x":(m)k` (pre-size `m`, size `k`) so a reshape can keep data in place ("Axis splitting and sub-axes"). Several meshes over the same device ids may coexist; propagation across meshes is not planned ("Multiple logical meshes"). Each dimension sharding may carry a priority `p<i>`, default 0 ("Priorities"). Axes whose size product does not divide the dimension are allowed and "would require the dimension to be padded" ("Dimension sharding divisibility").

## Computation mapping
Propagation infers unspecified shardings along use-def chains in both directions to a fixed point (propagation.md, "Overview"). Each op supplies an `OpShardingRule` in einsum-like factor notation, e.g. `(i, k), (k, j) -> (i, j)`; compound factors such as `((ij), k)` cover reshapes ("Operation sharding rule", "Compound factors"). Shardings are projected to factors, the longest compatible major axes per factor propagated, and projected back ("Core Propagation Algorithm"). Conflicts follow a four-level hierarchy, interpretable as nested loops: (1) user priorities, iteration `i` propagating only priority `<= i` and never overriding lower-priority user shardings; (2) op priorities, pass-through ops (element-wise, reshape) before shape-transforming ops (dot, reduce); (3) aggressive propagation, which resolves conflicts and "can reduce the memory footprint at the cost of potential communication"; (4) basic propagation, only axes compatible between all operands and results ("Conflict resolution hierarchy"). Region ops (while, case, manual computation) use data-flow edges with an identity rule ("Data flow ops"). Named uses: batch parallelism, megatron, ZeRO ("Conflict resolution hierarchy").

## Communication generation
Not designed in these pages. The SPMD partitioner "adding the necessary data movement/formatting and collective operations" is, short term, "the current GSPMD SPMD partitioner"; an MLIR-based one is planned (overview.md, "Components"). Communication otherwise appears as a cost to avoid (sub-axes, reshapes), as resharding when a constraint's uses differ or tensors cross meshes (compiler_api.md, "Sharding Constraint"; sharding_representation.md, "Multiple logical meshes"), as an option to "all-gather sub-axes" on function I/O ("Function Input/output shardings"), and as user-written collectives such as "collective matmul" in manual computations (compiler_api.md, "Manual Computation").

## Compiler / runtime split
All compile time. The compiler decides every unannotated sharding given user constraints (compiler_api.md, "Background"); the user fixes closed dimensions, replicated axes, priorities and groups, and may take over a sub-computation via `manual_computation`, local along manual axes and still propagated along free axes ("Manual Computation", "Invariants"). "Compiler cost-models and heuristics" are mentioned (overview.md, "Components") but not described.

## Evaluation
None in the documentation.

## Principal limitation
Stated: StableHLO dependence; no propagation across meshes; sub-axes not expressible in JAX `NamedSharding`; constant splitting and user-defined op priorities "not yet implemented" (dialect_agnostic_sharding.md, "Interfaces not yet implemented"). Our observation: no page states how aggressive propagation picks a winner.

## Relationship to earlier / later work
- GSPMD: joint origin, reuse of its propagation and SPMD partitioner (overview.md, "Benefits", "Components"); open dimensions "similar (but not exactly the same as)" `unspecified_dims`; closed dimensions mirror GSPMD not modifying module I/O; multiple meshes replace `HloSharding` device lists; op priorities follow GSPMD (sharding_representation.md, "Open/closed dimensions", "Multiple logical meshes"; dialect_agnostic_sharding.md, "Op priorities").
- PartIR: source of incremental partitioning (overview.md, "Benefits").
- JAX: `jax.jit` `in_shardings`, `PartitionSpec`, `NamedSharding`, `PositionalSharding` (sharding_representation.md).
- XLA appears only as `HloSharding` and the openxla URLs; Mesh TensorFlow is not named.
- inferred: successor to GSPMD within the XLA/JAX stack.

## Sources used
| claim | section / pages |
|---|---|
| Problem, components, partitioner plan | overview.md |
| Representation features | sharding_representation.md, headings named above |
| Fixed point, hierarchy, rules, factors, data flow ops | propagation.md |
| I/O shardings, constraints, groups, manual computation | compiler_api.md |
| StableHLO dependence, missing interfaces | dialect_agnostic_sharding.md |

## Open questions for the survey
- How does the aggressive strategy choose between conflicting axes, and is the choice cost-driven in the code?
- Will the planned MLIR partitioner change the collectives inherited from GSPMD?

## Reference list check
The documentation has no reference list. External systems or papers named: GSPMD (arXiv 2105.04663), PartIR (arXiv 2401.11202), Megatron (arXiv 1909.08053), ZeRO (arXiv 1910.02054), JAX (`jax.jit`, `jax.sharding.PartitionSpec`, `NamedSharding`, `PositionalSharding`, with readthedocs links), StableHLO (ops and spec links at openxla.org/stablehlo), MLIR, GSPMD's `HloSharding`, and the openxla/shardy GitHub repository.
