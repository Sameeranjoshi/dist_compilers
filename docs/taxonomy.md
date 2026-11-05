# Taxonomy

The taxonomy classifies each paper or system along **independent axes**.
Chronology (`catalog/eras.yaml`) is *one* dimension; it is never the only
classification, because the same mechanism (for example block-cyclic
distribution or inspector–executor communication planning) appears in several
eras under different names.

The machine-readable definition is `catalog/taxonomy.yaml`; the validator
rejects any catalog value that is not defined there.  This page explains the
axes and how to apply them.

## Provenance

The taxonomy is a **survey taxonomy introduced by this project**.  Individual
category names are taken from the literature where a standard term exists
(e.g. *owner-computes* from the Fortran D / Kali literature, *inspector–
executor* from the PARTI work, *BLOCK/CYCLIC* from HPF).  The grouping into
axes, and the decision to treat ML sharding systems and wafer-scale compilers
on the same axes as 1990s HPF compilers, is ours.

## Axes

| axis | catalog field | question answered |
|------|---------------|-------------------|
| A. Target / memory model | `target_hardware` | What machine class is the compiler targeting? |
| B. Programming abstraction | `input_abstraction` | What did the programmer write? (RQ1) |
| C. Data decomposition | `data_decomposition` | How are data partitions represented? (RQ2) |
| D. Computation mapping | `computation_mapping` | How is work assigned to places? (RQ3) |
| E. Communication synthesis | `communication_generation` | How is communication derived? (RQ4) |
| F. Compilation time | `compiler_runtime_boundary` | When are decisions made? (RQ5) |
| G. Compiler architecture | `compiler_architecture` | How is the compiler structured? |
| H. Optimization objective | `optimization_objectives` | What is optimized? (RQ7) |
| I. Maturity / artifact | `maturity` | How usable is the system today? |
| J. Paper type | `paper_type` | What kind of document is this? |
| K. Compiler representation | `ir_representation` | What representation enabled the transformation? (RQ6) |

Full value lists with one-line definitions are in `catalog/taxonomy.yaml`.

## Applying the axes

1. **Tag from evidence.**  A tag is added only if the `evidence` entries on
   the catalog record name the section of the paper that supports it.  A paper
   whose full text was not consulted (`access_status: paywalled` or
   `abstract-only`) is tagged only on the axes its abstract clearly supports.
2. **Multiple values are normal.**  Fortran D supports BLOCK and CYCLIC
   distributions and both compiler-generated point-to-point messages and
   message vectorization.
3. **Foundations are tagged sparsely.**  Era-0 papers get a target class, a
   paper type, and representation tags only; they must not be tagged with
   distribution or communication values they did not have.
4. **Do not tag influence.**  `predecessors` / `successors` record relationships
   that the paper itself states (e.g. in related work) or that a cited survey
   states.  An inferred lineage goes into `notes`, prefixed "inferred:".
5. **Hardware papers.**  A handful of architecture papers are catalogued with
   `paper_type: hardware` and `relevance_tier: foundation` to date target
   classes (ILLIAC IV, CRAY-1, Cosmic Cube, systolic arrays).  They receive
   only a target tag.

## Why chronology alone is insufficient

- HPF (1993) and GSPMD (2021) share axis-C and axis-E values (block
  distribution over a processor grid; collective insertion by propagation)
  while sitting three eras apart.
- Inspector–executor (1990) and distributed sparse tensor compilation (2022–
  2025) share the runtime-inspector value on axis F.
- A chronological list would separate these and hide the rediscovery pattern
  that is one of the survey's main findings (see `assets/rediscovery-map.svg`).

## Empty-cell search

`scripts/generate_tables.py` prints a coverage matrix (axis value × era).
Empty cells are inputs to the *gap snowball* step of the methodology.
