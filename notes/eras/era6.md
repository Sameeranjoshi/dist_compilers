# Era 6: Mesh sharding, ML systems, and spatial accelerators (2020–2026)

Working notes for the era section of the paper. Everything here is either a pointer to catalog evidence or an explicitly labelled hypothesis.

**Machine driver.** TPU/GPU pods, AI accelerators, wafer-scale engines, spatial dataflow chips.

**Programming abstraction.** Sharding annotations on device meshes; tensor algebra with distribution formats; MLIR dialects; stencil DSLs.

**Decomposition representation.** Device meshes with per-dimension sharding; distributed tensor formats; MLIR shard/mesh attributes.

**Generated communication.** Collective insertion by propagation; resharding; automated search over parallelism plans.

**Limitation that motivated the next era.** Dynamic/irregular workloads, heterogeneous hierarchies, and memory-capacity constraints remain weakly handled; fragmentation across frameworks.

**Boundary evidence.** GSPMD (2021); Alpa and DISTAL/SpDISTAL (2022); PartIR and Shardy (2024-25); MLIR distributed sparse tensors (2025).

## Catalog entries in this era

| id | year | status | paper card |
|---|---|---|---|
| `lepikhin2020gshard` | 2020 | discovered |  |
| `rajbhandari2020zero` | 2020 | discovered |  |
| `rocki2020cerebras` | 2020 | read | yes |
| `li2021dlcompiler` | 2021 | screened |  |
| `xu2021gspmd` | 2021 | read | yes |
| `jacquelin2022wse` | 2022 | discovered |  |
| `yadav2022distal` | 2022 | read | yes |
| `yadav2022spdistal` | 2022 | read | yes |
| `zheng2022alpa` | 2022 | read | yes |
| `kong2023automatic` | 2023 | discovered |  |
| `bisbas2024shared` | 2024 | read | yes |
| `openxla2024shardy` | 2024 | screened |  |
| `thangamani2024polyhedral` | 2024 | screened |  |
| `tramm2024cerebras` | 2024 | discovered |  |
| `alabed2025partir` | 2025 | read | yes |
| `hall2025scheduling` | 2025 | screened |  |
| `mlir2025shard` | 2025 | screened |  |
| `vaidya2025distributed` | 2025 | discovered |  |
| `stawinoga2026mlir` | 2026 | read | yes |

## Synthesis (draft)

- What changed: TODO after the era's core papers are read.
- What remained: TODO.
- Limitation motivating the next era: see above; to be confirmed from primary sources.
